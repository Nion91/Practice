# -*- coding: utf-8 -*-

import re
import os
import urllib2
from bs4 import BeautifulSoup


class CANRecall:
    def __init__(self):
        self.domain='http://www.healthycanadians.gc.ca'
        self.url='http://www.healthycanadians.gc.ca/recall-alert-rappel-avis/search-recherche/simple?s=&plain_text=&js_en=&page=20'
        self.contenturl=[]

    #获取目录
    def getUrlList(self,url=None):
        if url==None: url=self.url
        response=urllib2.urlopen(url)
        soup=BeautifulSoup(response.read())
        content=soup.find_all('div',class_='single_awr')
        for i in content:
            keyword=re.findall('Type of communication.*?(\w+?)\W',i.text,re.S|re.IGNORECASE)[0].lower()
            if keyword!='recall': continue
            iurl=self.domain+i.a['href']
            title=i.a.text.strip()
            date=re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}',i.text)[0]
            self.contenturl.append((date,title,iurl))

        #更新下一页
        self.nextpage=None
        alinks=soup.find_all('div',class_='margin-top-medium margin-bottom-none alignRight')[0].select('a')
        for a in alinks:
            if a.text.lower()=='next':
                self.nextpage=self.domain+a['href']
            else:
                continue

    def searchPage(self,pagenum=1):
        self.getUrlList()
        pagenum-=1
        while pagenum>0:
            self.getUrlList(self.nextpage)
            pagenum-=1

    #获取正文及图片
    def getRecall(self,url,filepath):
        response=urllib2.urlopen(url)
        soup=BeautifulSoup(response.read())

        #处理信息
        parent=soup.select('ul.anchor')[0].parent
        text=[]        
        for i in parent.descendants:
            if i.name==None: continue
            if re.match('h[1-9]',i.name):
                text.append('\n\n\n'+i.text.strip())
            elif re.match('d[dt]|p|caption|th$|td',i.name):
                temp=i.text.strip()
                temp=re.sub('\t\s*|\n\s+','\n',temp,re.S)
                text.append('\n'+temp)
            elif re.match('table|tr',i.name):
                text.append('\n')
            else:
                continue

        txtfile=filepath+os.sep+'recall.txt'
        self.saveContent(''.join(text),txtfile)

        #处理图片
        pct=soup.select('div[data-id="image_container"]')
        pctnum=1
        pct_domain=re.findall('(.*/)[^/]*',url)[0]
        if len(pct)>0:
            for i in pct:
                if len(i.select('a'))>0:
                    for a in i.select('a'):
                        if re.match('.*\\.jpg$',a['href']):
                            pctname=filepath+os.sep+'recall_%s.png' % pctnum
                            pcturl=pct_domain+urllib2.quote(a['href'].encode('utf-8'))
                            self.saveImage(pcturl,pctname)
                            pctnum+=1


    #储存信息
    def saveContent(self,text,filename):
        f=open(filename,'w')
        f.write(text.encode('utf-8'))
        f.close()

    #储存图片
    def saveImage(self,url,filename):
        reponse=urllib2.urlopen(url)
        img=open(filename,'wb')
        img.write(reponse.read())
        img.close()

    #执行
    def start(self,pagenum,filepath):
        print u'正在搜索目录...'
        self.searchPage(pagenum)

        print u'总共有%s个文件需要爬取' % len(self.contenturl)
        for i in range(len(self.contenturl)):           
            date=self.contenturl[i][0]
            title=self.contenturl[i][1]
            name=re.sub('[\\\\/:*?"<>|]','_',date+'_'+title)
            path=filepath+os.sep+name
            if not os.path.exists(path): os.mkdir(path)            
            url=self.contenturl[i][2]
            self.getRecall(url,path)

            print u'完成第%s个文件' % (i+1)

        print u'完成任务'

                    



if __name__=='__main__':
    can=CANRecall()
    can.start(5,'C:\\Users\\Administrator\\desktop\\test')
