#a
def tr(srcstr,dststr,string):
    loc = string.find(srcstr)
    return string[:loc] + dststr + string[loc+len(srcstr):]
print tr('abc','mno','abcdef')