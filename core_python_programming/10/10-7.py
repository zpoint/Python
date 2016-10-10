def wrapopen():
    try:
        f = open(raw_input('Please enter a filename:'))
    except IOError as reason:
        f = None
    return f
print wrapopen()