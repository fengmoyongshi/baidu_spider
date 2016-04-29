#encoding:utf-8
from bs4 import BeautifulSoup
import re
import requests
import csv
import time
import codecs
import sys
import io

class FileRead:
    filename = ''
    def UrlParser(self,new_Url):
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
        first_url = new_Url
        try:
            html = requests.get(first_url, headers=headers)
            html.encoding = 'utf-8'
        except Exception as e:
            print(e)
        else:
            result = re.findall(r'<a class="result-title" href="(.*?)" target="_blank"><em>.*?</em>_百度百科</a>', html.text)
            if len(result)!=0:
                return result[0]
            
        
    def UserInfoParser(self,new_Url,name,job_detal):
        name1 = self.filename+'.csv'
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
        first_url = new_Url
        select_string = job_detal
        try:
            html = requests.get(first_url, headers=headers)
            html.encoding = 'utf-8'
        except Exception as e:
            print(e)
        else:
            soup = BeautifulSoup(html.text, 'html.parser', from_encoding='utf-8')
            url = soup.find_all("ul", "polysemantList-wrapper cmn-clearfix")
    ##        print(url)
            page_url = 'http://baike.baidu.com'
            new_full_url = []
            new_full_url.append(first_url)
            person_abstract = ''
            
            for e in url:
                s = str(e)
                model = re.findall(r'<li class="item">▪<a href="(.*?)" title', s,re.M)
                if model is not None:
                     for item in model:
                        new_full_url.append(page_url+item)
##                print(new_full_url)

            for url1 in new_full_url:
    ##            print(url1+"//n")
                isWrite = False
                try:
                    html1 = requests.get(url1, headers=headers)
                    html1.encoding = 'utf-8'
                except HTTPError as e:
                    break
                    print(e)
                soup1 = BeautifulSoup(html1.text, 'html.parser', from_encoding='utf-8')
                t1 = soup1.find_all("div", "lemma-summary")
                t2 = soup1.find_all("div", "basic-info cmn-clearfix")
                for link in t1:
##                    print("============================================================")
                    s = link.get_text()
                    person_abstract = s
##                    print(s)
    ##                for item in select_string:
                    pattern = re.compile(select_string)
                    match = pattern.search(s)
                    if match:
                        isWrite = True
##                    print("******")
##                    print(isWrite)
##                    print("*******")
##                    print("------------------------------------------------------------")   

                for link in t2:
                    line1 = link.get_text().splitlines()
                    line2 =[]
                    ch_name=name
                    birthplace=''
                    school=''
                    for item in line1:
                        if len(item)>0:
                            line2.append(item)
    ##                print(line2)
                    if isWrite == True:
    ##                    print(line2)
                        try:
                            try:
                                with open(name1,'a+',newline='',encoding='utf-8') as csvFile:
                                    writer = csv.writer(csvFile)
                                    count = 0
                                    for item in line2:
                                        if item=='中文名':
                                            ch_name = name
                                        elif item=='出生地':
                                            birthplace = line2[count+1]
                                        elif item=='毕业院校':
                                            school = line2[count+1]
                                        count = count + 1
                                    writer.writerow([ch_name,birthplace,school,person_abstract])
                            except Exception as err:
                                print(err)
                        finally:
                            csvFile.close()
                            
##                print("============================================================")

    def Open_CSV(self):
        try:
            try:
                name1 = self.filename+'.txt'
##                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors = 'replace', line_buffering = True)
                file=open(name1,'r',encoding='utf-8')
                text = file.read()
                lines = text.splitlines()
                for c1 in lines:
##                    print(c1)
                    root_url1 = 'http://baike.baidu.com/search?word='+c1+'&pn=0&rn=0&enc=utf8'
                    root_url = self.UrlParser(root_url1)
    ##                root_url = 'http://baike.baidu.com/item/'+c1
    ##                job_detal = c2
                    job_detal = '管理|首席|总监|董事|监事|会计|工程师|总裁|经理|秘书|财务|财务负责人|法律顾问|纪检组长|总经济师|工会主席|技术总监|办公室主任'
                    if root_url is not None:
    ##                    print(root_url)
                        self.UserInfoParser(root_url,c1,job_detal)
                    else:
                        root_url = 'http://baike.baidu.com/item/'+c1
                        self.UserInfoParser(root_url,c1,job_detal)
##                    time.sleep(1)
                print("All is done!")
            except Exception as err:
                print(err)
        finally:
            file.close()

                
if __name__=="__main__":
    Filename = input('please input the name of txt:')
    print("please wait..")
    obj_spider = FileRead()
    obj_spider.filename = Filename
    obj_spider.Open_CSV()
    print("All is done!")



