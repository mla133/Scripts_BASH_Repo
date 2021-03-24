# Relics

# Developer: Warren, https://www.patreon.com/rpgpython
# Script Version Number: v1.0
# Date: 21 Feb 2021

# If script errors, you may need to install the random and/or Columnar package
# Installing packages: https://packaging.python.org/tutorials/installing-packages/

# https://pypi.org/project/random2/
# pip install random2
import random

# If you add more relic types, you'll need to add an if(relic_type == 'xxxx'): below
relic_type = random.choice(['tool','machine', 'tomb','armor','weapon','container'])
contents = ''

if(relic_type == 'tool'):
    # Feel free to add more types
    r_type = random.choice(['ladder','plow','pick','hoe','anvil','axe'])
    # Feel free to add more quality descriptions
    quality = random.choice(['broken','damaged','decent','fine','exceptional'])
    print('You have found an object from an earlier period, belonging to a period in the past' + 
          ' but has survived into the present. The object looks like a ' + relic_type +
          ', possibly a ' + r_type + '. Its quality is ' + quality + '.')

if(relic_type == 'machine'):
    # Feel free to add more types
    r_type = random.choice(['loom','grinding wheel','clock','balance','potter wheel','printing press'])
    # Feel free to add more quality descriptions
    quality = random.choice(['broken','damaged','decent','fine','exceptional'])
    print('You have found an object from an earlier period, belonging to a period in the past' + 
          ' but has survived into the present. The object looks like a ' + relic_type +
          ', possibly a ' + r_type + '. Its quality is ' + quality + '.')

if(relic_type == 'tomb'):
    # Feel free to add more types
    r_type = random.choice(['grave','sepulcher','mausoleum','catacomb','vault','crypt'])
    print('You have found an object from an earlier period, belonging to a period in the past' + 
          ' but has survived into the present. The object looks like a ' + relic_type + ', possibly a ' + r_type + '.')

if(relic_type == 'armor'):
    # Feel free to add more types
    r_type = random.choice(['breastplate','pair of greaves','a pair of gauntlets','helmut','chainmail','shield'])
    # Feel free to add more quality descriptions
    quality = random.choice(['broken','damaged','decent','fine','exceptional'])
    print('You have found an object from an earlier period, belonging to a period in the past' + 
          ' but has survived into the present. The object looks like a ' + relic_type +
          ', possibly a ' + r_type + '. Its quality is ' + quality + '.')

if(relic_type == 'weapon'):
    # Feel free to add more types
    r_type = random.choice(['dagger','scimitar','handaxe','spear','trident','battle axe'])
    # Feel free to add more quality descriptions
    quality = random.choice(['broken','damaged','decent','fine','exceptional'])
    print('You have found an object from an earlier period, belonging to a period in the past' + 
          ' but has survived into the present. The object looks like a ' + relic_type +
          ', possibly a ' + r_type + '. Its quality is ' + quality + '.')
    magical = random.randrange(1,21,1) # 1d20
    if(magical>18): # 19 or better rolled
        # Feel free to add more quality descriptions
        magic_quality = random.choice(['cursed','malfunctioning','a +1 item', 'charged with 1d6 uses'])
        print('The item is magical and is ' + magic_quality + '.')

if(relic_type == 'container'):
    # Feel free to add more types
    r_type = random.choice(['barrel(s)','urn(s)','trunk(s)','jar(s)','bottle(s)','box(es)'])
    # Feel free to add more content descriptions
    contents = random.choice(['containing nothing','containing spoiled food','containing drink','containing preserved food','containing general equipment item(s)','containing treasure'])
    print('You have found an object from an earlier period, belonging to a period in the past' + 
          ' but has survived into the present. The object looks like a ' + relic_type + ', possibly a ' + r_type + ' ' + contents  + '.')



# Relics
