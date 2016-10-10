s = raw_input("Please enter a string\n")
i = 0
slen = len(s)
while i<slen:
    print i+1,s[i]
    i += 1

s = raw_input('Please enter a string\n')
for i in range(len(s)):
    print i+1,s[i]