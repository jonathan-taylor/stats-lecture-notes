import tempfile, sys, json, os
from shutil import rmtree
from glob import glob

from IPython.extensions import rmagic
from IPython.core.magic import register_cell_magic
from IPython.core.displaypub import publish_display_data

Rcode = """
library(knitr)
library(stringr)

ke = environment(knit)
render_ipynb = function (strict = FALSE) 
{
    knit_hooks$restore()
    opts_chunk$set(dev = "png", highlight = FALSE)
    hook.t = function(x, options) {
        fn = tempfile()
        of = file(fn, "w")
        writeChar(ke$indent_block(x), of)
        close(of)
        return(str_c('["text/plain","', fn, '"],'))
    }
    hook.o = function(x, options) {
        return(hook.t(x, options))
    }
    knit_hooks$set(source = hook.t, output = hook.o, warning = hook.t, error = hook.t, 
        message = hook.t, inline = function(x) sprintf(if (inherits(x, 
            "AsIs")) 
            "%s"
        else "`%s`", ke$.inline.hook(ke$format_sci(x, "html"))), plot = hook_plot_ipynb)
}

hook_plot_ipynb = function (x, options) 
{
    base = opts_knit$get("base.url")
    if(is.null(base)) {
        base = ''
    }
    filename = sprintf("%s%s", base, ke$.upload.url(x));
    return(sprintf('["image/png","%s"],', filename))
}

render_ipynb()
"""

rm = rmagic.RMagics(get_ipython())

def Reval(line):
    '''
    Parse and evaluate a line with rpy2.
    Returns the output to R's stdout() connection
    and the value of eval(parse(line)).
    '''
    return rm.eval(line)

Reval(Rcode)

@register_cell_magic
def knitr(line, cell=None):

    tmpd = tempfile.mkdtemp()

    Rmd_file = open("%s/code.Rmd" % tmpd, "w")
    md_filename = Rmd_file.name.replace("Rmd", "md")
    Rmd_file.write("""

``` {r fig.path="%s"}
%s
```

""" % (tmpd, cell.strip()))
    Rmd_file.close()
    Reval("library(knitr); knit('%s','%s')" % (Rmd_file.name, md_filename))
    sys.stdout.flush(); sys.stderr.flush()
    json_str = '[' + open(md_filename, 'r').read().strip()[:-1].replace('\n','\\n') + ']'
    md_output = json.loads(json_str)

    display_data = []
    # flush text streams before sending figures, helps a little with output
    for mime, fname in md_output:
        # synchronization in the console 
        # (though it's a bandaid, not a real sln)
        sys.stdout.flush(); sys.stderr.flush()
        data = open(fname).read()
        os.remove(fname)
        if data:
            display_data.append(('RMagic.R', {mime: data}))

    # kill the temporary directory
    rmtree(tmpd)

    for tag, disp_d in display_data:
        publish_display_data(tag, disp_d)

