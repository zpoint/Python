"""
如室网图片下载
"""
import re
import os
import argparse
import requests

# http://new.rushi.net/home/works/detail/id/329211
url: str = ""
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Referer": url

}
id_ = ""
count = 0


def download_img(image_url):
    global count
    count += 1
    if ".png" in image_url:
        suffix = ".png"
    else:
        suffix = ".jpeg"
    file_name = str(id_) + "_" + str(count) + suffix
    print("正在下载图片: %s" % (img_url,))
    resp = requests.get(image_url, headers=headers)
    with open(file_name, "wb") as f:
        f.write(resp.content)
    print("已保存至: %s" % (os.path.abspath('.') + os.path.sep + file_name))

parser = argparse.ArgumentParser(prog='get_img')
parser.add_argument('url', help='链接')
args = parser.parse_args()
url = args.url
id_ = url.split("/")[-1]
# <img class="extend-original b-lazy b-loaded caiji_tupian" src="http://rushiwork.oss-cn-beijing.aliyuncs.com//works/wechat/202012/vh9kdwrushi.net.jpeg?x-oss-process=image/resize,w_800"
r = requests.get(url, headers=headers)
text = r.text
res = re.findall("<.+?extend-original.+?src=\"(.+?)\".+?>", text, re.DOTALL)
for each in res:
    img_url = each.replace("w_800", "w_3600")
    download_img(img_url)
