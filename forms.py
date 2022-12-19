from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField, \
    SelectField, SelectMultipleField, TextAreaField, FileField, BooleanField
from wtforms.validators import DataRequired, URL
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
    name = StringField("Character Name", validators=[DataRequired()])
    campaign = SelectField("Please select which campaign this character is part off", choices=campaigns,
                           validators=[DataRequired()])
    sex = StringField("What is the characters gender?")
    char_img = StringField("Character Image URL", validators=[DataRequired()])
    token_img = StringField("Character Token URL", validators=[DataRequired()])
    char_lvl = IntegerField("What is the starting level of your character?", validators=[DataRequired()])
    alignment = SelectField("What is your characters alignment?", choices=alignments)

    # ------------- Character Race -----------------
    race = SelectField("Character Race", choices=list_of_races, validators=[DataRequired()])
    subrace = StringField("What Subrace are you?")
    main_bonus_score = SelectField("Which stat would you like your +2 bonus to be in?", choices=stats)
    sub_bonus_score = SelectField("Which stat would you like your +1 bonus to be in?",
                                  choices=stats)  # Remember that the sub and main bonus score must be different values.
    age = IntegerField("What is your characters age?")

    # ------------- Ability Scores -----------------
    strength = IntegerField("Character Strength")
    dexterity = IntegerField("Character Dexterity")
    constitution = IntegerField("Character Constitution")
    wisdom = IntegerField("Character Wisdom")
    intelligence = IntegerField("Character Intelligence")
    charisma = IntegerField("Character Charisma")

    # -------------- Character Class ----------------
    class_main = SelectField("What is your main Character Class", choices=all_classes,
                             validators=[DataRequired()])
    class_main_level = IntegerField("What is your main class level?")
    multiclass = SelectField("Do you have a second class?", choices=yes_no)
    hp_calculation = SelectField("Do you wish to take the average values for HP?", choices=yes_no)

    # ------------ Character Background -----------------------
    appearance_summary = StringField("Short description of character appearance (up to 300 characters)")
    background = StringField("Character Background", validators=[DataRequired()])
    personality_trait_1 = StringField("What is your first personality trait?", validators=[DataRequired()])
    personality_trait_2 = StringField("What is your second personality trait?", validators=[DataRequired()])
    ideals = StringField("Character Ideals", validators=[DataRequired()])
    bonds = StringField("Character Bonds", validators=[DataRequired()])
    flaws = StringField("Character Flaws", validators=[DataRequired()])
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

    # darkvision - Determined by race
    # saves = Determined by primary class
    # class_main_subclass = Column(String) ---- Own table based on class level
    # class_second = Column(String(150)) ---- Own Table for this.
    # class_second_level = Column(Integer)
    # class_second_subclass = Column(String)


class CreateFactionForm(FlaskForm):
    faction_name = StringField("Name of Faction", validators=[DataRequired()])
    faction_description = CKEditorField("Faction Summary", validators=[DataRequired()])
    faction_image = StringField("Faction image", validators=[DataRequired()])
    campaign = SelectField("Please select which campaign this faction is found in", choices=campaigns,
                           validators=[DataRequired()])
    submit = SubmitField("Submit Faction")


class CreateLocationForm(FlaskForm):
    place_name = StringField("Name of Location", validators=[DataRequired()])
    summary = CKEditorField("Description of the Location", validators=[DataRequired()])
    image = StringField("Local file location for campaign card image", validators=[DataRequired()])
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
    npc_image = StringField("NPC Image", validators=[DataRequired()])
    npc_description = CKEditorField("Describe the NPC", validators=[DataRequired()])
    npc_history = CKEditorField("NPC Backstory", validators=[DataRequired()])
    npc_notes = CKEditorField("Interactions between the NPC and the party", validators=[DataRequired()])
    campaign = SelectField("Please select the campaign for this NPC", choices=campaigns, validators=[DataRequired()])
    faction = StringField("What faction is this NPC associated with?")
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


class CharacterBaseDetailsForm(FlaskForm):
    name = StringField("Character name", default="Character name")
    campaign = SelectField("Please select which campaign this character is part off", choices=campaigns,
                           validators=[DataRequired()])
    sex = StringField("What gender is your character?")
    char_img = StringField("URL for character image")
    token_img = StringField("URL for token image")
    char_lvl = IntegerField("What level is your character?", default=1)
    alignment = SelectField("What is your character's alignment?", choices=alignments)


class CharacterRaceFormFirst(FlaskForm):
    race = SelectField("What race would you like to be?", choices=list_of_races)

# Build the below form into the route directly following the above form.
# class CharacterRaceFormSecond(FlaskForm):
#     subrace = Column(String(50))
#     main_bonus_score = Column(String)
#     sub_bonus_score = Column(String)
#     size = Column(String)
#     speed = Column(Integer)
#     age = Column(Integer)
