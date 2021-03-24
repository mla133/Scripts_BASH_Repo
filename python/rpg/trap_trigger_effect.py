# Trap Trigger & Effects
# Developer: Warren, https://www.patreon.com/rpgpython
# Script Version Number: v1.0
# Date: 05 March 2021

# If script errors, you may need to install the random package
# https://pypi.org/project/random2/
# pip install random2
# Installing packages: https://packaging.python.org/tutorials/installing-packages/
import random 

   # these are all the different trigger options for what initiates the trap door.
    # add more if you like!!!
trigger = random.choice(['touch','pressure plate','opening','proximity','tension cable','picking lock',
                         'passing a threshold','trip wire','music/auditory','a lighted torch','detector/sensor',
                         'reading writing on wall outloud','a switch','a tapestry','levers','failing password','sleep/unconsciousness',
                         'trigger word','looking into a hole','closing','a button','turning a wheel/crank','a weapon drawn',
                         'using a wrong key','pulling rope/chain','searching dead creature','disturbing liquid','casting spell',
                         'removing barrier','picking up object','open flame','unsheathed weapon'])
# these are all the different effect options for what initiates the trap door.
# add more if you like!!!
effect = random.choice(['acid','crossbow','fire bolt','falling net','needle','poison','swinging object',
                        'animiated object','spears','trap door','fire jug','sleep','summon creature',
                        'scything blades','missile magic','spikes','dart','portcullis','burning hands',
                        'falling object','bound','spiked walls','water','sand','paralyzed','elemental blast',
                        'drop into monster lair','spiders','swarm','reptiles','crushing ceiling/walls',
                        'drop into lower level','barrier','heat metal','darts','spider webs','wall of fire',
                        'dropped into water','hold person', 'frightened 1d4 hrs.', 'blinded 1d4 hrs.', 'deafened 1d4 hrs.', 'petrified 1d4 hrs.',
                        'prone 1d4 hrs.', 'stunned 1d4 hrs.','ice storm','invisible','teleported','cage','hail of bolts',
                        'rolling boulder','teleporting drop','fire blast', 'snare','amnesia',
                        'reverse gravity','lightning','transmutation','spring floor','cave-in',
                        'curse','slide','losing speech 1d4 long rest'])


print('\nThe trap is tiggered by: ' + trigger)
print('\nThe trap effect is: ' + effect)


    