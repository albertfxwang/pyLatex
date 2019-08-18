# -*- coding: utf-8 -*-
# Require Python 3 astroconda env
from __future__ import print_function, division

#========================================================================================================
#                    Python scripts to create Latex table files written by Xin Wang
#=========================================================================================================
# IMPORTING MODULES
from importlib import reload
import numpy as np
import collections
import os, sys
import astropy.io.ascii as ascii
import grismreductxin as grx; reload(grx)
ELinfo = grx.ELinfo(latex='simple')

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
def p7table_ELobjs(GiGzcatfile, tablename='p7table_ELobjs.tex', includeallcol=False, verbose=True):
    """
    Make a latex table based on the GiGz catalog file created by subroutine "mkGiGzcat" in grismreductxin.py
    :param GiGzcatfile: the path and name of the GiGz catalog file
    --- Additional Note ---
    * Used to make the table for ELobjs sample in paper7 of GLASS
    * Based on the subroutine "write_latextable" developed by Kasper in paper2_LBGsAbove7InGLASS.py
    * You have to manually edit the coldic renaming part if want to add specific columns that don't exist in GiGzcatfile
    """
    assert os.path.isfile(GiGzcatfile), ' ERR: cannot find the input GiGz catalog file'

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if verbose: print(' - Writing '+GiGzcatfile+' to the latex table '+tablename)
    fout = open(tablename,'w')
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if verbose: print('   Loading data ')
    GiGzcat = np.genfromtxt(GiGzcatfile,dtype=None,names=True,comments='#')
    colnames = GiGzcat.dtype.names
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if verbose: print('   Setting columns to include ')
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
    if verbose: print('   Writing header ')
    header = r"""
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
    if verbose: print('   Filling rows ')
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
    if verbose: print('   Writing footer ')
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
    if verbose: print(' - Successfully created '+tablename)


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
def metalgradfull_table(mastercat, tablename='source.tex', includeallcol=False, verbose=True,
                        linelist=['OII', 'Hg', 'Hb', 'OIII', 'Ha', 'SII']):
    """
    Produce a latex table showing the source properties in the full GLASS metallicity gradient paper。
    """
    assert os.path.isfile(mastercat), ' ERR: cannot find the input master catalog'

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if verbose: print(' - Writing '+mastercat+' to the latex table '+tablename)
    fout = open(tablename,'w')
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if verbose: print('   Loading data ')
    catdat = ascii.read(mastercat)
    colnames = catdat.colnames
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if verbose: print('   Setting columns to include ')
    coldic     = collections.OrderedDict({})    # fixing order of dictionary keys
    if includeallcol:
        colarr = np.asarray(colnames)    # include all columns in table
        for col in colarr: coldic[col] = col.replace('_','')
    else:
        coldic['clalias']           = 'cluster'
        coldic['ID']                = 'ID'
        coldic['RA']                = 'R.A.'
        coldic['DEC']               = 'Dec.'
        coldic['redshift']          = '$z_\\textrm{spec}$'
        coldic['grad']              = '$\\Delta\\log({\\rm O/H})/\\Delta r$~[dex/kpc]'
        coldic['F140W_mag']         = 'F140W~[ABmag]'
        coldic['reduce_factor']     = '$r_{\\rm F140W}$'
        for line in linelist:
            coldic['flux_'+line]    = '$f_{{\\rm {:s}}}$'.format(ELinfo[line]['latex'].replace('$',''))
        coldic['mu_m']              = '$\\mu$'
        coldic['lmstar_m']          = '$\\log(M_{\\ast}/M_{\\odot})$'
        coldic['sfr_m']             = 'SFR$^{\\rm S}$'
        coldic['Av_m']              = 'A$_{\\rm V}^{\\rm S}$'
        coldic['N2Ha_m']            = '[N II]/H$\\alpha$'
        coldic['oh12_me']           = '$12+\log({\\rm O/H})$'
        coldic['Av_me']             = 'A$_{\\rm V}^{\\rm N}$'
        coldic['sfr_me']            = 'SFR$^{\\rm N}$'

    Ncol       = len(coldic)
    columnstring = ' '
    for col in coldic.keys():
        columnstring = columnstring + '\colhead{'+coldic[col]+'} & \n '

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if verbose: print('   Writing header ')
    header = r"""
% = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
% Include this table with \input{filename.tex}
% To rotate in emulateapj do: \begin{turnpage}\input{filename.tex}\end{turnpage}
% To display it on multiple pages do: \LongTables\input{filename.tex}
% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
%\tabletypesize{\scriptsize}
%\tabcolsep=2pt
\begin{deluxetable*}{"""+('c'*Ncol)+r'}   \tablecolumns{'+str(Ncol)+'}'+r"""
\tablewidth{0pt}
\tablecaption{ CAPTION OF TABLE }
% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\tablehead{
"""+ columnstring[:-2] +"""
}
% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\startdata
"""
    fout.write(header)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if verbose: print('   Filling rows ')

    for ii, id in enumerate(catdat['ID']):
        tablerow = ' '
        for col in coldic.keys():
            if col not in colnames:
                valstr = ''
            else:
                val = catdat[col][ii]
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                if (col == 'clalias'):
                    valstr = str(val)
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                elif (col == 'ID'):
                    valstr = str("%.5d" % val)
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                elif (col == 'RA') or (col == 'DEC'):
                    valstr = str("%.6f" % val)
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                elif col in ['redshift', 'F140W_mag', 'reduce_factor']:
                    valstr = r"{:.2f}".format(val)
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                elif col == 'grad':
                    val2 = catdat[col+'_err'][ii].tolist()
                    valstr = r"${:.3f}\pm{:.3f}$".format(val, val2)
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                elif col.startswith('flux_'):
                    if val == -999. or val > 1.e3:
                        valstr = r"\nodata"
                    else:
                        val2 = catdat[col.replace('flux_','err_')][ii]
                        assert val2>0., ' ERR: wrong value of {:s} = {}'.format(col.replace('flux_','err_'), val2)
                        valstr = r"${:.2f}\pm{:.2f}$".format(val, val2)
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                elif col in ['mu_m', 'lmstar_m', 'sfr_m', 'Av_m', 'N2Ha_m']:
                    val_l = catdat[col.replace('_m', '_l')][ii]
                    val_u = catdat[col.replace('_m', '_u')][ii]
                    valstr = r"${:.2f}_{{-{:.2f}}}^{{+{:.2f}}}$".format(val, val-val_l, val_u-val)
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                elif col in ['oh12_me', 'Av_me', 'sfr_me']:
                    val_cond = int(catdat[col.replace('_me', '_cond')][ii])
                    val_l = catdat[col.replace('_me', '_low')][ii]
                    val_u = catdat[col.replace('_me', '_up')][ii]
                    if val_cond == 0:
                        valstr = r"${:.2f}_{{-{:.2f}}}^{{+{:.2f}}}$".format(val, val-val_l, val_u-val)
                    elif val_cond == 1:     # lower limit
                        valstr = r"$>{:.2f}$".format(val)
                    elif val_cond == 2:     # upper limit
                        valstr = r"$<{:.2f}$".format(val)
                    else:
                        sys.exit(' ERR: keyword option not supported!')
                else:
                    valstr = 'ERROR'
            tablerow = tablerow+valstr+' & '

        fout.write(tablerow[:-2]+'\\\\ \n')

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if verbose: print('   Writing footer ')
    footercomments = ' Table footer comments'
    # for ref in photoselrefs.keys():
    #     footercomments = footercomments + photoselrefs[ref][0]+': '+photoselrefs[ref][1]+', '
    footer = r"""
\enddata
% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\tablecomments{"""+footercomments+"""}
\label{tab:?}
\end{deluxetable*}
% = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    """
    fout.write(footer)
    fout.close()
    if verbose: print(' - Successfully created '+tablename)



