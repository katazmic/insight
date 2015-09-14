from bs4 import BeautifulSoup
import urllib2
import json



# scraping whiskycast.com
linkList = []
nameList = []

for i in range(154):
    i=i+1
    print i
    url = "http://whiskycast.com/search/lagavelin/page/%d/?post_types=ratings&search_type=unified&s=lagavelin"%(i)
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    for link in soup.findAll("h2", {"class":"post-title"}):
        wLink = link.find('a').get('href')
        linkList.append(wLink)
        wName = wLink.split('/')[4].replace('-',' ')
        nameList.append(wName)
        print wName
        print wLink


wName = nameList
wLink = linkList

data = {}



for i in range(1530):
    print i
    data[wName[i]] = {}
    data[wName[i]]['link'] = wLink[i]
    page = urllib2.urlopen(wLink[i])
    soup = BeautifulSoup(page.read())
    content = soup.find("div", {"class":"post-content"})
    if len(content.findAll('p'))>1:
        specs = content.findAll('p')[0].get_text()
        desc =  content.findAll('p')[1].get_text()
    else:
        specs = 'N/A'
        desc =  content.findAll('p')[0].get_text()
    data[wName[i]]['specs'] = specs
    data[wName[i]]['description'] = desc
    print wName[i]


with open('whiskycast.json', 'w') as fp:
     json.dump(data, fp)


fp.close()



#for cigar in jrcigars
#https://www.jrcigars.com/brands/cigars
#find image from class="img-large"
