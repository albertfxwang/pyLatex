#!/usr/bin/env python
# -*- coding: utf-8 -*-

#=========================================================================================================
# IMPORTING MODULES
import numpy as np
import collections
import os
import grismreductxin as grx


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
def p7table_ELobjs(GiGzcatfile, tablename='p7table_ELobjs.tex', includeallcol=False, verbose=True):
    """
    Make a latex table basing on the GiGz catalog file created by subroutine "mkGiGzcat" in grismreductxin.py
    :param GiGzcatfile: the path and name of the GiGz catalog file
    --- Additional Note ---
    * Used to make the table for ELobjs sample in paper7 of GLASS
    * Based on the subroutine "write_latextable" developed by Kasper in paper2_LBGsAbove7InGLASS.py
    * You have to manually edit the coldic renaming part if want to add specific columns that don't exist in GiGzcatfile
    """
    if not os.path.isfile(GiGzcatfile):
        print ' ERR: cannot find the input GiGz catalog file'
        return
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if verbose: print ' - Writing '+GiGzcatfile+' to the latex table '+tablename
    fout = open(tablename,'w')
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if verbose: print '   Loading data '
    GiGzcat = np.genfromtxt(GiGzcatfile,dtype=None,names=True,comments='#')
    colnames = GiGzcat.dtype.names
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if verbose: print '   Setting columns to include '
    coldic     = collections.OrderedDict({})    # fixing order of dictionary keys
    if includeallcol:
        colarr = np.asarray(GiGzcat.dtype.names)    # include all columns in table
        for col in colarr: coldic[col] = col.replace('_','')
    else:
        coldic['ID']                = 'ID$_\\textrm{GLASS}$'
        coldic['IDarc']             = 'ID$_\\textrm{arc}$'
        coldic['RA']                = 'R.A.'
        coldic['Dec']               = 'Dec.'
        coldic['F140Wmag']          = 'F140W'
        coldic['zphoto']            = '$z_\\textrm{photo}$'
        coldic['zspec']             = '$z_\\textrm{spec}$'
        coldic['zspecQ']            = 'Quality'
        coldic['PA1']               = 'P.A.'
        coldic['NlinesmatchPA1']    = 'Nlines'
        coldic['linesmatchPA1str']  = 'line names'
        # coldic['EWPA1']             = 'EW limit [\\AA]'
        coldic['flinePA1']          = '$f_\\textrm{line}$'
        coldic['mu']                = '$\\mu$'

    Ncol       = len(coldic)
    columnstring = ' '
    for col in coldic.keys():
        columnstring = columnstring + '\colhead{'+coldic[col]+'} & '

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if verbose: print '   Writing header '
    header = """
% = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
% Include this table with \input{filename.tex}
% To rotate in emulateapj, do: \\begin{turnpage}\input{filename.tex}\end{turnpage}
% To display it on multiple pages, do: \LongTables\input{filename.tex}
% To display it sideways on multiple pages, do: \usepackage{longtable} in front and
% \clearpage\LongTables\\begin{landscape}\input{filename.tex}\clearpage\end{landscape} when calling it
% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\\tabletypesize{\\tiny} \\tabcolsep=0.11cm
\\begin{deluxetable*}{"""+('c'*Ncol)+'} \\tablecolumns{'+str(Ncol)+'}'+"""
\\tablewidth{0pt}
\\tablecaption{ CAPTION OF TABLE }
% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\\tablehead{
"""+ columnstring[:-2] +"""
}
% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\startdata
"""
    fout.write(header)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if verbose: print '   Filling rows '
    ids = GiGzcat['ID']
    for ii, id in enumerate(ids):
        tablerow = ' '
        for col in coldic.keys():
            if col not in colnames:
                valstr = ''
            else:
                val = GiGzcat[col][ii].tolist()
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                if (col == 'ID'):
                    valstr = str("%.5d" % val)
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                elif (col == 'RA') or (col == 'Dec'):
                    valstr = str("%.9f" % val)
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                elif (col == 'PA1'):
                    val2   = GiGzcat[col.replace('1','2')][ii].tolist()
                    if (int(val)!=-999) and (int(val2)!=-999):
                        valstr = str("%.3d" % val)+', '+str("%.3d" % val2)
                    elif int(val) == -999:
                        valstr = str("%.3d" % val2)
                    else:
                        valstr = str("%.3d" % val)
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                elif (col == 'NlinesmatchPA1'):
                    val2    = GiGzcat[col.replace('1','2')][ii].tolist()
                    if (int(val)!=-999) and (int(val2)!=-999):
                        valstr  = str("%.0f" % val)+', '+str("%.0f" % val2)
                    elif int(val) == -999:
                        valstr  = str("%.0f" % val2)
                    else:
                        valstr  = str("%.0f" % val)
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                elif (col == 'linesmatchPA1str'):
                    val2   = GiGzcat[col.replace('1','2')][ii].tolist()
                    if (val!='-999') and (val2!='-999'):
                        lines1 = [ grx.getLineInfo(ll)[1] for ll in val.split('&&')]
                        lines2 = [ grx.getLineInfo(ll)[1] for ll in val2.split('&&')]
                        valstr = str("%s" % ' '.join(lines1))+', '+str("%s" % ' '.join(lines2))
                    elif val == '-999':
                        lines2 = [ grx.getLineInfo(ll)[1] for ll in val2.split('&&')]
                        valstr = str("%s" % ' '.join(lines2))
                    else:
                        lines1 = [ grx.getLineInfo(ll)[1] for ll in val.split('&&')]
                        valstr = str("%s" % ' '.join(lines1))
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                elif (col == 'zspec'):
                    valstr = str("%.3f" % val)
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                elif (col == 'zspecQ'):
                    valstr = str("%.0f" % val)
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                else:
                    valstr = 'ERROR'
            tablerow = tablerow+valstr+' & '

        fout.write(tablerow[:-2]+'\\\\ \n')

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if verbose: print '   Writing footer '
    footercomments = 'Photometric selections correspond to:'
    # for ref in photoselrefs.keys():
    #     footercomments = footercomments + photoselrefs[ref][0]+': '+photoselrefs[ref][1]+', '
    footer = """
\enddata
% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\\tablecomments{"""+footercomments+"""}
\label{tab:?}
\end{deluxetable*}
% = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    """
    fout.write(footer)
    fout.close()
    if verbose: print ' - Successfully created '+tablename
