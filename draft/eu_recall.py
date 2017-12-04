# -*- coding: utf-8 -*-

import os
import re
import urllib2
from bs4 import BeautifulSoup
import time



class EuroRecall:
    def __init__(self):
        self.url='https://ec.europa.eu/consumers/consumers_safety/safety_products/rapex/alerts/?event=main.listNotifications'
        self.reporturl=[]

    #获取report目录
    def getReportUrl(self,year,num=None):
        response=urllib2.urlopen(self.url)
        soup=BeautifulSoup(response.read(),'lxml')
        alist=soup.find_all('a',href=re.compile('.*Year=%s$' % year,re.IGNORECASE))
        if num!=None: alist=alist[:num]
        for a in alist:
            url=a['href']
            date=re.findall('\d{2}/\d{2}/\d{4}',a.text)[0]
            date=time.strftime('%Y-%m-%d',time.strptime(date,'%d/%m/%Y'))
            report_id=re.findall('\\xa0([1-9]+?)\\r',a.text)[0]
            self.reporturl.append((date,report_id,url))
        

    #获取正文及图片
    def getRecall(self,url,path):
        response=urllib2.urlopen(url)
        soup=BeautifulSoup(response.read(),'lxml')
        recalls=soup.find_all(lambda x:x.name=='td' and not x.has_attr('role'))

        for r in recalls:
            #搜索正文
            text=['\n'+i.text.strip() for i in r.find_all('div',attrs={'class':False,'id':False})]
            text=''.join(text).encode('utf-8')

            #设置文件名
            alert_num=re.findall('alert number.*?([\\w/]+)\\n',text,re.IGNORECASE)[0]
            category=re.findall('category:.*?(\\w.*?)\\n',text,re.IGNORECASE)[0]
            product=re.findall('product:.*?(\\w.*?)\\n',text,re.IGNORECASE)[0]

            filename='_'.join([alert_num,category,product])
            filename=re.sub('[\\\\/:*?"<>|]','_',filename)
            filepath=path+os.sep+filename
            if not os.path.exists(filepath): os.mkdir(filepath)

            #储存文件
            f=open(filepath+os.sep+'recall.txt','w')
            f.write(text)
            f.close()

            #搜索并储存图片
            imgs=r.select('img.imageItem')
            if len(imgs)>0:
                count=1
                for i in imgs:
                    imgurl=i['src']
                    response=urllib2.urlopen(imgurl)
                    img=open(filepath+os.sep+'recall_%s.png' % count,'wb')
                    img.write(response.read())
                    img.close()
                    count+=1

    #执行
    def start(self,year,num,filepath):
        print u'正在搜索报告目录...'
        self.getReportUrl(year,num)
        print u'共有%s份报告需要爬取' % len(self.reporturl)

        for i in range(len(self.reporturl)):
            print u'开始爬取第%s份报告' % (i+1)
            date,report_id,url=self.reporturl[i]
            path=filepath+os.sep+date+' '+'Report %s' % report_id
            if not os.path.exists(path): os.mkdir(path)
            self.getRecall(url,path)

        print u'完成任务'


if __name__=='__main__':
    eu=EuroRecall()
    eu.start(2017,1,'C:\\Users\\Administrator\\desktop\\test')

