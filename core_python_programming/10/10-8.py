def safe_input():
    try:
        temp = raw_input('Enter something:\n')
    except (EOFError,KeyboardInterrupt):
        temp = None
    return temp
print safe_input()