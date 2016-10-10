f1n = raw_input('Enter filename1:')
f2n = raw_input('Enter filename2:(I will copy filename1 to filename 2):')
f1 = open(f1n)
f2 = open(f2n,'w')
for eachline in f1:
    f2.write(eachline)