def text_processing(str):
    vowels = 0
    consonants = 0
    word_list = str.split()
    words = len(word_list)
    for i in str.upper():
        if i in 'AEIOU':
            vowels += 1
        elif i.isalpha():
            consonants += 1
    return vowels,consonants,words

str = raw_input('Please enter a string to determine:\n')
tx = text_processing(str)
print str,'\nhas %d vowels %d consonants and %d words\n' %(tx[0],tx[1],tx[2])