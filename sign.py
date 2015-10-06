#coding=utf-8
__author__ = 'ooooooooe'
import urllib2
import urllib
import cookielib
import threading
import json
import re
import time
import sys
reload(sys)
sys.setdefaultencoding("gbk")
Baidu_Url = u'http://www.baidu.com'
Title_Url = u'http://tieba.baidu.com/f/like/mylike?&pn='
#Sign_Url = u'http://tieba.baidu.com/sign/add'
Tbs_Url = u'http://tieba.baidu.com/dc/common/tbs'
Mo_Url = 'http://tieba.baidu.com/mo//m?kw='
###############################################################################
#--------------------------------cookie插入-----------------------------------#
###############################################################################
def make_cookie(name,value):
    cookie=cookielib.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain="baidu.com",
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None
    )
    return cookie
###############################################################################
#--------------------------------cookie确定-----------------------------------#
###############################################################################
def Cookie_Get():
    cookie = cookielib.CookieJar()
    BDUSS=''#此处是自己的BDUSS
    cookie_in=make_cookie('BDUSS',BDUSS)
    cookie.set_cookie(cookie_in)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    BaiduReq = urllib2.urlopen(Baidu_Url)
###############################################################################
#-------------------------------关注贴吧确定----------------------------------#
###############################################################################
def gz_sure(tot):
    Rec_Url = Title_Url + repr(tot)
    Listread = urllib2.urlopen(Rec_Url).read()
    str = r'title="(.+?)">\1</a></td>'
    p = re.compile(str)
    rs = re.findall(p,Listread)
    return rs
###############################################################################
#---------------------------------贴吧签到------------------------------------#
###############################################################################
def sign_tieba(Name):
    try:
        sj = urllib2.urlopen(Mo_Url+Name)
        s = sj.read().decode("utf-8")
        #print s
        s_str = r"<span >(?P<alright>.+)</span></td>"
        s_str = re.compile(s_str)
        mp = re.search(s_str,s)
        #print mp.group("alright") == u'已签到'
        if mp != None and mp.group("alright") == u'已签到':
            print "%s"% Name,u"吧已签到！"
            return 0
        str = '<div class="bc p">(?P<Name0>.+)<a href="(?P<Name1>.+)/(?P<Name2>.+)</a></div>'
        str = re.compile(str)
        mp = re.search(str,s)
        mp = mp.group("Name1")
        str2 = '<input type="hidden" name="fid" value="(?P<Name0>.+)"/>'
        str2 = re.compile(str2)
        mp2 = re.search(str2,s)
        s = urllib2.urlopen(Tbs_Url).read()
        str = r'{"tbs":"(?P<tbs>.+)","is_login":1}'
        str = re.compile(str)
        mp3 = re.search(str,s)
        tbs = mp3.group("tbs")
        Sign_Url = r'http://tieba.baidu.com'+mp+r'/sign?tbs='+tbs+'&fid='+mp2.group("Name0")+'&kw='+Name.decode('gb2312')
        #print Sign_Url
        urllib2.urlopen(Sign_Url).read()
        print "%s"% Name,u"吧成功！"
    except:
        print "%s"% Name,u"吧失败,请手动签到！"

Cookie_Get()
tot = 1
while(1):
    SignList = gz_sure(tot)
    if len(SignList) == 0:
        break
    for s in SignList :
        sign_tieba(s)
        time.sleep(10)
    tot = tot + 1
