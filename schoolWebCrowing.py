
from bs4 import BeautifulSoup
import time
import requests
from discord import Webhook, RequestsWebhookAdapter
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

urlIT = "https://cms.pknu.ac.kr"
urlPK = "http://www.pknu.ac.kr"

#urlIT+'/itcae/view.do?no=9576'
responseIT = requests.get( urlIT+'/itcae/view.do?no=9576' , verify=False)

responsePK = requests.get(urlPK + '/usrBoardActn.do?p_bm_idx=5&p_boardcode=PK10000005')

while responseIT.status_code != 200:
    time.sleep(10)
    responseIT = requests.get(urlIT+'/itcae/view.do?no=9576' , verify=False)

while responsePK.status_code != 200:
    time.sleep(10)
    responsePK = requests.get(urlPK+ '/usrBoardActn.do?p_bm_idx=5&p_boardcode=PK10000005')

htmlIT = responseIT.text
soupIT = BeautifulSoup(htmlIT , features='html.parser')
prelistIT = soupIT.select(' #board_list > li > a')

htmlPK = responsePK.text
soupPK = BeautifulSoup(htmlPK, features='html.parser')
prelistPK = soupPK.select('#contents > div.contents-inner > form > table > tbody > tr > td.title')



#url = os.environ["WEBHOOKURL"]
url = 'https://discord.com/api/webhooks/796754970833321994/qRHzXRbi1bmpWMg-L5nTUmo9P2Z32mBHRxOAfDZ8dGTi9Z8nlkrjWD_6l7a4e5qPVGWu'
webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
text = "hello"
webhook.send(text)

while True:
    # time.sleep(600)
    responseIT = requests.get(urlIT+'/itcae/view.do?no=9576', verify=False)
    responsePK = requests.get(urlPK + '/usrBoardActn.do?p_bm_idx=5&p_boardcode=PK10000005')

    while responseIT.status_code != 200:
        time.sleep(10)
        responseIT = requests.get(urlIT+'/itcae/view.do?no=9576', verify=False)
    while responsePK.status_code != 200:
        time.sleep(10)
        responsePK = requests.get(urlPK + '/usrBoardActn.do?p_bm_idx=5&p_boardcode=PK10000005')

    htmlIT = responseIT.text
    soupIT = BeautifulSoup(htmlIT, features='html.parser')
    listIT = soupIT.select(' #board_list > li > a ')

    # for i in range(len(listIT)):
    #     print( listIT[i].find('h4').text.strip() + '\n' + urlIT + listIT[i].attrs['href'])

    htmlPK = responsePK.text
    soupPK = BeautifulSoup(htmlPK, features='html.parser')
    listPK = soupPK.select('#contents > div.contents-inner > form > table > tbody > tr > td.title')
    #listPKtitle = soupPK.select('#contents > div.contents-inner > form > table > tbody > tr > td.title > a')

    # for i in range(len(listPK)):
    #     print(listPK[i].find('a').text.strip() + '\n' + urlPK + listPK[i].find('a')['href'])
    # - prelistIT

    differrentIT = []
    for i in listIT:
        isIn = False
        for j in prelistIT:
            if (i.find('h4').text.strip() == j.find('h4').text.strip()) :
                isIn = True
                break
        if isIn == False:
            differrentIT.append(i)
    differrentPk = []
    for i in listPK:
        isIn = False
        for j in prelistPK:
            if i.find('a').text.strip() == j.find('a').text.strip():
                isIn = True
                break
        if not isIn:
            differrentPk.append(i)



    # differrentIT = list(set(listIT) - set(prelistIT))
    # differrentPk = list(set(listPK) - set(prelistPK))

    print('starting')
    for i in differrentIT :
        text = i.find('h4').text.strip() +'\n' + urlIT + i.attrs['href']
        webhook.send(text)
    for i in differrentPk:
        text = +i.find('a').text.strip() + '\n' + urlPK + i.attrs['href']
        webhook.send(text)
    print('end')
    prelistIT = listIT
    prelistPK = listPK

    time.sleep(3600)

    #print(listPK[i].find('a').text.strip() + '\n' + urlPK + listPK[i].find('a')['href'])
    #listITtitle[i].text.strip() + '\n' + urlIT + listIT[i].attrs['href']