# auto_douban
豆瓣小组自动回帖、顶贴
**请看这篇文章：http://xfxuezhang.cn/index.php/archives/213/**    


支持cookie登录和账号密码登陆（位置代码中自己找，print("* 模拟登陆... *")上面）；  
还加了换ip代理的，不过好像没什么用。  
登录多了的话，豆瓣会要求验证码，所以也加了验证码识别，用的百度文字识别api，注册后加上access_token 就行；不想注册的话，我的可以借给大家~  
具体回复的评论url id，是帖子链接上的数字，然后改到print("* 开始刷留言...* ")下面的urls里；如https://www.douban.com/group/topic/12345/中的12345  
if ("时光" in html_cookie.text):这里，把“时光”改成自己的昵称。  

---

> 此版本为试用，不稳定；更新增强版可联系

--- 

# UI新版
- 下载：[releases](https://github.com/1061700625/auto_douban/releases)

- CSDN：https://blog.csdn.net/sxf1061700625/article/details/140240548

![image](https://github.com/1061700625/auto_douban/assets/31002981/06ef3e0e-9dcb-464a-bade-f34927070674)


~~更：手机上的autojs脚本 —— https://blog.csdn.net/sxf1061700625/article/details/106652129~~
