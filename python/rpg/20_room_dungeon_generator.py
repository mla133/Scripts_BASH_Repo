# Dungeon Generator - 20 rooms
# Developer: Warren, https://www.patreon.com/rpgpython
# Script Version Number: v1.0
# Date: 12 March 2021

# If script errors, you may need to install the random package
# https://pypi.org/project/random2/
# pip install random2
# Installing packages: https://packaging.python.org/tutorials/installing-packages/
import random

# percentage chance of occurance - adjust as you like
encounter = 10
hazard = 15
obstacle = 20
trap = 10
trick = 10
treasure = 10

# increased level of complication percentage - set between 1-5
# this gets added to percentages above as more rooms are generated
# 1 = +20% max, 2 = +40% max, 3 = +60% max, 4 = +80% max, 5 = +100% max
enc = 3
haz = 3
obs = 2
tra = 2
tri = 1
tre = 3

#https://pypi.org/project/Columnar/
#pip install Columnar
from columnar import columnar

# Enter the names of your characters
headers = ['Area', 'Encounter', 'Hazard', 'Obstacle','Trap','Trick','Treasure']
data = []

for x in range (1,21):     # generates 20 rooms
    en_roll = random.randrange(1,101,1)
    if(en_roll <= encounter):
        en = 'Yes'
    else: en=''
    ha_roll = random.randrange(1,101,1)
    if(ha_roll <= hazard):
        ha = 'Yes'
    else: ha=''
    ob_roll = random.randrange(1,101,1)
    if(ob_roll <= obstacle):
        ob = 'Yes'
    else: ob=''
    tp_roll = random.randrange(1,101,1)
    if(tp_roll <= trap):
        tp = 'Yes'
    else: tp=''
    tk_roll = random.randrange(1,101,1)
    if(tk_roll <= trap):
        tk = 'Yes'
    else: tk=''
    tr_roll = random.randrange(1,101,1)
    if(tr_roll <= treasure):
        tr = 'Yes'
    else: tr=''
 
    encounter += enc
    hazard += haz
    obstacle += obs
    trap += tra
    trick += tri
    treasure += tre
    
    data.append([str(x),en,ha,ob,tp,tk,tr])
    


table = columnar(data, headers)
print(table)





