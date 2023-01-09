from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField, \
    SelectField, SelectMultipleField, TextAreaField, FileField, BooleanField, widgets
from wtforms.validators import DataRequired, URL, Regexp
from flask_ckeditor import CKEditorField
from dnd5e_api_stored_details import list_of_races, all_weapon_details, all_classes, \
    all_languages, all_race_details, all_tools

# List of campaigns currently running:
campaigns = ["GoS", "CoS", "LotST"]

# Skill and Save lists
all_skills = ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History",
              "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception",
              "Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"]

all_saves = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

# List of dm's:
dm_list = ["DungeonDelverDean", "FirehouseGames", "TestDM"]

# Alignments
alignments = ['Lawful Good', 'Neutral Good', 'Chaotic Good', 'Lawful Neutral', 'Neutral',
              'Chaotic Neutral', 'Lawful Evil', 'Neutral Evil', 'Chaotic Evil']

# Stats
stats = ["Strength", "Dexterity", "Constitution", "Wisdom", "Intelligence", "Charisma"]

# Boolean Selection
yes_no = ["Yes", "No"]

# ALl Tools

first_half_tools = ["Alchemist's Supplies", "Brewer's Supplies", "Calligrapher's Supplies", "Carpenter's Tools",
                    "Cartographer's Tools", "Cobbler's Tools", "Cook's Utensils", "Glassblower's Tools",
                    "Jeweler's Tools", "Leatherworker's Tools", "Mason's Tools"]

second_half_tools = ["Painter's Supplies", "Poisoner Kit", "Smith's Tools",
                     "Tinker's Tools", "Weaver's Tools", "Woodcarver's Tools",
                     "Navigator's Tools", "Thieves' Tools", "Forgery Kit", "Disguise Kit"]

instruments = ['Bagpipes', 'Drum', 'Dulcimer', 'Flute', 'Lute', 'Lyre',
             'Horn', 'Pan flute', 'Shawm', 'Viol']


# All languages

first_half_all_languages = ['Abyssal', 'Celestial', 'Common', 'Deep Speech',
                            'Draconic', 'Dwarvish', 'Elvish', 'Giant']

second_half_all_languages = ['Gnomish', 'Goblin', 'Halfling', 'Infernal',
                             'Orcish', 'Primordial', 'Sylvan', 'Undercommon']

class CreateCampaignForm(FlaskForm):
    title = StringField("Campaign Title", validators=[DataRequired()])
    subtitle = StringField("Campaign Subtitle", validators=[DataRequired()])
    description = CKEditorField("Campaign Summary", validators=[DataRequired()])
    page_image = StringField("URL for campaign page image", validators=[DataRequired()])
    campaign_card_img = StringField("URL for campaign card image", validators=[DataRequired()])
    central_location = StringField("Campaign central location", validators=[DataRequired()])
    central_location_img = StringField("Campaign central location img", validators=[DataRequired()])
    central_location_map = StringField("Campaign central location map", validators=[DataRequired()])
    region_summary = CKEditorField("Describe the region of the campaign", validators=[DataRequired()])
    region_map = StringField("Map of the region.")
    faction_summary = CKEditorField("Describe the factions of the campaign", validators=[DataRequired()])
    regular_day = StringField("What day will the weekly game take place?", validators=[DataRequired()])
    regular_time = StringField("What time will the weekly game take place?", validators=[DataRequired()])
    dm_username = SelectField("Username of the DM for the campaign?", choices=dm_list, validators=[DataRequired()])
    dm_img = FileField("Image File")
    submit = SubmitField("Submit Campaign")


class CreateNewCharacter(FlaskForm):
    # ----------- Character Details -------------
    name = StringField("Character Name")
    file = FileField("Character Token")
    campaign = SelectField("Please select which campaign this character is part off", choices=campaigns)
    sex = StringField("What is the characters gender?")
    char_lvl = IntegerField("What is the starting level of your character?")
    alignment = SelectField("What is your characters alignment?", choices=alignments)

    # ------------- Character Race -----------------
    race = SelectField("Character Race", choices=list_of_races)
    subrace = StringField("What Subrace are you?")
    main_bonus_score = SelectField("Which stat would you like your +2 bonus to be in?", choices=stats)
    sub_bonus_score = SelectField("Which stat would you like your +1 bonus to be in?", choices=stats)  # Remember that the sub and main bonus score must be different values.
    age = IntegerField("What is your characters age?")

    # ------------- Ability Scores -----------------
    strength = IntegerField("Character Strength")
    dexterity = IntegerField("Character Dexterity")
    constitution = IntegerField("Character Constitution")
    wisdom = IntegerField("Character Wisdom")
    intelligence = IntegerField("Character Intelligence")
    charisma = IntegerField("Character Charisma")

    # -------------- Character Class ----------------
    class_main = SelectField("What is your main Character Class", choices=all_classes,)
    class_main_level = IntegerField("What is your main class level?")
    multiclass = SelectField("Do you have a second class?", choices=yes_no)
    hp_calculation = SelectField("Do you wish to take the average values for HP?", choices=yes_no)

    # ------------ Character Background -----------------------
    appearance_summary = StringField("Short description of character appearance (up to 300 characters)")
    background = StringField("Character Background")
    personality_trait_1 = StringField("What is your first personality trait?")
    personality_trait_2 = StringField("What is your second personality trait?")
    ideals = StringField("Character Ideals")
    bonds = StringField("Character Bonds")
    flaws = StringField("Character Flaws")
    appearance_detailed = CKEditorField("Please provide a detailed description of your characters appearance")
    height = IntegerField("What is your characters height in cm: ")
    weight = IntegerField("What is your characters weight in kg: ")
    backstory = CKEditorField("Character Backstory")

    # ------------ Tool, language and skill Proficiencies --------------
    skills = SelectMultipleField("Please select which skills you are proficient with", choices=all_skills)
    languages = SelectMultipleField("Which languages do you know?", choices=all_languages)
    tool_proficiencies = SelectMultipleField("Select which tools you are proficient with?", choices=all_tools)
    instruments = TextAreaField("Which instruments are you proficient with?")

    submit = SubmitField("Submit Character")


class SpellSelection(FlaskForm):
    spells = SelectMultipleField("Please select your spells")
    submit = SubmitField("Submit")


class CreateStats(FlaskForm):
    strength = IntegerField("Strength")
    dexterity = IntegerField("Dexterity")
    constitution = IntegerField("Constitution")
    intelligence = IntegerField("Intelligence")
    wisdom = IntegerField("Wisdom")
    charisma = IntegerField("Charisma")
    submit = SubmitField("Submit")


class CreateFactionForm(FlaskForm):
    faction_name = StringField("Name of Faction", validators=[DataRequired()])
    faction_description = CKEditorField("Faction Summary", validators=[DataRequired()])
    faction_image = StringField("Faction image", validators=[DataRequired()])
    campaign = SelectField("Please select which campaign this faction is found in", choices=campaigns,
                           validators=[DataRequired()])
    submit = SubmitField("Submit Faction")


class EditNotes(FlaskForm):
    notes = CKEditorField("Edit Faction Notes")
    submit = SubmitField("Submit Notes")


class AddComment(FlaskForm):
    body = CKEditorField("Please write your comment")
    submit = SubmitField("Submit Comment")


class CreateLocationForm(FlaskForm):
    location_name = StringField("Name of Location", validators=[DataRequired()])
    location_summary = CKEditorField("Description of the Location", validators=[DataRequired()])
    location_img = StringField("Local file location for campaign card image", validators=[DataRequired()])
    location_notes = TextAreaField("Notes of the location")
    campaign = SelectField("Please select which campaign this location is a part off",
                           choices=campaigns, validators=[DataRequired()])
    submit = SubmitField("Submit Location")


class CreateNewPlayerForm(FlaskForm):
    email = EmailField("Please enter your email address", validators=[DataRequired()])
    username = StringField("Please enter your username", validators=[DataRequired()])
    password = PasswordField("Please enter your password", validators=[DataRequired()])
    submit = SubmitField("Submit Player")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SessionReviewForm(FlaskForm):
    title = StringField("Review Title", validators=[DataRequired()])
    subtitle = StringField("Review Subtitle", validators=[DataRequired()])
    body = CKEditorField("Session Review", validators=[DataRequired()])
    submit = SubmitField("Submit")


class NPCForm(FlaskForm):
    name = StringField("NPC Name", validators=[DataRequired()])
    race = StringField("NPC Race")
    sex = StringField("What is the NPC's gender?")
    npc_image = StringField("Full NPC Image", validators=[DataRequired()])
    npc_token = StringField("NPC Token Image")
    npc_description = CKEditorField("Describe the NPC", validators=[DataRequired()])
    personality_trait_1 = TextAreaField("Please Enter the first personality trait", validators=[DataRequired()])
    personality_trait_2 = TextAreaField("Enter a second personality trait if applicable")
    ideals = TextAreaField("NPC Ideals", validators=[DataRequired()])
    bonds = TextAreaField("NPC Bonds", validators=[DataRequired()])
    flaws = TextAreaField("NPC Flaws", validators=[DataRequired()])
    npc_history = CKEditorField("Notes the characters know about the NPC", validators=[DataRequired()])
    npc_notes = CKEditorField("Secret DM notes regarding the NPC", validators=[DataRequired()])
    campaign = SelectField("Please select the campaign for this NPC", choices=campaigns, validators=[DataRequired()])
    faction = SelectField("What faction is this NPC associated with?")
    location = SelectField("Where is the NPC based?")
    submit = SubmitField("Submit")


class UpcomingCampaignForm(FlaskForm):
    name = StringField("Campaign Title", validators=[DataRequired()])
    timeslot = StringField("Desired Timeslot", validators=[DataRequired()])
    image = StringField("Campaign Image", validators=[DataRequired()])
    premise = CKEditorField("Describe the campaign", validators=[DataRequired()])
    registered_players = IntegerField("How many players have currently agreed to play?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ContactMe(FlaskForm):
    name = StringField("Name", default="Your name...", validators=[DataRequired()])
    email = EmailField("Email", default="Your email...", validators=[DataRequired()])
    subject = StringField("Subject", default="Your subject...", validators=[DataRequired()])
    message = TextAreaField("Message", default="Your message...", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UploadImageForm(FlaskForm):
    file = FileField("Select the image file")
    name = StringField("Name")
    submit = SubmitField("Submit")


class EditNameRaceClass(FlaskForm):
    name = StringField("Name")
    race = StringField("Character Race")
    subrace = StringField("Character Subrace")
    class_main = StringField("Primary class")
    class_main_level = IntegerField("Primary Class Level")
    class_second = StringField("Multiclass Option")
    class_second_level = IntegerField("Multiclass level")
    submit = SubmitField("Submit Changes")


class EditBackground(FlaskForm):
    background = StringField("Character Background")
    alignment = StringField("Character Alignment")
    appearance_summary = StringField("Short description of character appearance (up to 300 characters)")
    submit = SubmitField("Submit Changes")


class EditAbilityScores(FlaskForm):
    strength = IntegerField("Character Strength")
    dexterity = IntegerField("Character Dexterity")
    constitution = IntegerField("Character Constitution")
    wisdom = IntegerField("Character Wisdom")
    intelligence = IntegerField("Character Intelligence")
    charisma = IntegerField("Character Charisma")
    submit = SubmitField("Submit Changes")


class MultiCheckboxField(SelectMultipleField):
    """Class to generate a checkbox field for use in WTForms"""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class EditSkillProfs(FlaskForm):
    skills = MultiCheckboxField("Which skills are your proficient with?", choices=all_skills)
    submit = SubmitField("Submit Changes")


class EditStatsSenses(FlaskForm):
    current_hit_points = IntegerField("What's your current HP?")
    max_hit_points = IntegerField("What's your max HP?")
    temp_hit_points = IntegerField("How many temp Hit Points?")
    darkvision = SelectField("Have you gained Darkvision?", choices=yes_no)
    darkvision_range = IntegerField("What's your dark vision range?")
    blindsight = SelectField("Have you gained blindsight?", choices=yes_no)
    blindsight_range = IntegerField("Whats your blindsight range?")
    truesight = SelectField("Have you gained Truesight?", choices=yes_no)
    truesight_range = IntegerField("What's your truesight range?")
    first_half_tools = MultiCheckboxField(choices=first_half_tools)
    second_half_tools = MultiCheckboxField(choices=second_half_tools)
    first_half_languages = MultiCheckboxField(choices=first_half_all_languages)
    second_half_languages = MultiCheckboxField(choices=second_half_all_languages)
    submit = SubmitField("Submit Changes")


class EditPersonality(FlaskForm):
    personality_trait_1 = StringField("What is your first personality trait?")
    personality_trait_2 = StringField("What is your second personality trait?")
    ideals = StringField("Character Ideals")
    bonds = StringField("Character Bonds")
    flaws = StringField("Character Flaws")
    submit = SubmitField("Submit Changes")

