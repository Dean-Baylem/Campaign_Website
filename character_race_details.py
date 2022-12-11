# Details from the dnd5eapi are gathered and stored here. The details for the character races
# will not change from the 5e SRD frequently, if at all, so will be easier to store here.

import requests

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

#
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