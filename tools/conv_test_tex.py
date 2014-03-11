#!/usr/bin/env python
""" Process pandoc json into text

Using definitions from:

http://hackage.haskell.org/package/pandoc-types-1.12.2/docs/Text-Pandoc-Definition.html

Need pandoc on path
Needs rpy2 etc installed to run tests on notebook

Example use:

    python tools/conv_test_tex.py notebooks/stats191/oldslides/selection.tex
"""
from __future__ import print_function

import sys
from os.path import join as pjoin, split as psplit, abspath, dirname, splitext
from warnings import warn

import io
import json
from subprocess import Popen, PIPE

from pygments.lexers import guess_lexer

import IPython.nbformat.current as nbf

from checkipnb import run_notebook

META_SLIDE = {u'slideshow': {u'slide_type': u'slide'}}
META_SKIP = {u'slideshow': {u'slide_type': u'skip'}}


class ParsePDJ(object):
    tablen = 4

    def __init__(self, force_inline=True):
        self.force_inline = force_inline

    def process_math(self, math, force_inline=None):
        """ Process math fragment """
        if force_inline is None:
            force_inline = self.force_inline
        mt, c = math
        if mt == 'InlineMath' or force_inline:
            return "${0}$".format(c)
        return "\n$$\n{0}\n$$\n".format(c)

    def process_quoted(self, quote):
        """ Process quoted fragment """
        qt, c = quote
        quotemark = "\'" if qt == 'SingleQuote' else "\""
        return "{0}{1}{0}".format(quotemark, self.process_inline(c))

    def process_link(self, link):
        txt, target = link
        url, name = target
        return '[{0}]({1})'.format(self.process_inline(txt), url)

    def process_block(self, block, indentation_level=0):
        t, c = block['t'], block['c']
        if t in ('Plain', 'Para'):
            bres = self.process_inline(c)
        elif t == 'BulletList':
            bres = self.process_bulletlist(c, indentation_level + 1)
        elif t == 'OrderedList':
            bres = self.process_orderedlist(c, indentation_level + 1)
        elif t == 'Table':
            bres = self.process_table(c)
        elif t == 'BlockQuote':
            bres = []
            for block in c:
                bres.append(self.process_block(block, indentation_level+1))
            bres = '\n'.join(bres)
        else:
            raise ValueError('Not yet for ' + t)
        return bres

    def apply_indent(self, in_str, first_suff, indentation_level=0):
        prefix = ' ' * self.tablen * indentation_level
        line1 = prefix + first_suff
        others = prefix + ' ' * len(first_suff)
        bres = in_str.split('\n')
        bres[0] = line1 + bres[0]
        bres[1:] = [others + line for line in bres[1:]]
        return '\n'.join(bres)

    def process_bulletlist(self, blist, indentation_level=0):
        """ A list of blocks """
        res = []
        for item in blist:
            for block in item:
                out_str = self.process_block(block, indentation_level)
                res.append(self.apply_indent(out_str, '* ', indentation_level))
        return '\n'.join(res)

    def process_definitionlist(self, dlist, indentation_level=0):
        """ A list of blocks """
        res = []
        # Discard attributes
        for item in dlist:
            label, blocks = item
            line_res = [self.process_inline(label)]
            line_res.append(self.process_bulletlist(blocks, indentation_level))
            res.append(' '.join(line_res))
        return '\n'.join(res)

    def process_orderedlist(self, blist, indentation_level=0):
        """ A list of blocks """
        res = []
        # Discard attributes
        _, blist = blist
        for item in blist:
            for block in item:
                out_str = self.process_block(block, indentation_level)
                res.append(self.apply_indent(out_str, '1. ', indentation_level))
        return '\n'.join(res)

    def process_blockquote(self, bquote):
        return self.apply_indent(self.process_block(bquote), '> ')

    def process_inline(self, inline, math_inline=None):
        """ Process an inline element """
        if math_inline is None:
            math_inline = self.force_inline
        res = []
        for cell in inline:
            t, c = cell['t'], cell['c']
            if t == 'Str':
                res.append(c)
            elif t == 'Space':
                assert c == []
                res.append(' ')
            elif t == 'Math':
                res.append(self.process_math(c, math_inline))
            elif t in ('Code', 'RawInline'):
                res += ['``', c[1], '``']
            elif t == 'Quoted':
                res.append(self.process_quoted(c))
            elif t == 'Span':
                res += [self.process_inline(c[1]), '\n']
            elif t == 'Link':
                res.append(self.process_link(c))
            elif t == 'Emph':
                res += ['*', self.process_inline(c), '*']
            elif t == 'Strong':
                res += ['**', self.process_inline(c), '**']
            elif t == 'LineBreak':
                res += '\n'
            elif t == 'Superscript':
                res += '<sup>' + self.process_inline(c) + '</sup>'
            elif t == 'Subscript':
                res += '<sup>' + self.process_inline(c) + '</sup>'
            else:
                raise ValueError("not yet for " + t)
        return ''.join(res)

    def process_header(self, header):
        """ Process a header from pandoc json """
        level, attrs, contents = header
        contents = self.process_inline(contents)
        self._add_cell(nbf.new_heading_cell(contents,
                                            metadata=META_SLIDE,
                                            level=level))

    def process_codeblock(self, codeblock):
        """ Process a code block from pandoc json """
        attrs, contents = codeblock
        if self.guess_language(contents) == 'R':
            contents = '%%R\n' + contents
        self._add_cell(nbf.new_code_cell(contents))

    def process_block_list(self, blocks):
        return '\n'.join([self.process_block(block) for block in blocks])

    def process_table(self, table):
        """ Process a table

        From the doc above:
        Table [Inline] [Alignment] [Double] [TableCell] [[TableCell]]

        Table, with caption, column alignments, relative column widths (0 =
        default), column headers (each a list of blocks), and rows (each a list of
        lists of blocks)
        """
        caption, alignments, relcol_width, col_headers, rows = table
        caption = self.process_inline(caption)
        ncols = len(col_headers)
        col_headers = [self.process_block_list(ch) for ch in col_headers]
        proc_rows = []
        for row in rows:
            proc_rows.append([self.process_block_list(elem) for elem in row])
        tab_res = ['']
        if not caption == '':
            tab_res += [caption, '']
        tab_res.append(' | '.join(col_headers))
        tab_res.append(' | '.join(['---'] * ncols))
        for row in proc_rows:
            assert len(row) == ncols
            tab_res.append(' | '.join(row))
        return '\n'.join(tab_res)

    def guess_language(self, lang_str):
        """ Guess whether passed string is R or python
        """
        for shoey in 'matplotlib', 'numpy', 'scipy', 'pylab':
            if shoey in lang_str:
                return 'python'
        return 'R'

    def flush_markdown(self):
        if len(self._markdown_buffer) == 0:
            return
        self._cells.append(
            nbf.new_text_cell('markdown', self._markdown_buffer))
        self._markdown_buffer = ''

    def _add_cell(self, cell):
        self.flush_markdown()
        self._cells.append(cell)

    def _init_cells(self):
        self._cells = []

    def _post_cells(self):
        pass

    def parse(self, pdj, name=''):
        meta, body = pdj
        self._markdown_buffer = ''
        self._init_cells()
        for cell in body:
            t, c = cell['t'], cell['c']
            if t == 'Header':
                self.process_header(c)
                continue
            elif t == 'CodeBlock':
                self.process_codeblock(c)
                continue
            elif t in ('Para', 'Plain'):
                res = self.process_inline(c)
            elif t == 'RawBlock':
                res = c[1]
            elif t == 'BlockQuote':
                res = self.process_blockquote(c)
            elif t == 'BulletList':
                res = self.process_bulletlist(c)
            elif t == 'OrderedList':
                res = self.process_orderedlist(c)
            elif t == 'Table':
                res = self.process_table(c)
            elif t == 'DefinitionList':
                res = self.process_definitionlist(c)
            else:
                raise ValueError('Not yet for ' + t)
            if res != '':
                self._markdown_buffer = '\n'.join((self._markdown_buffer, res))
        self.flush_markdown()
        self._post_cells()
        nb = nbf.new_notebook(name=name)
        ws = nbf.new_worksheet()
        ws['cells'] += self._cells[:]
        nb['worksheets'].append(ws)
        return nb


class ParsePDJJT(ParsePDJ):

    def _init_cells(self):
        self._cells = [
            nbf.new_code_cell('%load_ext rmagic',
                              metadata=META_SKIP)
        ]

    def _post_cells(self):
        pass


def insert_codes(liner):
    """ Extract code fragments from tex file and replace in tex

    Extract continuous lines of comments starting with %CODE and replace in
    tex file using verbatim environment

    Specific to Jonathan's slide output format
    """
    state = 'default'
    new_lines = []
    for raw_line in liner:
        line = raw_line.strip()
        rline = raw_line.rstrip()
        if state == 'default':
            if line == '%CODE':
                state = 'code'
                code_lines = []
            else:
                new_lines.append(rline)
        elif state == 'code':
            if not line.startswith('%'):
                state = 'after-code'
            elif line == '%':
                code_lines.append('')
            else:
                assert line[1] == ' '
                code_lines.append(line[2:])
        elif state == 'after-code':
            new_lines.append(rline)
            if line == r'\begin{frame}':
                state = 'after-frame'
        elif state == 'after-frame':
            if line.startswith(r'\resizebox'):
                new_lines.append(r'\begin{verbatim}')
                new_lines += code_lines
                new_lines.append(r'\end{verbatim}')
                state = 'after-resize'
            else:
                new_lines.append(rline)
        elif state == 'after-resize':
            if line.startswith(r'\href') and 'R code' in line:
                # skip this line
                continue
            new_lines.append(rline)
            if line == r'\end{frame}':
                state = 'default'
    return '\n'.join(new_lines)


def parse_tex(fname):
    with open(fname, 'rb') as fobj:
        proc_tex = insert_codes(fobj)
    to_json = Popen('pandoc -r latex -t json ', stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    json_str, err_str = to_json.communicate(proc_tex)
    if to_json.returncode != 0:
        raise RuntimeError('Command failed')
    json_str = json_str.decode('utf-8')
    pdj = json.loads(json_str)
    parser = ParsePDJJT()
    return parser.parse(pdj)


def main():
    fname = sys.argv[1]
    nb_fname = splitext(fname)[0] + '.ipynb'
    res = parse_tex(fname)
    with open(nb_fname, 'wt') as fobj:
        nbf.write(res, fobj, 'ipynb')
    run_notebook(res)


if __name__ == '__main__':
    main()
