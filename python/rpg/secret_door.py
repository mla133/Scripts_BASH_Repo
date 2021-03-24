# secret_door.py

# Developer: Warren, https://www.patreon.com/rpgpython
# Script Version Number: v1.0
# Date: 03 March 2021

# If script errors, you may need to install the random and/or math package
# Installing packages: https://packaging.python.org/tutorials/installing-packages/

# https://pypi.org/project/random2/
# pip install random2
import random

material = random.choice(['Adamantine, AC:23, HP:<5d10>, DC:35 Force Open [jammed] or DC:<pick> Pick [locked]',
                          'Iron, AC:19, HP:<5d10>, DC:30 Force Open [jammed] or DC:<pick> Pick [locked]',
                          'Stone, AC:17, HP:<5d10>, DC:28 Force Open [jammed] or DC:<pick> Pick [locked]',
                          'Stone, AC:17, HP:<5d10>, DC:28 Force Open [jammed] or DC:<pick> Pick [locked]'
                          'Wood, AC:15, HP:<5d10>, DC:18 Force Open [jammed] or DC:<pick> Pick [locked]',
                          'Wood, AC:15, HP:<5d10>, DC:18 Force Open [jammed] or DC:<pick> Pick [locked]',
                          'Wood, AC:15, HP:<5d10>, DC:18 Force Open [jammed] or DC:<pick> Pick [locked]',
                          'Wood, AC:15, HP:<5d10>, DC:18 Force Open [jammed] or DC:<pick> Pick [locked]'])
characteristics = random.choice(['It is made out of a pivoting bookcase which noiselessly spins about a central axis and partially blocks the entrance. Creatures that are Medium‐sized or larger must squeeze to get past the bookcase. The bookcase blocks line of sight, meaning it is possible someone might be going through the door on one side, while someone (or something) is coming out the other.',
                                 'It is hidden inside a large cupboard, set into its back wall behind several hanging cloaks and coats.',
                                 'A permanent image (CL 11, DC 19 Will) covers It so that it appears the same as the wall in which it is set.', 
                                 'It is one way. There is no way to open the door from one side.',
                                 'It is oddly shaped, being wider at the bottom than at the top.',
                                 'It is underneath an elaborately woven tapestry depicting a knight in full armour astride a galloping white stallion (or other thematically correct scene).',
                                 'It has been well oiled and opens soundlessly, sliding into the floor without making a sound to alert anyone on the other side.',  
                                 'Immediately behind It is a locked (DC 25 Disable Device) iron portcullis (hardness 10, hp 30, DC 28 Force Open).',
                                 'Opening It releases a strong gust of wind that blows out torches, lanterns and other natural light sources.',  
                                 'It is hidden behind natural foliage (vines, bushes, fungus, lichen etc.) grown specifically to conceal it. The first time the door is used, the foliage must be cleared away.',
                                 'This hallway or room is lined with decorative, false stained glass windows that appear to have only walls behind them. One of the windows, however, can be opened as a secret door.',  
                                 'A hidden flight of stairs that lead up to another level can be triggered by a secret catch to rise up from the floor.',  
                                 'It, which opens by pulling up on the grate or down on a nearby sconce, is behind the back wall of a fireplace.',  
                                 'It is through a giant tun (beer cask), that opens by twisting the tap that protrudes from the cask.',  
                                 'It is hidden halfway up the wall. Characters must scale the wall to be able to reach the opening mechanism.',
                                 'A massive grandfather clock tick tocks as normal, but its hands never advance. If set to a specific time (hour, minute and second), the body swings open revealing a passageway.',  
                                 'A peephole is inconspicuously drilled through It allowing someone to spy on the other side when a plug is removed.',  
                                 'It is in the middle of a large fresco on the wall. The fresco depicts a pastoral setting with peasants working in the fields. Careful examination notes small devilish imps hidden throughout the artwork causing trouble such as unhitching horses or setting fire to a haystack.',  
                                 'It is tied to another nearby door. GM’s choice of whether that door is secret or normal. Both cannot be open at the same and if one is ajar when the other opened, it slams shut.',
                                 'It is protected by a good quality look (DC 30 Disable Device) that is hidden under a flagstone in the floor (DC 20 Perception locates).',
                                 'There is a hole in the door covered over with paper painted to appear as the rest of the door. A loaded heavy crossbow is mounted in front of the small hole allowing someone to fire on anyone opening the door (but with a 20% miss chance). The DC to find the hidden arrow slit is 5 higher than the DC to locate It.',  
                                 'It is behind a pile of rubble, placed there on purpose to appear as though there has been a cave‐in.',  
                                 'It slides into the wall rather than opening like a standard door.',  
                                 'It is underneath a large potted plant. GM’s choice as to whether the plant is alive or long since dead from lack of care.',  
                                 'It is part of a large bas relief on the wall depicting a deity or holy symbol.',  
                                 'It is designed to make noise when triggered, decreasing Stealth checks made to open it quietly by 4.',  
                                 'It is only 3 ft. high. Medium or larger characters must squeeze to get through the door.',
                                 'It is keyed to a statue of two lovers staring longing towards each other. The statues are on pivots and the door is triggered when the statues are pushed together to kiss.',
                                 'It is hidden in the floor of a fountain. Opening the door causes a few gallons of water to momentarily flood down the stairs underneath, but it quickly stops.',  
                                 'It is in the ceiling, and opens by pulling down on a chandelier which is mounted in the middle of the door (DC 15 Climb to scale the chandelier).',
                                 'The door is also Trapped!','The door is also Trapped!','The door is also Trapped!'])

condition = random.choice(['Dilapitated, Perception/Investigaton DC: -2, HP: -50%; Break DC: -4',
                           'Average, Perception/Investigaton DC: +0, HP: +-0%; Break DC: +-0',
                           'Good, Perception/Investigaton DC: +1, HP: +25%; Break DC: +2',
                           'Poor, Perception/Investigaton DC: -1, HP: -25%; Break DC: -2',
                           'Average, Perception/Investigaton DC: +0, HP: +-0%; Break DC: +-0',
                           'Good, Perception/Investigaton DC: +1, HP: +25%; Break DC: +2',
                           'Poor, Perception/Investigaton DC: -1, HP: -25%; Break DC: -2',
                           'Average, Perception/Investigaton DC: +0, HP: +-0%; Break DC: +-0',
                           'Good, Perception/Investigaton DC: +1, HP: +25%; Break DC: +2',
                           'Poor, Perception/Investigaton DC: -1, HP: -25%; Break DC: -2',
                           'Excellent, Perception/Investigaton DC: +2, HP: +50%; Break DC: +4',])

door_status = random.choice(['Locked','Unlocked','Jammed'])
trap_description = ''
a = material.replace('<pick>', str(random.randrange(10,26,2)))
x = a.replace('<5d10>', str(random.randrange(1,13,1)+random.randrange(1,13,1)+random.randrange(1,13,1)+random.randrange(1,13,1)+random.randrange(1,13,1)))


if(characteristics == 'The door is also Trapped!'):
    trigger = random.choice(['touch','pressure plate','open','proximity','tension cable','pick lock',
                             'pass threshold','trip wire','music/auditory','lighted torch','detector/sensor',
                             'read writing','switch','tapestry','levers','fail password','sleep/unconsciousness',
                             'trigger word','look into','close','button','turn wheel/crank','weapon drawn',
                             'wrong key','pull rope/chain','search dead creature','disturb liquid','cast spell',
                             'remove barrier','pick up object','open flame','unsheathed weapon'])
    effect = random.choice(['acid','crossbow','fire bolt','falling net','needle','poison','swinging object',
                            'animiated object','spears','trap door','fire jug','sleep','summon creature',
                            'scything blades','missile magic','spikes','dart','portcullis','burning hands',
                            'falling object','bound','spiked walls','water','sand','paralyzed','elemental blast',
                            'drop into monster lair','spiders','swarm','reptiles','crushing ceiling/walls',
                            'drop into lower level','barrier','heat metal','darts','spider webs','wall of fire',
                            'dropped into water','hold person', 'frightened', 'blinded', 'deafened', 'petrified',
                            'prone', 'stunned','ice storm','invisible','teleported','cage','hail of bolts',
                            'rolling boulder','teleporting drop','fire blast', 'snare','amnesia',
                            'reverse gravity','lightning','transmutation','spring floor','cave-in',
                            'curse','slide'])
    trap_description = '\nTrap Mechanics: (trigger) ' + trigger + ' (effect) ' + effect 

print('The secret door is made of ' + x)
print('\n' + characteristics)
print('\nStatus: ' + door_status)
print('\nCondition: ' + condition)
print(trap_description)
x=None
# secret_door.py