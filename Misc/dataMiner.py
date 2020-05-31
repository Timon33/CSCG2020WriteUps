import requests
from lxml import etree
from io import StringIO
import base64
import codecs
import pytesseract
import time
try:
    import Image
except ImportError:
    from PIL import Image
from subprocess import check_output

url = "http://hax1.allesctf.net:9200/captcha/0"
#url = "google.com"

parser = etree.HTMLParser()

def get_links(tree):
    pass


def main():
    ses = requests.Session()
    ses.headers['User-Agent'] = 'Mozilla/5'

    response = ses.get(url)
    html = response.content.decode("utf-8")
    tree = etree.parse(StringIO(html), parser=parser)
    root = tree.getroot()

    base64Img = root[1][1][1][1][1][0][0].attrib['src'][22:]


    response = ses.post(url, data={"0": "0"})

    html = response.content.decode("utf-8")
    tree = etree.parse(StringIO(html), parser=parser)
    root = tree.getroot()

    answer = root[1][1][2][0].text

    fh = open("dataSet/" + answer + ".png", "wb")

    imgData = base64Img.encode('ASCII')
    fh.write(codecs.decode(imgData, encoding='base64'))
    fh.close()

# 100 images in ~30 sek
# 10000 images in ~50 min
# soulution would of been get parameter

for i in range(10000):
    main()
    if i % 100 == 0:
        print(i)
