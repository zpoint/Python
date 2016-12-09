import sys
import time
import urllib.parse
def pr_dir(obj):
    """print the type and content of the attribute of paramater"""
    print("Calling pr_dir for ", end="")
    print(obj)
    for each_attr in dir(obj):
        sys.stdout.write(each_attr + " ")
        exec(r'print((type(obj.%s), obj.%s))' % (each_attr, each_attr))
    print("Finish Call pr_dir for ", end="")
    print(obj)


def fix_cookie_format(filedir, filter_domain=()):
    result = ""
    linecount = 1
    with open(filedir, "r") as f:
        for line in f.readlines():
            if linecount == 1:
                if line != "# Netscape HTTP Cookie File":
                    result += "# Netscape HTTP Cookie File\n"
                    linecount += 1
            elif line[0] == "#":
                continue
            split_line = line.split("\t")
            if len(split_line) == 6:
                split_line.insert(4, str(int(time.time() + 2592000)))
            """
            index = 0
            while index < len(split_line):
                split_line[index] = urllib.parse.unquote(split_line[index])
                index += 1
            index = 0
            while index < len(split_line):
                split_line[index] = urllib.parse.unquote(split_line[index])
                index += 1
            """
            if filter_domain:
                if split_line[0] in filter_domain:
                    result += "\t".join(split_line)
            else:
                result += "\t".join(split_line)
    with open(filedir, "w") as f:
        f.write(result)
