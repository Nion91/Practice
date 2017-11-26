# -*- coding: utf-8 -*-
import reimport urllib2from bs4 import BeautifulSoup
class CANRecall:    def __init__(self):        self.domain='http://www.healthycanadians.gc.ca'        self.url='http://www.healthycanadians.gc.ca/recall-alert-rappel-avis/search-recherche/simple?s=&plain_text=&js_en=&page=20'        self.contenturl=[]        self.content=[]
    def getUrlList(self,url=None):        if url==None: url=self.url        response=urllib2.urlopen(url)        soup=BeautifulSoup(response.read())        content=soup.find_all('div',class_='single_awr')        for i in content:            keyword=re.findall('Type of communication.*?(\w+?)\W',i.text,re.S|re.IGNORECASE)[0].lower()            if keyword!='recall': continue            iurl=self.domain+i.a['href']            title=i.a.text.strip()            date=re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}',i.text)            self.contenturl.append((date,title,iurl))
        #更新下一页        nextpart=soup.find_all('div',class_='margin-top-medium margin-bottom-none alignRight')[0]        if nextpart.a.text.lower()=='next':            self.nextpage=self.domain+nextpart.a['href']        else:            self.nextpage=None
    def searchPage(self,pagenum=1):        self.getUrlList()        pagenum-=1        while pagenum>0:            self.getUrlList(self.nextpage)            pagenum-=1
    #获取正文及图片    def getRecall
if __name__=='__main__':    can=CANRecall()    can.searchPage(2)
