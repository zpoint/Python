f1 = open(raw_input('Please enter two filenames for comparison\nfirst:')).readlines()
f2 = open(raw_input('Second:')).readlines()
import difflib
dif = difflib.SequenceMatcher(None,f1,f2)
for tag,i1,i2,j1,j2 in dif.get_opcodes():
    if tag != 'equal':
        print '%s a[%d:%d] (%s) b[%d:%d] (%s)' %(tag,i1,i2,f1[i1:i2],j1,j2,f2[j1:j2])