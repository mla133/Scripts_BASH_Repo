# oracle_ask_question.py

# Mechanics used with permission by Solometanomy: 
# https://solometanomy.wordpress.com/2020/12/13/oracles-double-oracles-and-reverse-skill-checks-an-introduction/


# Developer: Warren, https://www.patreon.com/rpgpython
# Script Version Number: v1.0
# Date: 03 March 2021

# If script errors, you may need to install the random and/or math package
# Installing packages: https://packaging.python.org/tutorials/installing-packages/

# https://pypi.org/project/random2/
# pip install random2
import random


print('\n')
question = input ('What is your question?\n')
print('\n')

d100 = random.randrange(1,101,1) # d100
oracle = random.randrange(1,21,1) #d20
modifier_dice = 0


likelihood = ''
complication = ''

if(d100 == 1):
    likelihood = 'Impossible'
    # 5d4
    modifier_dice = random.randrange(1,5,1) + random.randrange(1,5,1) + random.randrange(1,5,1) + random.randrange(1,5,1) + random.randrange(1,5,1)
    oracle -= modifier_dice
    
    #resolve complication dice, 2d20
    c_die1 = random.randrange(1,21,1)
    c_die2 = random.randrange(1,21,1)
    
    #doubles
    if(c_die1 == c_die2):
        if(c_die1 < 11):
            complication = ', but...'
        if(c_die1 > 10):
            complication = ', and...'
    #extremes
    if((c_die1 == 1) and (c_die2 == 20)):
        complication = ", random event."
    if((c_die1 == 20) and (c_die2 == 1)):
        complication = ', random event.'
        
if(2<=d100<=3):
    likelihood = 'Near Impossible'
    # 4d4
    modifier_dice = random.randrange(1,5,1) + random.randrange(1,5,1) + random.randrange(1,5,1) + random.randrange(1,5,1)
    oracle -= modifier_dice
    
    #resolve complication dice, 2d12
    c_die1 = random.randrange(1,13,1)
    c_die2 = random.randrange(1,13,1)
    
    #doubles
    if(c_die1 == c_die2):
        if(c_die1 < 7):
            complication = ', but...'
        if(c_die1 > 6):
            complication = ', and...'
    #extremes
    if((c_die1 == 1) and (c_die2 == 12)):
        complication = ", random event."
    if((c_die1 == 12) and (c_die2 == 1)):
        complication = ', random event.'
        

if(4<=d100<=7):
    likelihood = 'Very Unlikely'
    # 3d4
    modifier_dice = random.randrange(1,5,1) + random.randrange(1,5,1) + random.randrange(1,5,1)
    oracle -= modifier_dice
    
    #resolve complication dice, 2d10
    c_die1 = random.randrange(1,11,1)
    c_die2 = random.randrange(1,11,1)
    
    #doubles
    if(c_die1 == c_die2):
        if(c_die1 < 6):
            complication = ', but...'
        if(c_die1 > 5):
            complication = ', and...'
    #extremes
    if((c_die1 == 1) and (c_die2 == 10)):
        complication = ", random event."
    if((c_die1 == 10) and (c_die2 == 1)):
        complication = ', random event.'
        

if(8<=d100<=15):
    likelihood = 'Unlikely'
    # 2d4
    modifier_dice = random.randrange(1,5,1) + random.randrange(1,5,1)
    oracle -= modifier_dice
    
    #resolve complication dice, 2d8
    c_die1 = random.randrange(1,9,1)
    c_die2 = random.randrange(1,9,1)
    
    #doubles
    if(c_die1 == c_die2):
        if(c_die1 < 5):
            complication = ', but...'
        if(c_die1 > 4):
            complication = ', and...'
    #extremes
    if((c_die1 == 1) and (c_die2 == 8)):
        complication = ", random event."
    if((c_die1 == 8) and (c_die2 == 1)):
        complication = ', random event.'
        
    
if(16<=d100<=31):
    likelihood = 'Somewhat Unlikely'
    # 1d4
    modifier_dice = random.randrange(1,5,1)
    oracle -= modifier_dice
    
    #resolve complication dice, 2d6
    c_die1 = random.randrange(1,7,1)
    c_die2 = random.randrange(1,7,1)
    
    #doubles
    if(c_die1 == c_die2):
        if(c_die1 < 4):
            complication = ', but...'
        if(c_die1 > 3):
            complication = ', and...'
    #extremes
    if((c_die1 == 1) and (c_die2 == 6)):
        complication = ", random event."
    if((c_die1 == 6) and (c_die2 == 1)):
        complication = ', random event.'
        

if(32<=d100<=69):
    likelihood = 'Even Odds'
    
     #resolve complication dice, 2d4
    c_die1 = random.randrange(1,5,1)
    c_die2 = random.randrange(1,5,1)
    
    complication = ''
    
    #doubles
    if(c_die1 == c_die2):
        if(c_die1 < 3):
            complication = ', but...'
        if(c_die1 > 2):
            complication = ', and...'
    #extremes
    if((c_die1 == 1) and (c_die2 == 4)):
        complication = ", random event."
    if((c_die1 == 4) and (c_die2 == 1)):
        complication = ', random event.'
        

if(70<=d100<=85):
    likelihood = 'Somewhat Likely'
    # 1d4
    modifier_dice = random.randrange(1,5,1)
    oracle += modifier_dice
    
    #resolve complication dice, 2d6
    c_die1 = random.randrange(1,7,1)
    c_die2 = random.randrange(1,7,1)
    
    #doubles
    if(c_die1 == c_die2):
        if(c_die1 < 4):
            complication = ', but...'
        if(c_die1 > 3):
            complication = ', and...'
    #extremes
    if((c_die1 == 1) and (c_die2 == 6)):
        complication = ", random event."
    if((c_die1 == 6) and (c_die2 == 1)):
        complication = ', random event.'
        

if(86<=d100<=93):
    likelihood = 'Likely'
    # 2d4
    modifier_dice = random.randrange(1,5,1) + random.randrange(1,5,1)
    oracle += modifier_dice
    
    #resolve complication dice, 2d8
    c_die1 = random.randrange(1,9,1)
    c_die2 = random.randrange(1,9,1)
    
    #doubles
    if(c_die1 == c_die2):
        if(c_die1 < 5):
            complication = ', but...'
        if(c_die1 > 4):
            complication = ', and...'
    #extremes
    if((c_die1 == 1) and (c_die2 == 8)):
        complication = ", random event."
    if((c_die1 == 8) and (c_die2 == 1)):
        complication = ', random event.'
        
    
if(94<=d100<=97):
    likelihood = 'Very Likely'
    # 3d4
    modifier_dice = random.randrange(1,5,1) + random.randrange(1,5,1) + random.randrange(1,5,1)
    oracle += modifier_dice
    
    #resolve complication dice, 2d10
    c_die1 = random.randrange(1,11,1)
    c_die2 = random.randrange(1,11,1)
    
    #doubles
    if(c_die1 == c_die2):
        if(c_die1 < 6):
            complication = ', but...'
        if(c_die1 > 5):
            complication = ', and...'
    #extremes
    if((c_die1 == 1) and (c_die2 == 10)):
        complication = ", random event."
    if((c_die1 == 10) and (c_die2 == 1)):
        complication = ', random event.'
    
    
    
if(98<=d100<=99):
    likelihood = 'Near Certain'
    # 4d4
    modifier_dice = random.randrange(1,5,1) + random.randrange(1,5,1) + random.randrange(1,5,1) + random.randrange(1,5,1)
    oracle += modifier_dice
    
    #resolve complication dice, 2d12
    c_die1 = random.randrange(1,13,1)
    c_die2 = random.randrange(1,13,1)
    
    #doubles
    if(c_die1 == c_die2):
        if(c_die1 < 7):
            complication = ', but...'
        if(c_die1 > 6):
            complication = ', and...'
    #extremes
    if((c_die1 == 1) and (c_die2 == 12)):
        complication = ", random event."
    if((c_die1 == 12) and (c_die2 == 1)):
        complication = ', random event.'
        

if(d100 == 100):
    likelihood = 'Certain'
    # 5d4
    modifier_dice = random.randrange(1,5,1) + random.randrange(1,5,1) + random.randrange(1,5,1) + random.randrange(1,5,1) + random.randrange(1,5,1)
    oracle += modifier_dice
    
    #resolve complication dice, 2d20
    c_die1 = random.randrange(1,21,1)
    c_die2 = random.randrange(1,21,1)
    
    #doubles
    if(c_die1 == c_die2):
        if(c_die1 < 11):
            complication = ', but...'
        if(c_die1 > 10):
            complication = ', and...'
    #extremes
    if((c_die1 == 1) and (c_die2 == 20)):
        complication = ", random event."
    if((c_die1 == 20) and (c_die2 == 1)):
        complication = ', random event.'

    

print('Your Oracle d100 roll is: ' + str(d100) + ' (' + likelihood + ')')
print('Your Likelihood d20 roll is: ' + str(oracle))

if(oracle <= 10):
    success = 'No'
else:
    success = 'Yes'
    
print('\n' + question + '  ' + success + complication)
print('\n')


# Oracle: Ask Question