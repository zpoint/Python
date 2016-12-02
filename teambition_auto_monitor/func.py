import sys


def pr_dir(obj):
    """print the type and content of the attribute of paramater"""
    print("Calling pr_dir for ", end="")
    print(obj)
    for each_attr in dir(obj):
        sys.stdout.write(each_attr + " ")
        exec(r'print((type(obj.%s), obj.%s))' % (each_attr, each_attr))
    print("Finish Call pr_dir for ", end="")
    print(obj)
