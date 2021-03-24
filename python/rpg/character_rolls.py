# Character Rolls

# Developer: Warren, https://www.patreon.com/rpgpython
# Script Version Number: v1.0
# Date: 10 Feb 2021

# If script errors, you may need to install the random and/or Columnar package
# Installing packages: https://packaging.python.org/tutorials/installing-packages/

# https://pypi.org/project/random2/
# pip install random2
import random

#https://pypi.org/project/Columnar/
#pip install Columnar
from columnar import columnar

# Enter the names of your characters
headers = ['Bastian', 'Hormand', '<enter name>', '<enter name>']

# Supports up to 4 characters.

# Bonuses to add to rolls for Character #1. manually adjust these to match your player character.
c1_initiative = 5
c1_str = 4; c1_dex = 6; c1_con = 2; c1_int = 1; c1_wis = 2; c1_cha = 0 # these are saving throws
c1_acrobatics = 3; c1_animal_handling = 2; c1_arcana = 1; c1_athletics = 1; c1_deception = 3; c1_history = 1; c1_insight = 2; c1_intimidation = 0; c1_investigation = 4
c1_medicine = 2; c1_nature = 1; c1_perception = 5; c1_performance = 0; c1_persuasion = 0; c1_religion = 1; c1_slight_of_hand = 3; c1_stealth = 6; c1_survival = 5
c1_passive_wis_perception = '15'; c1_passive_int_investigation = '14'; c1_passive_wis_insight = '12'
c1_strength = 1; c1_dexterity = 3; c1_constitution = 2; c1_intelligence = 1; c1_wisdom = 2; c1_charisma = 0

# Bonuses to add to rolls for Character #2. manually adjust these to match your player character.
c2_initiative = 2
c2_str = 6; c2_dex = 2; c2_con = 5; c2_int = -1; c2_wis = 0; c2_cha = 0 # these are saving throws
c2_acrobatics = 2; c2_animal_handling = 0; c2_arcana = -1; c2_athletics = 6; c2_deception = 0; c2_history = -1; c2_insight = 0; c2_intimidation = 3; c2_investigation = 2
c2_medicine = 0; c2_nature = -1; c2_perception = 3; c2_performance = 0; c2_persuasion = 3; c2_religion = -1; c2_slight_of_hand = 2; c2_stealth = 2; c2_survival = 0
c2_passive_wis_perception = '13'; c2_passive_int_investigation = '12'; c2_passive_wis_insight = '10'
c2_strength = 3; c2_dexterity = 2; c2_constitution = 2; c2_intelligence = -1; c2_wisdom = 0; c2_charisma = 0

# Bonuses to add to rolls for Character #3. manually adjust these to match your player character.
c3_initiative = 0
c3_str = 6; c3_dex = 0; c3_con = 5; c3_int = 0; c3_wis = 0; c3_cha = -1 # these are saving throws
c3_acrobatics = 2; c3_animal_handling = 0; c3_arcana = 0; c3_athletics = 6; c3_deception = -1; c3_history = 0; c3_insight = 0; c3_intimidation = 1; c3_investigation = 0
c3_medicine = 0; c3_nature = 0; c3_perception = 2; c3_performance = -1; c3_persuasion = -1; c3_religion = 0; c3_slight_of_hand = 0; c3_stealth = 0; c3_survival = 2
c3_passive_wis_perception = '12'; c3_passive_int_investigation = '13'; c3_passive_wis_insight = '12'
c3_strength = 4; c3_dexterity = 0; c3_constitution = 3; c3_intelligence = 0; c3_wisdom = 0; c3_charisma = -1

# Bonuses to add to rolls for Character #4. manually adjust these to match your player character.
c4_initiative = 3
c4_str = 2; c4_dex = 3; c4_con = 4; c4_int = 0; c4_wis = 5; c4_cha = 6 # these are saving throws
c4_acrobatics = 3; c4_animal_handling = 2; c4_arcana = 0; c4_athletics = 5; c4_deception = 3; c4_history = 0; c4_insight = 2; c4_intimidation = 3; c4_investigation = 3
c4_medicine = 2; c4_nature = 3; c4_perception = 2; c4_performance = 3; c4_persuasion = 3; c4_religion = 0; c4_slight_of_hand = 3; c4_stealth = 3; c4_survival = 5
c4_passive_wis_perception = '12'; c4_passive_int_investigation = '10'; c4_passive_wis_insight = '10'
c4_strength = 5; c4_dexterity = 3; c4_constitution = 3; c4_intelligence = 1; c4_wisdom = 1; c4_charisma = 1

data = [
    
    ['Initiative: ' + str(random.randrange(1,21,1) + c1_initiative) + ' / ' + str(random.randrange(1,21,1) + c1_initiative), 'Initiative: ' + str(random.randrange(1,21,1) + c2_initiative) + ' / ' + str(random.randrange(1,21,1) + c2_initiative),'Initiative: ' + str(random.randrange(1,21,1) + c3_initiative) + ' / ' + str(random.randrange(1,21,1) + c3_initiative),'Initiative: ' + str(random.randrange(1,21,1) + c4_initiative) + ' / ' + str(random.randrange(1,21,1) + c4_initiative)],
    ['Pass (Wis) Perception: ' + c1_passive_wis_perception,'Pass (Wis) Perception: ' + c2_passive_wis_perception,'Pass (Wis) Perception: ' + c3_passive_wis_perception,'Pass (Wis) Perception: ' + c4_passive_wis_perception],   
    ['Pass (Int) Investigation: ' + c1_passive_int_investigation,'Pass (Int) Investigation: ' + c2_passive_int_investigation,'Pass (Int) Investigation: ' + c3_passive_int_investigation,'Pass (Int) Investigation: ' + c4_passive_int_investigation],    
    ['Pass (Wis) Insight: '+ c1_passive_wis_insight, 'Pass (Wis) Insight: '+ c2_passive_wis_insight,'Pass (Wis) Insight: '+ c3_passive_wis_insight,'Pass (Wis) Insight: '+ c4_passive_wis_insight],
    ['Strength Roll: ' + str(random.randrange(1,21,1) + c1_strength) + ' / ' + str(random.randrange(1,21,1) + c1_strength),'Strength Roll: ' + str(random.randrange(1,21,1) + c2_strength) + ' / ' + str(random.randrange(1,21,1) + c2_strength),'Strength Roll: ' + str(random.randrange(1,21,1) + c3_strength) + ' / ' + str(random.randrange(1,21,1) + c3_strength),'Strength Roll: ' + str(random.randrange(1,21,1) + c4_strength) + ' / ' + str(random.randrange(1,21,1) + c4_strength)],
    ['Dexterity Roll: ' + str(random.randrange(1,21,1) + c1_dexterity) + ' / ' + str(random.randrange(1,21,1) + c1_dexterity),'Dexterity Roll: ' + str(random.randrange(1,21,1) + c2_dexterity) + ' / ' + str(random.randrange(1,21,1) + c2_dexterity),'Dexterity Roll: ' + str(random.randrange(1,21,1) + c3_dexterity) + ' / ' + str(random.randrange(1,21,1) + c3_dexterity),'Dexterity Roll: ' + str(random.randrange(1,21,1) + c4_dexterity) + ' / ' + str(random.randrange(1,21,1) + c4_dexterity)],
    ['Constitution Roll: ' + str(random.randrange(1,21,1) + c1_constitution) + ' / ' + str(random.randrange(1,21,1) + c1_constitution),'Constitution Roll: ' + str(random.randrange(1,21,1) + c2_constitution) + ' / ' + str(random.randrange(1,21,1) + c2_constitution),'Constitution Roll: ' + str(random.randrange(1,21,1) + c3_constitution) + ' / ' + str(random.randrange(1,21,1) + c3_constitution),'Constitution Roll: ' + str(random.randrange(1,21,1) + c4_constitution) + ' / ' + str(random.randrange(1,21,1) + c4_constitution)],
    ['Intelligence Roll: ' + str(random.randrange(1,21,1) + c1_intelligence) + ' / ' + str(random.randrange(1,21,1) + c1_intelligence),'Intelligence Roll: ' + str(random.randrange(1,21,1) + c2_intelligence) + ' / ' + str(random.randrange(1,21,1) + c2_intelligence),'Intelligence Roll: ' + str(random.randrange(1,21,1) + c3_intelligence) + ' / ' + str(random.randrange(1,21,1) + c3_intelligence),'Intelligence Roll: ' + str(random.randrange(1,21,1) + c4_intelligence) + ' / ' + str(random.randrange(1,21,1) + c4_intelligence)],
    ['Wisdom Roll: ' + str(random.randrange(1,21,1) + c1_wisdom) + ' / ' + str(random.randrange(1,21,1) + c1_wisdom),'Wisdom Roll: ' + str(random.randrange(1,21,1) + c2_wisdom) + ' / ' + str(random.randrange(1,21,1) + c2_wisdom),'Wisdom Roll: ' + str(random.randrange(1,21,1) + c3_wisdom) + ' / ' + str(random.randrange(1,21,1) + c3_wisdom),'Wisdom Roll: ' + str(random.randrange(1,21,1) + c4_wisdom) + ' / ' + str(random.randrange(1,21,1) + c4_wisdom)],
    ['Charisma Roll: ' + str(random.randrange(1,21,1) + c1_charisma) + ' / ' + str(random.randrange(1,21,1) + c1_charisma),'Charisma Roll: ' + str(random.randrange(1,21,1) + c2_charisma) + ' / ' + str(random.randrange(1,21,1) + c2_charisma),'Charisma Roll: ' + str(random.randrange(1,21,1) + c3_charisma) + ' / ' + str(random.randrange(1,21,1) + c3_charisma),'Charisma Roll: ' + str(random.randrange(1,21,1) + c4_charisma) + ' / ' + str(random.randrange(1,21,1) + c4_charisma)],
    ['Strength (Save): ' + str(random.randrange(1,21,1) + c1_str) + ' / ' + str(random.randrange(1,21,1) + c1_str), 'Strength (Save): ' + str(random.randrange(1,21,1) + c2_str) + ' / ' + str(random.randrange(1,21,1) + c2_str), 'Strength (Save): ' + str(random.randrange(1,21,1) + c3_str) + ' / ' + str(random.randrange(1,21,1) + c3_str), 'Strength (Save): ' + str(random.randrange(1,21,1) + c4_str) + ' / ' + str(random.randrange(1,21,1) + c4_str)],
    ['Dexterity (Save): ' + str(random.randrange(1,21,1) + c1_dex) + ' / ' + str(random.randrange(1,21,1) + c1_dex), 'Dexterity (Save): ' + str(random.randrange(1,21,1) + c2_dex) + ' / ' + str(random.randrange(1,21,1) + c2_dex), 'Dexterity (Save): ' + str(random.randrange(1,21,1) + c3_dex) + ' / ' + str(random.randrange(1,21,1) + c3_dex), 'Dexterity (Save): ' + str(random.randrange(1,21,1) + c4_dex) + ' / ' + str(random.randrange(1,21,1) + c4_dex)],
    ['Constitution (Save): ' + str(random.randrange(1,21,1) + c1_con) + ' / ' + str(random.randrange(1,21,1) + c1_con), 'Constitution (Save): ' + str(random.randrange(1,21,1) + c2_con) + ' / ' + str(random.randrange(1,21,1) + c2_con),'Constitution (Save): ' + str(random.randrange(1,21,1) + c3_con) + ' / ' + str(random.randrange(1,21,1) + c3_con),'Constitution (Save): ' + str(random.randrange(1,21,1) + c4_con) + ' / ' + str(random.randrange(1,21,1) + c4_con)],
    ['Intelligence (Save): ' + str(random.randrange(1,21,1) + c1_int) + ' / ' + str(random.randrange(1,21,1) + c1_int), 'Intelligence (Save): ' + str(random.randrange(1,21,1) + c2_int) + ' / ' + str(random.randrange(1,21,1) + c2_int),'Intelligence (Save): ' + str(random.randrange(1,21,1) + c3_int) + ' / ' + str(random.randrange(1,21,1) + c3_int),'Intelligence (Save): ' + str(random.randrange(1,21,1) + c4_int) + ' / ' + str(random.randrange(1,21,1) + c4_int)],
    ['Wisdom (Save): ' + str(random.randrange(1,21,1) + c1_wis) + ' / ' + str(random.randrange(1,21,1) + c1_wis), 'Wisdom (Save): ' + str(random.randrange(1,21,1) + c2_wis) + ' / ' + str(random.randrange(1,21,1) + c2_wis),'Wisdom (Save): ' + str(random.randrange(1,21,1) + c3_wis) + ' / ' + str(random.randrange(1,21,1) + c3_wis),'Wisdom (Save): ' + str(random.randrange(1,21,1) + c4_wis) + ' / ' + str(random.randrange(1,21,1) + c4_wis)],
    ['Charisma (Save): ' + str(random.randrange(1,21,1) + c1_cha) + ' / ' + str(random.randrange(1,21,1) + c1_cha),'Charisma (Save): ' + str(random.randrange(1,21,1) + c2_cha) + ' / ' + str(random.randrange(1,21,1) + c2_cha),'Charisma (Save): ' + str(random.randrange(1,21,1) + c3_cha) + ' / ' + str(random.randrange(1,21,1) + c3_cha),'Charisma (Save): ' + str(random.randrange(1,21,1) + c4_cha) + ' / ' + str(random.randrange(1,21,1) + c4_cha)],
    ['Acrobatics (DEX): ' + str(random.randrange(1,21,1) + c1_acrobatics) + ' / ' + str(random.randrange(1,21,1) + c1_acrobatics),'Acrobatics (DEX): ' + str(random.randrange(1,21,1) + c2_acrobatics) + ' / ' + str(random.randrange(1,21,1) + c2_acrobatics),'Acrobatics (DEX): ' + str(random.randrange(1,21,1) + c3_acrobatics) + ' / ' + str(random.randrange(1,21,1) + c3_acrobatics),'Acrobatics (DEX): ' + str(random.randrange(1,21,1) + c4_acrobatics) + ' / ' + str(random.randrange(1,21,1) + c4_acrobatics)],
    ['Animal Handling (WIS): ' + str(random.randrange(1,21,1) + c1_animal_handling) + ' / ' + str(random.randrange(1,21,1) + c1_animal_handling),'Animal Handling (WIS): ' + str(random.randrange(1,21,1) + c2_animal_handling) + ' / ' + str(random.randrange(1,21,1) + c2_animal_handling),'Animal Handling (WIS): ' + str(random.randrange(1,21,1) + c3_animal_handling) + ' / ' + str(random.randrange(1,21,1) + c3_animal_handling),'Animal Handling (WIS): ' + str(random.randrange(1,21,1) + c4_animal_handling) + ' / ' + str(random.randrange(1,21,1) + c4_animal_handling)],
    ['Arcana (INT): ' + str(random.randrange(1,21,1) + c1_arcana) + ' / ' + str(random.randrange(1,21,1) + c1_arcana),'Arcana (INT): ' + str(random.randrange(1,21,1) + c2_arcana) + ' / ' + str(random.randrange(1,21,1) + c2_arcana),'Arcana (INT): ' + str(random.randrange(1,21,1) + c3_arcana) + ' / ' + str(random.randrange(1,21,1) + c3_arcana),'Arcana (INT): ' + str(random.randrange(1,21,1) + c4_arcana) + ' / ' + str(random.randrange(1,21,1) + c4_arcana)],
    ['Athletics (STR): ' + str(random.randrange(1,21,1) + c1_athletics) + ' / ' + str(random.randrange(1,21,1) + c1_athletics),'Athletics (STR): ' + str(random.randrange(1,21,1) + c2_athletics) + ' / ' + str(random.randrange(1,21,1) + c2_athletics),'Athletics (STR): ' + str(random.randrange(1,21,1) + c3_athletics) + ' / ' + str(random.randrange(1,21,1) + c3_athletics),'Athletics (STR): ' + str(random.randrange(1,21,1) + c4_athletics) + ' / ' + str(random.randrange(1,21,1) + c4_athletics)],
    ['Deception (CHA): ' + str(random.randrange(1,21,1) + c1_deception) + ' / ' + str(random.randrange(1,21,1) + c1_deception),'Deception (CHA): ' + str(random.randrange(1,21,1) + c2_deception) + ' / ' + str(random.randrange(1,21,1) + c2_deception), 'Deception (CHA): ' + str(random.randrange(1,21,1) + c3_deception) + ' / ' + str(random.randrange(1,21,1) + c3_deception),'Deception (CHA): ' + str(random.randrange(1,21,1) + c4_deception) + ' / ' + str(random.randrange(1,21,1) + c4_deception)],
    ['History (INT): ' + str(random.randrange(1,21,1) + c1_history) + ' / ' + str(random.randrange(1,21,1) + c1_history),'History (INT): ' + str(random.randrange(1,21,1) + c2_history) + ' / ' + str(random.randrange(1,21,1) + c2_history),'History (INT): ' + str(random.randrange(1,21,1) + c3_history) + ' / ' + str(random.randrange(1,21,1) + c3_history),'History (INT): ' + str(random.randrange(1,21,1) + c4_history) + ' / ' + str(random.randrange(1,21,1) + c4_history)],
    ['Insight (WIS): ' + str(random.randrange(1,21,1) + c1_insight) + ' / ' + str(random.randrange(1,21,1) + c1_insight),'Insight (WIS): ' + str(random.randrange(1,21,1) + c2_insight) + ' / ' + str(random.randrange(1,21,1) + c2_insight), 'Insight (WIS): ' + str(random.randrange(1,21,1) + c3_insight) + ' / ' + str(random.randrange(1,21,1) + c3_insight),'Insight (WIS): ' + str(random.randrange(1,21,1) + c4_insight) + ' / ' + str(random.randrange(1,21,1) + c4_insight)],
    ['Intimidation (CHA): ' + str(random.randrange(1,21,1) + c1_intimidation) + ' / ' + str(random.randrange(1,21,1) + c1_intimidation),'Intimidation (CHA): ' + str(random.randrange(1,21,1) + c2_intimidation) + ' / ' + str(random.randrange(1,21,1) + c2_intimidation),'Intimidation (CHA): ' + str(random.randrange(1,21,1) + c3_intimidation) + ' / ' + str(random.randrange(1,21,1) + c3_intimidation),'Intimidation (CHA): ' + str(random.randrange(1,21,1) + c4_intimidation) + ' / ' + str(random.randrange(1,21,1) + c4_intimidation)],
    ['Investigation (INT): ' + str(random.randrange(1,21,1) + c1_investigation) + ' / ' + str(random.randrange(1,21,1) + c1_investigation),'Investigation (INT): ' + str(random.randrange(1,21,1) + c2_investigation) + ' / ' + str(random.randrange(1,21,1) + c2_investigation), 'Investigation (INT): ' + str(random.randrange(1,21,1) + c3_investigation) + ' / ' + str(random.randrange(1,21,1) + c3_investigation),'Investigation (INT): ' + str(random.randrange(1,21,1) + c4_investigation) + ' / ' + str(random.randrange(1,21,1) + c4_investigation)],
    ['Medicine (WIS): ' + str(random.randrange(1,21,1) + c1_medicine) + ' / ' + str(random.randrange(1,21,1) + c1_medicine),'Medicine (WIS): ' + str(random.randrange(1,21,1) + c2_medicine) + ' / ' + str(random.randrange(1,21,1) + c2_medicine),'Medicine (WIS): ' + str(random.randrange(1,21,1) + c3_medicine) + ' / ' + str(random.randrange(1,21,1) + c3_medicine),'Medicine (WIS): ' + str(random.randrange(1,21,1) + c4_medicine) + ' / ' + str(random.randrange(1,21,1) + c4_medicine)],
    ['Nature (INT): ' + str(random.randrange(1,21,1) + c1_nature) + ' / ' + str(random.randrange(1,21,1) + c1_nature), 'Nature (INT): ' + str(random.randrange(1,21,1) + c2_nature) + ' / ' + str(random.randrange(1,21,1) + c2_nature), 'Nature (INT): ' + str(random.randrange(1,21,1) + c3_nature) + ' / ' + str(random.randrange(1,21,1) + c3_nature), 'Nature (INT): ' + str(random.randrange(1,21,1) + c4_nature) + ' / ' + str(random.randrange(1,21,1) + c4_nature)], 
    ['Perception (WIS): ' + str(random.randrange(1,21,1) + c1_perception) + ' / ' + str(random.randrange(1,21,1) + c1_perception),'Perception (WIS): ' + str(random.randrange(1,21,1) + c2_perception) + ' / ' + str(random.randrange(1,21,1) + c2_perception),'Perception (WIS): ' + str(random.randrange(1,21,1) + c3_perception) + ' / ' + str(random.randrange(1,21,1) + c3_perception),'Perception (WIS): ' + str(random.randrange(1,21,1) + c4_perception) + ' / ' + str(random.randrange(1,21,1) + c4_perception)],
    ['Performance (CHA): ' + str(random.randrange(1,21,1) + c1_performance) + ' / ' + str(random.randrange(1,21,1) + c1_performance),'Performance (CHA): ' + str(random.randrange(1,21,1) + c2_performance) + ' / ' + str(random.randrange(1,21,1) + c2_performance), 'Performance (CHA): ' + str(random.randrange(1,21,1) + c3_performance) + ' / ' + str(random.randrange(1,21,1) + c3_performance),'Performance (CHA): ' + str(random.randrange(1,21,1) + c4_performance) + ' / ' + str(random.randrange(1,21,1) + c4_performance)],
    ['Persuasion (CHA): ' + str(random.randrange(1,21,1) + c1_persuasion) + ' / ' + str(random.randrange(1,21,1) + c1_persuasion),'Persuasion (CHA): ' + str(random.randrange(1,21,1) + c2_persuasion) + ' / ' + str(random.randrange(1,21,1) + c2_persuasion),'Persuasion (CHA): ' + str(random.randrange(1,21,1) + c3_persuasion) + ' / ' + str(random.randrange(1,21,1) + c3_persuasion),'Persuasion (CHA): ' + str(random.randrange(1,21,1) + c4_persuasion) + ' / ' + str(random.randrange(1,21,1) + c4_persuasion)],
    ['Religion (INT): ' + str(random.randrange(1,21,1) + c1_religion) + ' / ' + str(random.randrange(1,21,1) + c1_religion), 'Religion (INT): ' + str(random.randrange(1,21,1) + c2_religion) + ' / ' + str(random.randrange(1,21,1) + c2_religion), 'Religion (INT): ' + str(random.randrange(1,21,1) + c3_religion) + ' / ' + str(random.randrange(1,21,1) + c3_religion), 'Religion (INT): ' + str(random.randrange(1,21,1) + c4_religion) + ' / ' + str(random.randrange(1,21,1) + c4_religion)], 
    ['Slight of Hand (DEX): ' + str(random.randrange(1,21,1) + c1_slight_of_hand) + ' / ' + str(random.randrange(1,21,1) + c1_slight_of_hand),'Slight of Hand (DEX): ' + str(random.randrange(1,21,1) + c2_slight_of_hand) + ' / ' + str(random.randrange(1,21,1) + c2_slight_of_hand),'Slight of Hand (DEX): ' + str(random.randrange(1,21,1) + c3_slight_of_hand) + ' / ' + str(random.randrange(1,21,1) + c3_slight_of_hand),'Slight of Hand (DEX): ' + str(random.randrange(1,21,1) + c4_slight_of_hand) + ' / ' + str(random.randrange(1,21,1) + c4_slight_of_hand)],
    ['Stealth (DEX): ' + str(random.randrange(1,21,1) + c1_stealth) + ' / ' + str(random.randrange(1,21,1) + c1_stealth), 'Stealth (DEX): ' + str(random.randrange(1,21,1) + c2_stealth) + ' / ' + str(random.randrange(1,21,1) + c2_stealth), 'Stealth (DEX): ' + str(random.randrange(1,21,1) + c3_stealth) + ' / ' + str(random.randrange(1,21,1) + c3_stealth), 'Stealth (DEX): ' + str(random.randrange(1,21,1) + c4_stealth) + ' / ' + str(random.randrange(1,21,1) + c4_stealth)], 
    ['Survival (WIS): ' + str(random.randrange(1,21,1) + c1_survival) + ' / ' + str(random.randrange(1,21,1) + c1_survival),'Survival (WIS): ' + str(random.randrange(1,21,1) + c2_survival) + ' / ' + str(random.randrange(1,21,1) + c2_survival),'Survival (WIS): ' + str(random.randrange(1,21,1) + c3_survival) + ' / ' + str(random.randrange(1,21,1) + c3_survival),'Survival (WIS): ' + str(random.randrange(1,21,1) + c4_survival) + ' / ' + str(random.randrange(1,21,1) + c4_survival)],
]

table = columnar(data, headers, min_column_width=35)
print(table)

# TableOverflowError Fix
# NOTE: script uses Columnar. If script throws TableOverflowError, adjust the width of your command prompt
#       or terminal screen so that it matches the width of the columns being generated. This will provide
#       enough space for the table to draw itself.

