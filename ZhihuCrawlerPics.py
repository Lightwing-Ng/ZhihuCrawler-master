#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
 * @author: Lightwing Ng
 * email: rodney_ng@iCloud.com
 * created on May 02, 2018, 5:14 PM
 * Software: PyCharm
 * Project Name: Tutorial
"""

import urllib, urllib2
import os, re


class ZhihuImgs:
    def __init__(self, url):
        self.url = url

    def getHtmlSourceCode(self):
        try:
            response = urllib2.urlopen(urllib2.Request(self.url))
            return response.read().decode('UTF-8')
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print('Lost Connection for: ', e.reason)
                return None

    def saveImages(self, imgList, title, author):
        count = 1
        if not os.path.exists('%s/%s' % (RES_DIR, title)):
            os.mkdir('%s/%s' % (RES_DIR, title))
        for x in imgList:
            fileName = '%s/%s/%s_%s.jpg' % (RES_DIR, title, author, str(count))
            try:
                u = urllib2.urlopen(x)
                data = u.read()
                f = open(fileName, 'wb+')
                f.write(data)
                print('Saving Picture: %s/%s_%s.jpg...' % (title, author, str(count)))
                f.close()

            except urllib2.URLError as e:
                print('Error: %s.' % e.reason)
            count += 1

    def getAllImgs(self, source):
        pattern = re.compile('data-actualsrc="(.*?)">', re.S | re.I)
        imgList = pattern.findall(source)

        return imgList

    def getTitle(self, source):
        pattern = re.compile('<h1 class="QuestionHeader-title">(.*?)</h1>', re.S)
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

    def run(self):
        source = self.getHtmlSourceCode().encode('UTF-8')
        title = self.getTitle(source)
        imgList = self.getAllImgs(source)
        author = self.getAuthor(source)
        self.saveImages(imgList, title, author)


RES_DIR = '知乎看片指日可待'
if not os.path.exists(RES_DIR):
    os.mkdir(RES_DIR)

f = open('URLs.txt')
for x in f:
    task = ZhihuImgs(x.strip())
    task.run()
f.close()
