import numpy as np
import json 
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
import matplotlib.pyplot as plt



def find_notes_and_categories(flc,app):
    st = LancasterStemmer()
    words_f = []
    notes = []
    category = []
    flav_wrds =  word_tokenize(flc)
    for i in flav_wrds:
        try:
            words_f.append(str(i).lower())
            words_f.append(st.stem(str(i).lower()))  
        except:
            pass    
    catbinary  = []
    for i in app:
        if len(set(words_f).intersection(app[i])) !=0:
            notes = notes + list(set(words_f).intersection(app[i]))
            category.append(str(i))
            catbinary.append(1)
        else:
            catbinary.append(0)        
    return notes, category, catbinary


def find_notes_profile(flc,app):
    st = LancasterStemmer()
    words_f = []
    notes = []
    notesbinary = []
    flav_wrds =  word_tokenize(flc)
    for i in flav_wrds:
        try:
            words_f.append(str(i).lower())
            words_f.append(st.stem(str(i).lower())) 
        except:
            pass
    for i in range(len(app)):
        if app[i] in words_f:
            notes.append(app[i])
            notesbinary.append(1)
        else:
            notesbinary.append(0)
    return notes, notesbinary

#####################################################################


with open('NonCubanCigar.json') as cig_file:
    dataNCCig= json.load(cig_file)

cig_file.close()



with open('CubanCigar.json') as cig_file:
    dataCCig= json.load(cig_file)

cig_file.close()


dataNCCig.update(dataCCig);
data =  dataNCCig       


name = []
for i in data.keys():
    name.append(i.lower())


L = len(data)
for i in range(L):
    if data[name[i]]['flavor'] == 'N/A':
        del data[name[i]]

    
fl = []    
for i in data:
    fl.append(data[i]['flavor'])


# cigar attributes



# cigar attributes

strength = ['medium', 'light', 'strong', 'full','strenght','strong','full-bodied']
categories_notes = {'flowers':['tulips','violets','bouquet','flowers','floral'], 'plants':['hay','grass','grassy','moss','cedar','cedary','oak','smoky','wood','woody','woodsy','woodiness','tea','tobacco','vegetal'], 'herbs and spices':['spice','spiciness','spicy','spices','mint','anice','licorice','cardamom','cardamon','nutmeg','pepper','peppery','cinnamon','clove','cloves','cumin','cayenne','chili','minty'],'earth and minerals':['barnyard','earth','earthy','earthy/peaty','earthiness','lead','graphite','mineral','musk','musty','salt','salty','saltiness','savory'],'fruit':['peach','fruity','fruit','mango','pineapple','apple','raisin','plum','orange','zest','molasses','currant','citrus','lemon','cherry','cherries','berry','vanilla'],'nuts':['walnut','peanut','marzipan','cashew','almond','nut','nuts','nuttiness','nutty','hazelnut'],'leather':['leather','leathery'],'honey':['honey','sweet','sweetness','candy'],'cream':['cream','milky','creamy','creaminess'],'chocolate':['cocoa','chocolate','chocolately','chocolaty'],'coffee':['espresso','coffee/mocha','coffee','mocha','roasted'],'caramel':['caramel','toffee','butter','buttery','butterscotch'],'hrashness':['char','bread','oat','dry','harsh','harshness','ammonia','barley']}

# add body! and strength perhaps?! need bigrams! 

categories = categories_notes.keys()

allNotes = []
for i in categories_notes:
    allNotes = allNotes + categories_notes[i]


app = categories_notes
cat_list = []
catB_list = []
k=0
for i in fl:
    notes, category,catBinary = find_notes_and_categories(i,app)
    cat_list.append(category)
    catB_list.append(catBinary)
    if len(category) == 0:
        print i
        k = k+1

app = allNotes
notes_list = []
notesBinary_list = []
for i in fl:
    notes, notesBin = find_notes_profile(i,app)
    notes_list.append(notes)
    notesBinary_list.append(notesBin)
    if len(notes) == 0:
        print i


dataStr = {}
k=0
for i in data:
    if len(notes_list[k]) !=0:
        dataStr[i] = {}
        dataStr[i]['name'] = str(i)
        notes = ''
        for nts in notes_list[k]:
            notes = notes + nts
            if nts != notes_list[k][-1]:
                notes = notes + ', '
        dataStr[i]['notes'] = notes
        dataStr[i]['flavor'] = data[i]['flavor']
        dataStr[i]['link'] = str(data[i]['link']) 
        dataStr[i]['image'] = str(data[i]['image'])
        categories = ''
        for nts in cat_list[k]:
            categories = categories + nts 
            if nts != cat_list[k][-1]:
                categories = categories + ', '
        dataStr[i]['categories'] = categories
        dataStr[i]['binaryNotes'] = notesBinary_list[k]
        dataStr[i]['binaryCategories'] = catB_list[k]
    k=k+1


with open('CigarStructured.json', 'w') as ff:
    json.dump(dataStr, ff)

div = []
for i in dataStr:
    div.append(float(sum(dataStr[i]['binaryCategories']))/float(sum(dataStr[i]['binaryNotes'])))

