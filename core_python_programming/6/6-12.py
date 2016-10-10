#a
def findchr(string,char):
    if string.find(char):
        return string.index(char)
    else:
        return -1
str = raw_input('Enter a string:\n')
chr = raw_input('Enter a char to be founded\n')
print findchr(str,chr[0])
#b
def rfindchr(string,char):
    str2 = ''
    l = len(string)
    if string.find(char):
        for i in range(l):
            str2 += string[l -1 - i]
        return l - str2.index(char)
    else:
        return -1

str = raw_input('Enter a string:\n')
chr = raw_input('Enter a char:\n')
print rfindchr(str,chr)

#c
def subchr(string,origchar,newchar):
    if string.find(origchar):
        str2 = ''
        index = string.index(origchar)
        for i in range(len(string)):
            if i != index:
                str2 += string[i]
            else:
                str2 += newchar
    return str2

str = raw_input('Enter a string')
ori = raw_input('origchar')
new = raw_input('newchar')
print subchr(str,ori[0],new[0])