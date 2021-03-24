# Random Archer Sidekick, Auto-Generation
# Developer (code only): Warren, https://www.patreon.com/rpgpython
# Inspired by Sidekicks: Beyond the Essentials by Paul Metzger
# User of script responsible for following Community Content Agreement and Copyright
# Script Version Number: v1.0
# Date: 24 March 2021

# If script errors, you may need to install the random package
# https://pypi.org/project/random2/
# pip install random2
# Installing packages: https://packaging.python.org/tutorials/installing-packages/
import random

level = input('What level do you want your Archer Sidekick to be (1-20)? ')

def modifiers(score):
    if(score == 1): return -5
    if(score >=2 and score <=3): return '-4'
    if(score >=4 and score <=5): return '-3'
    if(score >=6 and score <=7): return '-2'
    if(score >=8 and score <=9): return '-1'
    if(score >=10 and score <=11): return '+0'
    if(score >=12 and score <=13): return '+1'
    if(score >=14 and score <=15): return '+2'
    if(score >=16 and score <=17): return '+3'
    if(score >=18 and score <=19): return '+4'
    if(score >=20 and score <=21): return '+5'
    if(score >=22 and score <=23): return '+6'
    if(score >=24 and score <=25): return '+7'
    if(score >=26 and score <=27): return '+8'
    if(score >=28 and score <=29): return '+9'
    if(score >=30): return '+10'
    

armors = (['Padded', '11', 'Stealth: Disadvantage'], ['Leather','11','Stealth: Normal'],
          ['Studded Leather','12','Stealth: Normal'])
armor = random.choice(armors)

# Character Ability Scores - uses 4d6 and drops lowest
a_scores = []
for x in range (0,6):
    s = random.choices(range(1, 7), k=4) # pick 4 random between 1-6, allow them to be similar
    s.remove(min(s)) # drop lowest 1d6 from the 4 randoms
    a = sum(s)  # add them together
    a_scores.append(a)
    a_scores.sort(reverse = True)

# set ability scores and modifiers from high to low
dex = a_scores[0]; dex_mod = modifiers(dex)
con = a_scores[1]; con_mod = modifiers(con)
sth = a_scores[2]; sth_mod = modifiers(sth)
wis = a_scores[3]; wis_mod = modifiers(wis)
intel = a_scores[4]; intel_mod = modifiers(intel)
cha = a_scores[5]; cha_mod = modifiers(cha)

# other abilities
prof_bonus = 2

print("\n\nARCHER SIDEKICK (Medium Humanoid)")
print("\nLevel:\t\t\t{}".format(level))
print("Hit Points:\t\t" + str(((int(level)+1)*8)+random.randrange(1,7,1)))
print("Armor Class:\t\t{} ({}, {})".format((int(armor[1]) + int(dex_mod)),armor[0],armor[2]))
print("\nStrength:\t\t{}({})".format(sth,sth_mod))
print("Dexterity:\t\t{}({})".format(dex,dex_mod))
print("Constitution:\t\t{}({})".format(con,con_mod))
print("Intelligence:\t\t{}({})".format(intel,intel_mod))
print("Wisdom:\t\t\t{}({})".format(wis,wis_mod))
print("Charisma:\t\t{}({})".format(cha,cha_mod))
print("\nProficency Bonus:\t+{}".format(prof_bonus))
print("Proficiencies:\t\tSimple Melee, Simple Ranged, and Martial Ranged")
print("Languages:\t\tCommon, +1 (you pick)")
print("Saving Throws:\t\tDex(+{})".format(int(dex_mod) + int(prof_bonus)))
print("Skills:\t\t\tPerception +{}, Stealth +{}, Survival +{}".format((int(prof_bonus)+int(wis_mod)),
                                                                 (int(prof_bonus)+int(dex_mod)),
                                                                 (int(prof_bonus)+int(wis_mod))))
print("Senses:\t\t\tpassive Perception {}".format(10 + (int(prof_bonus)+int(wis_mod))))
print("Weapons:\t\tpick 1 Simple Melee, and 1 Simple Ranged or Martial Ranged")

features = (['Successful ranged hit, additional 1d6 damage.',
             'One extra ranged attack w/ same weapon at another target 5ft from first target.',
             'Increase Dex +1 (no more than 18) during this turn.',
             'Increase proficency bonus +1 during this turn.',
             'Attacks per Action = 2 during this turn.',
             '+2 to initative rolls & advantage on attack rolls against creature that has not taken turn in combat yet.',
             'Attacking at long range does not impose disdavantage.',
             'Hits medium or smaller enemy, enemy speed reduced to 10ft until it regains 1hp. DC 12 (STR) or knocked prone.',
             'If miss target during ranged attack, if another enemy is 30ft directly behind (in line) of first, make attack roll against this target.',
             'No disadvantage using ranged weapons while within melee (5ft) range.',
             'During ranged attack, use action to target 3 enemies within 10ft of eachother, seperate attack roll for each target. Counts as full action',
             'As a reaction, when within 60ft of friendly who is ranged attacked, can launch a single range attack at missile to deflect (AC15).',
             'Does not move during turn, add 1d4 to ranged attack roll for hit.',
             'Critical damage with ranged weapon attack of 19 or 20.',
             'Can re-roll 1 or 2 during a ranged attack.',
             'As a reaction, can range attack a spell caster to dispell a spell requiring a somatic component. Enemy caster takes no damage, spell is stopped if enemy fails constitution saving throw with DC 5 + amount of damage that would have been delt.',
             'Reroll range attack if first one misses. Once per long rest.',
             'No disadvantage when range attack against enemy they cannot see (except if 100% behind cover) and is within 30 feet.',
             'Range weapon goes straight through target. If another enemy directly behind first target and is within 10ft, make attack roll. Success deals 1d8 damage.',
             'Range weapon hits enemy behind full cover (range attack bends around obstacle) if a natural 20 is rolled.'])

print("\nFeatures (Use only one per turn):")
f = 0
if(1 <= int(level) <= 4): f = 1   
if(5 <= int(level) <= 10): f = 3   
if(11 <= int(level) <= 16): f = 5   
if(17 <= int(level) <= 20): f = 7
    
for x in range(0,f):
    feature = random.choice(features)
    features.remove(feature)
    print(str(x+1) + ". " + feature)
    
