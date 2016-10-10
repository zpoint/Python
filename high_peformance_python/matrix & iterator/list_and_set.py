def list_unique_names(phonebook):
    unique_names = []
    for name, phonenumber in phonebook:
        firstname, lastname = name.split(" ", 1)
        for unique in unique_names:
            if unique == firstname:
                break
        else:
            unique_names.append(firstname)
    return len(unique_names)

def set_unique_names(phonebook):
    unique_names = set()
    for name, phonenumber in phonebook:
        first_name, last_name = name.split(" ", 1)
        unique_names.add(first_name)
    return len(unique_names)

phonebook = [
    ("Joe Doe", "555-555-5555"),
    ("Albert Einstein", "212-555-5555"),
    ("John Murphey", "202-555-5555"),
    ("Albert Rutherford", "647-555-5555"),
    ("Elaine Bodian", "301-555-5555")
    ]
for i in range(10000):
    if (i % 2 == 0):
        phonebook.append(("Jo" + chr(i) + " Doe", "555-555-5555"))
    else:
        phonebook.append(("Elaine"+ chr(i) +" Bodian", "301-555-5555"))

print ("Number of unique name from set method", set_unique_names(phonebook))
print ("Number of unique names from list method", list_unique_names(phonebook))
#In [21]: %timeit list_unique_names(phonebook)
#1 loop, best of 3: 2.3 s per loop

#In [22]: %timeit set_unique_names(phonebook)
#100 loops, best of 3: 9.44 ms per loop