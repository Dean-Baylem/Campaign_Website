# Details from the dnd5eapi are gathered and stored here.

import requests


# Data obtained from DND5eapi and stored as lists and dictionaries.

class_saves = {'barbarian': ['str', 'con'],
               'bard': ['dex', 'cha'],
               'cleric': ['wis', 'cha'],
               'druid': ['int', 'wis'],
               'fighter': ['str', 'con'],
               'monk': ['str', 'dex'],
               'paladin': ['wis', 'cha'],
               'ranger': ['str', 'dex'],
               'rogue': ['dex', 'int'],
               'sorcerer': ['con', 'cha'],
               'warlock': ['wis', 'cha'],
               'wizard': ['int', 'wis']}


class_hit_die = {'barbarian': 12, 'bard': 8, 'cleric': 8,
                 'druid': 8, 'fighter': 10, 'monk': 8,
                 'paladin': 10, 'ranger': 10, 'rogue': 8,
                 'sorcerer': 6, 'warlock': 8, 'wizard': 6}

class_skill_profs = {'barbarian': {'desc': 'Choose two from Animal Handling, Athletics,'
                                           ' Intimidation, Nature, Perception, and Survival'},
                     'bard': {'desc': 'Choose any three'},
                     'cleric': {'desc': 'Choose two from History, Insight, Medicine, Persuasion, and Religion'},
                     'druid': {'desc': 'Choose two from Arcana, Animal Handling, Insight,'
                                       ' Medicine, Nature, Perception, Religion, and Survival'},
                     'fighter': {'desc': 'Choose two skills from Acrobatics,'
                                         ' Animal Handling, Athletics, History, Insight,'
                                         ' Intimidation, Perception, and Survival'},
                     'monk': {'desc': 'Choose two from Acrobatics, Athletics, History, Insight, Religion, and Stealth'},
                     'paladin': {'desc': 'Choose two from Athletics, Insight,'
                                         ' Intimidation, Medicine, Persuasion, and Religion'},
                     'ranger': {'desc': 'Choose three from Animal Handling, Athletics, Insight,'
                                        ' Investigation, Nature, Perception, Stealth, and Survival'},
                     'rogue': {'desc': 'Choose four from Acrobatics, Athletics, Deception, Insight,'
                                       ' Intimidation, Investigation, Perception, Performance,'
                                       ' Persuasion, Sleight of Hand, and Stealth'},
                     'sorcerer': {'desc': 'Choose two from Arcana, Deception, Insight,'
                                          ' Intimidation, Persuasion, and Religion'},
                     'warlock': {'desc': 'Choose two skills from Arcana, Deception, History,'
                                         ' Intimidation, Investigation, Nature, and Religion'},
                     'wizard': {'desc': 'Choose two from Arcana, History, Insight,'
                                        ' Investigation, Medicine, and Religion'}}


list_of_races = ['dragonborn', 'dwarf', 'elf', 'gnome', 'half-elf', 'half-orc', 'halfling', 'human', 'tiefling']

all_race_details = {'dragonborn': {'name': 'Dragonborn',
                                   'age description': 'Young dragonborn grow quickly. They walk hours after hatching, '
                                                      'attain the size and development of a 10-year-old human child'
                                                      ' by the age of 3, and reach adulthood by 15.'
                                                      ' They live to be around 80.',
                                   'languages': [{'index': 'common', 'name': 'Common', 'url': '/api/languages/common'},
                                                 {'index': 'draconic', 'name': 'Draconic', 'url': '/api/languages/draconic'}]},
                    'dwarf': {'name': 'Dwarf',
                              'age description': "Dwarves mature at the same rate as humans,"
                                                 " but they're considered young until they reach the age of 50."
                                                 " On average, they live about 350 years.",
                              'languages': [{'index': 'common', 'name': 'Common', 'url': '/api/languages/common'},
                                            {'index': 'dwarvish', 'name': 'Dwarvish', 'url': '/api/languages/dwarvish'}]},
                    'elf': {'name': 'Elf',
                            'age description': 'Although elves reach physical maturity at about the same age as humans,'
                                               ' the elven understanding of adulthood goes beyond physical'
                                               ' growth to encompass worldly experience. '
                                               'An elf typically claims adulthood and an adult name '
                                               'around the age of 100 and can live to be 750 years old.',
                            'languages': [{'index': 'common', 'name': 'Common', 'url': '/api/languages/common'},
                                          {'index': 'elvish', 'name': 'Elvish', 'url': '/api/languages/elvish'}]},
                    'gnome': {'name': 'Gnome',
                              'age description': 'Gnomes mature at the same rate humans do, and most are '
                                                 'expected to settle down into an adult life by around age 40. '
                                                 'They can live 350 to almost 500 years.',
                              'languages': [{'index': 'common', 'name': 'Common', 'url': '/api/languages/common'},
                                            {'index': 'gnomish', 'name': 'Gnomish', 'url': '/api/languages/gnomish'}]},
                    'half-elf': {'name': 'Half-Elf',
                                 'age description': 'Half-elves mature at the same rate humans do and reach'
                                                    ' adulthood around the age of 20. They live much longer than '
                                                    'humans, however, often exceeding 180 years.',
                                 'languages': [{'index': 'common', 'name': 'Common', 'url': '/api/languages/common'},
                                               {'index': 'elvish', 'name': 'Elvish', 'url': '/api/languages/elvish'}]},
                    'half-orc': {'name': 'Half-Orc',
                                 'age description': 'Half-orcs mature a little faster than humans,'
                                                    ' reaching adulthood around age 14. '
                                                    'They age noticeably faster and rarely live longer than 75 years.',
                                 'languages': [{'index': 'common', 'name': 'Common', 'url': '/api/languages/common'},
                                               {'index': 'orc', 'name': 'Orc', 'url': '/api/languages/orc'}]},
                    'halfling': {'name': 'Halfling',
                                 'age description': 'A halfling reaches adulthood at the age of 20 and '
                                                    'generally lives into the middle of his or her second century.',
                                 'languages': [{'index': 'common', 'name': 'Common', 'url': '/api/languages/common'},
                                               {'index': 'halfling', 'name': 'Halfling', 'url': '/api/languages/halfling'}]},
                    'human': {'name': 'Human',
                              'age description': 'Humans reach adulthood in their late '
                                                 'teens and live less than a century.',
                              'languages': [{'index': 'common', 'name': 'Common', 'url': '/api/languages/common'}]},
                    'tiefling': {'name': 'Tiefling',
                                 'age description': 'Tieflings mature at the same rate as '
                                                    'humans but live a few years longer.',
                                 'languages': [{'index': 'common', 'name': 'Common', 'url': '/api/languages/common'},
                                               {'index': 'infernal', 'name': 'Infernal', 'url': '/api/languages/infernal'}]}}



all_classes = ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin',
               'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard']


all_languages = ['Abyssal', 'Celestial', 'Common', 'Deep Speech', 'Draconic', 'Dwarvish', 'Elvish',
                 'Giant', 'Gnomish', 'Goblin', 'Halfling', 'Infernal', 'Orc',
                 'Primordial', 'Sylvan', 'Undercommon']

all_weapon_details = {'club': {'name': 'Club', 'weapon_range': 'Melee',
                               'dice': '1d4', 'num_die': '1', 'die_size': '4'},
                      'dagger': {'name': 'Dagger', 'weapon_range': 'Melee',
                                 'dice': '1d4', 'num_die': '1', 'die_size': '4'},
                      'greatclub': {'name': 'Greatclub', 'weapon_range': 'Melee',
                                    'dice': '1d8', 'num_die': '1', 'die_size': '8'},
                      'handaxe': {'name': 'Handaxe', 'weapon_range': 'Melee',
                                  'dice': '1d6', 'num_die': '1', 'die_size': '6'},
                      'javelin': {'name': 'Javelin', 'weapon_range': 'Melee',
                                  'dice': '1d6', 'num_die': '1', 'die_size': '6'},
                      'light-hammer': {'name': 'Light hammer', 'weapon_range': 'Melee',
                                       'dice': '1d4', 'num_die': '1', 'die_size': '4'},
                      'mace': {'name': 'Mace', 'weapon_range': 'Melee',
                               'dice': '1d6', 'num_die': '1', 'die_size': '6'},
                      'quarterstaff': {'name': 'Quarterstaff', 'weapon_range': 'Melee',
                                       'dice': '1d6', 'num_die': '1', 'die_size': '6'},
                      'sickle': {'name': 'Sickle', 'weapon_range': 'Melee',
                                 'dice': '1d4', 'num_die': '1', 'die_size': '4'},
                      'spear': {'name': 'Spear', 'weapon_range': 'Melee',
                                'dice': '1d6', 'num_die': '1', 'die_size': '6'},
                      'crossbow-light': {'name': 'Crossbow, light', 'weapon_range': 'Ranged',
                                         'dice': '1d8', 'num_die': '1', 'die_size': '8'},
                      'dart': {'name': 'Dart', 'weapon_range': 'Ranged',
                               'dice': '1d4', 'num_die': '1', 'die_size': '4'},
                      'shortbow': {'name': 'Shortbow', 'weapon_range': 'Ranged',
                                   'dice': '1d6', 'num_die': '1', 'die_size': '6'},
                      'sling': {'name': 'Sling', 'weapon_range': 'Ranged',
                                'dice': '1d4', 'num_die': '1', 'die_size': '4'},
                      'battleaxe': {'name': 'Battleaxe', 'weapon_range': 'Melee',
                                    'dice': '1d8', 'num_die': '1', 'die_size': '8'},
                      'flail': {'name': 'Flail', 'weapon_range': 'Melee',
                                'dice': '1d8', 'num_die': '1', 'die_size': '8'},
                      'glaive': {'name': 'Glaive', 'weapon_range': 'Melee',
                                 'dice': '1d10', 'num_die': '1', 'die_size': '10'},
                      'greataxe': {'name': 'Greataxe', 'weapon_range': 'Melee',
                                   'dice': '1d12', 'num_die': '1', 'die_size': '12'},
                      'greatsword': {'name': 'Greatsword', 'weapon_range': 'Melee',
                                     'dice': '2d6', 'num_die': '2', 'die_size': '6'},
                      'halberd': {'name': 'Halberd', 'weapon_range': 'Melee',
                                  'dice': '1d10', 'num_die': '1', 'die_size': '10'},
                      'lance': {'name': 'Lance', 'weapon_range': 'Melee',
                                'dice': '1d12', 'num_die': '1', 'die_size': '12'},
                      'longsword': {'name': 'Longsword', 'weapon_range': 'Melee',
                                    'dice': '1d8', 'num_die': '1', 'die_size': '8'},
                      'maul': {'name': 'Maul', 'weapon_range': 'Melee',
                               'dice': '2d6', 'num_die': '2', 'die_size': '6'},
                      'morningstar': {'name': 'Morningstar', 'weapon_range': 'Melee',
                                      'dice': '1d8', 'num_die': '1', 'die_size': '8'},
                      'pike': {'name': 'Pike', 'weapon_range': 'Melee',
                               'dice': '1d10', 'num_die': '1', 'die_size': '10'},
                      'rapier': {'name': 'Rapier', 'weapon_range': 'Melee',
                                 'dice': '1d8', 'num_die': '1', 'die_size': '8'},
                      'scimitar': {'name': 'Scimitar', 'weapon_range': 'Melee',
                                   'dice': '1d6', 'num_die': '1', 'die_size': '6'},
                      'shortsword': {'name': 'Shortsword', 'weapon_range': 'Melee',
                                     'dice': '1d6', 'num_die': '1', 'die_size': '6'},
                      'trident': {'name': 'Trident', 'weapon_range': 'Melee',
                                  'dice': '1d6', 'num_die': '1', 'die_size': '6'},
                      'war-pick': {'name': 'War pick', 'weapon_range': 'Melee',
                                   'dice': '1d8', 'num_die': '1', 'die_size': '8'},
                      'warhammer': {'name': 'Warhammer', 'weapon_range': 'Melee',
                                    'dice': '1d8', 'num_die': '1', 'die_size': '8'},
                      'whip': {'name': 'Whip', 'weapon_range': 'Melee',
                               'dice': '1d4', 'num_die': '1', 'die_size': '4'},
                      'blowgun': {'name': 'Blowgun', 'weapon_range': 'Ranged',
                                  'dice': '1d1', 'num_die': '1', 'die_size': '1'},
                      'crossbow-hand': {'name': 'Crossbow, hand', 'weapon_range': 'Ranged',
                                        'dice': '1d6', 'num_die': '1', 'die_size': '6'},
                      'crossbow-heavy': {'name': 'Crossbow, heavy', 'weapon_range': 'Ranged',
                                         'dice': '1d10', 'num_die': '1', 'die_size': '10'},
                      'longbow': {'name': 'Longbow', 'weapon_range': 'Ranged',
                                  'dice': '1d8', 'num_die': '1', 'die_size': '8'}}

all_tools = ["Alchemist's Supplies", "Brewer's Supplies", "Calligrapher's Supplies", "Carpenter's Tools",
             "Cartographer's Tools", "Cobbler's Tools", "Cook's utensils", "Glassblower's Tools",
             "Jeweler's Tools", "Leatherworker's Tools", "Mason's Tools", "Painter's Supplies",
             "Potter's Tools", "Smith's Tools", "Tinker's Tools", "Weaver's Tools", "Woodcarver's Tools",
             'Dice Set', 'Playing Card Set', 'Bagpipes', 'Drum', 'Dulcimer', 'Flute', 'Lute', 'Lyre',
             'Horn', 'Pan flute', 'Shawm', 'Viol', "Navigator's Tools", "Thieves' Tools"]

# {'index': 'barbarian', 'name': 'Barbarian', 'proficiencies': [{'index': 'light-armor', 'name': 'Light Armor', 'url': '/api/proficiencies/light-armor'}, {'index': 'medium-armor', 'name': 'Medium Armor', 'url': '/api/proficiencies/medium-armor'}, {'index': 'shields', 'name': 'Shields', 'url': '/api/proficiencies/shields'}, {'index': 'simple-weapons', 'name': 'Simple Weapons', 'url': '/api/proficiencies/simple-weapons'}, {'index': 'martial-weapons', 'name': 'Martial Weapons', 'url': '/api/proficiencies/martial-weapons'}, {'index': 'saving-throw-str', 'name': 'Saving Throw: STR', 'url': '/api/proficiencies/saving-throw-str'}, {'index': 'saving-throw-con', 'name': 'Saving Throw: CON', 'url': '/api/proficiencies/saving-throw-con'}], 'saving_throws': [{'index': 'str', 'name': 'STR', 'url': '/api/ability-scores/str'}, {'index': 'con', 'name': 'CON', 'url': '/api/ability-scores/con'}], 'starting_equipment': [{'equipment': {'index': 'explorers-pack', 'name': "Explorer's Pack", 'url': '/api/equipment/explorers-pack'}, 'quantity': 1}, {'equipment': {'index': 'javelin', 'name': 'Javelin', 'url': '/api/equipment/javelin'}, 'quantity': 4}], 'starting_equipment_options': [{'desc': '(a) a greataxe or (b) any martial melee weapon', 'choose': 1, 'type': 'equipment', 'from': {'option_set_type': 'options_array', 'options': [{'option_type': 'counted_reference', 'count': 1, 'of': {'index': 'greataxe', 'name': 'Greataxe', 'url': '/api/equipment/greataxe'}}, {'option_type': 'choice', 'choice': {'desc': 'any martial melee weapon', 'choose': 1, 'type': 'equipment', 'from': {'option_set_type': 'equipment_category', 'equipment_category': {'index': 'martial-melee-weapons', 'name': 'Martial Melee Weapons', 'url': '/api/equipment-categories/martial-melee-weapons'}}}}]}}, {'desc': '(a) two handaxes or (b) any simple weapon', 'choose': 1, 'type': 'equipment', 'from': {'option_set_type': 'options_array', 'options': [{'option_type': 'counted_reference', 'count': 2, 'of': {'index': 'handaxe', 'name': 'Handaxe', 'url': '/api/equipment/handaxe'}}, {'option_type': 'choice', 'choice': {'desc': 'any simple weapon', 'choose': 1, 'type': 'equipment', 'from': {'option_set_type': 'equipment_category', 'equipment_category': {'index': 'simple-weapons', 'name': 'Simple Weapons', 'url': '/api/equipment-categories/simple-weapons'}}}}]}}], 'class_levels': '/api/classes/barbarian/levels', 'multi_classing': {'prerequisites': [{'ability_score': {'index': 'str', 'name': 'STR', 'url': '/api/ability-scores/str'}, 'minimum_score': 13}], 'proficiencies': [{'index': 'shields', 'name': 'Shields', 'url': '/api/proficiencies/shields'}, {'index': 'simple-weapons', 'name': 'Simple Weapons', 'url': '/api/proficiencies/simple-weapons'}, {'index': 'martial-weapons', 'name': 'Martial Weapons', 'url': '/api/proficiencies/martial-weapons'}]}, 'subclasses': [{'index': 'berserker', 'name': 'Berserker', 'url': '/api/subclasses/berserker'}], 'url': '/api/classes/barbarian'}

# ------------------------- DnD 5e Spells --------------------------
# cure_wounds = requests.get("https://www.dnd5eapi.co/api/spells/cure-wounds").json()
# print(cure_wounds)

spell_data = requests.get("https://www.dnd5eapi.co/api/spells").json()
for spell in spell_data['results']:
    primary_damage_lvl_1 = "None"
    primary_damage_lvl_2 = "None"
    primary_damage_lvl_3 = "None"
    primary_damage_lvl_4 = "None"
    primary_damage_lvl_5 = "None"
    primary_damage_lvl_6 = "None"
    primary_damage_lvl_7 = "None"
    primary_damage_lvl_8 = "None"
    primary_damage_lvl_9 = "None"
    cantrip_damage_die_1 = "None"
    cantrip_damage_die_2 = "None"
    cantrip_damage_die_3 = "None"
    cantrip_damage_die_4 = "None"
    url = "https://www.dnd5eapi.co/api/spells/" + spell['index']
    spell_details = requests.get(url).json()
    # print(spell_details)
    primary_damage = ""
    try:
        if spell_details['level'] == 0:
            level_damage = {}
            try:
                damage_data = spell_details['damage']
                level_damage = damage_data['damage_at_character_level']
            except KeyError:
                level_damage = spell_details['heal_at_slot_level']
            print(f"{spell_details['name']} : {level_damage}")
            damage_dies = ""
            for level, damage in level_damage.items():
                damage_dies += f"'{level}:{damage}'"
            getting_dies = damage_dies.split("'")
            for dies in getting_dies:
                level = (dies.split(":")[0])
                if level == '1':
                    cantrip_damage_die_1 = dies.split(":")[1]
                if level == '5':
                    cantrip_damage_die_2 = dies.split(":")[1]
                if level == '11':
                    cantrip_damage_die_3 = dies.split(":")[1]
                if level == '17':
                    cantrip_damage_die_4 = dies.split(":")[1]
        else:
            level_damage = {}
            try:
                damage_data = spell_details['damage']
                level_damage = damage_data['damage_at_slot_level']
            except KeyError:
                level_damage = spell_details['heal_at_slot_level']
            print(f"{spell_details['name']} : {level_damage}")
            damage_dies = ""
            for level, damage in level_damage.items():
                damage_dies += f"'{level}:{damage}'"
            getting_dies = damage_dies.split("'")
            for dies in getting_dies:
                level = (dies.split(":")[0])
                if level == '1':
                    primary_damage_lvl_1 = dies.split(":")[1]
                if level == '2':
                    primary_damage_lvl_2 = dies.split(":")[1]
                if level == '3':
                    primary_damage_lvl_3 = dies.split(":")[1]
                if level == '4':
                    primary_damage_lvl_4 = dies.split(":")[1]
                if level == '5':
                    primary_damage_lvl_5 = dies.split(":")[1]
                if level == '6':
                    primary_damage_lvl_6 = dies.split(":")[1]
                if level == '7':
                    primary_damage_lvl_7 = dies.split(":")[1]
                if level == '8':
                    primary_damage_lvl_8 = dies.split(":")[1]
                if level == '9':
                    primary_damage_lvl_9 = dies.split(":")[1]
    except KeyError:
        pass

    # print(spell_details)
    print("Spell Slot Damage")
    spell_slot_damages = [primary_damage_lvl_1, primary_damage_lvl_2, primary_damage_lvl_3, primary_damage_lvl_4,
                          primary_damage_lvl_5, primary_damage_lvl_6, primary_damage_lvl_7, primary_damage_lvl_8,
                          primary_damage_lvl_9]
    print(spell_slot_damages)
    print("Cantrip damage")
    cantrip_damages = [cantrip_damage_die_1, cantrip_damage_die_2, cantrip_damage_die_3, cantrip_damage_die_4]
    print(cantrip_damages)

    # print(spell_details)



# fireball_data = requests.get("https://www.dnd5eapi.co/api/spells/fireball").json()
# # print(fireball_data)
# primary_damage = ""
# damage_data = fireball_data['damage']
# level_damage = damage_data['damage_at_slot_level']
# damage_dies = ""
# for level, damage in level_damage.items():
#     damage_dies += f"'{level}:{damage}'"
# getting_dies = damage_dies.split("'")
# for dies in getting_dies:
#     level = (dies.split(":")[0])
#     if level == '1':
#         primary_damage_lvl_1 = dies.split(":")[1]
#     if level == '2':
#         primary_damage_lvl_2 = dies.split(":")[1]
#     if level == '3':
#         primary_damage_lvl_3 = dies.split(":")[1]
#     if level == '4':
#         primary_damage_lvl_4 = dies.split(":")[1]
#     if level == '5':
#         primary_damage_lvl_5 = dies.split(":")[1]
#     if level == '6':
#         primary_damage_lvl_6 = dies.split(":")[1]
#     if level == '7':
#         primary_damage_lvl_7 = dies.split(":")[1]
#     if level == '8':
#         primary_damage_lvl_8 = dies.split(":")[1]
#     if level == '9':
#         primary_damage_lvl_9 = dies.split(":")[1]
#
# print(primary_damage_lvl_1)
# print(primary_damage_lvl_2)
# print(primary_damage_lvl_3)
# print(primary_damage_lvl_4)
# print(primary_damage_lvl_5)
# print(primary_damage_lvl_6)
# print(primary_damage_lvl_7)
# print(primary_damage_lvl_8)
# print(primary_damage_lvl_9)






# ---------------- Checking for all playable races ----------------------

# races = requests.get("https://www.dnd5eapi.co/api/races")
# race_data = races.json()
# all_races = race_data['results']
#
# for race in all_races:
#     print(race['index'])
#     url = "https://www.dnd5eapi.co/api/races/" + race['index']
#     race_details = requests.get(url).json()
#     print(race_details)
#     all_race_details[race_details['index']] = {
#         "name": race_details['name'],
#         "age description": race_details['age'],
#         "languages": race_details['languages'],
#     }
#
#
# print(all_race_details)
# print(all_race_details['elf'])

# ------------- Checking for playable classes and details ------------------

#
# data = requests.get('https://www.dnd5eapi.co/api/classes/')
# all_data = data.json()
# for player_class in all_data['results']:
#     url = "https://www.dnd5eapi.co" + player_class['url']
#     class_data = requests.get(url).json()
#
#     # Obtaining the saving throws for each class
#     # saving_throw_data = class_data['saving_throws']
#     # saving_throws = []
#     # for save in saving_throw_data:
#     #     saving_throws.append(save['index'])
#     # class_saves[class_data['index']] = saving_throws
#
#
#     # Obtaining skill_prof details per class and storing into a dictionary
#     # class_skill_profs[class_data['index']] = {
#     #     'desc': class_data['proficiency_choices'][0]['desc']
#     # }
#
#     # Obtaining hit die data per class and storing into a dictionary
#     # class_hit_die[class_data['index']] = class_data['hit_die']
#
#

# -------------------- Get languages! -------------------

# languages = requests.get('https://www.dnd5eapi.co/api/languages')
#
# language_data = languages.json()
#
# all_data = language_data['results']
# list_of_languages = []
# for language in all_data:
#     all_languages.append(language['name'])
#
# print(all_languages)


# --------------- Get the weapon details!!! --------------------

# for race in all_races:
#     print(race['index'])
#     url = "https://www.dnd5eapi.co/api/races/" + race['index']
#     race_details = requests.get(url).json()
#     all_race_details[race_details['index']] = {
#         "name": race_details['name'],
#         "age description": race_details['age'],
#         "languages": race_details['languages'],
#     }


# weapons = requests.get('https://www.dnd5eapi.co/api/equipment-categories/weapon')
# weapon_data = weapons.json()
# for weapon in weapon_data['equipment']:
#     if weapon['index'] == "net":
#         pass
#     else:
#         try:
#             url = 'https://www.dnd5eapi.co' + (weapon['url'])
#             weapon_data = requests.get(url).json()
#             all_weapon_details[weapon_data['index']] = {
#             'name': weapon_data['name'],
#             'weapon_range': weapon_data['weapon_range'],
#             'dice': weapon_data['damage']['damage_dice'],
#             'num_die': (weapon_data['damage']['damage_dice'].split("d")[0]),
#             'die_size': (weapon_data['damage']['damage_dice'].split("d")[1]),
#             }
#         except: ## This except will ignore the magic weapons later in the API that are not needed.
#             pass
#
# print(all_weapon_details)

# ------------- Get the Proficiencies ---------------
# profs = requests.get('https://www.dnd5eapi.co/api/proficiencies')
# all_profs = profs.json()
# print(all_profs['results'])


# -------------- Get all non-magical armor --------------
# armor = requests.get('https://www.dnd5eapi.co/api/equipment-categories/armor')
# armor_data = armor.json()
# for armor in armor_data['equipment']:
#     url = 'https://www.dnd5eapi.co' + (armor['url'])
#     armor_details = requests.get(url).json()
#     try:
#         if armor_details['contents'] == []:
#             print(armor_details)
#     except KeyError:
#         pass
#
# all_tools = ["Alchemist's Supplies", "Brewer's Supplies", "Calligrapher's Supplies", "Carpenter's Tools",
#              "Cartographer's Tools", "Cobbler's Tools", "Cook's utensils", "Glassblower's Tools",
#              "Jeweler's Tools", "Leatherworker's Tools", "Mason's Tools", "Painter's Supplies",
#              "Potter's Tools", "Smith's Tools", "Tinker's Tools", "Weaver's Tools", "Woodcarver's Tools",
#              'Dice Set', 'Playing Card Set', 'Bagpipes', 'Drum', 'Dulcimer', 'Flute', 'Lute', 'Lyre',
#              'Horn', 'Pan flute', 'Shawm', 'Viol', "Navigator's Tools", "Thieves' Tools"]
#
# filled_types_of_equipment = ['adventuring-gear', 'tools', 'mounts-and-vehicles', 'weapon', 'armor']

# data = requests.get('https://www.dnd5eapi.co/api/equipment-categories/mounts-and-vehicles')
# vehicle_data = data.json()['equipment']
# for vehicle in vehicle_data:
#     url = 'https://www.dnd5eapi.co' + vehicle['url']
#     vehicle_information = requests.get(url).json()
#     print(vehicle_information)

# data = requests.get('https://www.dnd5eapi.co/api/equipment-categories/tools')
# tool_data = data.json()['equipment']
# for tool in tool_data:
#     url = 'https://www.dnd5eapi.co' + tool['url']
#     tool_information = requests.get(url).json()
#     print(tool_information)
#
# print(all_tools)

# ---------------- Getting Adventuring Gear ----------------------
# data = requests.get('https://www.dnd5eapi.co/api/equipment-categories/adventuring-gear')
# adventuring_gear_data = data.json()
# for gear in adventuring_gear_data['equipment']:
#     url = 'https://www.dnd5eapi.co' + gear['url']
#     gear_information = requests.get(url).json()
#     name = gear_information['name']
#     equip_category = gear_information['equipment_category']['name']
#     gear_category = gear_information['gear_category']['name']
#     cost = str(gear_information['cost']['quantity']) + " " + str(gear_information['cost']['unit'])
#     description = gear_information['desc']
#     print(name)
#     print(equip_category)
#     print(gear_category)
#     print(cost)
#     if not description:
#         pass
#     else:
#         print(description)

# ------------- Checking for different equipment categories -------------
# types_of_equipment = []
# data = requests.get('https://www.dnd5eapi.co/api/equipment/')
# all_data = data.json()
# for item in all_data['results']:
#     url = 'https://www.dnd5eapi.co' + item['url']
#     all_information = requests.get(url).json()
#     if all_information['equipment_category']['index'] in types_of_equipment:
#         pass
#     else:
#         types_of_equipment.append(all_information['equipment_category']['index'])
#
# print(types_of_equipment)


# 'equipment_category': {'index': 'adventuring-gear', 'name': 'Adventuring Gear', 'url': '/api/equipment-categories/adventuring-gear'}


# abacus_data = requests.get('https://www.dnd5eapi.co/api/equipment/abacus')
# print(abacus_data.json())


