# D&D BX Edition - Generate Random 1st Level Character
# Developer: Warren, https://www.patreon.com/rpgpython
# Script Version Number: v1.0
# Date: 10 March 2021

# If script errors, you may need to install the random package
# https://pypi.org/project/random2/
# pip install random2
# Installing packages: https://packaging.python.org/tutorials/installing-packages/
import random 
# https://pypi.org/project/Columnar/
# pip install Columnar
from columnar import columnar

# STEP 1: Roll for Ability Scores

def roll_ability():
    rolls = []
    # generate ability scores
    for x in range(0,6):
        r = random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1) # 3d6
        rolls.append(r)
        #rolls.sort()
    return rolls

def get_class(seq):
    max_indices = []
    if seq:
        max_val = seq[0]
        for i,val in ((i,val) for i,val in enumerate(seq) if val >= max_val):
            if val == max_val:
                max_indices.append(i)
            else:
                max_val = val
                max_indices = [i]
    
    if(max_indices[0] == 0):
        print("Class: Fighter")
        return 'Fighter'
    if(max_indices[0] == 1):
        print("Class: Magic-User")
        return 'Magic-User'
    if(max_indices[0] == 2):
        print("Class: Cleric")
        return 'Cleric'
    if(max_indices[0] == 3):
        print("Class: Thief")
        return 'Thief'


get_rolls = [0,0,0,0,0,0]
reroll = True

while(reroll == True):   
    get_rolls = roll_ability()
    die_check = 0
    for r in get_rolls:
        if(r<6): 
            die_check += 1
    if (die_check >= 2):
        reroll = True
    else:
        reroll = False

# Resolve Modifiers

melee = 0; open_doors = ''
# Strength Modifiers
s = get_rolls[0]
if(s==3): melee = -3; open_doors = '1-in-6'
if(s==4 or s==5): melee = '-2'; open_doors = '1-in-6'
if(s>=6 and s<=8): melee = '-1'; open_doors = '1-in-6'
if(s>=9 and s<=12): melee = '+0'; open_doors = '2-in-6'
if(s>=13 and s<=15): melee = '+1'; open_doors = '3-in-6'
if(s>=16 and s<=17): melee = '+2'; open_doors = '4-in-6'
if(s==18): melee = 3; open_doors = '5-in-6'

# Intelligence Modifiers
i = get_rolls[1]
if(s==3): language = 'Native, Broken Speech)'; literacy = 'Illiterate'; lang=1
if(s==4 or s==5): language = 'Native'; literacy = 'Illiterate'; lang=1
if(s>=6 and s<=8): language = 'Native'; literacy = 'Basic'; lang=1
if(s>=9 and s<=12): language = 'Native'; literacy = 'Literate'; lang=1
if(s>=13 and s<=15): language = 'Native +1'; literacy = 'Literate'; lang=2
if(s>=16 and s<=17): language = 'Native +2'; literacy = 'Literate'; lang=3
if(s==18): language = 'Native +3'; literacy = 'Literate'; lang=4
    
# Wisdom Modifiers
w = get_rolls[2]
if(w==3): m_saves = -3
if(w==4 or w==5): m_saves = '-2'
if(w>=6 and w<=8): m_saves = '-1'
if(w>=9 and w<=12): m_saves = '+0'
if(w>=13 and w<=15): m_saves = '+1'
if(w>=16 and w<=17): m_saves = '+2'
if(w==18): m_saves = 3

# Dexterity Modifiers
d = get_rolls[3]
if(d==3): ac = -3; missile = -3; initiative = -2
if(d==4 or d==5): ac = '-2'; missile = '-2'; initiative = '-1'
if(d>=6 and d<=8): ac = '-1'; missile = '-1'; initiative = '-1'
if(d>=9 and d<=12): ac = '+0'; missile = '+0'; initiative = '+0'
if(d>=13 and d<=15): ac = '+1'; missile = '+1'; initiative = '+1'
if(d>=16 and d<=17): ac = '+2'; missile = '+2'; initiative = '+1'
if(d==18): ac = 3; missile = '+3'; initiative = '+2'
    
# Constitution Modifiers
c = get_rolls[4]
if(c==3): con = -3
if(c==4 or c==5): con = '-2'
if(c>=6 and c<=8): con = '-1'
if(c>=9 and c<=12): con = '+0'
if(c>=13 and c<=15): con = '+1'
if(c>=16 and c<=17): con = '+2'
if(c==18): con = 3
    
# Charisma Modifiers
ch = get_rolls[5]
if(ch==3): con = -3
if(ch==4 or ch==5): npc = '-2'; retainer_max = '1'; loyalty = '4'
if(ch>=6 and ch<=8): npc = '-1'; retainer_max = '2'; loyalty = '5'
if(ch>=9 and ch<=12): npc = '-1'; retainer_max = '3'; loyalty = '6'
if(ch>=13 and ch<=15): npc = '+0'; retainer_max = '4'; loyalty = '7'
if(ch>=16 and ch<=17): npc = '+1'; retainer_max = '6'; loyalty = '9'
if(ch==18): npc = '+2'; retainer_max = 7; loyalty = '10'
    

       
# STEP 2: Choose a Class
character_class = get_class(get_rolls[:4])
print('Level: 01')

# Prime Requisite Modifiers
pr = ''; gold = 0; equipment = ''; total_weight = 0; armour_worn = ''; armour_class = 9; weight=0
hit_die = ''

if(character_class == 'Cleric'):
    hit_dice = random.randrange(1,7,1) + int(con) #  1d6 + con (hp modifier)
    w = get_rolls[2]
    if(w>=3 or w<=5): pr = '-20%'
    if(w>=6 and w<=8): pr = '-10%'
    if(w>=9 and w<=12): pr = '+0%'
    if(w>=13 and w<=15): pr = '+5%'
    if(w>=16 and w<=18): pr = '+10%'
    armour = 'Any, including shields'
    weapon = 'Any blunt weapons'
    hp = random.randrange(3,7,1) + int(con) # 1d6, however accept 3-6
    hit_die = '(1d6)'
    gold = (random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1)) * 10
    equipment = 'holy symbol, shield (-1 AC), ' + random.choice(['club (1d4' + melee + ')',
                                                                 'mace (1d6' + melee + ')',
                                                                 'sling (1d4' + missile + ')', 
                                                                 'staff (1d4' + melee + ')', 
                                                                 'warhammer (1d6' + melee + ')'])
    armour_worn = random.choice(['Leather','Chainmail','Plate mail', 'None'])
    if(armour_worn.find('Leather') != -1): gold = gold - 20; weight += 200; armour_class = 7
    if(armour_worn.find('Chainmail') != -1): gold = gold - 40; weight += 400; armour_class = 5
    if(armour_worn.find('Plate mail') != -1): gold = gold - 60; weight += 500; armour_class = 3
    if equipment.find('shield'): armour_class -= 1
    if equipment.find('club') != -1: gold = gold - 3; weight += 50
    if equipment.find('mace') != -1: gold = gold - 5; weight += 30
    if equipment.find('sling') != -1: gold = gold - 2; weight += 20
    if equipment.find('staff') != -1: gold = gold - 2; weight += 40
    if equipment.find('warhammer') != -1: gold = gold - 5; weight += 30
    weight += 100 # weight of shield
    gold = (gold - 25) - 10 # subtract holy symbol and shield from gold
    total_weight = gold + weight
if(character_class == 'Fighter'):
    hit_dice = random.randrange(1,9,1) + int(con) # 1d10 + con (hp modifier)
    w = get_rolls[2]
    if(w>=3 or w<=5): pr = '-20%'
    if(w>=6 and w<=8): pr = '-10%'
    if(w>=9 and w<=12): pr = '+0%'
    if(w>=13 and w<=15): pr = '+5%'
    if(w>=16 and w<=18): pr = '+10%'
    armour = 'Any, including shields'
    weapon = 'Any'
    hp = random.randrange(5,9,1) + int(con) # 1d8, however accept 5-8
if(character_class == 'Magic-User'):
    hit_dice = random.randrange(1,5,1) + int(con) # 1d4 + con (hp modifier)
    w = get_rolls[2]
    if(w>=3 or w<=5): pr = '-20%'
    if(w>=6 and w<=8): pr = '-10%'
    if(w>=9 and w<=12): pr = '+0%'
    if(w>=13 and w<=15): pr = '+5%'
    if(w>=16 and w<=18): pr = '+10%'
    armour = 'None'
    weapon = 'Dagger'
    hp = random.randrange(2,5,1) + int(con) # 1d4, however accept 2-4
if(character_class == 'Thief'):
    hit_dice = random.randrange(1,5,1) + int(con) # 1d4 + con (hp modifier)
    w = get_rolls[2]
    if(w>=3 or w<=5): pr = '-20%'
    if(w>=6 and w<=8): pr = '-10%'
    if(w>=9 and w<=12): pr = '+0%'
    if(w>=13 and w<=15): pr = '+5%'
    if(w>=16 and w<=18): pr = '+10%'
    armour = 'Leather, no sheilds'
    weapon = "Any"
    hp = random.randrange(2,5,1) + int(con) # 1d4, however accept 2-4
# XP and Prime Requisite

print('HP ' + hit_die + ': ' + str(hp))
print('XP (' + pr +'): 00')
print('Armor Class: ' + str(armour_class - int(ac)))
print('Armor Usage:    ' + armour)
print('Weapon Usage:   ' + weapon)

# Step 3: Alignment
a= 0
# roll 3d6 to determine alignment
a = random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1)
if(a>=3 and a<=9): alignment = 'Lawful'    #  odds 37.51%
if(a>=10 and a<=15): alignment = 'Neutral' #  odds 57.86%
if(a>=16 and a<=18): alignment = 'Chaotic' #  odds  4.63%
    
    
# Step 4: Languages
language_type = 'Alignment, Common'
language_types = (['Bugbear','Doppelganger','Dragon','Dwarvish','Elvish','Gargoyle','Gnoll','Gnomish','Goblin',
              'Halflint','Harpy','Hobgoblin','Kobold','Lizard Man','Medusa','Minotaur','Orge','Pixie',
              'Human Dialiect'])
if(lang==2):
    language_type = 'Alignment, Common, ' + random.choice(language_types)
if(lang==3):
    language_type = 'Alignment, Common, ' + random.choice(language_types) + ', ' + random.choice(language_types)
if(lang==4):
    language_type = 'Alignment, Common, ' + random.choice(language_types) + ', ' + random.choice(language_types) + ', ' + random.choice(language_types) 


# Print Step 3
if(total_weight <= 400): movement_rate = '120ft/40ft'
if(total_weight >=401 and total_weight <=600): movement_rate = '90ft/30ft'
if(total_weight >=601 and total_weight <=800): movement_rate = '60ft/20ft'
if(total_weight >=801): movement_rate = '30ft/10ft'
if(total_weight > 1600): movement_rate = '0ft/0ft'
print('Alignment: \t' + alignment)
print('Language(s): \t' + language_type)
if(gold<0): gold = 10  # set gold to 10 if negative balance for first time character
print('Gold: ' + str(gold))
print('Starting Equipment: ' + equipment)
print('Armour Worn: ' + armour_worn)
print('Total Weight Carried (max 1600): ' + str(total_weight + 80) + ' (80 coins of weight added for misc. adventure gear)')
print('Movement Rate (Detailed Encumbrance): ' + movement_rate)

    
# Print STEP 1 after Class
print('\nAbility Scores & Modifiers:')
data_1 = [['Str: ' + str(get_rolls[0]), 'melee: ' + str(melee), 'open doors: ' + open_doors,'-'],
          ['Int: ' + str(get_rolls[1]), 'language: ' + language, 'literacy: ' + literacy,'-'],
          ['Wis: ' + str(get_rolls[2]), 'magic saves: ' + str(m_saves),'-','-'], 
          ['Dex: ' + str(get_rolls[3]), 'AC: ' + str(ac), 'missile: ' + str(missile), 'initiative: ' + str(initiative)],
          ['Con: ' + str(get_rolls[4]), 'HP: ' + str(con),'-','-'], 
          ['Cha: ' + str(get_rolls[5]), 'NPC reactions: ' + str(npc), 'retainer max #: ' + str(retainer_max), 'loyalty: ' + str(loyalty)]]
table = columnar(data_1, justify='c', min_column_width=18)
print(table)

# THAC0 - 1st level is same for every class
print('\nTHAC0: 19[0]')
data_2 = [['Atk. Roll', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19','20'],
       ['A/C Hit','9','8','7','6','5','4','3','2','1','0','-1,-2,-3']]
table = columnar(data_2, justify='c')
print(table)

# Cleric Turning the Undead
if (character_class == 'Cleric'):
    print('Turning the Undead (2d6):')
    data_3 = [['Monster Hit Dice','1','2','2*','3','4','5','6','7-9'], ['Level 1','7','9','11','-','-','-','-','-']]
    table = columnar(data_3, justify='c')
    print(table)
    print('Saving Throws:')
    data_4 = [['(D) Death Ray\nPoison','(W) Wands','(P) Paralysis\nPetrify','(B) Breath\nAttacks','(S) Spells\nrods\nstaves'],
              ['11','12','14','16','15']]
    table = columnar(data_4, justify='c')
    print(table)
    print('Spells:')
    data_5 = [['1','2','3','4','5'], ['-','-','-','-','-']]
    table = columnar(data_5, justify='c')
    print(table)

    # Other Details
    print('Additional Details:')
    print('Deity Disfavour: Clerics must be faithful to the tenets of their alignment, clergy, and religion. Clerics who fall from favour with their deity may incur penalties.')
    print('\nMagical research: A cleric of any level may spend time and money on magical research. This allows them to create new spells or other magical effects associated with their deity. When a cleric reaches 9th level, they are also able to create magic items.')
    print('\nSpell casting: Once a cleric has proven their faith (from 2nd level), the character may pray to receive spells. The power and number of spells available to a cleric are determined by the character’s experience level. The list of spells available to clerics is found on p62.')
    print('\nUsing magic items: As spell casters, clerics can use magic scrolls of spells on their spell list. They can also use items that may only be used by divine spell casters (e.g. some magic staves).')
    print('\nSuccessful Turning If the turning attempt succeeds, the player must roll 2d6 to determine the number of HD affected (turned or destroyed).')
