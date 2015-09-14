from bs4 import BeautifulSoup
import urllib2
import json

################

url = "http://cigarinspector.com/index-of-all-cuban-cigar-reviews"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
list = soup.find("div", {"class":"post-page-content"})

htmlToAppendCubanDic = []
data = {}
names = []
number = 0
LinkList = []
for link in list.findAll('a')[4:-4]:
    LinkList.append(link)

for link in LinkList: #back to 2
    number = number+1
    cigLink = link.get('href')
    cigName = cigLink.split('/')[-1].replace('-',' ')
    print cigName
    print number
    names.append(cigName)
    cPage = urllib2.urlopen(cigLink)
    cSoup = BeautifulSoup(cPage.read())
    cContent = cSoup.find("div", {"class":"post_content"})
    if cContent != None :
        leng = len(cContent.findAll('p'))
        data[cigName]={}
        data[cigName]['link'] = cigLink
        data[cigName]['brand'] = cigLink.split('/')[-2].replace('-',' ')

        if data[cigName]['brand'] == 'www.cigarinspector.com':
            data[cigName]['brand'] = 'N/A'
            
        try:
            data[cigName]['image'] = cSoup.find("meta" ,{"property":"og:image"}).get('content')
        except:
            data[cigName]['image'] = 'N/A'
            
        tot = ''
        for i in range(2,leng-1):
            scrpd = cContent.findAll('p')[i].get_text()  # origin format size ring price   
            if 'Origin :' in scrpd: # Flavor :  # Construction : # Value :  # Overall Rating :  # Origin :   
                data[cigName]['origin'] = scrpd # add_att_to_dict(scrpd,data[cigName])         
            if 'Flavor :' in scrpd:
                data[cigName]['flavor'] = scrpd.split('Flavor : ')[1]
            if 'Appearance :' in scrpd:
                data[cigName]['appearance'] = scrpd.split('Appearance : ')[1]
            if 'Construction :' in scrpd:
                data[cigName]['construction'] = scrpd.split('Construction : ')[1]
            if 'Value :' in scrpd:
                data[cigName]['value'] = scrpd.split('Value : ')[1]
            if 'Overall Rating :' in scrpd:
                data[cigName]['overall rating'] = scrpd.split('Overall Rating : ')[1]
            tot = tot+scrpd
        
        if len(tot)>1:
            data[cigName]['full review'] = tot
        else:
            data[cigName]['full review'] = 'N/A'
            
        try:
            data[cigName]['flavor']
        except: 
            data[cigName]['flavor'] = 'N/A'
        try:
            data[cigName]['origin']
        except: 
            data[cigName]['origin'] = 'N/A'
        try:
            data[cigName]['appearance']
        except: 
            data[cigName]['appearance'] = 'N/A'
        try:
            data[cigName]['construction']
        except: 
            data[cigName]['construction'] = 'N/A'
        try:
            data[cigName]['value']
        except: 
            data[cigName]['value'] = 'N/A'
        try:
            data[cigName]['overall rating']
        except: 
            data[cigName]['overall rating'] = 'N/A'
    
        rev = []
        for revs in cSoup.findAll("div",{"class":"comment_inside"}):
            rev.append(revs.find('p').get_text())
        
        if len(rev)>0:
            data[cigName]['reviews'] = rev
        else:
            data[cigName]['reviews'] = 'N/A'
                
                
    else:
        htmlToAppendCubanDic.append(cigLink)
    print 'done..'        
        
cubanCigar = data

with open('CubanCigar.json', 'w') as fp:
     json.dump(data, fp)
fp.close()
