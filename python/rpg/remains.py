# Remains

# Developer: Warren, https://www.patreon.com/rpgpython
# Script Version Number: v1.0
# Date: 21 Feb 2021

# If script errors, you may need to install the random and/or Columnar package
# Installing packages: https://packaging.python.org/tutorials/installing-packages/

# https://pypi.org/project/random2/
# pip install random2
import random

remains_type = random.choice(['utensils','apparel','harness','toys','optics','tome'])
u_type = ''
remains_type = 'tome'
if(remains_type == 'utensils'):
    roll = random.randrange(1,7,1)
    if(roll == 1): u_type = 'eating'
    if(roll == 2): u_type = 'digging'
    if(roll==3): u_type = 'writing'
    if(roll==4): u_type = 'navigating'
    if(roll==5): u_type = 'measuring'
    if(roll==6): u_type = 'musical'
    
if(remains_type == 'apparel'):
    roll = random.randrange(1,7,1)
    if(roll == 1): u_type = 'hauberk'
    if(roll == 2): u_type = 'boots'
    if(roll==3): u_type = 'cloak'
    if(roll==4): u_type = 'tunic'
    if(roll==5): u_type = 'mask'
    if(roll==6): u_type = 'breeches'
              
if(remains_type == 'harness'):
    roll = random.randrange(1,7,1)
    if(roll == 1): u_type = 'swimmer'
    if(roll == 2): u_type = 'flyer'
    if(roll==3): u_type = 'giant-animal'
    if(roll==4): u_type = 'small-animal'
    if(roll==5): u_type = 'man-sized'
    if(roll==6): u_type = 'colossal'
          
if(remains_type == 'toys'):
    roll = random.randrange(1,7,1)
    if(roll == 1): u_type = 'doll'
    if(roll == 2): u_type = 'vehicle'
    if(roll==3): u_type = 'weapon'
    if(roll==4): u_type = 'tool'
    if(roll==5): u_type = 'game'
    if(roll==6): u_type = 'house'
        
if(remains_type == 'optics'):
    roll = random.randrange(1,7,1)
    if(roll == 1): u_type = 'monocle'
    if(roll == 2): u_type = 'spectacles'
    if(roll==3): u_type = 'spyglass'
    if(roll==4): u_type = 'mirror'
    if(roll==5): u_type = 'colored pane'
    if(roll==6): u_type = 'periscope'
    
if(remains_type == 'tome'):
    
    c_roll = random.randrange(1,7,1)
    if(c_roll == 1): c_type = ' (treasure map)'
    if(c_roll == 2): c_type = ' (ancient legends)'
    if(c_roll==3): c_type = ' (natural guide and recipes)'
    if(c_roll==4): c_type = '(' + str(random.randrange(1,5,1)) + ' cleric prayers)'
    if(c_roll==5): c_type = '(' + str(random.randrange(1,5,1)) + ' arcane spells)'
    if(c_roll==6): c_type = 'codex, an ancient book composed of sheets of vellum, papyrus, or other materials.'
    
    roll = random.randrange(1,7,1)
    if(roll == 1): u_type = 'lexicon (dictionary)'
    if(roll == 2): u_type = 'scroll ' + c_type
    if(roll==3): u_type = 'manual'
    if(roll==4): u_type = 'tablet ' +  c_type
    if(roll==5): u_type = 'book ' + c_type
    if(roll==6): u_type = 'codex, an ancient book composed of sheets of vellum, papyrus, or other materials. ' +  c_type

print('You have come across some remains. The remains look to be ' + remains_type + ': ' + u_type + '.')

# Remains