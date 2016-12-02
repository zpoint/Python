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


def fix_cookie_format(filedir):
    result = ""
    with open(filedir, "r") as f:
        for line in f.readlines():
            print(line)
