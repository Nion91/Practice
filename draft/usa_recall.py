# -*- coding: utf-8 -*-

import os
import re
import time
import urllib2
from bs4 import BeautifulSoup


#USA

class USARecall:
    def __init__(self):
        self.domain='https://www.cpsc.gov'
        self.url='https://www.cpsc.gov/Recalls'
        self.contenturl=[]
        self.content=[]

    #获取目录
    def getUrlList(self,url=None):
        if url==None: url=self.url
        response=urllib2.urlopen(url)
        soup=BeautifulSoup(response.read())
        content=soup.find_all('div',class_='views-field views-field-php')
        for i in content:
            date=i.find('div',class_='date').text
            title=i.find('div',class_='title').text
            iurl=self.domain+urllib2.quote(i.a['href'])
            self.contenturl.append((date,title,iurl))

        #准备下一页
        nexturl=soup.find('li',class_='next')
        self.nextpage=self.domain+nexturl.a['href'] if nexturl!=None else None


    def searchPage(self,pagenum=1):
        self.getUrlList()
        pagenum-=1
        while pagenum>0 and self.nextpage!=None:
            self.getUrlList(self.nextpage)
            pagenum-=1

    #获取正文及图片
    def getRecall(self):
        for i in range(len(self.contenturl)):
            url=self.contenturl[i][2]
            response=urllib2.urlopen(url)
            soup=BeautifulSoup(response.read())
            img=soup.find('div',class_='carousel-inner').img['src']
            if re.match('http',img)==None: img=self.domain+img
            summary=soup.find(id='summary_section').text
            details=soup.find(id='details_section').text
            self.content.append((img,summary,details))

            #停顿时间
            #if i%5==0: time.sleep(5)


    #保存正文
    def saveContent(self,content,filename):
        f=open(filename,'w')
        f.write(content[1].encode('utf-8'))
        f.write(content[2].encode('utf-8'))
        f.close()


    #保存图片
    def saveImage(self,imgurl,imgname):
        response=urllib2.urlopen(imgurl)
        img=open(imgname,'wb')
        img.write(response.read())
        img.close()

    #保存到目录
    def saveDir(self,filepath):
        for i in range(len(self.content)):
            date=self.contenturl[i][0]
            title=re.findall('(.*?) Due to',self.contenturl[i][1],re.IGNORECASE)
            title=title[0] if len(title)>0 else self.contenturl[i][1]
            name=re.sub('[\\\\/:*?"<>|]','_',date+'_'+title)
            path=filepath+os.sep+name

            if os.path.exists(path):
                print u'文件已存在 %s' % name
                continue
            
            os.mkdir(path)
            self.saveContent(self.content[i],path+os.sep+'recall.txt')
            self.saveImage(self.content[i][0],path+os.sep+'recall.png')

    #执行
    def start(self,pagenum,filepath):
        print u'正在搜索目录...'
        self.searchPage(pagenum)
        print u'正在爬取正文...'
        self.getRecall()
        print u'正在储存文件...'
        self.saveDir(filepath)
        print u'完成任务'

    




if __name__=='__main__':
    usa=USARecall()
    usa.start(1,'C:\\Users\\Administrator\\desktop\\test')
