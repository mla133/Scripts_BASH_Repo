# kobold.py

# Developer: Warren, https://www.patreon.com/rpgpython
# Script Version Number: v1.0
# Date: 13 Feb 2021

# If script errors, you may need to install the random and/or Columnar package
# Installing packages: https://packaging.python.org/tutorials/installing-packages/

# https://pypi.org/project/random2/
# pip install random2
import random

def melee_weapon():
    m = random.randrange(1,7,1)  # 1d6
    if(m==1): return 'Pick, +4 hit, 1d4+2'
    if(m==2): return 'Javelin, +5 hit, 1d6+3'
    if(m==3): return 'Sickle, +4 hit, 1d6+2'
    if(m==4): return 'Shortsword, +4 hit, 1d6+2'
    if(m==5): return 'Club, +5 hit, 1d4+2'
    if(m==6): return 'Dagger, +4 hit, 1d4+2'
    
def range_weapon():
    r = random.randrange(1,7,1)  # 1d6
    if(r==1):
        rw = 'Shortbow w/ <1d10> Arrow(s), 80/320, +4 hit, 1d6+2'
        r = rw.replace('<1d10>',str(random.randrange(1,11,1)))
        return r
    if(r==2): 
        rw ='Sling w/ <1d10> Bullet(s), 30/120, +4 hit, 1d4+2'
        r = rw.replace('<1d10>',str(random.randrange(1,11,1)))
        return r
    if(r==3):
        rw = '<1d6> Dart(s), 20/60, +4 hit, 1d4+2'
        r = rw.replace('<1d6>', str(random.randrange(1,7,1)))
        return r
    if(r==4): 
        rw ='Hand Crossbow with <1d10> bolt(s), 30/120, +4 hit, 1d6+2'
        r = rw.replace('<1d10>',str(random.randrange(1,11,1)))
        return r
    if(r==5): 
        rw = 'Light Crossbow with <1d10> bolt(s), 80/320, +4 hit, 1d8+2'
        r = rw.replace('<1d10>',str(random.randrange(1,11,1)))
        return r
    if(r==6): return 'Spear, 20/60, +4 hit, 1d4+2'

status = input('(1) Generate Kobold Party, (2) In Combat: ')
weapon = 0 # 1 = melee, 2 = melee & range, 3 = range
trick_trap = ''
if(status=='1'):   # Weapons
    clan = input('How many Kobolds? ')
    for x in range(0,int(clan)):
        melee = ''; rrange = ''; r = 0; t = 0; tt = 0; trick_trap = ''
        r = random.randrange(1,7,1) + random.randrange(1,7,1) # 2d6
        if(2 <= r <= 4): weapon = 1
        if(5 <= r <= 9): weapon = 2
        if(10 <= r <= 12): weapon = 3
        if(weapon == 1): melee = melee_weapon()
        if(weapon == 2): 
            melee = melee_weapon()
            rrange = range_weapon()
        if(weapon == 3): rrange = range_weapon()
         
        t = random.randrange(1,21,1) # 1d20
        if(t>=18): # 15% chance of having a trick/trap
            tt = random.randrange(1,7,1) # 1d6
            if(tt==1):
                trick_trap = 'Jar of Bugs: A jar filled with swarm of insects (pg. 338 MM) which\n\tcan be thrown.'
            if(tt==2):
                trick_trap = 'Jar of Ooze: A jar filled with from a Gray Jelly (pg. 243 MM). 10HP,\n\t1d4+1 bludgeoning and 1d4+1 acid damage.'
            if(tt==3):
                trick_trap = 'Molotov cocktail: A glass bottle filled with fuel, lit cloth on fire. +4 Hit, 1d4+1\n\tfire damage.'
            if(tt==4):
                trick_trap = 'Big Bag of Rats: A large bag full of rats, when thrown at enemy, rats spill out\n\tand attack target (pg. 339 MM). 12 HP, 1d6 bite damage.'
            if(tt==5):
                trick_trap = 'Caltrops: A bag of caltrops that cover 5ft.x 5ft. square. Enemy must succeed on a\n\tDC 15 Dexterity saving throw or stop moving and take 1 piercing damage. Until the\n\tcreature regains at least 1-hit point, its walking speed is reduced by 10 feet'
            if(tt==6):
                trick_trap = 'Ball Bearings: Spill these tiny metal balls from their pouch to cover a level,\n\tsquare area that is 10 feet on a side. A creature moving across the covered area\n\tmust succeed on a DC 10 Dexterity saving throw or fall prone.\n\tA creature moving through the area at half speed doesn’t need to make the save.'
                
        print('\nKobold #' + str(x+1) + ': ' + '\n\t' + melee + '\n\t' + rrange +
              '\n\t' + trick_trap)
        

elif(status=='2'):  # Combat
    c = ''; l = ''; r = ''
    c = input("Is Kobold in (1) Melee, (2) Range: ")
    l = input('Is Kobold Hit Points Below 50%? y/n: ')
    action = ''
    if(c=='1'):
        if(l=='y'):
            r = random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1) # 3d6
            if(3 <= r <= 5): action = '3-5 (4.63%): Attack'
            if(6 <= r <= 9): action =  '6-9 (32.86%): Dodge'
            if(10 <= r <= 13): action =  '10-13 (46.29%): Disengage, Move Full Speed'
            if(14 <= r <= 18): action =  '14-18(16.2%): Move, Take Opportunity Attack, Range Attack'
        if(l=='n'):
            r = random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1) # 3d6
            if(3 <= r <= 5): action =  '3-5 (4.63%): Disengage'
            if(6 <= r <= 9): action =  '6-9 (32.86%): Attack'
            if(10 <= r <= 13): action =  '10-13 (46.29%): Flank, Attack'
            if(14 <= r <= 18): action =  '14-18 (16.2%): Move, Take Opportunity Attack, Range Attack'
    if(c=='2'):
        if(l=='y'):
            r = random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1) # 3d6
            if(3 <= r <= 10): action = '3-10 (49.99%): Dash, Move Away'
            if(11 <= r <= 14): action =  '11-14 (40.73%): Move to Optimal, Hide'
            if(15 <= r <= 18): action =  '15-18 (9.26%): Ranged Attack, Move to Optimal'
        if(l=='n'):
            r = random.randrange(1,7,1) + random.randrange(1,7,1) + random.randrange(1,7,1) # 3d6
            if(3 <= r <= 10): action = '3-10 (49.99%): Move to Optimal, Ranged Attack'
            if(11 <= r <= 14): action =  '11-14 (40.73%): Ranged Attack, Move to Optimal'
            if(15 <= r <= 18): action =  '15-18 (9.26%): Position for Melee, Melee Attack otherwise Ranged Attack'      
    print('\nThe Kobolds Actions: ' + action)    
else:
    print('Error: Input 1 or 2.')

# kobold.py