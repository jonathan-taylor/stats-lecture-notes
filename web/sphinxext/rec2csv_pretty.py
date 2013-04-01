from matplotlib.mlab import csvformat_factory, get_formatd, cbook, csv

def rec2csv_pretty(r, fname, delimiter=',', formatd=None, missing='',
            missingd=None, withheader=True,
            overwrite_float_precision=True):
    """
    Save the data from numpy recarray *r* into a
    comma-/space-/tab-delimited file.  The record array dtype names
    will be used for column headers.

    *fname*: can be a filename or a file handle.  Support for gzipped
      files is automatic, if the filename ends in '.gz'

    *withheader*: if withheader is False, do not write the attribute
      names in the first row

    *overwrite_float_precision*: if True, write out floats as raw, else
      use the implied precision of formatd
      
    .. seealso::

        :func:`csv2rec`
            For information about *missing* and *missingd*, which can
            be used to fill in masked values into your CSV file.
    """

    if missingd is None:
        missingd = dict()

    def with_mask(func):
        def newfunc(val, mask, mval):
            if mask:
                return mval
            else:
                return func(val)
        return newfunc

    formatd = get_formatd(r, formatd)
    funcs = []
    for i, name in enumerate(r.dtype.names):
        if overwrite_float_precision:
            funcs.append(with_mask(csvformat_factory(formatd[name]).tostr))
        else:
            funcs.append(with_mask(formatd[name].tostr))            
    fh, opened = cbook.to_filehandle(fname, 'wb', return_opened=True)
    writer = csv.writer(fh, delimiter=delimiter)
    header = r.dtype.names
    if withheader:
        writer.writerow(header)

    # Our list of specials for missing values
    mvals = []
    for name in header:
        mvals.append(missingd.get(name, missing))

    ismasked = False
    if len(r):
        row = r[0]
        ismasked = hasattr(row, '_fieldmask')

    for row in r:
        if ismasked:
            row, rowmask = row.item(), row._fieldmask.item()
        else:
            rowmask = [False] * len(row)
        srow = [func(val, mask, mval) for func, val, mask, mval
                         in zip(funcs, row, rowmask, mvals)]
        writer.writerow(srow)
    if opened:
        fh.close()
