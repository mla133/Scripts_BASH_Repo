# Ruins

# Developer: Warren, https://www.patreon.com/rpgpython
# Script Version Number: v1.0
# Date: 17 Feb 2021

# If script errors, you may need to install the random and/or Columnar package
# Installing packages: https://packaging.python.org/tutorials/installing-packages/

# https://pypi.org/project/random2/
# pip install random2
import random


#for n in range(0,10):

condition = random.choice (['partially covered by ','fully covered by ','above ground','on a rocky slope','inside a cavern',
                            'in a crevice','beneath an overhang','in a large crater','partially sunken',
                            'charred and burnt'])
covered_by = ''
if(condition == 'partially covered by ' or condition == 'fully covered by '):
    covered_by = random.choice (['sand','ashes','cinders','earth','thicket','mold','slime','rocks',
                                 'web and dust','vines'])

state = random.choice (['cumbled and decayed','disfigured and defaced','worm-eaten','crystallized and petrified',
          'corroded and eroded','mouldy and contaminated','dangerous, but operational','partially operational',
          'fully operational'])

keeper = random.choice(['mechanical devices','some type of giant','some type of dragon','undead','lycanthropes',
                        'wild animals','traps','nothing','a humanoid (Goblin, Kolbold, Orc, Gnoll, Hobgoblin, Bugbear)',
                        'a humanoid (Mage, Archmage, or other Spellcaster)', 'a beast or monstrosity',
                        'a construct or elemental','fey or aberration (hag, fey, beholder, slaad, mind flayer)',
                        'a celestial or fiend (celestial, demon, yugologh, rakshasa)',
                        'ooze and/or plants'])




ruin_type = random.choice(['manor','village','city','citadel:','castle','temple'])


# MANOR

if(ruin_type == 'manor'):
    r_sub_type = random.choice(['hut','hovel','hall','villa','cottage','palace'])
    print('You have come across Ruins. The ruins are ' + condition + covered_by + ', ' + state + 
          '. Upon investigation, you notice that the ruins seem to be protected by ' + keeper +
          '. The ruins were once a ' + ruin_type + ', a ' + r_sub_type  + '.')

# VILLAGE

if(ruin_type == 'village'):
    r_sub_type = random.choice(['huts','hovels','cottages','cottages w/ a ditch','cottages w/ a palisade (stakewall)','cottages w/ a palisade (stakewall) and a moat'])
    if(r_sub_type == 'huts'):
        roll = random.randrange(1,7,1) + random.randrange(1,7,1)
    elif(r_sub_type == 'hovels'):
        roll = random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1)
    else:
        roll = random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1)    

    print('You have come across Ruins. The ruins are ' + condition + covered_by + ', ' + state + 
          '. Upon investigation, you notice that the ruins seem to be protected by ' + keeper + 
          '. The ruins were once a ' + ruin_type + ' of ' + str(roll) + ' ' + r_sub_type  + '.')

# CITY

if(ruin_type == 'city'):
    r_sub_type = random.choice(['houses and citadel','houses','houses and protective wall','houses and protective wall with',
                                     'houses and'])
    if(r_sub_type == 'houses and a citadel'):
        roll = random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1)
    if(r_sub_type == 'houses'):
        roll2 = random.randrange(1,3,1)
        if(roll2 == 1):
            roll = random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1)
        if(roll2 == 2):
            roll = random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1)
    if(r_sub_type == 'houses and protective wall'):
        roll = random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1)
    if(r_sub_type == 'houses and protective wall with'):
        roll_cit = random.randrange(1,5,1)
        r_sub_type = 'houses and wall with ' + str(roll_cit) + ' citadel(s)'
        roll = random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1) +random.randrange(1,7,1)
    if(r_sub_type == 'houses and'):
        roll_temple = random.randrange(1,5,1)
        r_sub_type = 'houses and ' + str(roll_temple) + ' temples'

    print('You have come across Ruins. The ruins are ' + condition + covered_by + ', ' + state + 
          '. Upon investigation, you notice that the ruins seem to be protected by ' + keeper +
          '. The ruins were once a ' + ruin_type + ' of ' + str(roll) + ' ' + r_sub_type + '.')


# CITADEL

if(ruin_type == 'citadel:'):
    r_sub_type = random.choice(['tower','tower and outer wall','great keep','keep and 4 towers',
                                'keep, 4 towers, and outer wall','keep, 4 towers, outer wall, and a moat'])
    print('You have come across Ruins. The ruins are ' + condition + covered_by + ', ' + state + 
          '. Upon investigation, you notice that the ruins seem to be protected by ' + keeper +
          '. The ruins were once a ' + ruin_type + ' a ' + r_sub_type  + '.')


# CASTLE

if(ruin_type == 'castle'):
    r_sub_type = random.choice(['keep and palisade (stakewall)','keep, palisade (stakewall), and moat',
                                'keep, palisade (stakewall), moat, and walls',
                                'keep, palisade (stakewall), moat, walls, and manor',
                                'keep, palisade (stakewall), moat, walls, manor, and 4 walls',
                                'keep, palisade (stakewall), moat, walls, manor, 4 towers, and outer walls'])
    print('You have come across Ruins. The ruins are ' + condition + covered_by + ', ' + state + 
          '. Upon investigation, you notice that the ruins seem to be protected by ' + keeper +
          '. The ruins were once a ' + ruin_type + ': a ' + r_sub_type  + '.')


# TEMPLE

if(ruin_type == 'temple'):
    r_sub_type = random.choice(['alter','shrine','sanctuary','oracle','pantheon','monastery'])
    print('You have come across Ruins. The ruins are ' + condition + covered_by + ', ' + state + 
          '. Upon investigation, you notice that the ruins seem to be protected by ' + keeper +
          '. The ruins were once a ' + ruin_type + ': a ' + r_sub_type  + '.')

print('\n')


# Ruins