# Universal NPC Emulator - https://www.drivethrurpg.com/product/134163/UNE-The-Universal-NPC-Emulator-rev

# Developer: Warren, https://www.patreon.com/rpgpython
# Script Version Number: v1.0
# Date: 28 Feb 2021

# If script errors, you may need to install the random package
# https://pypi.org/project/random2/
# pip install random2
# Installing packages: https://packaging.python.org/tutorials/installing-packages/
import random  

a = 1

while (a < 101):
    chaos = random.choice(['Orderly','Calm','Normal','in Disarray','in Chaos'])
    power_level = random.randrange(1,101,1)

    if (chaos == 'Orderly'):
        if(power_level < 2):
            npc_level = 'much weaker'

        if(power_level <11 and power_level >2):
            npc_level = 'slightly weaker'

        if(power_level <91 and power_level >10):
            npc_level = 'comparable strength'

        if(power_level <99 and power_level >90):
            npc_level = 'slightly stronger'

        if(power_level >98):
            npc_level = 'much stronger'

    if (chaos == 'Calm'):
        if(power_level < 5):
            npc_level = 'much weaker'

        if(power_level <16 and power_level >4):
            npc_level = 'slightly weaker'

        if(power_level <86 and power_level >15):
            npc_level = 'comparable strength'

        if(power_level <97 and power_level >85):
            npc_level = 'slightly stronger'

        if(power_level >96):
            npc_level = 'much stronger'

    if (chaos == 'Normal'):
        if(power_level < 5):
            npc_level = 'much weaker'

        if(power_level <21 and power_level >5):
            npc_level = 'slightly weaker'

        if(power_level <81 and power_level >20):
            npc_level = 'comparable strength'

        if(power_level <96 and power_level >80):
            npc_level = 'slightly stronger'

        if(power_level >95):
            npc_level = 'much stronger'

    if (chaos == 'in Disarray'):
        if(power_level < 9):
            npc_level = 'much weaker'

        if(power_level <26 and power_level >8):
            npc_level = 'slightly weaker'

        if(power_level <76 and power_level >25):
            npc_level = 'comparable strength'

        if(power_level <93 and power_level >75):
            npc_level = 'slightly stronger'

        if(power_level >92):
            npc_level = 'much stronger'

    if (chaos == 'in Chaos'):
        if(power_level < 13):
            npc_level = 'much weaker'

        if(power_level <31 and power_level >12):
            npc_level = 'slightly weaker'

        if(power_level <71 and power_level >30):
            npc_level = 'comparable strength'

        if(power_level <89 and power_level >70):
            npc_level = 'slightly stronger'

        if(power_level >88):
            npc_level = 'much stronger'


    # NPC Modifier
    npc_modifier = random.choice(['superfluous','inept','pleasant','lethargic','jovial','addicted',
                                  'insensitive','defiant','shrewd','conformist','logical','titled',
                                  'obnoxious','liberal','nefarious','subtle','inexperienced','insightful',
                                  'compliant','sensible','reputable','prying','tactless','destitute','untrained',
                                  'wicked','oblivious','fanatic','conniving','romantic','lazy','refined',
                                  'plebeian','careful','unreasonable','pessimistic','indispensable','childish',
                                  'alluring','skilled','solemn','scholarly','pious','defective','neglectful',
                                  'habitual','conservative','uneducated','optimistic','lively','meek','uncouth',
                                  'inconsiderate','affluent','forthright','helpful','willful','cultured',
                                  'despondent','idealistic','unconcerned','indifferent','revolting','mindless',
                                  'unsupportive','genrous', 'fickle','curious','passionate','rational','docile',
                                  'elderly','touchy','devoted','coarse','cheery','sinful','needy','established',
                                  'foolish','pragmatic','naive','dignified','unseemly','cunning','serene',
                                  'privileged','pushy','dependable','delightful','thoughtful','glum','kind',
                                  'righteous','miserly','hopeless','likable','corrupt','confident'])

    #NPC Noun
    npc_noun = random.choice(['gypsy','missionary','villager','mediator','performer','witch','outcast','magus','crook',
                 'magister','merchant','mercenary','conscript','civilian','serf','expert','caretaker','worker',
                 'activist','brute','commoner', 'hermit', 'actor', 'hero', 'inquisitor','judge', 'orator', 
                 'herald', 'champion', 'lord','ranger', 'chieftain', 'highwayman', 'cleric', 'villain','occultist',
                 'pioneer', 'fortune-hunter', 'slave', 'professor','reverend', 'burglar', 'governor', 
                 'gunman', 'servant','thug', 'vicar', 'scrapper', 'clairvoyant', 'charmer','drifter', 'officer', 
                 'monk', 'patriarch', 'globetrotter','journeyman', 'explorer', 'homemaker','shopkeeper',
                 'sniper','statesman', 'warden', 'recluse', 'crone', 'courtier','astrologer','outlaw', 'steward', 
                 'adventurer', 'priest','duelist', 'adept', 'polymath', 'soldier', 'tradesman',
                 'jack-of-all-trades', 'bum', 'magician', 'entertainer', 'hitman','aristocrat','sorcerer', 
                 'traveler', 'craftsman', 'wizard','preacher','laborer','vagrant','scientist','beggar',
                 'artisan','master','apprentice','ascetic','tradesman','rogue','ascendant','politician',
                 'superior','warrior'])

    #motivation Verb
    motivation_verb = (['advise','shepherd','take','work','manage','obtain','abuse','discover',
                                     'accompany','suppress','attempt','indulge','deter','offend','proclaim',
                                     'spoil','chronicle','acquire','guide','operate','oppress','fulfill','damage',
                                     'learn','access','interact','drive','publicize','persecute','refine',
                                     'create','review','burden','communicate','compose','abduct','aid','advocate',
                                     'process','undermine','promote','follow','implement','report','explain',
                                     'conceive','advance','understand','develop','discourage','blight','guard',
                                     'collaborate','steal','attend','progress','conquer','strive','suggest',
                                     'detect','distress','hinder','complete','weaken','execute','possess',
                                     'plunder','compel','achieve','maintain','record','construct','join','secure',
                                     'realize','embrace','encourage','assist','inform','convey','contact',
                                     'agonize','defile','patronize','rob','pursue','comprehend','produce',
                                     'depress','establish','associate','administer','institute','determine',
                                     'overthrow','prepare','relate','account','seek','support'])


    motivation_noun = (['wealth','the wealthy','dreams','gluttony','advice','hardship',
                                     'the populous','discretion','lust','propaganda','affluence','enemies',
                                     'love','envy','science','resources','the public','freedom','greed',
                                     'knowledge','prosperity','religion','pain','laziness','communications',
                                     'poverty','the poor','faith','wrath','lies','populence','family',
                                     'slavery','pride','myths','deprivation','the elite','enlightenment',
                                     'purity','riddles','success','academia','racism','moderation','stories',
                                     'distress','the forsaken','sensuality','vigilance','legends','contraband',
                                     'the law','dissonance','zeal','industry','music','the government','peace',
                                     'composure','new religions','literature','the oppressed','discrimination',
                                     'charity','progress','technology','friends','disbelief','modesty',
                                     'animals','alcohol','criminals','pleasure','atrocities','ghosts',
                                     'medicines','allies','hate','cowardice','magic','beauty','secret societies',
                                     'happiness','narcissism','nature','strength','the world','servitude',
                                     'compassion','old religions','intelligence','military','harmony','valor',
                                     'expertise','force','the church','justice','patience','spirits'])

    motive_one = random.choice(motivation_verb) + ' ' + random.choice(motivation_noun)
    motive_two = random.choice(motivation_verb) + ' ' + random.choice(motivation_noun)
    motive_three = random.choice(motivation_verb) + ' ' + random.choice(motivation_noun)

    npc_relationship = random.choice(['loved', 'friendly','peaceful','neutral','distrustful','hostile','hated'])
    mood_roll = random.randrange(1,101,1)
    conv_mood = 'and '
    if(npc_relationship == 'loved'):
        if (mood_roll <2): conv_mood += 'withdrawn'
        if (mood_roll >1 and mood_roll <7): conv_mood += 'guarded'
        if (mood_roll >6 and mood_roll <17): conv_mood += 'cautious'
        if (mood_roll >16 and mood_roll <32): conv_mood += 'neutral'
        if (mood_roll >31 and mood_roll <71): conv_mood += 'sociable'
        if (mood_roll >70 and mood_roll <86): conv_mood += 'helpful'
        if (mood_roll >85): conv_mood += 'forthcoming'
    if(npc_relationship == 'friendly'):
        if (mood_roll <3): conv_mood += 'withdrawn'
        if (mood_roll >2 and mood_roll <9): conv_mood += 'guarded'
        if (mood_roll >8 and mood_roll <21): conv_mood += 'cautious'
        if (mood_roll >20 and mood_roll <41): conv_mood += 'neutral'
        if (mood_roll >40 and mood_roll <77): conv_mood += 'sociable'
        if (mood_roll >76 and mood_roll <90): conv_mood += 'helpful'
        if (mood_roll >89): conv_mood += 'forthcoming'
    if(npc_relationship == 'peaceful'):
        if (mood_roll <4): conv_mood += 'withdrawn'
        if (mood_roll >3 and mood_roll <12): conv_mood += 'guarded'
        if (mood_roll >11 and mood_roll <26): conv_mood += 'cautious'
        if (mood_roll >25 and mood_roll <56): conv_mood += 'neutral'
        if (mood_roll >55 and mood_roll <83): conv_mood += 'sociable'
        if (mood_roll >82 and mood_roll <94): conv_mood += 'helpful'
        if (mood_roll >93): conv_mood += 'forthcoming'
    if(npc_relationship == 'neutral'):
        if (mood_roll <6): conv_mood += 'withdrawn'
        if (mood_roll >5 and mood_roll <16): conv_mood += 'guarded'
        if (mood_roll >15 and mood_roll <31): conv_mood += 'cautious'
        if (mood_roll >30 and mood_roll <71): conv_mood += 'neutral'
        if (mood_roll >60 and mood_roll <86): conv_mood += 'sociable'
        if (mood_roll >85 and mood_roll <96): conv_mood += 'helpful'
        if (mood_roll >95): conv_mood += 'forthcoming'
    if(npc_relationship == 'distrustful'):
        if (mood_roll <8): conv_mood += 'withdrawn'
        if (mood_roll >7 and mood_roll <19): conv_mood += 'guarded'
        if (mood_roll >18 and mood_roll <47): conv_mood += 'cautious'
        if (mood_roll >46 and mood_roll <77): conv_mood += 'neutral'
        if (mood_roll >76 and mood_roll <91): conv_mood += 'sociable'
        if (mood_roll >90 and mood_roll <98): conv_mood += 'helpful'
        if (mood_roll >97): conv_mood += 'forthcoming'
    if(npc_relationship == 'hostile'):
        if (mood_roll <12): conv_mood += 'withdrawn'
        if (mood_roll >11 and mood_roll <25): conv_mood += 'guarded'
        if (mood_roll >24 and mood_roll <62): conv_mood += 'cautious'
        if (mood_roll >61 and mood_roll <82): conv_mood += 'neutral'
        if (mood_roll >81 and mood_roll <94): conv_mood += 'sociable'
        if (mood_roll >93 and mood_roll <99): conv_mood += 'helpful'
        if (mood_roll >98): conv_mood += 'forthcoming'
    if(npc_relationship == 'hated'):
        if (mood_roll <16): conv_mood += 'withdrawn'
        if (mood_roll >15 and mood_roll <31): conv_mood += 'guarded'
        if (mood_roll >30 and mood_roll <70): conv_mood += 'cautious'
        if (mood_roll >69 and mood_roll <85): conv_mood += 'neutral'
        if (mood_roll >84 and mood_roll <95): conv_mood += 'sociable'
        if (mood_roll >94 and mood_roll <100): conv_mood += 'helpful'
        if (mood_roll >99): conv_mood += 'forthcoming'

    bearing_one = random.choice(['scheming', 'insane', 'friendly', 'hostile', 'inquisitive', 'knowing', 
                             'mysterious', 'prejudiced'])

    if(bearing_one == 'scheming'):
        bearing_two = random.choice(['intent', 'bargain', 'means', 'proposition', 'plan', 'compromise', 
                                    'agenda', 'arrangement', 'negotiation', 'plot'])
    if(bearing_one == 'insane'):
        bearing_two = random.choice(['madness', 'fear','accident','chaos','idiocy','illusion','turmoil',
                                    'confusion','facade','bewilderment'])
    if(bearing_one == 'friendly'):
        bearing_two = random.choice(['alliance','comfort','gratitude','shelter','happiness','support',
                                    'promise','delight','aid','celebration'])
    if(bearing_one == 'hostile'):
        bearing_two = random.choice(['death','capture','judgement','combat','surrender','rage',
                                    'resentment','submission','injury','destruction'])
    if(bearing_one == 'inquisitive'):
        bearing_two = random.choice(['questions','investigation','interest','demand','suspicion','request',
                                    'curiosity','skepticicm','command','petition'])
    if(bearing_one == 'knowing'):
        bearing_two = random.choice(['report', 'effects','examination','records','account','news','history',
                                    'telling','discourse','speech'])
    if(bearing_one == 'mysterious'):
        bearing_two = random.choice(['rumor','uncertainty','secrets','misdirection','whispers','lies',
                                    'shadows','enigma','obscurity','conundrum'])
    if(bearing_one == 'prejudiced'):
        bearing_two = random.choice(['reputation','doubt','bias','dislike','partiality','belief','view',
                                    'discrimination','assessment','difference'])

    focus = random.choice(['current scene', 'last story','equipment','parents','history','retainers',
                          'wealth','relics','last action','skills','superiors','fame','campaign',
                          'future action','friends','allies','last scene','contacts','flaws',
                          'advesary','rewards','experience','knowledge','recent scene','community',
                          'treasure','character (one of the party members)','current story','family','power',
                          'weapons','previous scene','enemy'])


    npc = 'A ' + npc_modifier + ' ' + npc_noun + ', ' + npc_level + ' to the party. NPC moods: ' + motive_one + ', ' + motive_two + ', and '+ motive_three + '. The NPCs conversation mood is ' + npc_relationship + ' ' + conv_mood + '. The NPC regards the discussion as ' + bearing_one + ' ' + bearing_two + ', focusing ' + 'the conversation on the parties ' + focus + '.'
        
    print('(' + str(a) + ') ' + str(npc) + '\n')
    a+=1
    
    mood_rool = None; conv_mood = None; npc_relationship = None; npc_modifier = None
    npc_noun = None; npc_level = None; motive_one = None; motive_two = None; motive_three = None
    bearing_one = None; bearing_two = None; npc = None