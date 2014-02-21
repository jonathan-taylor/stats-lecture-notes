#!/usr/bin/env python
""" Process pandoc json into text

Using definitions from:

http://hackage.haskell.org/package/pandoc-types-1.12.2/docs/Text-Pandoc-Definition.html

Need pandoc on path
Needs rpy2 etc installed to run tests on notebook

Example use:

    python tools/conv_test_tex.py notebooks/stats191/oldslides/selection.tex
"""

import sys
from os.path import join as pjoin, split as psplit, abspath, dirname, splitext

import io
import json
from subprocess import Popen, PIPE

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
            elif t == 'Quoted':
                res.append(self.process_quoted(c))
            elif t == 'Span':
                res += self.process_inline(c[1])
            elif t == 'Link':
                res.append(self.process_link(c))
            elif t == 'Emph':
                res += ['*', self.process_inline(c), '*']
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

    def process_block_list(self, blocks):
        return '\n'.join(self.process_block(block) for block in blocks)

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

    def parse(self, pdj, name=''):
        meta, body = pdj
        self._markdown_buffer = ''
        self._init_cells()
        for cell in body:
            t, c = cell['t'], cell['c']
            if t == 'Header':
                self.process_header(c)
                continue
            elif t == 'Para':
                res = self.process_inline(c)
            elif t == 'BulletList':
                res = self.process_bulletlist(c)
            elif t == 'Table':
                res = self.process_table(c)
            else:
                raise ValueError('Not yet for ' + t)
            if res != '':
                self._markdown_buffer = '\n'.join((self._markdown_buffer, res))
        self.flush_markdown()
        nb = nbf.new_notebook(name=name)
        ws = nbf.new_worksheet()
        ws['cells'] += self._cells[:]
        nb['worksheets'].append(ws)
        return nb


class ParsePDJJT(ParsePDJ):

    def __init__(self, code_fragments, force_inline=True):
        self.code_fragments = code_fragments
        super(ParsePDJJT, self).__init__(force_inline)

    def process_link(self, link):
        """ Trap [R Code] links and replace with found R code """
        txt, target = link
        url, name = target
        txt = self.process_inline(txt)
        if txt == 'R code':
            code = '\n'.join(('%%R', self._code_waiting.pop(0)))
            self._add_cell(nbf.new_code_cell(code))
            return ''
        return '[{0}]({1})'.format(txt, url)

    def _init_cells(self):
        self._cells = [
            nbf.new_code_cell('%load_ext rmagic',
                              metadata=META_SKIP)
        ]

    def parse(self, pdj, name=''):
        self._code_waiting = self.code_fragments[:]
        res = super(ParsePDJJT, self).parse(pdj, name)
        assert len(self._code_waiting) == 0
        return res


def extract_codes(liner):
    """ Extract code fragments from tex file

    Extract continuous lines of comments starting with %CODE

    Specific to Jonathan's slide output format
    """
    in_code = False
    codes = []
    for line in liner:
        line = line.strip()
        if not in_code:
            in_code = line == '%CODE'
            code_lines = []
            continue
        if not line.startswith('%'):
            in_code = False
            codes.append('\n'.join(code_lines))
            continue
        if line == '%':
            code_lines.append('')
            continue
        assert line[1] == ' '
        code_lines.append(line[2:])
    if in_code: # in case we're at the last line
        codes.append('\n'.join(code_lines))
    return codes


def parse_tex(fname):
    to_json = Popen('pandoc -t json ' + fname, stdout=PIPE, stderr=PIPE, shell=True)
    json_str, err_str = to_json.communicate()
    if to_json.returncode != 0:
        raise RuntimeError('Command failed')
    json_str = json_str.decode('utf-8')
    pdj = json.loads(json_str)
    with open(fname, 'rt') as fobj:
        codes = extract_codes(fobj)
    parser = ParsePDJJT(codes)
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
