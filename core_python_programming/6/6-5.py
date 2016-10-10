str = raw_input('Enter a string to determine whether a string is palindromic\n')
l = len(str)-1
p = True
if l >= 1:
    for i in range(l/2 + 1):
        if str[i] != str[l-i]:
            p = False
            break
if p:
    print 'It\'s a palindromic string!'
else:
    print 'Sorry, It\'s not a palindromic string!'
	
str = raw_input('Please enter a string\n')
str += str[::-1]
print str