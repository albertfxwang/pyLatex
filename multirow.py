# made by Kuang in March 2015

import numpy as np

example_row = r"00523  & 6.2 & 3.594060460 & -30.407997680  & $24.66\pm0.025$  & $2.333_{-2.256}^{+0.621}$  &  2.023  &  4  &  135, 233  &  2, 2  &  [OII] [OIII], [OII] [OIII] & 9.7$\pm$0.97 23.0$\pm$2.4, 1.2$\pm$0.8 30.0$\pm$1.9 & 0.71 [0.69-0.83]"
example_row2 = r"00336  &    1.3   &  3.586232335  &  -30.409968879   & $22.92\pm0.011$  & $1.599_{-1.518}^{+0.985}$  &  1.498  &  3  &  135, 233  &  3, 1  &  [OII] [OIII] H$\alpha$, H$\alpha$  &    & 5.45 [4.86-6.71] "

def convert_multirow_table2(row, split_cols=[8,9,10,11]):
   """
   Take a string, convert to multirow LaTeX format.
   """
   # get rid of the trailing \\
   row = ' '.join(row.split()[:-1])
   fields = row.split('&')
   assert len(fields) == 13
   line1_fields = []

   line2_fields = []
   
   for i in range(13):
      if i not in split_cols:
         # add multirow
         line1_fields.append(r"\multirow{2}{*}{%s}" % fields[i])
         line2_fields.append("")
      else:
         # split the values
         values = fields[i].split(',')
         if len(values) == 2:
            line1_fields.append(values[0])
            line2_fields.append(values[1])
         else:
            # Add the single value to line 1... this shouldn't happen
            print "Warning: single value in an expected split column! (%s)" % values
            line1_fields.append(values[0])
            line2_fields.append("")
   # Now join the lines
   line1 = " & ".join(line1_fields) + r'\\'
   line2 = " & ".join(line2_fields) + r'\\'
   print ""
   print line1
   print line2
   print ""
   return line1, line2

def convert_all_lines_table2(lines, output='temp2.txt'):
   l = lines.split('\n')
   f2 = open(output, 'wb')
   for line in l:
      # line = r"%s" % line
      # line.replace("\\\\", "")
      # print line
      # print "original line:"
      # print line
      line1, line2 = convert_multirow_table2(line)
      f2.write(line1 + '\n')
      f2.write(line2 + '\n')
   f2.close()

def super_convert_multirow_table2(row, split_cols=[8,9,10,11], super_split_cols=[10,11]):
   """
   The extreme version---split not just by PA, but also by lines!!
   For each PA, there will be one row per line that also contains line flux.
   We'll see how this looks and maybe we can then turn the table around in 
   portrait mode.
   """
   # get rid of the trailing \\
   row = ' '.join(row.split()[:-1])
   fields = row.split('&')
   assert len(fields) == 13
   # lines = []
   nrows = [1, 1]  # default number of split rows
   # Now figure out how many total rows we should split this in
   PAcol = split_cols[0] # column to determine how many PAs
   numPA = len(fields[PAcol].split(','))
   LINEcol = super_split_cols[0]  # column to determine how many lines per PA
   lines = fields[LINEcol].split(',')  # a list of lines for each PA
   print "fields[LINEcol].split(','):", lines
   nrows[0] = len(lines[0].split())
   if len(fields[PAcol].split(',')) == 1:
      nrows[1] = 0  # just one PA
   else:
      nrows[1] = len(lines[1].split())
   print "Number of rows for each PA: ", nrows
   nrows_total = np.sum(nrows)
   lines = {}
   for i in range(nrows_total):
      lines[i] = []  # initialize lists to add stuff to
   for i in range(len(fields)):
      if i not in split_cols:
         # add multirow
         lines[0].append(r"\multirow{%d}{*}{%s}" % (nrows_total, fields[i]))
         for j in range(1, nrows_total):
            lines[j].append("")
      else:
         # Now split PA and N_lines
         values = fields[i].split(',')
         if i not in super_split_cols:
            # append first PA
            if nrows[0] == 1:
               lines[0].append(values[0])
            else:
               lines[0].append(r"\multirow{%d}{*}{%s}" % (nrows[0], values[0]))
               for j in range(1, nrows[0]):
                  lines[j].append("")
            # append second PA
            if nrows[1] == 0:
               continue
            elif nrows[1] == 1:
               lines[nrows[0]].append(values[1])
            else:
               lines[nrows[0]].append(r"\multirow{%d}{*}{%s}" % (nrows[1], values[1]))
               for j in range(nrows[0]+1, nrows_total):
                  lines[j].append("")
         else:
            # Check how many fields are there in each line
            # print "Looking at the %d-th column..." % i
            # for j in range(nrows_total):
            #    print "len(lines[%d]) = %d" % (j, len(lines[j]))
            # Split the lines as well!
            # Check if there is value... if not then just append ""
            if values[0] == '':
               print "There is no value yet... (values=%s)" % values
               for j in range(nrows_total):
                  lines[j].append("")
                  print "len(lines[%d]) = %d" % (j, len(lines[j]))                  

            else:
               # Append the first PA
               if nrows[0] == 1:
                  # only one line for the first PA
                  lines[0].append(values[0])
               else:
                  # multiple lines for the first PA
                  speclines0 = values[0].split()  # assume the lines are separated by spaces
                  assert len(speclines0) == nrows[0], "len(speclines0)=%d but nrows[0]=%d; values[0] = %s" % (len(speclines0), nrows[0], values[0])
                  for j in range(nrows[0]):
                     lines[j].append(speclines0[j])
               # Now work on the second PA
               if nrows[1] == 0:
                  continue
               elif nrows[1] == 1:
                  # only one line for the second PA
                  lines[nrows[0]].append(values[1])
               else:
                  speclines1 = values[1].split() 
                  # print "speclines1", speclines1
                  assert len(speclines1) == nrows[1]
                  for j in range(nrows[0], nrows_total):
                     # print "(line 127) j=", j, "lines.keys():", lines.keys()
                     lines[j].append(speclines1[j-nrows[0]])
   # Now join the lines
   for k in lines.keys():
      print "len(lines[%d]) = %d" % (k, len(lines[k]))
   for k in lines.keys():
      assert len(lines[k]) == 13, "lines[%d] has length %d!" % (k, len(lines[k]))
   print ""
   for k in range(len(lines)):
      lines[k] = " & ".join(lines[k]) + r"\\"
      print lines[k]
   print ""
   return lines

def super_convert_all_lines_table2(inputfile='temp.txt', output='temp2.txt'):
   l = open(inputfile, 'rb').readlines()
   # l = lines.split('\n')
   f2 = open(output, 'wb')
   for line in l:
      # line = r"%s" % line
      # line.replace("\\\\", "")
      # print line
      # print "original line:"
      # print line
      print "Processing %s..." % line.split()[0]
      lines = super_convert_multirow_table2(line)
      for k in lines:
         f2.write(lines[k] + '\n')
   f2.close()
