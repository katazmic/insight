import numpy as np
import json 
import pandas as pd


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


with open('MoM_whiskeys.json') as mom_file:
    dataMoM = json.load(mom_file)

mom_file.close()

with open('whiskyCast.json') as castfile:
    dataCast = json.load(castfile)

castfile.close()



with open('NonCubanCigar.json') as cig_file:
    dataNCCig= json.load(cig_file)

cig_file.close()



with open('NonCubanCigar.json') as cig_file:
    dataNCCig= json.load(cig_file)

cig_file.close()

with open('CubanCigar.json') as cig_file:
    dataCCig= json.load(cig_file)

cig_file.close()



data = dataCCig;

attr = ['Palate','Nose']  
attr = ['flavor'] #check wrapper?!? in appearance


wrapper = data[name[100]]['origin'].split('Wrapper :')[1].split(' :')[0].split(' ')
wrapper.pop()

wrapper = ' '.join(wrapper)


k=0
num = []
for i in range(len(name)):
    if data[name[i]]['origin'] !='N/A':
        price = data[name[i]]['origin'].split('Price :')[1].split('More')[0]
        if 'each' in price:
            try:
                numP = str(price.split('$')[1].split(' ')[0])
                k=k+1
                try:
                    num.append(float(numP))
                except:
                    num.append((float(numP.split('-')[0])+ float(numP.split('-')[1]))/2)
            except:
                del data[name[i]]
                print price
            

name = []
for i in data.keys():
    name.append(i.lower())

#dataMoM = dataNCCig


oLen = len(data)
names =data.keys()
for i in range(oLen):
    if data[names[i]]['flavor'] == 'N/A':
        del data[names[i]]
        
    
fl = []    
for i in  data:
    fl.append(data[i]['flavor'])


newLen = len(data)

corpus = []
k=0
newLen = len(data)
for i in range(len(data)):
    corpus.append(data[data.keys()[i]]['flavor'])
    
    
    corpus.append(data[data.keys()[i]]['Nose'])

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

vectorizer = CountVectorizer( min_df = 1, stop_words = 'english',decode_error=u'ignore', ngram_range = (1, 1))

X = vectorizer.fit_transform(corpus)

A = X.toarray()


12_whiskey_flavor_cat = ['sweetness','fruity','floral','body','smoky','tobacco','medicinal','winey','spicy','malty','nutty','honey']

#cigar_flavors = 'flowers floral.hay grass moss cedar oak smoky wood tea tobacco vegetal.anice licorice cardamom cardamon black perrer white green red cinnamon clove cumin.barnyard earth lead graphite mineral must salt.raisin plum orange zest molasses currant citrus cherry.walnut peanut marzipan cashew almond.leaher.honey.cream.cocoa milt dark chocolate.espresso coffee roasted coffee coffee with milk.caramel.char.bread'

#appended_cigar_flavors = 'bouquet flowers floral.hay grass grassy moss cedar cedary oak smoky wood woodsy woodiness tea tobacco vegetal.spice spiciness spicy spices mint anice licorice cardamom cardamon nutmeg black pepper white green red cinnamon clove cloves cumin cayenne chili.barnyard earth earthy lead graphite mineral musk musty salt salty savory.raisin plum orange zest molasses currant citrus cherry vanilla.walnut peanut marzipan cashew almond nut nuts nuttiness nutty hazelnut.leather leathery.honey sweet sweetnesscandy.cream creamy creaminess.cocoa milk dark chocolate chocolately chocolaty.espresso coffee roasted coffee coffee with milk espresso.caramel butterscotch.char.breaddry harsh harshness ammonia.'

appended_cigar_flavors = {'flowers':['bouquet','flowers','floral'], 'plants':['hay','grass','grassy','moss','cedar','cedary','oak','smoky','wood','woodsy','woodiness','tea','tobacco','vegetal'], 'herbs and spices':['spice','spiciness','spicy','spices','mint','anice','licorice','cardamom','cardamon','nutmeg','black','pepper','white','green','red','cinnamon','clove','cloves','cumin','cayenne','chili'],'earth and minerals':['barnyard','earth','earthy','earthy/peaty','earthiness','lead','graphite','mineral','musk','musty','salt','salty','saltiness','savory'],'fruit':['raisin','plum','orange','zest','molasses','currant','citrus','lemon','cherry','cherries','berry','vanilla'],'nuts':['walnut','peanut','marzipan','cashew','almond','nut','nuts','nuttiness','nutty','hazelnut'],'leather':['leather','leathery'],'honey':['honey','sweet','sweetness','candy'],'cream':['cream','milky','creamy','creaminess'],'chocolate':['cocoa','chocolate','chocolately','chocolaty'],'coffee':['espresso','coffee/mocha','coffee','mocha','roasted'],'caramel':['caramel','butter','buttery','butterscotch'],'hrashness':['char','bread','dry','harsh','harshness','ammonia']}
# add body! and strength perhaps?! need bigrams! 


app = appended_cigar_flavors

def find_notes_and_categories(flc,app):
    words_f = []
    notes = []
    category = []
    flav_wrds =  flc.split(' ')
    for i in flav_wrds:
        try:
            words_f.append(str(i))
        except:
            pass
    for i in app:
        if len(set(words_f).intersection(app[i])) !=0:
            notes = notes + list(set(words_f).intersection(app[i]))
            category.append(app.keys().index(i))
    return notes, category


cat_list = []

for i in fl:
    notes, category = find_notes_and_categories(i,app)
    cat_list.append(category)
    
    if len(category) == 0:
        print i



cigar_fl_categ = cigar_flavors.split('.')
cigar_fl_list = []
for i in cigar_fl_categ:
    cigar_fl_list = cigar_fl_list + i.split(' ')

trA = np.transpose(A)
feat = vectorizer.get_feature_names()


strength = ['medium', 'light', 'strong', 'full','strenght','strong','full-bodied']


k=0
featsim = []
for i in range(len(trA)):
        if sum(trA[i])>20:
            featsim.append(feat[i])
            k = k+1


SS = strength  # finds if any of the words are part of bi or trigrams
for i in featsim:
    for j in SS:
        if i.lower().find(j.lower()) != -1:
            print i


for SS in cigar_fl_categ:
    for i in featsim:
        for j in SS.split(' '):
            if i.lower().find(j.lower()) != -1:
                print SS


    


inc = 0
for i in cigar_fl_list:
    if i in featsim:
        inc = inc+1
        print i

#find intersection between the feature and the corpus.. 


def find_in(s,data,feature):
    for i in range(len(data.keys())):
        if s.lower() in data.keys()[i].lower(): 
            print '%s palate is %s'%( data.keys()[i],data[data.keys()[i]][feature])


