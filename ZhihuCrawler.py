#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
 * @author: Lightwing Ng
 * email: rodney_ng@iCloud.com
 * created on May 02, 2018, 10:00 AM
 * Software: PyCharm
 * Project Name: 自己模仿写
未得到问题下所有回答
原因：JS自动加载
"""

import os
import urllib, urllib2
import re, datetime


class removeTool:
    '''
    Remove HTML tags from the original results
    '''
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a>')  # <a.*?>(.*?)</a>
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')  # <div.*?>(.*?)</div>
    replaceTD = re.compile('<td>')  # <td>.*?</td>
    replacePara = re.compile('<p.*?>')  # <p.*?>(.*?)</p>
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')  # <.*?></(.*?)>

    def replace(self, x):
        x = re.sub(self.removeImg, '', x)
        x = re.sub(self.removeAddr, '', x)
        x = re.sub(self.replaceLine, '\n', x)
        x = re.sub(self.replaceTD, '\t', x)
        x = re.sub(self.replacePara, '\n    ', x)
        x = re.sub(self.replaceBR, '\n', x)
        x = re.sub(self.removeExtraTag, '', x)

        return x.strip()


class ZhihuCom(object):
    def __init__(self, baseUrl):
        self.baseURL = baseUrl
        self.tool = removeTool()
        self.file = None
        self.defaultTitle = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def getHtmlSourceCode(self):
        try:
            # return the source code
            response = urllib2.urlopen(urllib2.Request(self.baseURL))
            return response.read().decode('UTF-8')

        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print(u'Lost Connection for: ', e.reason)
                return None

    def getTitle(self, source):
        pattern = re.compile('<h1 class="QuestionHeader-title".*?>(.*?)</h1>', re.S)
        result = re.search(pattern, source)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getAuthor(self, source):
        pattern = re.compile('alt="(.*?)"/>', re.S | re.I)
        result = re.search(pattern, source)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getContent(self, source):
        '''
        获取正文内容
        :param source:
        :return:
        '''
        pattern = re.compile('itemProp="text">(.*?)</span>', re.S | re.I | re.M)
        results = re.findall(pattern, source)
        contents = []
        for x in results:
            content = self.tool.replace(x)
            contents.append(content)
        return contents

    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title + '.txt', 'w+')
        else:
            self.file = open(self.defaultTitle + '.txt', 'w+')

    def run(self):
        source = self.getHtmlSourceCode().encode('UTF-8')
        title = self.getTitle(source)
        author = self.getAuthor(source)

        f = open('%s/%s_%s.txt' % (RES_DIR, title, author), 'w+')
        result = self.getContent(source)
        print('>>> %s' % title)
        for x in result:
            f.write(x.strip())
        f.close()


RES_DIR = '知乎女子图鉴'
if not os.path.exists(RES_DIR):
    os.mkdir(RES_DIR)

f = open('URLs.txt')
for x in f:
    task = ZhihuCom(x.strip())
    task.run()
f.close()
