import numpy as np
import json 
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


from sklearn.decomposition import PCA


with open('MoM_whiskeys.json') as mom_file:
    dataMoM = json.load(mom_file)

mom_file.close()

with open('whiskyCast.json') as castfile:
    dataCast = json.load(castfile)

castfile.close()



with open('NonCubanCigar.json') as cig_file:
    dataNCCig= json.load(cig_file)

cig_file.close()



with open('CubanCigar.json') as cig_file:
    dataCCig= json.load(cig_file)

cig_file.close()


data = dataCCig;

            

name = []
for i in data.keys():
    name.append(i.lower())





for i in data:
    if data[i]['flavor'] == 'N/A':
        print i
        del data[i]
        
    
fl = []    
for i in  data:
    fl.append(data[i]['flavor'])


# cigar attributes

strength = ['medium', 'light', 'strong', 'full','strenght','strong','full-bodied']
appended_cigar_flavors = {'flowers':['bouquet','flowers','floral'], 'plants':['hay','grass','grassy','moss','cedar','cedary','oak','smoky','wood','woodsy','woodiness','tea','tobacco','vegetal'], 'herbs and spices':['spice','spiciness','spicy','spices','mint','anice','licorice','cardamom','cardamon','nutmeg','black','pepper','white','green','red','cinnamon','clove','cloves','cumin','cayenne','chili'],'earth and minerals':['barnyard','earth','earthy','earthy/peaty','earthiness','lead','graphite','mineral','musk','musty','salt','salty','saltiness','savory'],'fruit':['raisin','plum','orange','zest','molasses','currant','citrus','lemon','cherry','cherries','berry','vanilla'],'nuts':['walnut','peanut','marzipan','cashew','almond','nut','nuts','nuttiness','nutty','hazelnut'],'leather':['leather','leathery'],'honey':['honey','sweet','sweetness','candy'],'cream':['cream','milky','creamy','creaminess'],'chocolate':['cocoa','chocolate','chocolately','chocolaty'],'coffee':['espresso','coffee/mocha','coffee','mocha','roasted'],'caramel':['caramel','butter','buttery','butterscotch'],'hrashness':['char','bread','dry','harsh','harshness','ammonia']}
# add body! and strength perhaps?! need bigrams! 


appExt = []
for i in appended_cigar_flavors:
    appExt = appExt + appended_cigar_flavors[i]

app = appExt


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
    
    catbinary  = []
    for i in app:
        if len(set(words_f).intersection(app[i])) !=0:
            notes = notes + list(set(words_f).intersection(app[i]))
            category.append(app.keys().index(i))
            catbinary.append(1)
        else:
            catbinary.append(0)
        
    return notes, category, catbinary


def find_notes_profile(flc,app):
    words_f = []
    notes = []
    notesbinary = []
    flav_wrds =  flc.split(' ')
    for i in flav_wrds:
        try:
            words_f.append(str(i))
        except:
            pass
    for i in range(len(app)):
        if app[i] in words_f:
            notes.append(app[i])
            notesbinary.append(1)
        else:
            notesbinary.append(0)
    return notes, notesbinary




cat_list = []
catB_list = []
for i in fl:
    notes, category,catBin = find_notes_and_categories(i,app)
    cat_list.append(category)
    catB_list.append(catBin)
    
    if len(category) == 0:
        print i

notes_list = []
notesB_list = []
for i in fl:
    notes, notesBin = find_notes_profile(i,app)
    notes_list.append(notes)
    catB_list.append(notesBin)
    
    if len(category) == 0:
        print i


arr_inner_prod = np.inner(catB_list,catB_list)

catBarr = np.array(catB_list)

pca = PCA(n_components=2)

out = pca.fit_transform(catBarr)

LC = out.tolist()
X = []
Y = []
for i in LC:
    X.append(i[0])
    Y.append(i[1])

cpmC = pca.components_

from sklearn.decomposition import ProjectedGradientNMF
pca = ProjectedGradientNMF(n_components=2)

out = pca.fit_transform(catBarr)

LC = out.tolist()
X = []
Y = []
Z = []
for i in LC:
    X.append(i[0])
    Y.append(i[1])

cpmC = pca.components_
lis1 = cpmC[1].tolist()

for i in range(len(lis1)):
     if lis1[i]>0.5:
             print app[i]
 


