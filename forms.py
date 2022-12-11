from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField, \
    SelectField, SelectMultipleField, TextAreaField, FileField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
from character_race_details import list_of_races

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


class CreateCampaignForm(FlaskForm):
    title = StringField("Campaign Title", validators=[DataRequired()])
    subtitle = StringField("Campaign Subtitle", validators=[DataRequired()])
    description = CKEditorField("Campaign Summary", validators=[DataRequired()])
    page_image = StringField("URL for campaign page image", validators=[DataRequired()])
    campaign_card_img = StringField("URK for campaign card image", validators=[DataRequired()])
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
    name = StringField("Character Name", validators=[DataRequired()])
    campaign = SelectField("Please select which campaign this character is part off", choices=campaigns,
                           validators=[DataRequired()])
    character_image = StringField("Character Image URL", validators=[DataRequired()])
    token = StringField("Character Token URL", validators=[DataRequired()])
    race = StringField("Character Race", validators=[DataRequired()])
    character_class = StringField("Character Class", validators=[DataRequired()])
    alignment = StringField("Character Alignment", validators=[DataRequired()])
    appearance_summary = StringField("Short description of character appearance (up to 300 characters)",
                                     validators=[DataRequired()])
    background = StringField("Character Background", validators=[DataRequired()])
    personality_traits = CKEditorField("Personality Traits", validators=[DataRequired()])
    ideals = StringField("Character Ideals", validators=[DataRequired()])
    bonds = StringField("Character Bonds", validators=[DataRequired()])
    flaws = StringField("Character Flaws", validators=[DataRequired()])
    description = CKEditorField("Character Description", validators=[DataRequired()])
    backstory = CKEditorField("Character Backstory", validators=[DataRequired()])

    level = IntegerField("Character Level", validators=[DataRequired()])
    strength = IntegerField("Character Strength", validators=[DataRequired()])
    dexterity = IntegerField("Character Dexterity", validators=[DataRequired()])
    constitution = IntegerField("Character Constitution", validators=[DataRequired()])
    wisdom = IntegerField("Character Wisdom", validators=[DataRequired()])
    intelligence = IntegerField("Character Intelligence", validators=[DataRequired()])
    charisma = IntegerField("Character Charisma", validators=[DataRequired()])

    skills = SelectMultipleField("Please select which skills you are proficient with", choices=all_skills)
    saves = SelectMultipleField("Please select which saves you are proficient with", choices=all_saves)
    languages = CKEditorField("Please write down which languages you know. Please use bullet points")
    darkvision = IntegerField("Please write down your darkvision in ft")
    tool_proficiencies = CKEditorField("Please write down you tool proficiencies. Please use bullet points")
    submit = SubmitField("Submit Character")


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

