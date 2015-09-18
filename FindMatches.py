import numpy as np
import json 
import pandas as pd

import matplotlib.pyplot as plt


with open('CigarStructured.json') as cig_file:
    dataC= json.load(cig_file)

cig_file.close()


with open('WhiskeyStructured.json') as whisk_file:
    dataW= json.load(whisk_file)

whisk_file.close()





##### creating the SQL table


#SQL COMMAND
     ORDER BY matchScore


