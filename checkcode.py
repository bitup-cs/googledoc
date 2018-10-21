#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib,urllib.request, urllib.parse
from xml.etree import ElementTree as ET
from datetime import *


class APIClient(object):
    def http_request(self, url, paramDict):
        paras = urllib.parse.urlencode(paramDict).encode('utf-8')
        # print post_content
        req = urllib.request.Request(url, data=paras)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor)
        response = opener.open(req, data=paras)
        return response.read()

    def http_upload_image(self, url, paramDict, filebytes):
        timestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        boundary = '------------' + hashlib.md5(timestr.encode('utf-8')).hexdigest().lower()
        boundarystr = '\r\n--%s\r\n' % (boundary)

        bs = b''
        for key in paramDict.keys():
            bs = bs + boundarystr.encode('ascii')
            param = "Content-Disposition: form-data; name=\"%s\"\r\n\r\n%s" % (key, paramDict[key])
            bs = bs + param.encode('utf8')
        bs = bs + boundarystr.encode('ascii')

        header = 'Content-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/gif\r\n\r\n' % (
            'sample')
        bs = bs + header.encode('utf8')

        bs = bs + filebytes
        tailer = '\r\n--%s--\r\n' % (boundary)
        bs = bs + tailer.encode('ascii')

        import requests
        headers = {'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
                   'Connection': 'Keep-Alive',
                   'Expect': '100-continue',
                   }
        response = requests.post(url, params='', data=bs, headers=headers)
        return response.text

class CheckCode():
    def __init__(self, username, password, softid = None, softkey=None, typeid = None):
        self.paramDict = {}
        self.paramDict['username'] = username
        self.paramDict['password'] = password
        self.paramDict['timeout'] = 60
        self.paramDict['softid'] = softid
        self.paramDict['softkey'] = softkey
        self.paramDict['typeid'] = typeid

        self.client = APIClient()

    def parse_result(self,result):
        root = ET.fromstring(result)
        rst_dict = {}
        for child in root:
            rst_dict[child.tag] = child.text
        print(rst_dict)
        return rst_dict


    def get_checkcode_byfile(self, file):
        from PIL import Image

        img = Image.open(file)
        if img is None:
            print('get file error!')
            return None
        img.save("upload.gif", format="gif")
        filebytes = open("upload.gif", "rb").read()

        respone_result = self.client.http_upload_image("http://api.ruokuai.com/create.xml", self.paramDict, filebytes)
        return self.parse_result(respone_result)

    def get_checkcode_byurl(self, url):
        self.paramDict['imageurl'] = url
        respone_result = self.client.http_request('http://api.ruokuai.com/create.xml', self.paramDict)

        return self.parse_result(respone_result)

    def get_user_info(self):
        para_dict = {'username':self.paramDict['username'], 'password':self.paramDict['password']}
        result = self.client.http_request('http://api.ruokuai.com/info.xml', para_dict)
        #{'Score': '24895', 'HistoryScore': '105', 'TotalScore': '105', 'TotalTopic': '7'}
        return self.parse_result(result)

    def report_fail_checkcode(self, id):
        para_dict = {'username':self.paramDict['username'], 'password':self.paramDict['password'], 'id':id}
        result = self.client.http_request('http://api.ruokuai.com/create.xml', para_dict)
        return self.parse_result(result)

if __name__ == '__main__':
    client = APIClient()

    checkcode = CheckCode('nijiahao', 'nijiahao1994', '1', 'b40ffbee5c1cf4e38028c197eb2fc751', '3060')
    while 1:
        paramDict = {}
        result = ''
        act = input('Action:')
        if act == 'info':
            paramDict['username'] = input('username:')
            paramDict['password'] = input('password:')
            result = client.http_request('http://api.ruokuai.com/info.xml', paramDict)

        elif act == 'info2':
            checkcode.get_user_info()

        elif act == 'register':
            paramDict['username'] = input('username:')
            paramDict['password'] = input('password:')
            paramDict['email'] = input('email:')
            result = client.http_request('http://api.ruokuai.com/register.xml', paramDict)
        elif act == 'recharge':
            paramDict['username'] = input('username:')
            paramDict['id'] = input('id:')
            paramDict['password'] = input('password:')
            result = client.http_request('http://api.ruokuai.com/recharge.xml', paramDict)
        elif act == 'url':
            paramDict['username'] = input('username:')
            paramDict['password'] = input('password:')
            paramDict['typeid'] = input('typeid:')
            paramDict['timeout'] = input('timeout:')
            paramDict['softid'] = input('softid:')
            paramDict['softkey'] = input('softkey:')
            paramDict['imageurl'] = input('imageurl:')
            result = client.http_request('http://api.ruokuai.com/create.xml', paramDict)
        elif act == 'report':
            paramDict['username'] = input('username:')
            paramDict['password'] = input('password:')
            paramDict['id'] = input('id:')
            result = client.http_request('http://api.ruokuai.com/create.xml', paramDict)
        elif act == 'upload':
            paramDict['username'] = input('username:')
            paramDict['password'] = input('password:')
            paramDict['typeid'] = input('typeid:')
            paramDict['timeout'] = input('timeout:')
            paramDict['softid'] = input('softid:')
            paramDict['softkey'] = input('softkey:')
            from PIL import Image

            imagePath = input('Image Path:')
            img = Image.open(imagePath)
            if img is None:
                print( 'get file error!')
                continue
            img.save("upload.gif", format="gif")
            filebytes = open("upload.gif", "rb").read()
            result = client.http_upload_image("http://api.ruokuai.com/create.xml", paramDict, filebytes)
        elif act == 'upload2':
            checkcode.get_checkcode_byfile('save.jpg')

        elif act == 'help':
            pass
        elif act == 'exit':
            break

        print(result)