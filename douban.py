#coding:utf-8

import requests
import time
import sys, os
import random
from bs4 import BeautifulSoup
import re
from PIL import Image
import urllib.request, urllib.parse, urllib3, base64
import requests.adapters
from goto import with_goto


def main():
    global sess
    sess = requests.session()
    start_flag = False
    vcode_flag = False
    proxies = {'https': '134.249.165.49:53281'}
    Reload = 0
    print("程序开始")
    while 1:
        if(Reload > 5):
            return
        ck = ''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }
        if(start_flag == False):
            url_login = "https://accounts.douban.com/j/mobile/login/basic"
            # requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
            # sess = requests.session()
            sess.keep_alive = False  # 关闭多余连接
            # sess.proxies = proxies
            while 1:
                print("* 获取验证码... *")
                url_img = sess.post(url_login, headers=headers)
                if(url_img.status_code == 403):
                    print("* 登录次数过多... *")
                    time.sleep(10)
                    return
                    # print("* 登录次数过多，1小时后重试 *")
                    # time.sleep(60*60)
                    # continue
                soup = BeautifulSoup(url_img.text, 'lxml')
                try:
                    img = soup.find("img", id="captcha_image")["src"]
                    img_id = re.findall(r'id=(.*)&', img)[0]
                    if(os.path.isfile('img.jpg')):
                        os.remove('img.jpg')
                    if (os.path.isfile('img2.jpg')):
                        os.remove('img2.jpg')
                    with open('img.jpg', 'ab+') as f:
                        f.write(requests.get(img).content)
                        f.close()
                    print("* 验证码处理... *")
                    vcode_proc()
                    time.sleep(1)
                    img_code = vcode2str()
                    print("* 验证码：", img_code, '*')
                except:
                    print("* 无需验证码登录 *")
                data = {
                    'name': USERNAME,
                    'password': PASSWORD,
                    'remember': 'on',
                    'ticket': '',
                    'ck': '',
                }
                print("* 模拟登陆... *")
                cookie_login_flag = False
                ck = ''
                html_login = sess.post(url_login, data=data, headers=headers)
                if(html_login.status_code != 200):
                    print("* 访问错误: ", html_login.status_code, '*')
                    print("1小时后重试")
                    time.sleep(60 * 60)
                    continue
                print(html_login.json())
                if html_login.json()['status'] == 'failed':
                    print('\r\n')
                    print(html_login.json()['description'])
                    return 0
                if(NAME in html_login.text):
                    break
                else:
                    if(html_login.json()['description'] == '需要图形验证码'):
                        print(">> 糟糕，需要滑块验证。")
                        print("如果是今天第一次运行，请手动打开网页登陆一下，再运行程序")
                        print("不然就过一会儿再试试")
                        print("滑块验证下次再加了")
                        break
                    else:
                        print("* 验证码识别错误,状态重置 *")
                    time.sleep(5)

            if("登录" in html_login.text or html_login.json()['description'] == '需要图形验证码'):
                # cookie登录部分未用到，可做参考
                print("* 模拟登录失败，那就换cookie登录吧 *")
                print("* Cookie登陆... *")
                url_cookie = "https://www.douban.com/group/topic/%s/?start=0" % ID
                header = {
                    'Cookie': COOKIE,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                }
                try:
                    html_cookie = sess.get(url_cookie, headers=header)
                except InvalidHeader:
                    print("Cookie无效")
                headers = header
                if ("登录" not in html_cookie.text):
                    cookie_login_flag = True
                    print("* Cookie登录成功 *")
                    print("* 获取ck... *")
                    soup = BeautifulSoup(html_cookie.text, 'lxml')
                    ck = soup.find_all('tbody')[0].find_all("a")[-1]['href'][-4:]
                    print("* 获取ck成功: ", ck, "*")
                else:
                    print("* Cookie登录也失败!!! *")
                    return 0
            else:
                print("* 模拟登录成功 *")

            if(cookie_login_flag == False):
                print("* 获取ck... *")
                url_ck = "https://www.douban.com/group/topic/%s/?start=0" % ID
                html_ck = sess.get(url_ck, headers=headers)
                soup = BeautifulSoup(html_ck.text, 'lxml')
                ck = soup.find_all('tbody')[0].find_all("a")[-1]['href'][-4:]
                print("* 成功获取ck: ", ck, "*")

            print("* 开始刷留言...* ")
            start_flag = True
        while 1:
            if(start_flag == True):
                urls = [
                        # r'https://www.douban.com/group/topic/144511002',
                        r'https://www.douban.com/group/topic/%s' % ID,
                        ]
                url_len = len(urls)
                for i in range(url_len):
                    url_group = urls[i] + r'/add_comment'
                    pars = [
                            "up"
                            "upup ",
                            "顶帖 ",
                            # "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。 ",
                            # "寥落古行宫，宫花寂寞红。白头宫女在，闲坐说玄宗。 ",
                            # "三日入厨下，洗手作羹汤。未谙姑食性，先遣小姑尝。 ",
                            # "君自故乡来，应知故乡事。来日绮窗前，寒梅著花未？ ",
                            # "独坐幽篁里，弹琴复长啸。深林人不知，明月来相照。 ",
                            # "床前明月光，疑是地上霜。举头望明月，低头思故乡。 ",
                            # "移舟泊烟渚，日暮客愁新。野旷天低树，江清月近人。 "
                    ]
                    one_par = pars[random.randint(0, len(pars)-1)]
                    Reload += 1
                    try:
                        url_2 = urls[i]
                        url_img = sess.post(url_2, headers=headers)
                        soup = BeautifulSoup(url_img.text, 'lxml')
                        if "登录" in url_img.text:
                            print(">> 未登录")
                        img = soup.find("img", id="captcha_image")["src"]
                        print(img)
                        print("* 刷留言失败，可能需要验证码 *")
                        while 1:
                            img_code = ''
                            img_id = ''
                            print("* 获取验证码... *")
                            url_img = sess.get(url_2, headers=headers)
                            if (url_img.status_code == 403):
                                print("403!!!")
                                break
                            soup = BeautifulSoup(url_img.text, 'lxml')
                            img = soup.find("img", id="captcha_image")["src"]
                            if (img != ''):
                                img_id = re.findall(r'id=(.*)&', img)[0]
                                if (os.path.isfile('img.jpg')):
                                    os.remove('img.jpg')
                                if (os.path.isfile('img2.jpg')):
                                    os.remove('img2.jpg')
                                with open('img.jpg', 'ab+') as f:
                                    f.write(requests.get(img).content)
                                    f.close()
                                print("* 验证码处理... *")
                                vcode_proc()
                                time.sleep(1)
                                try_count = 0
                                retry_flag = False
                                while 1:
                                    try:
                                        img_code = vcode2str()
                                        break
                                    except:
                                        try_count += 1
                                        if(try_count > 3):
                                            print("* 验证码无法识别，将重新获取 *")
                                            retry_flag = True
                                            break
                                        time.sleep(1)
                                        pass
                                if(retry_flag == True):
                                    continue
                                print("* 验证码：", img_code, '*')
                            data = {
                                'captcha-id': img_id,
                                'captcha-solution': img_code,
                                'ck': ck,
                                'rv_comment': one_par,
                                'start': 0,
                                'submit_btn': '发送',
                            }
                            html_group = sess.post(url_group, data=data, headers=headers, allow_redirects=False)
                            if(html_group.status_code == 200):
                                print("* 验证码识别错误,状态重置 *")
                            else:
                                break
                            start_flag = True
                    except Exception as e:
                        print("## 此为验证信息，请忽略 -", e, "##")
                        print("* 留言无需验证码 *")
                        data = {
                            'ck': ck,
                            'rv_comment': one_par,
                            'start': 0,
                            'submit_btn': '发送',
                        }
                        html_group = sess.post(url_group, data=data, headers=headers)
                    finally:
                        if(i == url_len-1):
                            delay = random.randint(30, 60)
                            print("-> 全部发送成功,休息", delay, "分钟 - ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                            time.sleep(60 * delay)
                            return
                        print("* 第", i+1, "个发送成功:%s *" % one_par)
                        print("* 休息5s *")
                        time.sleep(5)
                        start_flag = True


def vcode_proc():
    img = Image.open(r'img.jpg').convert("L")
    pixdata = img.load()
    threshold = 50
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1] > 245:
                count = count + 1
            if pixdata[x,y+1] > 245:
                count = count + 1
            if pixdata[x-1,y] > 245:
                count = count + 1
            if pixdata[x+1,y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x,y] = 255
    img.save('img2.jpg')
    
def vcode2str():
    access_token = ''
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/webimage?access_token=' + access_token
    f = open(r'img2.jpg', 'rb')
    img = base64.b64encode(f.read())
    f.close()
    params = {"image": img}
    params = urllib.parse.urlencode(params).encode(encoding='UTF-8')
    request = urllib.request.Request(url, params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib.request.urlopen(request)
    content = response.read()
    if (content):
        strings = eval(bytes.decode(content))
        try:
            words = strings["words_result"][0]['words']
            print("识别结果：", words)
            return words
        except Exception as e:
            print("* API接口调用出错：", e)
            print(strings)
            try:
                if(strings["error_code"] == 17):
                    print("* 日调用次数已上限：", strings["error_msg"], "*\r\n")
                    input()
                    return 0
            except:
                pass

if __name__ == '__main__':
    # vcode2str()函数下的access_token请自行添加
    sess = requests.session()
    ID = input("输入贴子地址猴的数字，如https://www.douban.com/group/topic/12345/中的12345：").strip()
    NAME = input('输入你的豆瓣昵称，如 时光：').strip()
    USERNAME = input('输入你的登陆用户名，如15797698335：').strip()
    PASSWORD = input('输入你的登陆密码，如pwd：').strip()
    COOKIE = input('可选！输入Cookie，回车跳过：').strip()

    print('\r\n')
    print('*'*50)
    print('* ID: ', ID)
    print('* NAME: ', NAME)
    print('* USERNAME: ', USERNAME)
    print('*'*50, '\r\n')
    while 1:
        if main() == 0:
            break
    input('任意键退出...')

