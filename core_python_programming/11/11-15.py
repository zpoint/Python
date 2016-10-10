def backwards(str,i=-1):
    if i + 2 <= len(str):
        i += 1
        backwards(str,i)
        print "%c" %(str[i]),
str = raw_input('Input a string ,I will print it backwards to use recursion\n')
backwards(str)