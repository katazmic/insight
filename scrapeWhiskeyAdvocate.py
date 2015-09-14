from bs4 import BeautifulSoup
import urllib2
import json


# Whiskey Advocate

data = {}
nameList2 = []
for i in range(287):
    url = 'http://whiskyadvocate.com/ratings-reviews/?brand_id=0&rating=0&price=0&category_id=0&issue_id=0&reviewer=0&page_num=%d'%(i)
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    for link in soup.findAll("div", {"class":"review"}):
        nameF = link.find('h2').get_text()
        name = nameF.split('Price: ')[0]
        data[name] = {}
        review = link.get_text()
        nameList2.append(name)
        print name
        data[name]['price'] = str(nameF.split('Price: ')[1])
        data[name]['desc'] = review
    print i

with open('whiskyadv.json', 'w') as ff:
     json.dump(data, ff)


ff.close()


#for cigar in jrcigars
#https://www.jrcigars.com/brands/cigars
#find image from class="img-large"
