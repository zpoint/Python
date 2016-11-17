from PIL import Image
import os
"""
import pytesseract
image = Image.open('C:\\Users\\z\\Desktop\\1.png')
vcode = pytesseract.image_to_string(image, lang='chi_sim')
print(vcode)
with open('C:\\Users\\z\\Desktop\\1.txt', 'w', encoding='utf8') as f:
    f.write(vcode)
"""

def cut(im, piece = 1, vertical = True):
    """横向(纵向)平均分成piece等分, 返回 [region1, region2...region(piece)]"""
    imList = []
    if piece == 1:
        imList.append(im)
        return imList
    else:
        xsize = im.size[0] / piece
        ysize = im.size[1] / piece
        baseLeft = 0
        baseUp = 0
        baseRight = 0
        baseDown = 0
        if vertical: # 左右分
            baseRight = xsize
            baseDown = im.size[1]
            for _ in range(piece):
                imList.append(im.crop((baseLeft, baseUp, baseRight, baseDown)))
                baseLeft += xsize
                baseRight += xsize
        else: # up down split
            baseRight = im.size[0]
            baseDown = ysize
            for _ in range(piece):
                imList.append(im.crop((baseLeft, baseUp, baseRight, baseDown)))
                baseUp += ysize
                baseDown += ysize
    return imList
    
            
def resize(im,  ratio = 1):
    "压缩ratio倍图片并返回region"
    xsize = im.size[0]
    ysize =im.size[1]
    return im.resize((int(xsize / ratio), int(ysize / ratio)), Image.ANTIALIAS)

def getFilePath(path = "", rec = False, format = ("jpg", "png", "jpeg")):
    "return a list of jpg/png/... file name"
    FileList = []
    pathobj = os.listdir() if path == "" else os.listdir(path)
    for filename in pathobj:
        filename = path + filename
        #print ("path:", path, "Filename:", filename)
        if (os.path.isdir(filename)) and rec:
            new_list = getFilePath(filename + "/", rec, format)
            FileList += new_list
            continue;
        postfix = filename.split(".")[-1]
        if postfix in format:
            FileList.append(filename)
    return FileList

def getYN(string, V = False):
    while (1):
        rec = input("\n" * 2 + string + "\n").strip()
        if rec == "Y" or rec == 'y':
            return True
        elif rec == "N" or rec == "n":
            return False
        elif V == True and (rec == "Q" or rec == 'q'):
            return "Q"
        else:
            print("错误输入, 请重新输入")

def getint(string):
    while (1):
        piece = input(string + "\n")
        try: 
            piece = int(piece)
            return piece
        except Exception:
            print ("输入有误，请重试")

def getnerate_newdir(eachFile, imList, i):
    tmp = "" if len(imList) == 1 else str(i)
    filestr_list = eachFile.split("/")
    if len(filestr_list) == 1:
        new_dir = "new_" + eachFile[:eachFile.index(".")] + tmp + "." + eachFile.split(".")[-1]
    else:
        final_str = filestr_list[-1]
        filestr_list[-1] = "new_" + final_str[:final_str.index(".")] + tmp + "." + final_str.split(".")[-1]
        new_dir = "/".join(filestr_list)
    if os.path.isfile(new_dir):
        return getnerate_newdir(eachFile, imList, str(i) + "0")
    else:
        return new_dir

def main():
    print("本程序将帮助您批量裁剪，压缩当前目录下的图片\n")
    rec = getYN("是否寻找当前目录下子文件夹中的图片, 输入 Y 确定, N 不需要")

    FileList = getFilePath(rec=rec)
    if (len(FileList) == 0):
        print ("当前指定的目录下无图片文件, 欢迎下次使用")
        return
    for eachFile in FileList:
        print(eachFile)
    vertical = getYN("\n\n在您指定的目录下搜索到如上文件, 需要从左至右切割或从上到下切割吗?\n\n输入 Y 从左至右, N 从上到下,  Q 不需要", True)
    if (vertical == "Q"):
        piece = 1
    else:
        piece = getint("\n\n您想把一副图片分成几小幅? (输入小于10的整数)")
    ratio = getint("\n\n您想把一副图压缩至原来的几分之一呢? (小于10的整数) (输入1不压缩)")

    for eachFile in FileList:
        im = Image.open(eachFile)
        imList = cut(im, piece, vertical)
        for i in range(len(imList)):
            #print (eachFile)
            imList[i] = resize(imList[i], ratio = ratio)
            new_dir = getnerate_newdir(eachFile, imList, i)
            #print(new_dir)
            imList[i].save(new_dir)
            print("保存成功 ", new_dir)
            
    

if __name__ == "__main__":
    main()
    os.system('pause')