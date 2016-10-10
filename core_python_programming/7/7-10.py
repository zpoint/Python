def rot13(str):
    st = ''
    for i in str:
        if i.isalpha():
            st += chr(ord(i) + 13)
        else:
            st += i
    return st
def derot13(str):
    st = ''
    for i in str:
        j = chr(ord(i) - 13)
        if j.isalpha():
            st += j
        else:
            st += i
    return st
str = raw_input('Enter string to rot13: ')
print 'Your string to en/decrypt was: [%s]' %(str)
en = rot13(str)
print 'The rot13 string is: [%s]' %(en)
print 'After decryption: [%s]' %(derot13(en))