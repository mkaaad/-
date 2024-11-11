import requests
import re
option=['A','B','C','D']
website='http://172.22.214.200/ctas/ajaxpro/CExam.CPractice,App_Web_tzfdzrj8.ashx'
print("欢迎使用刷题机")
print("源码：https://github.com/mkaaad/AutoWriter.git")
print("请输入cookie：")
cookie=input()
cookie={
		"ASP.NET_SessionId":cookie
        }
head={'Host': '172.22.214.200',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://172.22.214.200/ctas/CPractice.aspx',
    'Content-Length': '100',
    'Origin': 'http://172.22.214.200',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain; charset=utf-8', 
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'}
chapter=input("请输入章节号，如02：")
start=1
if chapter!="08" and chapter!="09":
    end=int(input("请输入结束小节："))
    nums=range(start,end+1)
sumer=0
if chapter=="09":
    nums=[1,11,2,21,3,31,4,41,5,51,6,61,7,71,8]
if chapter=="08":
    nums=['01','02','03','04','05','06','07','08','09','091','10','101','11','111','12','121','13','131','14','141','15','151','16','161','17','171','18','181','19','191']
for num in nums:
    index=0
    if (int(num)<10 or chapter=="09") and chapter!="08":
            num='0'+str(num)
    else:
            num=str(num)
    while True:       
        quest='{"strTestParam":"<cTest><cProgram>ch0'+chapter+'_0'+num+'</cProgram><cQuestionIndex>'+str(index)+'</cQuestionIndex></cTest>"}'
        head['X-AjaxPro-Method']='GetJSONTest'
        r=requests.post(website,data=quest,headers=head,cookies=cookie)
        text=r.text
        if 'null'==text[0:4]:  
            break
        else:
            questionid=re.search(r'\d+',r.text)
            questionid=questionid[0]
            head['X-AjaxPro-Method']='IsOrNotTrue'
            for answer in option:
                data='{"strTestParam":"<cTestParam><cQuestion>'+str(questionid)+'</cQuestion><cUserAnswer>'+answer+'</cUserAnswer></cTestParam>"}'
                r=requests.post(website,data=data,headers=head,cookies=cookie)
                if r.text=='1;/*':
                    print("第",chapter,"章第",num,"节第",index,"题答案为",answer)
                    head['X-AjaxPro-Method']='WriteLog'
                    requests.post(website,data=data,headers=head,cookies=cookie)
                    req=requests.post(website,data=data,headers=head,cookies=cookie)
                    if req.text=="null;/*":
                        print("第",questionid,"题已提交")
                    else :
                        print("第",questionid,"题提交错误")
                    break
        index+=1
        sumer+=1
print("题目已做完，共做",sumer,"题")
input("按回车键继续")
