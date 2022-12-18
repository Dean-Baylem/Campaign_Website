# Details from the dnd5eapi are gathered and stored here.

import requests


# Data obtained from DND5eapi and stored as lists and dictionaries.

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

# ---------------- Checking for all playable races ----------------------

# races = requests.get("https://www.dnd5eapi.co/api/races")
# race_data = races.json()
# all_races = race_data['results']
#
# for race in all_races:
#     print(race['index'])
#     url = "https://www.dnd5eapi.co/api/races/" + race['index']
#     race_details = requests.get(url).json()
#     all_race_details[race_details['index']] = {
#         "name": race_details['name'],
#         "age description": race_details['age'],
#         "languages": race_details['languages'],
#     }
#
#
# print(all_race_details)
# print(all_race_details['elf'])

# ------------- Checking for all the playable classes ------------------

# data = requests.get('https://www.dnd5eapi.co/api/classes/')
# all_data = data.json()
# for player_class in all_data['results']:
#     all_classes.append(player_class['name'])
#
# print(all_classes)

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


