
from bs4 import BeautifulSoup
import time
import requests
from discord import Webhook, RequestsWebhookAdapter
import os
import urllib3
import traceback
from apscheduler.schedulers.blocking import BlockingScheduler

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

urlIT = "https://cms.pknu.ac.kr"
urlPK = "http://www.pknu.ac.kr"

#urlIT+'/itcae/view.do?no=9576'

prelistPK = []
prelistIT = []
prelistCS = []

def timed_job():
    global prelistPK
    global prelistIT
    global prelistCS
    # contents > div.contents-inner > form:nth-child(3) > table > tbody > tr:nth-child(5) > td.title > a
    #while True:
    try:
        time.sleep(3600)
        # webhook.send("hellohello")
        responseIT = requests.get(urlIT + '/itcae/view.do?no=9576', verify=False)
        responseCS = requests.get(urlIT + '/ced/view.do?no=11084', verify=False)
        responsePK = requests.get(urlPK + '/usrBoardActn.do?p_bm_idx=5&p_boardcode=PK10000005')

        listIT = []
        listPK = []
        listCS = []

        while True:
            while responseIT.status_code != 200:
                time.sleep(10)
                responseIT = requests.get(urlIT + '/itcae/view.do?no=9576', verify=False)
            while responseCS.status_code != 200:
                time.sleep(10)
                responseIT = requests.get(urlIT + '/ced/view.do?no=11084', verify=False)
            while responsePK.status_code != 200:
                time.sleep(10)
                responsePK = requests.get(urlPK + '/usrBoardActn.do?p_bm_idx=5&p_boardcode=PK10000005')

            htmlIT = responseIT.text
            soupIT = BeautifulSoup(htmlIT, features='html.parser')
            listIT = soupIT.select(' #board_list > li > a ')

            htmlCS = responseCS.text
            soupCS = BeautifulSoup(htmlCS, features='html.parser')
            listCS = soupCS.select(' #board_list > li > a ')

            # for i in range(len(listIT)):
            #     print( listIT[i].find('h4').text.strip() + '\n' + urlIT + listIT[i].attrs['href'])

            htmlPK = responsePK.text
            soupPK = BeautifulSoup(htmlPK, features='html.parser')
            listPK = soupPK.select('#contents > div.contents-inner > form > table > tbody > tr > td.title')
            # listPKtitle = soupPK.select('#contents > div.contents-inner > form > table > tbody > tr > td.title > a')
            #    print(listPK)
            if listPK == [] or listIT == [] or listCS == []:
                print("break this")
                continue
            break
        # for i in range(len(listPK)):
        #     print(listPK[i].find('a').text.strip() + '\n' + urlPK + listPK[i].find('a')['href'])
        # - prelistIT

        differrentIT = []
        for i in listIT:
            isIn = False
            for j in prelistIT:
                if (i.find('h4').text.strip() == j.find('h4').text.strip()):
                    isIn = True
                    break
            if isIn == False:
                differrentIT.append(i)
        
        differrentCS = []
        for i in listCS:
            isIn = False
            for j in prelistCS:
                if (i.find('h4').text.strip() == j.find('h4').text.strip()):
                    isIn = True
                    break
            if isIn == False:
                differrentCS.append(i)

        differrentPk = []
        for i in listPK:
            isIn = False
            # print(i.find('a').text.strip())
            for j in prelistPK:
                if i.find('a').text.strip() == j.find('a').text.strip():
                    isIn = True
                    break
            if isIn == False:
                differrentPk.append(i)

        print('starting')
        for i in differrentIT:
            text =  'IT '+ i.find('h4').text.strip() + '\n' + urlIT + i.attrs['href']
            webhook.send(text)
        for i in differrentCS:
            text =  'CS '+ i.find('h4').text.strip() + '\n' + urlIT + i.attrs['href']
            webhook.send(text)
        for i in differrentPk:
            text = i.find('a').text.strip() + '\n' + urlPK + i.find('a').attrs['href']
            webhook.send(text)
        print('end')
        if listIT != [] and listCS != [] and listPK != []:
            prelistIT = listIT
            prelistPK = listPK
            prelistCS = listCS

    except Exception as e:
        print(e)
        webhook.send(e)
        webhook.send(traceback.format_exc(limit=None, chain=True))
        # print(listPK[i].find('a').text.strip() + '\n' + urlPK + listPK[i].find('a')['href'])
        # listITtitle[i].text.strip() + '\n' + urlIT + listIT[i].attrs['href']



while True:
    responseIT = requests.get( urlIT+'/itcae/view.do?no=9576' , verify=False)
    responseCS = requests.get(urlIT + '/ced/view.do?no=11084', verify=False)
    responsePK = requests.get(urlPK + '/usrBoardActn.do?p_bm_idx=5&p_boardcode=PK10000005')

    while responseIT.status_code != 200:
        time.sleep(10)
        responseIT = requests.get(urlIT+'/itcae/view.do?no=9576' , verify=False)

    while responseCS.status_code != 200:
        time.sleep(10)
        responseIT = requests.get(urlIT + '/ced/view.do?no=11084', verify=False)


    while responsePK.status_code != 200:
        time.sleep(10)
        responsePK = requests.get(urlPK+ '/usrBoardActn.do?p_bm_idx=5&p_boardcode=PK10000005')

    htmlIT = responseIT.text
    soupIT = BeautifulSoup(htmlIT, features='html.parser')
    prelistIT = soupIT.select('#board_list > li > a')

    htmlCS = responseCS.text
    soupCS = BeautifulSoup(htmlCS, features='html.parser')
    prelistCS = soupCS.select(' #board_list > li > a ')

    htmlPK = responsePK.text
    soupPK = BeautifulSoup(htmlPK, features='html.parser')
    prelistPK = soupPK.select('#contents > div.contents-inner > form > table > tbody > tr > td.title')

    if prelistPK == [] or prelistIT == [] or prelistCS == []:
        print("break this")
        continue
    break


url = os.environ["WEBHOOKURL"]
webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
text = "hello"
print(text)
#webhook.send(text)
#schedul

sched = BlockingScheduler()
sched.add_job(timed_job,'interval', minutes=60)
print("scheduled")
sched.start()

