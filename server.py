import datetime
from statistics import median
from math import floor, ceil
import os
from flask import Flask, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_wtf import FlaskForm
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
from functools import wraps
import forms
from dnd5e_api_stored_details import class_hit_die, class_skill_profs, all_race_details, class_saves
import random
import requests


# ------------- Character Functions ---------------------
all_tools = ["Alchemist's Supplies", "Brewer's Supplies", "Calligrapher's Supplies", "Carpenter's Tools",
             "Cartographer's Tools", "Cobbler's Tools", "Cook's utensils", "Glassblower's Tools",
             "Jeweler's Tools", "Leatherworker's Tools", "Mason's Tools", "Painter's Supplies",
             "Potter's Tools", "Smith's Tools", "Tinker's Tools", "Weaver's Tools", "Woodcarver's Tools",
             'Dice Set', 'Playing Card Set', 'Bagpipes', 'Drum', 'Dulcimer', 'Flute', 'Lute', 'Lyre',
             'Horn', 'Pan flute', 'Shawm', 'Viol', "Navigator's Tools", "Thieves' Tools"]


def character_tools(character):
    """
    This function checks the boolean values for the tools in the character database table
    and returns a list containing the tools the character is proficient with.
    """
    proficient_tools = []
    if character.alchemist_tools:
        proficient_tools.append("Alchemist Supplies")
    if character.calligrapher_tools:
        proficient_tools.append("Calligrapher Tools")
    if character.cartographer_tools:
        proficient_tools.append("Cartographer Tools")
    if character.cooks_utensils:
        proficient_tools.append("Cooks Utensils")
    if character.forgery_kit:
        proficient_tools.append("Forgery Kit")
    if character.herbalism_kit:
        proficient_tools.append("Herbalism Kit")
    if character.leatherworker_tools:
        proficient_tools.append("Leatherworker Tools")
    if character.navigator_tools:
        proficient_tools.append("Navigator Tools")
    if character.poisoner_kit:
        proficient_tools.append("Poisoner Kit")
    if character.smith_tools:
        proficient_tools.append("Smith Tools")
    if character.tinker_tools:
        proficient_tools.append("Tinker Tools")
    if character.woodcarver_tools:
        proficient_tools.append("Woodcarver Tools")
    if character.brewer_tools:
        proficient_tools.append("Brewer Tools")
    if character.carpenter_tools:
        proficient_tools.append("Carpenter Tools")
    if character.cobbler_tools:
        proficient_tools.append("Cobbler Tools")
    if character.disguise_kit:
        proficient_tools.append("Disguise Kit")
    if character.glassblower_tools:
        proficient_tools.append("Glassblower Tools")
    if character.jeweler_tools:
        proficient_tools.append("Jeweler Tools")
    if character.mason_tools:
        proficient_tools.append("Mason Tools")
    if character.painter_tools:
        proficient_tools.append("Painter Tools")
    if character.thief_tools:
        proficient_tools.append("Thief Tools")
    if character.weaver_tools:
        proficient_tools.append("Weaver Tools")
    return proficient_tools



def character_languages(character):
    """
    This function Checks the Boolean Values for the languages in the character database table
     and returns a list containing the characters known languages.
     """
    known_languages = []
    if character.abyssal:
        known_languages.append("Abyssal")
    if character.celestial:
        known_languages.append("Celestial")
    if character.common:
        known_languages.append("Common")
    if character.deep_speech:
        known_languages.append("Deep Speech")
    if character.draconic:
        known_languages.append("Draconic")
    if character.dwarvish:
        known_languages.append("Dwarvish")
    if character.elvish:
        known_languages.append("Elvish")
    if character.giant:
        known_languages.append("Giant")
    if character.gnomish:
        known_languages.append("Gnomish")
    if character.goblin:
        known_languages.append("Goblin")
    if character.halfling:
        known_languages.append("Halfling")
    if character.infernal:
        known_languages.append("Infernal")
    if character.orc:
        known_languages.append("Orc")
    if character.primordial:
        known_languages.append("Primordial")
    if character.sylvan:
        known_languages.append("Sylvan")
    if character.undercommon:
        known_languages.append("Undercommon")
    return known_languages


def prof_bonus(requested_character):
    """
    This function returns a numerical value for the character's proficiency bonus based on
    the overall level of the character
    """
    if requested_character.char_lvl < 5:
        return 2
    elif requested_character.char_lvl < 9:
        return 3
    elif requested_character.char_lvl < 13:
        return 4
    elif requested_character.char_lvl < 16:
        return 5
    else:
        return 6


def ability_bonus(stat):
    """This function checks the characters ability stat and returns the corresponding bonus value"""
    if stat == 1:
        return -5
    elif stat < 4:
        return -4
    elif stat < 6:
        return -3
    elif stat < 8:
        return -2
    elif stat < 10:
        return -1
    elif stat < 12:
        return 0
    elif stat < 14:
        return 1
    elif stat < 16:
        return 2
    elif stat < 18:
        return 3
    elif stat < 20:
        return 4
    else:
        return 5


def generate_stat(num_stats):
    """
    This function returns a list of integers to be used as stats in accordance to the roll 4
    d6's and subtract the lowest value method of rolling stats.
    """
    stats = []
    for stat in range(num_stats):
        stat_numbers = [random.randint(1, 6) for x in range(4)]
        stat_numbers.sort(reverse=True)
        stat_numbers.pop()
        stats.append(sum(stat_numbers))
    return stats


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.jinja_env.globals.update(ability_bonus=ability_bonus, floor=floor, len=len, ceil=ceil, median=median)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ckeditor = CKEditor(app)
Bootstrap(app)

# --------------- Setup Login Manager -----------------

login_manager = LoginManager()
login_manager.init_app(app)

# --------------- Connect to database ------------------

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///campaign_manager.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ------------ Data stored in lists and dictionaries for use in routes --------------

api_endpoint = "https://www.dnd5eapi.co/api"

skills = ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History",
          "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception",
          "Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"]




all_languages = ['abyssal', 'celestial', 'common', 'deep_speech', 'draconic', 'dwarvish', 'elvish',
                 'giant', 'gnomish', 'goblin', 'halfling', 'infernal', 'orc',
                 'primordial', 'sylvan', 'undercommon']

# ---------------- Function to check if allowed file ---------------

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------- Database Tables --------------------

class Campaign(db.Model):
    __tablename__ = "campaign"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    subtitle = Column(String(500), nullable=False)
    campaign_card_img = Column(String, nullable=False)
    page_image = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    central_location = Column(String, nullable=False)
    central_location_img = Column(String, nullable=False)
    central_location_map = Column(String, nullable=False)
    region_summary = Column(Text, nullable=False)
    region_map = Column(String)
    faction_summary = Column(Text, nullable=False)
    regular_day = Column(String, nullable=False)
    regular_time = Column(String, nullable=False)
    dm_username = Column(String, nullable=False)
    dm_img = Column(String)

    # ------- Relationships --------
    characters = relationship("Character", back_populates="campaign")
    locations = relationship("Location", back_populates="campaign")
    factions = relationship("Faction", back_populates="campaign")
    players = relationship("Player", back_populates="campaign")  # !!! Change to Many to Many !!!
    npcs = relationship("NPC", back_populates="campaign")
    scheduled_sessions = relationship("ScheduledSession", back_populates="campaign")
    session_review = relationship("SessionReview", back_populates="campaign")
    house_rules = relationship("HouseRule", back_populates="campaign", uselist=False)


class Location(db.Model):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    location_name = Column(String(150))
    location_summary = Column(Text)
    location_img = Column(String)
    location_notes = Column(Text)
    npcs = relationship("NPC", back_populates="location")
    location_comments = relationship("LocationComments", back_populates="location")
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="locations")


class LocationComments(db.Model):
    __tablename__ = "location_comments"
    id = Column(Integer, primary_key=True)
    body = Column(Text)
    date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    location_id = Column(Integer, ForeignKey("location.id"))
    location = relationship("Location", back_populates="location_comments")
    player_id = Column(Integer, ForeignKey("players.id"))
    players = relationship("Player", back_populates="location_comments")


class Player(UserMixin, db.Model):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String, nullable=False)
    characters = relationship("Character", back_populates="player")
    session_review = relationship("SessionReview", back_populates="player")
    session_review_comments = relationship("SessionReviewComments")
    faction_comments = relationship("FactionComments", back_populates="player")
    location_comments = relationship("LocationComments")
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="players")  # !!! Change to Many to Many !!!


class NPC(db.Model):
    __tablename__ = "npc"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    race = Column(String)
    sex = Column(String)
    personality_trait_1 = Column(Text)
    personality_trait_2 = Column(Text)
    ideals = Column(Text)
    bonds = Column(Text)
    flaws = Column(Text)
    npc_image = Column(String, nullable=False)
    npc_token = Column(String, nullable=False)
    npc_description = Column(Text, nullable=False)
    npc_history = Column(Text, nullable=False)
    npc_notes = Column(Text, nullable=False)

    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="npcs")
    faction_id = Column(Integer, ForeignKey("faction.id"))
    faction = relationship("Faction", back_populates="npcs")
    location_id = Column(Integer, ForeignKey("location.id"))
    location = relationship("Location", back_populates="npcs")


class Faction(db.Model):
    __tablename__ = "faction"
    id = Column(Integer, primary_key=True)

    faction_name = Column(String(100), nullable=False, unique=True)
    faction_description = Column(Text)
    faction_img = Column(String)
    faction_notes = Column(Text)
    faction_motto = Column(String)

    faction_comments = relationship("FactionComments", back_populates="faction")
    npcs = relationship("NPC", back_populates="faction")
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="factions")


class FactionComments(db.Model):
    __tablename__ = "faction_comments"
    id = Column(Integer, primary_key=True)
    body = Column(Text)
    date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    player_id = Column(Integer, ForeignKey("players.id"))
    player = relationship("Player", back_populates="faction_comments")
    faction_id = Column(Integer, ForeignKey("faction.id"))
    faction = relationship("Faction", back_populates="faction_comments")


class SessionReview(db.Model):
    __tablename__ = "session_review"
    id = Column(Integer, primary_key=True)
    title = Column(String(150))
    subtitle = Column(String(300))
    body = Column(Text)
    date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    player_id = Column(Integer, ForeignKey("players.id"))
    player = relationship("Player", back_populates="session_review")
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="session_review")
    session_review_comments = relationship("SessionReviewComments", back_populates="session_review")


class SessionReviewComments(db.Model):
    __tablename__ = "session_review_comment"
    id = Column(Integer, primary_key=True)
    body = Column(Text)
    date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    player_id = Column(Integer, ForeignKey("players.id"))
    player = relationship("Player", back_populates="session_review_comments")
    session_review_id = Column(Integer, ForeignKey("session_review.id"))
    session_review = relationship("SessionReview", back_populates="session_review_comments")


class ScheduledSession(db.Model):
    __tablename__ = "scheduled_session"
    id = Column(Integer, primary_key=True)
    day = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    preview = Column(String(500))
    preview_img = Column(String)
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="scheduled_sessions")


class HouseRule(db.Model):
    __tablename__ = "house_rules"
    id = Column(Integer, primary_key=True)
    allowed_races = Column(Text)
    ability_scores_rules = Column(Text)
    pvp_rules = Column(Text)
    homebrew_rules = Column(Text)
    special_rules = Column(Text)
    allowed_sources = Column(Text)
    third_party_sources = Column(Text)
    dm_message = Column(Text)
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="house_rules")


class Character(db.Model):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)

    # ----------- Character Details -------------
    name = Column(String(100))
    sex = Column(String(50))
    char_img = Column(String(250))
    token_img = Column(String(250))
    char_lvl = Column(Integer)
    alignment = Column(String(50))
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="characters")
    player_id = Column(Integer, ForeignKey("players.id"))
    player = relationship("Player", back_populates="characters")

    # ------------- Character Race -----------------
    race = Column(String(50))
    subrace = Column(String(50))
    main_bonus_score = Column(String)
    sub_bonus_score = Column(String)
    size = Column(String)
    speed = Column(Integer)
    age = Column(Integer)

    # ------------- Ability Scores -----------------
    strength = Column(Integer, default=0)
    dexterity = Column(Integer, default=0)
    constitution = Column(Integer, default=0)
    wisdom = Column(Integer, default=0)
    intelligence = Column(Integer, default=0)
    charisma = Column(Integer, default=0)

    # -------------- Character Class ----------------
    class_main = Column(String(150))
    class_main_level = Column(Integer)
    class_main_subclass = Column(String)
    class_second = Column(String(150))
    class_second_level = Column(Integer)
    class_second_subclass = Column(String)
    hit_dice = Column(Integer)
    max_hit_points = Column(Integer)
    current_hit_points = Column(Integer)
    temp_hit_points = Column(Integer)
    armor_profs = Column(Text)
    weapon_profs = Column(Text)
    strength_save = Column(Boolean, default=False)
    dexterity_save = Column(Boolean, default=False)
    constitution_save = Column(Boolean, default=False)
    intelligence_save = Column(Boolean, default=False)
    wisdom_save = Column(Boolean, default=False)
    charisma_save = Column(Boolean, default=False)
    spellcaster = Column(Boolean)

    # ----------- Spellcasting -------------------
    # Depending on the character there will be another table for spell options!
    spell_ability = Column(String)  # All of these will be updated after a player changes the level of the character.
    spell_dc = Column(Integer)
    spell_attack_mod = Column(Integer)
    cantrips = Column(Integer)
    first_level_slots = Column(Integer)
    second_level_slots = Column(Integer)
    third_level_slots = Column(Integer)
    fourth_level_slots = Column(Integer)
    fifth_level_slots = Column(Integer)
    sixth_level_slots = Column(Integer)
    seventh_level_slots = Column(Integer)
    eighth_level_slots = Column(Integer)
    ninth_level_slots = Column(Integer)
    spells_known = relationship("CharacterKnownSpells")
    short_save_restore = Column(Boolean)

    # ----------- Skill Profs --------------------
    acrobatics = Column(Boolean, default=False)
    animal_handling = Column(Boolean, default=False)
    arcana = Column(Boolean, default=False)
    athletics = Column(Boolean, default=False)
    deception = Column(Boolean, default=False)
    history = Column(Boolean, default=False)
    insight = Column(Boolean, default=False)
    intimidation = Column(Boolean, default=False)
    investigation = Column(Boolean, default=False)
    medicine = Column(Boolean, default=False)
    nature = Column(Boolean, default=False)
    perception = Column(Boolean, default=False)
    performance = Column(Boolean, default=False)
    persuasion = Column(Boolean, default=False)
    religion = Column(Boolean, default=False)
    sleight_of_hand = Column(Boolean, default=False)
    stealth = Column(Boolean, default=False)
    survival = Column(Boolean, default=False)

    # ------------ Tool & language Proficiencies --------------
    alchemist_tools = Column(Boolean, default=False)
    calligrapher_tools = Column(Boolean, default=False)
    cartographer_tools = Column(Boolean, default=False)
    cooks_utensils = Column(Boolean, default=False)
    forgery_kit = Column(Boolean, default=False)
    herbalism_kit = Column(Boolean, default=False)
    leatherworker_tools = Column(Boolean, default=False)
    navigator_tools = Column(Boolean, default=False)
    poisoner_kit = Column(Boolean, default=False)
    smith_tools = Column(Boolean, default=False)
    tinker_tools = Column(Boolean, default=False)
    woodcarver_tools = Column(Boolean, default=False)
    brewer_tools = Column(Boolean, default=False)
    carpenter_tools = Column(Boolean, default=False)
    cobbler_tools = Column(Boolean, default=False)
    disguise_kit = Column(Boolean, default=False)
    glassblower_tools = Column(Boolean, default=False)
    jeweler_tools = Column(Boolean, default=False)
    mason_tools = Column(Boolean, default=False)
    painter_tools = Column(Boolean, default=False)
    thief_tools = Column(Boolean, default=False)
    weaver_tools = Column(Boolean, default=False)
    instruments = Column(Text)
    common = Column(Boolean, default=False)
    dwarvish = Column(Boolean, default=False)
    elvish = Column(Boolean, default=False)
    giant = Column(Boolean, default=False)
    gnomish = Column(Boolean, default=False)
    goblin = Column(Boolean, default=False)
    halfling = Column(Boolean, default=False)
    orc = Column(Boolean, default=False)
    abyssal = Column(Boolean, default=False)
    celestial = Column(Boolean, default=False)
    draconic = Column(Boolean, default=False)
    deep_speech = Column(Boolean, default=False)
    infernal = Column(Boolean, default=False)
    primordial = Column(Boolean, default=False)
    sylvan = Column(Boolean, default=False)
    undercommon = Column(Boolean, default=False)
    druidic = Column(Boolean, default=False)
    thieves_cant = Column(Boolean, default=False)

    # ------------ Character Background -----------------------
    background = Column(String(100))
    appearance_summary = Column(String(150))
    appearance_detailed = Column(Text)
    personality_trait_1 = Column(String)
    personality_trait_2 = Column(String)
    ideals = Column(String)
    bonds = Column(String)
    flaws = Column(String)
    height = Column(Integer)
    weight = Column(Integer)
    backstory = Column(Text)

    # -------------- Inventory --------------------------------
    cp = Column(Integer)
    sp = Column(Integer)
    ep = Column(Integer)
    gp = Column(Integer)
    pp = Column(Integer)
    weapons = relationship("Weapons")
    equipped_armor = Column(String)

    # ---------------- Bonuses ------------------------------

    init_bonus = Column(Integer, default=0)
    ac_bonus = Column(Integer, default=0)
    ac_override = Column(Boolean, default=False)
    ac_override_value = Column(Integer)

    # ------ Skllls, languages and senses --------

    darkvision = Column(Boolean, default=False)
    darkvision_distance = Column(Integer, default=0)
    blindsight = Column(Boolean, default=False)
    blindsight_distance = Column(Integer, default=0)
    tremorsense = Column(Boolean, default=False)
    tremorsense_distance = Column(Integer, default=0)
    truesight = Column(Boolean, default=False)
    truesight_distance = Column(Integer, default=0)

    # ---------------- Miscellaneous -----------------

    notes = Column(Text)
    actions = relationship("Actions")
    inventory = relationship("Items")


class CharacterKnownSpells(db.Model):
    __tablename__ = "character_known_spells"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    character_id = Column(Integer, ForeignKey("characters.id"))


class Actions(db.Model):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)  # Full, bonus, reaction
    damaging_action = Column(Boolean, default=True, nullable=False)  # True or False in table
    saving_action = Column(Boolean, default=False, nullable=False)
    saving_attribute = Column(String(50))  # List Options
    range = Column(String(50))
    target = Column(String(50))
    damage_roll_main = Column(String(50))
    damage_type_main = Column(String(50))
    damage_roll_secondary = Column(String(50))
    damage_type_secondary = Column(String(50))
    character_id = Column(Integer, ForeignKey("characters.id"))


class CharacterRaces(db.Model):
    __tablename__ = "character_races"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age_desc = Column(Text)
    size_desc = Column(Text)
    size = Column(String)
    speed = Column(Integer)
    subraces = relationship("Subraces", back_populates="race")
    racial_features = relationship("RacialFeatures", back_populates="race")


class RacialFeatures(db.Model):
    __tablename__ = "racial_features"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    feature_desc = Column(Text)
    race_id = Column(Integer, ForeignKey("character_races.id"))
    race = relationship("CharacterRaces", back_populates="racial_features")


class Subraces(db.Model):
    __tablename__ = "subraces"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    subrace_desc = Column(Text)
    race_id = Column(Integer, ForeignKey("character_races.id"))
    race = relationship("CharacterRaces", back_populates="subraces")


class CharacterClasses(db.Model):
    __tablename__ = "character_classes"
    id = Column(Integer, primary_key=True)
    class_name = Column(String)
    hit_dice = Column(Integer)

    light_armor = Column(Boolean, default=False)
    medium_armor = Column(Boolean, default=False)
    heavy_armor = Column(Boolean, default=False)
    shields = Column(Boolean, default=False)
    simple_weapons = Column(Boolean, default=False)
    martial_weapons = Column(Boolean, default=False)

    class_save_1 = Column(String, nullable=False)
    class_save_2 = Column(String, nullable=False)

    num_skills = Column(Integer)
    skill_desc = Column(String)
    num_tools = Column(Integer)
    tool_desc = Column(String)
    start_equipment = Column(Text)

    class_features = relationship("ClassFeatures")
    subclass_features = relationship("SubclassFeatures")


class ClassFeatures(db.Model):
    __tablename__ = "class_features"
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("character_classes.id"))  # Remember to have a class option in
    # the form that then fills the id out
    class_level = Column(Integer, nullable=False)
    title = Column(String)
    class_feature_desc = Column(Text)


class SubclassFeatures(db.Model):
    __tablename__ = "subclass_features"
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("character_classes.id"))  # Remember to have a class option in
    # the form that then fills the id out
    class_level = Column(Integer, nullable=False)
    optional = Column(Boolean)
    title = Column(String)
    subclass_feature_desc = Column(Text)


class Spells(db.Model):
    __tablename__ = "spells"
    id = Column(Integer, primary_key=True)
    classes = Column(String)
    name = Column(String)
    cast_time = Column(String)
    verbal = Column(Boolean)
    somatic = Column(Boolean)
    material = Column(Boolean)
    material_desc = Column(Text)
    concentration = Column(Boolean)
    attack_type = Column(String)
    range = Column(String)
    spell_desc = Column(Text)
    spell_level = Column(Integer)
    spell_school = Column(String)
    duration = Column(String)
    save_type = Column(String)
    ritual = Column(Boolean)
    primary_damage_lvl_1 = Column(String)
    primary_damage_lvl_2 = Column(String)
    primary_damage_lvl_3 = Column(String)
    primary_damage_lvl_4 = Column(String)
    primary_damage_lvl_5 = Column(String)
    primary_damage_lvl_6 = Column(String)
    primary_damage_lvl_7 = Column(String)
    primary_damage_lvl_8 = Column(String)
    primary_damage_lvl_9 = Column(String)
    cantrip_damage_die_1 = Column(String)
    cantrip_damage_die_2 = Column(String)
    cantrip_damage_die_3 = Column(String)
    cantrip_damage_die_4 = Column(String)


class Weapons(db.Model):
    __tablename__ = "weapons"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    value = Column(Integer)
    martial = Column(Boolean)
    simple = Column(Boolean)
    magic_weapon = Column(Boolean)
    reach_range = Column(String)
    hit_bonus = Column(Integer)
    primary_damage_die = Column(Integer)
    number_primary_die = Column(Integer)
    primary_damage_type = Column(String)
    secondary_damage_die = Column(Integer)
    number_secondary_die = Column(Integer)
    secondary_damage_type = Column(String)
    properties = Column(Text)
    character_id = Column(Integer, ForeignKey("characters.id"))


class Armor(db.Model):
    __tablename__ = "armor"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    armor_class = Column(Integer)
    dex_bonus = Column(Boolean)
    dex_bonus_limit = Column(Boolean)
    str_min = Column(Integer)
    stealth_disadvantage = Column(Boolean)
    value = Column(Integer)


class Items(db.Model):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    value = Column(Integer)
    item_desc = Column(Text)
    character_id = Column(Integer, ForeignKey("characters.id"))


# db.create_all()


# ------------------ Filling database with information from dnd5eapi.com ---------------

# spell_data = requests.get(api_endpoint + "/spells").json()
# for spell in spell_data['results']:
#     url = api_endpoint + "/spells/" + spell['index']
#     spell_details = requests.get(url).json()
#
#     # Get the classes that have access to the spell
#     classes = ""
#     class_list = spell_details['classes']
#     for character_class in class_list:
#         classes += character_class['name'] + ","
#
#     # Establish verbal, somatic and material boolean values
#
#     components = spell_details['components']
#     verbal = False
#     somatic = False
#     materials = False
#     if 'V' in components:
#         verbal = True
#     if 'S' in components:
#         somatic = True
#     if 'M' in components:
#         materials = True
#
#     # Establish material description string
#     material_desc = ""
#     try:
#         material_desc = spell_details['material']
#     except KeyError:
#         material_desc = "None"
#
#     # Establish attack_type
#     attack_type = ""
#     try:
#         attack_type = spell_details['attack_type']
#     except KeyError:
#         attack_type = "Save"
#
#     # Establish the damage die entries for each spell and level
#
#     primary_damage_lvl_1 = "None"
#     primary_damage_lvl_2 = "None"
#     primary_damage_lvl_3 = "None"
#     primary_damage_lvl_4 = "None"
#     primary_damage_lvl_5 = "None"
#     primary_damage_lvl_6 = "None"
#     primary_damage_lvl_7 = "None"
#     primary_damage_lvl_8 = "None"
#     primary_damage_lvl_9 = "None"
#     cantrip_damage_die_1 = "None"
#     cantrip_damage_die_2 = "None"
#     cantrip_damage_die_3 = "None"
#     cantrip_damage_die_4 = "None"
#
#     # print(spell_details)
#     primary_damage = ""
#     try:
#         if spell_details['level'] == 0:
#             level_damage = {}
#             try:
#                 damage_data = spell_details['damage']
#                 level_damage = damage_data['damage_at_character_level']
#             except KeyError:
#                 level_damage = spell_details['heal_at_slot_level']
#             print(f"{spell_details['name']} : {level_damage}")
#             damage_dies = ""
#             for level, damage in level_damage.items():
#                 damage_dies += f"'{level}:{damage}'"
#             getting_dies = damage_dies.split("'")
#             for dies in getting_dies:
#                 level = (dies.split(":")[0])
#                 if level == '1':
#                     cantrip_damage_die_1 = dies.split(":")[1]
#                 if level == '5':
#                     cantrip_damage_die_2 = dies.split(":")[1]
#                 if level == '11':
#                     cantrip_damage_die_3 = dies.split(":")[1]
#                 if level == '17':
#                     cantrip_damage_die_4 = dies.split(":")[1]
#         else:
#             level_damage = {}
#             try:
#                 damage_data = spell_details['damage']
#                 level_damage = damage_data['damage_at_slot_level']
#             except KeyError:
#                 level_damage = spell_details['heal_at_slot_level']
#             print(f"{spell_details['name']} : {level_damage}")
#             damage_dies = ""
#             for level, damage in level_damage.items():
#                 damage_dies += f"'{level}:{damage}'"
#             getting_dies = damage_dies.split("'")
#             for dies in getting_dies:
#                 level = (dies.split(":")[0])
#                 if level == '1':
#                     primary_damage_lvl_1 = dies.split(":")[1]
#                 if level == '2':
#                     primary_damage_lvl_2 = dies.split(":")[1]
#                 if level == '3':
#                     primary_damage_lvl_3 = dies.split(":")[1]
#                 if level == '4':
#                     primary_damage_lvl_4 = dies.split(":")[1]
#                 if level == '5':
#                     primary_damage_lvl_5 = dies.split(":")[1]
#                 if level == '6':
#                     primary_damage_lvl_6 = dies.split(":")[1]
#                 if level == '7':
#                     primary_damage_lvl_7 = dies.split(":")[1]
#                 if level == '8':
#                     primary_damage_lvl_8 = dies.split(":")[1]
#                 if level == '9':
#                     primary_damage_lvl_9 = dies.split(":")[1]
#     except KeyError:
#         pass
#
#     # Getting the DC Type if required
#
#     save_type = ""
#     try:
#         save_type = spell_details['dc']['dc_type']['index']
#     except KeyError:
#         save_type = "None"
#
#     # Changing Spell desc from list provided by api into a string
#
#     spell_desc = spell_details['desc']
#     full_desc = ""
#     for desc in spell_desc:
#         full_desc += desc
#
#     # Build the database entry
#     new_spell = Spells(
#         classes=classes,
#         name=spell_details['name'].lower(),
#         cast_time=spell_details['casting_time'],
#         verbal=verbal,
#         somatic=somatic,
#         material=materials,
#         material_desc=material_desc,
#         concentration=spell_details['concentration'],
#         attack_type=attack_type,
#         range=spell_details['range'],
#         spell_desc=full_desc,
#         spell_level=spell_details['level'],
#         spell_school=spell_details['school']['name'],
#         duration=spell_details['duration'],
#         ritual=spell_details['ritual'],
#         primary_damage_lvl_1=primary_damage_lvl_1,
#         primary_damage_lvl_2=primary_damage_lvl_2,
#         primary_damage_lvl_3=primary_damage_lvl_3,
#         primary_damage_lvl_4=primary_damage_lvl_4,
#         primary_damage_lvl_5=primary_damage_lvl_5,
#         primary_damage_lvl_6=primary_damage_lvl_6,
#         primary_damage_lvl_7=primary_damage_lvl_7,
#         primary_damage_lvl_8=primary_damage_lvl_8,
#         primary_damage_lvl_9=primary_damage_lvl_9,
#         cantrip_damage_die_1=cantrip_damage_die_1,
#         cantrip_damage_die_2=cantrip_damage_die_2,
#         cantrip_damage_die_3=cantrip_damage_die_3,
#         cantrip_damage_die_4=cantrip_damage_die_4,
#         save_type=save_type,
#     )
#     db.session.add(new_spell)
#     db.session.commit()


# Filling out the character race tables

# races = requests.get(api_endpoint + "/races")
# race_data = races.json()
# all_races = race_data['results']
#
# for race in all_races:
#     url = api_endpoint + "/races/" + race['index']
#     race_details = requests.get(url).json()
#     new_race = CharacterRaces(
#         name=race_details['name'],
#         age_desc=race_details['age'],
#         size=race_details['size'],
#         size_desc=race_details['size_description'],
#         speed=race_details['speed']
#     )
#     db.session.add(new_race)
#     db.session.commit()

#  Filling out the armor table

# armor = requests.get(api_endpoint + '/equipment-categories/armor')
# armor_data = armor.json()
# for armor in armor_data['equipment']:
#     url = 'https://www.dnd5eapi.co' + (armor['url'])
#     armor_details = requests.get(url).json()
#     try:
#         if armor_details['contents'] == []:
#             dex_limit = True
#             print(armor_details['name'])
#             try:
#                 if armor_details['armor_class']['max_bonus']:
#                     dex_limit = True
#             except KeyError:
#                 dex_limit = False
#             print(armor_details['name'])
#             new_armor = Armor(
#                 name=armor_details['name'],
#                 category=armor_details['armor_category'],
#                 armor_class=armor_details['armor_class']['base'],
#                 dex_bonus=armor_details['armor_class']['dex_bonus'],
#                 dex_bonus_limit=dex_limit,
#                 str_min=armor_details['str_minimum'],
#                 stealth_disadvantage=armor_details['stealth_disadvantage'],
#                 value=f"{armor_details['cost']['quantity']} {armor_details['cost']['unit']}",
#             )
#             db.session.add(new_armor)
#             db.session.commit()
#     except KeyError: # By searching for this KeyError we eliminate the magical items which have a contents key
#         pass

# ---------------------- Filling out Class Data Table ----------------------

# data = requests.get('https://www.dnd5eapi.co/api/classes/')
# all_data = data.json()
# for player_class in all_data['results']:
#     url = "https://www.dnd5eapi.co" + player_class['url']
#     class_data = requests.get(url).json() # Int
#     proficiencies = class_data['proficiencies']
#     light_armor = False
#     medium_armor = False
#     heavy_armor = False
#     shields = False
#     simple_weapons = False
#     martial_weapons = False
#     for proficiency in proficiencies:
#         if proficiency['index'] == "light-armor" or proficiency['index'] == "all-armor":
#             light_armor = True
#         if proficiency['index'] == "medium-armor" or proficiency['index'] == "all-armor":
#             medium_armor = True
#         if proficiency['index'] == "heavy-armor" or proficiency['index'] == "all-armor":
#             heavy_armor = True
#         if proficiency['index'] == "shields":
#             shields = True
#         if proficiency['index'] == "martial-weapons":
#             martial_weapons = True
#         if proficiency['index'] == "simple-weapons":
#             simple_weapons = True
#     saves = class_data['saving_throws']
#     save_1 = saves[0]['index']
#     save_2 = saves[1]['index']
#     num_tools = 0
#     tool_desc = ""
#     try:
#         num_tools = class_data['proficiency_choices'][1]['choose']
#         tool_desc = class_data['proficiency_choices'][1]['desc']
#     except IndexError:
#         num_tools = 0
#     new_class = CharacterClasses(
#         class_name=class_data['name'],
#         hit_dice=class_data['hit_die'],
#         light_armor=light_armor,
#         medium_armor=medium_armor,
#         heavy_armor=heavy_armor,
#         simple_weapons=simple_weapons,
#         martial_weapons=martial_weapons,
#         shields=shields,
#         class_save_1=save_1,
#         class_save_2=save_2,
#         num_skills=class_data['proficiency_choices'][0]['choose'],
#         skill_desc=class_data['proficiency_choices'][0]['desc'],
#         num_tools=num_tools,
#         tool_desc=tool_desc,
#     )
#     db.session.add(new_class)
#     db.session.commit()

# ---------------- Filling out Class Features Table ----------------

# data = requests.get('https://www.dnd5eapi.co/api/classes/')
# all_data = data.json()
# class_id = 0
# for player_class in all_data['results']:
#     class_id += 1
#     url = "https://www.dnd5eapi.co" + player_class['url'] + "/features"
#     class_data = requests.get(url).json()
#     features = class_data['results']
#     for feature in features:
#         feature_url = api_endpoint + "/features/" + feature['index']
#         feature_data = requests.get(feature_url).json()
#         title = ""
#         try:
#             if feature_data['subclass']:
#                 title = "Subclass Feature"
#         except KeyError:
#             title = feature_data['name']
#         new_feature = ClassFeatures(
#             class_id=class_id,
#             title=title,
#             class_level=feature_data['level'],
#             class_feature_desc=feature_data['desc'][0]
#         )
#         db.session.add(new_feature)
#         db.session.commit()


# ------------ Filling out the Character Race Features Table --------------
#
# races = requests.get("https://www.dnd5eapi.co/api/races")
# race_data = races.json()
# all_races = race_data['results']
# race_id = 0
#
# for race in all_races:
#     race_id += 1
#     url = "https://www.dnd5eapi.co/api/races/" + race['index']
#     race_details = requests.get(url).json()
#     print(race_details['index'])
#     all_traits = race_details['traits']
#     for trait in all_traits:
#         trait_details = requests.get("https://www.dnd5eapi.co" + trait['url']).json()
#         trait_desc_full = ""
#         for trait_desc in trait_details['desc']:
#             trait_desc_full += trait_desc
#         new_race_feature = RacialFeatures(
#             title=trait_details['name'],
#             feature_desc=trait_desc_full,
#             race_id=race_id,
#         )
#         db.session.add(new_race_feature)
#         db.session.commit()


# --------------------- Wrapper Functions -----------------------

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


@login_manager.user_loader
def load_player(player_id):
    return Player.query.get(player_id)


# --------- Provide the list of all current campaigns for the footer. ------------
all_campaigns = db.session.query(Campaign).all()


# ------------ Functions for use in routes involving database queries ------------
def get_spell_list(character_class, spell_level):
    """
    This function takes a character's class and inputted spell level to filter the database for matching
    spells and return their names as a list.
    """
    list_of_spells = []
    all_spells = Spells.query.filter_by(spell_level=spell_level).all()
    for spell in all_spells:
        if character_class in spell.classes.split(','):
            list_of_spells.append(spell.name)
    return list_of_spells


# --------- Testing Route - For experimentation without editing established routes first ---------

@app.route("/test/<int:character_id>",methods=["GET", "POST"])
def test_upload(character_id):
    form = forms.UploadImageForm()
    requested_character = Character.query.get(character_id)
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash("No file part")
            return redirect(url_for("home"))
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            flash("No selected file")
            return redirect(url_for("home"))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            requested_character.token_img = "static/uploads/" + filename
            db.session.commit()
            return redirect(url_for("home"))
    return render_template('edit-skills-form.html', form=form, character=requested_character, all_campaigns=all_campaigns)


@app.route("/test-skill")
def test_skills():
    form = forms.EditSkillProfs()
    if form.validate_on_submit():
        print("Okay")
        return redirect(url_for('home'))
    return render_template('edit-skills-form.html', form=form)


# ------------------ Home Related Routes --------------------------

@app.route("/")
def home():
    return render_template('index.html', all_campaigns=all_campaigns,
                           logged_in=current_user.is_authenticated)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    image = 'https://img.freepik.com/free-photo/top-view-beautiful-rpg-still-life-items_23-2149282425.jpg?w=1800&t=st=1668923891~exp=1668924491~hmac=1a144e548bff837473f7442b48915694068909663936c7cc36c77c7dc4166142'
    title = 'Log In'
    subtitle = "Welcome back adventurer"
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        player = Player.query.filter_by(username=username).first()
        if not player:
            flash("Username or password incorrect")
            return redirect(url_for('login'))
        elif not check_password_hash(player.password, password):
            flash("Username of password incorrect")
            return redirect(url_for('login'))
        if check_password_hash(player.password, password):
            login_user(player)
            return redirect(url_for('home'))
    return render_template("forms.html", form=form, logged_in=current_user.is_authenticated,
                           all_campaigns=all_campaigns, image=image, title=title, subtitle=subtitle)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/contact-us', methods=["GET", "POST"])
def contact_page():
    form = forms.ContactMe()
    subtitle = 'If you wish to join a campaign, run your own game under the D.D.Inc banner, or have any questions for us here at D.D.Inc, contact us.'
    image = "https://img.freepik.com/free-photo/still-life-objects-with-role-playing-game-sheet_23-2149352342.jpg?w=1800&t=st=1668816379~exp=1668816979~hmac=392e7123a6ce3251966987d3f5463a0704a9f98e1987b90645ffe93dde9ce361"
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        file_name = f"contact_messages/{form.name.data} - {datetime.datetime.now().strftime('%d-%m-%Y - %H-%M-%S')}.txt"
        with open(file_name, 'w') as file:
            file.write(f"Contact Message\n\nname: {name} - email: {email}\nsubject: {subject}\n{message}")
        return redirect(url_for('home'))
    return render_template('forms.html', form=form, all_campaigns=all_campaigns,
                           logged_in=current_user.is_authenticated, image=image,
                           title='Cast Message', subtitle=subtitle, classes="contact-form")

# --------------------- Campaign related routes ------------------------

@app.route("/campaigns")
def campaigns():
    return render_template('campaigns.html', all_campaigns=all_campaigns,
                           logged_in=current_user.is_authenticated)


@app.route("/campaign/<story_id>", methods=["GET", "POST"])
def campaign_page(story_id):
    requested_campaign = Campaign.query.get(story_id)
    if current_user.is_authenticated:
        requested_character = current_user.characters
    else:
        requested_character = None
    return render_template("campaign_page.html", campaign=requested_campaign,
                           characters=requested_character, logged_in=current_user.is_authenticated,
                           campaign_id=int(story_id), all_campaigns=all_campaigns)


@app.route('/rules/<campaign_id>', methods=["GET", "POST"])
def rules_page(campaign_id):
    requested_campaign = Campaign.query.get(campaign_id)
    return render_template("rules.html", campaign=requested_campaign, all_campaigns=all_campaigns)


@app.route('/<campaign_id>/session-review/<review_id>', methods=["GET", "POST"])
def session_review_page(campaign_id, review_id):
    requested_campaign = Campaign.query.get(campaign_id)
    requested_review = SessionReview.query.get(review_id)
    return render_template("session_review.html", campaign=requested_campaign, review=requested_review,
                           all_campaigns=all_campaigns, logged_in=current_user.is_authenticated)


@app.route('/schedule')
def schedule_page():
    return render_template('schedule.html', all_campaigns=all_campaigns, logged_in=current_user.is_authenticated)


@app.route("/faction/<int:faction_id>")
def faction_page(faction_id):
    requested_faction = Faction.query.get(faction_id)
    return render_template('faction_page.html', all_campaigns=all_campaigns,
                           logged_in=current_user.is_authenticated, faction=requested_faction)


@app.route("/location/<int:location_id>")
def location_page(location_id):
    requested_location = Location.query.get(location_id)
    return render_template('location_page.html', all_campaigns=all_campaigns,
                           logged_in=current_user.is_authenticated, location=requested_location)


@app.route("/npc/<int:npc_id>")
def npc_page(npc_id):
    requested_npc = NPC.query.get(npc_id)
    return render_template('npc_page.html', all_campaigns=all_campaigns,
                           logged_in=current_user.is_authenticated, npc=requested_npc)


# ----------------- Character Related Routes ------------------------

@app.route("/character-hub", methods=["GET", "POST"])
def character_hub():
    if not current_user.is_authenticated:
        flash("Please login or register to create characters")
        return redirect(url_for('login'))
    return render_template("character-hub.html", logged_in=current_user.is_authenticated, all_campaigns=all_campaigns)


@app.route('/character/<character_id>', methods=["GET", "POST"])
def character_page(character_id):
    requested_character = Character.query.get(character_id)
    prof = prof_bonus(requested_character)
    ac = 10
    dex_bonus = True
    dex_bonus_limit = False
    try:
        character_armor = Armor.query.filter_by(name=requested_character.equipped_armor).first()
        ac = character_armor.armor_class
        dex_bonus = character_armor.dex_bonus
        dex_bonus_limit = character_armor.dex_bonus_limit
    except AttributeError:
        print("Not Ok")
    known_languages = character_languages(requested_character)
    prof_tools = character_tools(requested_character)
    return render_template("character-page.html", character=requested_character,
                           all_campaigns=all_campaigns, prof=prof, logged_in=current_user.is_authenticated,
                           ac=ac, dex_bonus=dex_bonus, dex_bonus_limit=dex_bonus_limit,
                           known_languages=known_languages, prof_tools=prof_tools)


# ------------------------ Form Routes for DB -----------------------------


@app.route("/register", methods=["GET", "POST"])
def register_player():
    form = forms.CreateNewPlayerForm()
    image = 'https://img.freepik.com/free-photo/top-view-beautiful-rpg-still-life-items_23-2149282425.jpg?w=1800&t=st=1668923891~exp=1668924491~hmac=1a144e548bff837473f7442b48915694068909663936c7cc36c77c7dc4166142'
    title = "Register"
    subtitle = "Welcome to Dungeon Delvers Incorportated"
    if form.validate_on_submit():
        if Player.query.filter_by(username=form.username.data).first():
            flash("You have already signed up with that username. Please login")
            return redirect(url_for('login'))

        new_player = Player()
        new_player.username = request.form["username"]
        new_player.password = generate_password_hash(
            password=request.form["password"],
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_player.email = request.form["email"]
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("forms.html", form=form,
                           image=image, title=title, subtitle=subtitle, all_campaigns=all_campaigns)


@app.route("/location/edit-notes/<int:location_id>", methods=["GET", "POST"])
def edit_location_notes(location_id):
    requested_location = Location.query.get(location_id)
    form = forms.EditNotes(
        notes=requested_location.location_notes
    )
    if form.validate_on_submit():
        requested_location.location_notes = form.notes.data
        db.session.commit()
        return redirect(url_for("location_page", location_id=location_id))
    return render_template('forms.html', all_campaigns=all_campaigns,
                           logged_in=current_user.is_authenticated, location=requested_location, form=form)


@app.route("/location/add-comment/<int:location_id>", methods=["GET", "POST"])
def add_location_comment(location_id):
    requested_location = Location.query.get(location_id)
    form = forms.AddComment()
    if form.validate_on_submit():
        new_comment = LocationComments(
            body=form.body.data,
            date=datetime.datetime.utcnow(),
            player_id=current_user.id,
            location_id=requested_location.id
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("location_page", location_id=location_id))
    return render_template("forms.html", all_campaigns=all_campaigns,
                           logged_in=current_user.is_authenticated, location=requested_location, form=form)


@app.route("/faction/edit-notes/<int:faction_id>", methods=["GET", "POST"])
def edit_faction_notes(faction_id):
    requested_faction = Faction.query.get(faction_id)
    form = forms.EditNotes(
        notes=requested_faction.faction_notes
    )
    if form.validate_on_submit():
        requested_faction.faction_notes = form.notes.data
        db.session.commit()
        return redirect(url_for("faction_page", faction_id=faction_id))
    return render_template('forms.html', all_campaigns=all_campaigns,
                           logged_in=current_user.is_authenticated, faction=requested_faction, form=form)


@app.route("/faction/add-comment/<int:faction_id>", methods=["GET", "POST"])
def add_faction_comment(faction_id):
    requested_faction = Faction.query.get(faction_id)
    form = forms.AddComment()
    if form.validate_on_submit():
        new_comment = FactionComments(
            body=form.body.data,
            date=datetime.datetime.utcnow(),
            player_id=current_user.id,
            faction_id=requested_faction.id
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("faction_page", faction_id=faction_id))
    return render_template("forms.html", all_campaigns=all_campaigns,
                           logged_in=current_user.is_authenticated, faction=requested_faction, form=form)



@app.route("/add-new-character", methods=["GET", "POST"])
@login_required
def add_new_character():
    stats = generate_stat(6)
    form = forms.CreateNewCharacter()
    if form.validate_on_submit():
        token_img = ""
        if 'file' not in request.files:
            flash("No Token Provided")
            return redirect(url_for("add_new_character"))
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            flash("No selected token file")
            return redirect(url_for("home"))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            token_img = "static/uploads/" + filename
        spellcaster = False
        new_character = Character(
            name=form.name.data,
            token_img=token_img,
            sex=form.sex.data,
            alignment=form.alignment.data,
            char_lvl=form.char_lvl.data,
            player_id=current_user.id,

            race=form.race.data,
            subrace=form.subrace.data,
            main_bonus_score=form.main_bonus_score.data,
            sub_bonus_score=form.sub_bonus_score.data,
            age=form.age.data,

            class_main=form.class_main.data,
            class_main_level=form.class_main_level.data,

            strength=form.strength.data,
            dexterity=form.dexterity.data,
            constitution=form.constitution.data,
            wisdom=form.wisdom.data,
            intelligence=form.intelligence.data,
            charisma=form.charisma.data,

            background=form.background.data,
            personality_trait_1=form.personality_trait_1.data,
            personality_trait_2=form.personality_trait_2.data,
            ideals=form.ideals.data,
            bonds=form.bonds.data,
            flaws=form.flaws.data,
            backstory=form.backstory.data,

            appearance_summary=form.appearance_summary.data,
            appearance_detailed=form.appearance_detailed.data,
            height=form.height.data,
            weight=form.weight.data,

            cp=0,
            sp=0,
            ep=0,
            gp=0,
            pp=0,

            equipped_armor="",
        )
        if form.campaign.data == "GoS":
            new_character.campaign_id = 1
        new_character.hit_dice = class_hit_die[form.class_main.data.lower()]
        if "str" in class_saves[form.class_main.data.lower()]:
            new_character.strength_save = True
        if "dex" in class_saves[form.class_main.data.lower()]:
            new_character.dexterity_save = True
        if "con" in class_saves[form.class_main.data.lower()]:
            new_character.constitution_save = True
        if "int" in class_saves[form.class_main.data.lower()]:
            new_character.intelligence_save = True
        if "wis" in class_saves[form.class_main.data.lower()]:
            new_character.wisdom_save = True
        if "cha" in class_saves[form.class_main.data.lower()]:
            new_character.charisma_save = True
        if form.class_main == "Bard" or "Cleric" or "Druid" or "Sorcerer" or "Warlock" or "Wizard":
            new_character.spellcaster = True
            spellcaster = True
        db.session.add(new_character)
        db.session.commit()
        requested_character = Character.query.filter_by(name=new_character.name).first()
        character_id = requested_character.id
        return redirect(url_for('home'))
    return render_template("create_character_page.html", form=form, logged_in=current_user.is_authenticated,
                           stats=stats, all_campaigns=all_campaigns)


@app.route("/character-spellcasting/<int:character_id>", methods=["GET", "POST"])
def character_spellcasting(character_id):
    requested_character = Character.query.get(character_id)
    character_class = requested_character.class_main
    available_spells = []
    all_1st_level_spells = Spells.query.filter_by(spell_level=1).all()
    all_cantrips = Spells.query.filter_by(spell_level=0).all()
    for spell in all_1st_level_spells:
        class_list = spell.classes.split(",")

        # if character_class in spell.classes.split(","):
        #     available_spells.append(spell.name)
    print(available_spells)
    print(all_cantrips)
    available_spells = []
    form = forms.SpellSelection(available_spells)
    return render_template('forms.html', form=form, all_campaigns=all_campaigns)


@app.route("/new-location", methods=["GET", "POST"])
@admin_only
def add_new_location():
    form = forms.CreateLocationForm()
    if form.validate_on_submit():
        new_location = Location(
            location_name=form.location_name.data,
            location_summary=form.location_summary.data,
            location_img=form.location_img.data,
            location_notes=form.location_notes.data,
        )
        if form.campaign.data == "GoS":
            new_location.campaign_id = 1
        if form.campaign.data == "CoS":
            new_location.campaign_id = 2
        if form.campaign.data == "LotST":
            new_location.campaign_id = 3
        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("forms.html", form=form, logged_in=current_user.is_authenticated, all_campaigns=all_campaigns)


@app.route("/edit-location/<int:location_id>", methods=["GET", "POST"])
@admin_only
def edit_location(location_id):
    form = forms.CreateLocationForm()
    selected_location = Location.query.get(location_id)
    if form.validate_on_submit():
        print("Ok")
        selected_location.location_name = form.location_name.data
        selected_location.location_summary = form.location_summary.data
        selected_location.location_img = form.location_img.data
        selected_location.location_notes = form.location_notes.data
        db.session.commit()
        return redirect(url_for('home'))
    print("Not Ok")
    return render_template("forms.html", form=form, logged_in=current_user.is_authenticated, all_campaigns=all_campaigns)


@app.route("/add-npc", methods=["GET", "POST"])
@admin_only
def add_new_npc():
    all_locations = {}
    all_location_data = Location.query.all()
    for location in all_location_data:
        all_locations[location.location_name] = location.id
    all_factions = {}
    all_faction_data = Faction.query.all()
    for faction in all_faction_data:
        all_factions[faction.faction_name] = faction.id
    form = forms.NPCForm()
    form.location.choices = list(all_locations.keys())
    form.faction.choices = list(all_factions.keys())
    if form.validate_on_submit():
        new_npc = NPC(
            name=form.name.data,
            race=form.race.data,
            npc_image=form.npc_image.data,
            npc_description=form.npc_description.data,
            npc_history=form.npc_history.data,
            npc_notes=form.npc_notes.data,
            sex=form.sex.data,
            npc_token=form.npc_token.data,
            personality_trait_1=form.personality_trait_1.data,
            personality_trait_2=form.personality_trait_2.data,
            ideals=form.ideals.data,
            bonds=form.bonds.data,
            flaws=form.flaws.data,
        )
        new_npc.faction_id = all_factions[form.faction.data]
        new_npc.location_id = all_locations[form.location.data]
        if form.campaign.data == "GoS":
            new_npc.campaign_id = 1
        if form.campaign.data == "CoS":
            new_npc.campaign_id = 2
        if form.campaign.data == "LotST":
            new_npc.campaign_id = 3
        db.session.add(new_npc)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("forms.html", form=form, logged_in=current_user.is_authenticated, all_campaigns=all_campaigns)


@app.route("/new-campaign", methods=["GET", "POST"])
@admin_only
def add_new_campaign():
    form = forms.CreateCampaignForm()
    if form.validate_on_submit():
        new_campaign = Campaign(
            title=form.title.data,
            subtitle=form.subtitle.data,
            description=form.description.data,
            campaign_card_img=form.campaign_card_img.data,
            page_image=form.page_image.data,
            central_location=form.central_location.data,
            central_location_img=form.central_location_img.data,
            central_location_map=form.central_location_map.data,
            region_summary=form.region_summary.data,
            region_map=form.region_map.data,
            faction_summary=form.faction_summary.data,
            regular_day=form.regular_day.data,
            regular_time=form.regular_time.data,
            dm_username=form.dm_username.data,
        )
        # new_campaign.dm_img = request.files[form.dm_img.name] !! Need to finish this !!
        db.session.add(new_campaign)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("forms.html", form=form,
                           logged_in=current_user.is_authenticated, all_campaigns=all_campaigns)


@app.route("/new-faction", methods=["GET", "POST"])
@admin_only
def add_new_faction():
    form = forms.CreateFactionForm()
    if form.validate_on_submit():
        new_faction = Faction(
            faction_name=form.faction_name.data,
            faction_description=form.faction_description.data,
            faction_img=form.faction_image.data
        )
        if form.campaign.data == "GoS":
            new_faction.campaign_id = 1
        if form.campaign.data == "CoS":
            new_faction.campaign_id = 2
        if form.campaign.data == "LotST":
            new_faction.campaign_id = 3
        db.session.add(new_faction)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("forms.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/<campaign_id>/add-review", methods=["GET", "POST"])
@admin_only
def add_review(campaign_id):
    form = forms.SessionReviewForm()
    if form.validate_on_submit():
        new_review = SessionReview(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            date=date.today().strftime("%B %d, %Y")
        )
        new_review.player_id = current_user.id
        new_review.campaign_id = campaign_id
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for("campaign_page", story_id=campaign_id))
    return render_template("forms.html", form=form, logged_in=current_user.is_authenticated, all_campaigns=all_campaigns)


# ----------------- Character Sheet Edit Routes --------------------

@app.route("/character/<int:character_id>/edit-core-details", methods=["GET", "POST"])
def edit_core_character_details(character_id):
    requested_character = Character.query.get(character_id)
    title = "Edit Core Character Details"
    form = forms.EditNameRaceClass()
    if form.validate_on_submit():
        requested_character.name = form.name.data
        requested_character.race = form.race.data
        requested_character.subrace = form.subrace.data
        requested_character.class_main = form.class_main.data
        requested_character.class_second = form.class_second.data
        requested_character.class_main_level = form.class_main_level.data
        requested_character.class_second_level = form.class_second_level.data
        db.session.commit()
        return redirect(url_for('character_page', character_id=character_id))
    return render_template('edit_core_details.html', form=form,
                           character=requested_character, all_campaigns=all_campaigns, title=title)


@app.route("/character/<int:character_id>/edit-background", methods=["GET", "POST"])
def edit_background(character_id):
    requested_character = Character.query.get(character_id)
    title = "Edit Character Background"
    form = forms.EditBackground()
    if form.validate_on_submit():
        requested_character.background = form.background.data
        requested_character.alignment = form.alignment.data
        requested_character.appearance_summary = form.appearance_summary.data
        db.session.commit()
        return redirect(url_for('character_page', character_id=character_id))
    return render_template('edit-background.html', form=form,
                           character=requested_character, all_campaigns=all_campaigns, title=title)


@app.route("/character/<int:character_id>/edit-ability-scores", methods=["GET", "POST"])
def edit_ability_scores(character_id):
    requested_character = Character.query.get(character_id)
    title = "Edit Character Ability Scores"
    form = forms.EditAbilityScores()
    if form.validate_on_submit():
        requested_character.strength = form.strength.data
        requested_character.dexterity = form.dexterity.data
        requested_character.constitution = form.constitution.data
        requested_character.wisdom = form.wisdom.data
        requested_character.intelligence = form.intelligence.data
        requested_character.charisma = form.charisma.data
        db.session.commit()
        return redirect(url_for('character_page', character_id=character_id))
    return render_template('edit-ability-scores.html', form=form,
                           character=requested_character, all_campaigns=all_campaigns, title=title)


@app.route("/character/<int:character_id>/edit-personality", methods=["GET", "POST"])
def edit_personality(character_id):
    requested_character = Character.query.get(character_id)
    title = "Edit Character Personality"
    form = forms.EditPersonality()
    if form.validate_on_submit():
        requested_character.personality_trait_1 = form.personality_trait_1.data
        requested_character.personality_trait_2 = form.personality_trait_2.data
        requested_character.ideals = form.ideals.data
        requested_character.bonds = form.bonds.data
        requested_character.flaws = form.flaws.data
        db.session.commit()
        return redirect(url_for('character_page', character_id=character_id))
    return render_template('edit-personality.html', form=form, character=requested_character,
                           all_campaigns=all_campaigns, title=title)


@app.route("/character/<int:character_id>/edit-character-skill-profs", methods=["GET", "POST"])
def edit_skill_profs(character_id):
    requested_character = Character.query.get(character_id)
    title = "Select your skill proficiencies"
    form = forms.EditSkillProfs()
    if form.validate_on_submit():
        data = form.skills.data
        if "Acrobatics" in data:
            requested_character.acrobatics = True
        else:
            requested_character.acrobatics = False
        if "Animal Handling" in data:
            requested_character.animal_handling = True
        else:
            requested_character.animal_handling = False
        if "Arcana" in data:
            requested_character.arcana = True
        else:
            requested_character.arcana = False
        if "Athletics" in data:
            requested_character.athletics = True
        else:
            requested_character.athletics = False
        if "Deception" in data:
            requested_character.deception = True
        else:
            requested_character.deception = False
        if "History" in data:
            requested_character.history = True
        else:
            requested_character.history = False
        if "Insight" in data:
            requested_character.insight = True
        else:
            requested_character.insight = False
        if "Intimidation" in data:
            requested_character.intimidation = True
        else:
            requested_character.intimidation = False
        if "Investigation" in data:
            requested_character.investigation = True
        else:
            requested_character.investigation = False
        if "Medicine" in data:
            requested_character.medicine = True
        else:
            requested_character.medicine = False
        if "Nature" in data:
            requested_character.nature = True
        else:
            requested_character.nature = False
        if "Perception" in data:
            requested_character.perception = True
        else:
            requested_character.perception = False
        if "Performance" in data:
            requested_character.performance = True
        else:
            requested_character.performance = False
        if "Persuasion" in data:
            requested_character.persuasion = True
        else:
            requested_character.persuasion = False
        if "Religion" in data:
            requested_character.religion = True
        else:
            requested_character.religion = False
        if "Sleight of Hand" in data:
            requested_character.sleight_of_hand = True
        else:
            requested_character.sleight_of_hand = False
        if "Stealth" in data:
            requested_character.stealth = True
        else:
            requested_character.stealth = False
        if "Survival" in data:
            requested_character.survival = True
        else:
            requested_character.survival = False
        db.session.commit()
        return redirect(url_for('character_page', character_id=character_id))
    return render_template('edit-skills-form.html', form=form, character=requested_character,
                           all_campaigns=all_campaigns, title=title)


@app.route("/character/<int:character_id>/edit-stats-and-senses", methods=["GET", "POST"])
def edit_stats_senses(character_id):
    requested_character = Character.query.get(character_id)
    title = "Edit Character Hit Points, Senses, Tools and Languages"
    form = forms.EditStatsSenses()
    if form.validate_on_submit():
        requested_character.current_hit_points = form.current_hit_points.data
        requested_character.max_hit_points = form.max_hit_points.data
        requested_character.temp_hit_points = form.temp_hit_points.data
        if form.darkvision == "Yes":
            requested_character.darkvision = True
        else:
            requested_character.darkvision = False
        requested_character.darkvision_range = form.darkvision_range.data
        if form.blindsight == "Yes":
            requested_character.blindsight = True
        else:
            requested_character.blindsight = False
        requested_character.blindsight_range = form.blindsight_range.data
        if form.truesight == "Yes":
            requested_character.truesight = True
        else:
            requested_character.truesight = False
        requested_character.truesight_range = form.truesight_range.data
        first_tool_data = form.first_half_tools.data
        second_tool_data = form.second_half_tools.data
        first_languages = form.first_half_languages.data
        second_languages = form.second_half_languages.data
        # Check for skill Booleans and apply to database
        if "Alchemist's Supplies" in first_tool_data:
            requested_character.alchemist_tools = True
        else:
            requested_character.alchemist_tools = False
        if "Brewer's Supplies" in first_tool_data:
            requested_character.brewer_tools = True
        else:
            requested_character.brewer_tools = False
        if "Calligrapher's Supplies" in first_tool_data:
            requested_character.calligrapher_tools = True
        else:
            requested_character.calligrapher_tools = False
        if "Carpenter's Tools" in first_tool_data:
            requested_character.carpenter_tools = True
        else:
            requested_character.carpenter_tools = False
        if "Cartographer's Tools" in first_tool_data:
            requested_character.cartographer_tools = True
        else:
            requested_character.cartographer_tools = False
        if "Cobbler's Tools" in first_tool_data:
            requested_character.cobbler_tools = True
        else:
            requested_character.cobbler_tools = False
        if "Cook's Utensils" in first_tool_data:
            requested_character.cooks_utensils = True
        else:
            requested_character.cooks_utensils = False
        if "Glassblower's Tools" in first_tool_data:
            requested_character.glassblower_tools = True
        else:
            requested_character.glassblower_tools = False
        if "Jeweler's Tools" in first_tool_data:
            requested_character.jeweler_tools = True
        else:
            requested_character.jeweler_tools = False
        if "Leatherworker's Tools" in first_tool_data:
            requested_character.leatherworker_tools = True
        else:
            requested_character.leatherworker_tools = False
        if "Mason's Tools" in first_tool_data:
            requested_character.mason_tools = True
        else:
            requested_character.mason_tools = False
        if "Painter's Supplies" in second_tool_data:
            requested_character.painter_tools = True
        else:
            requested_character.painter_tools = False
        if "Smith's Tools" in second_tool_data:
            requested_character.smith_tools = True
        else:
            requested_character.smith_tools = False
        if "Tinker's Tools" in second_tool_data:
            requested_character.tinker_tools = True
        else:
            requested_character.tinker_tools = False
        if "Weaver's Tools" in second_tool_data:
            requested_character.weaver_tools = True
        else:
            requested_character.weaver_tools = False
        if "Woodcarver's Tools" in second_tool_data:
            requested_character.woodcarver_tools = True
        else:
            requested_character.woodcarver_tools = False
        if "Navigator's Tools" in second_tool_data:
            requested_character.navigator_tools = True
        else:
            requested_character.navigator_tools = False
        if "Thieves' Tools" in second_tool_data:
            requested_character.thief_tools = True
        else:
            requested_character.thief_tools = False
        if "Forgery Kit" in second_tool_data:
            requested_character.forgery_kit = True
        else:
            requested_character.forgery_kit = False
        if "Poisoner Kit" in second_tool_data:
            requested_character.poisoner_kit = True
        else:
            requested_character.poisoner_kit = False
        if "Disguise Kit" in second_tool_data:
            requested_character.disguise_kit = True
        else:
            requested_character.disguise_kit = False
        # Check for language Boolean Values and apply to database
        if "Abyssal" in first_languages:
            requested_character.abyssal = True
        else:
            requested_character.abyssal = False
        if "Celestial" in first_languages:
            requested_character.celestial = True
        else:
            requested_character.celestial = False
        if "Common" in first_languages:
            requested_character.common = True
        else:
            requested_character.common = False
        if "Deep Speech" in first_languages:
            requested_character.deep_speech = True
        else:
            requested_character.deep_speech = False
        if "Draconic" in first_languages:
            requested_character.draconic = True
        else:
            requested_character.draconic = False
        if "Dwarvish" in first_languages:
            requested_character.dwarvish = True
        else:
            requested_character.dwarvish = False
        if "Elvish" in first_languages:
            requested_character.elvish = True
        else:
            requested_character.elvish = False
        if "Giant" in first_languages:
            requested_character.giant = True
        else:
            requested_character.giant = False
        if "Gnomish" in second_languages:
            requested_character.gnomish = True
        else:
            requested_character.gnomish = False
        if "Goblin" in second_languages:
            requested_character.goblin = True
        else:
            requested_character.goblin = False
        if "Halfling" in second_languages:
            requested_character.halfling = True
        else:
            requested_character.halfling = False
        if "Infernal" in second_languages:
            requested_character.infernal = True
        else:
            requested_character.infernal = False
        if "Orcish" in second_languages:
            requested_character.orc = True
        else:
            requested_character.orc = False
        if "Primordial" in second_languages:
            requested_character.primordial = True
        else:
            requested_character.primordial = False
        if "Sylvan" in second_languages:
            requested_character.sylvan = True
        else:
            requested_character.sylvan = False
        if "Undercommon" in second_languages:
            requested_character.undercommon = True
        else:
            requested_character.undercommon = False
        db.session.commit()
        return redirect(url_for('character_page', character_id=character_id))
    return render_template('edit-stats-and-senses.html', form=form,
                           all_campaigns=all_campaigns, character=requested_character, title=title)


# ------------ Spell Selection Form -----------------


@app.route("/character/<int:character_id>/spell-selection", methods=["POST", "GET"])
def character_spell_selection(character_id):
    requested_character = Character.query.get(character_id)
    cantrips = []
    first_level_spells = []
    second_level_spells = []
    third_level_spells = []
    fourth_level_spells = []
    fifth_level_spells = []
    sixth_level_spells = []
    seventh_level_spells = []
    eighth_level_spells = []
    ninth_level_spells = []
    if requested_character.cantrips:
        cantrips = get_spell_list(requested_character.class_main, 0)
    if requested_character.first_level_slots:
        first_level_spells = get_spell_list(requested_character.class_main, 1)
    if requested_character.second_level_slots:
        second_level_spells = get_spell_list(requested_character.class_main, 2)
    if requested_character.third_level_slots:
        third_level_spells = get_spell_list(requested_character.class_main, 3)
    if requested_character.fourth_level_slots:
        fourth_level_spells = get_spell_list(requested_character.class_main, 4)
    if requested_character.fifth_level_slots:
        fifth_level_spells = get_spell_list(requested_character.class_main, 5)
    if requested_character.sixth_level_slots:
        sixth_level_spells = get_spell_list(requested_character.class_main, 6)
    if requested_character.seventh_level_slots:
        seventh_level_spells = get_spell_list(requested_character.class_main, 7)
    if requested_character.eighth_level_slots:
        eighth_level_spells = get_spell_list(requested_character.class_main, 8)
    if requested_character.ninth_level_slots:
        ninth_level_spells = get_spell_list(requested_character.class_main, 9)
    form = forms.SpellSelection()
    form.cantrips.choices = cantrips
    form.first_level_spells.choices = first_level_spells
    form.second_level_spells.choices = second_level_spells
    form.third_level_spells.choices = third_level_spells
    form.fourth_level_spells.choices = fourth_level_spells
    form.fifth_level_spells.choices = fifth_level_spells
    form.sixth_level_spells.choices = sixth_level_spells
    form.seventh_level_spells.choices = seventh_level_spells
    form.eighth_level_spells.choices = eighth_level_spells
    form.ninth_level_spells.choices = ninth_level_spells
    if form.validate_on_submit():
        for spell in form.cantrips.data:
            new_spell = CharacterKnownSpells(
                name=spell.title(),
                character_id=character_id,
            )
            db.session.add(new_spell)
            db.session.commit()
        for spell in form.first_level_spells.data:
            new_spell = CharacterKnownSpells(
                name=spell.title(),
                character_id=character_id,
            )
            db.session.add(new_spell)
            db.session.commit()
        for spell in form.second_level_spells.data:
            new_spell = CharacterKnownSpells(
                name=spell.title(),
                character_id=character_id,
            )
            db.session.add(new_spell)
            db.session.commit()
        for spell in form.third_level_spells.data:
            new_spell = CharacterKnownSpells(
                name=spell.title(),
                character_id=character_id,
            )
            db.session.add(new_spell)
            db.session.commit()
        for spell in form.fourth_level_spells.data:
            new_spell = CharacterKnownSpells(
                name=spell.title(),
                character_id=character_id,
            )
            db.session.add(new_spell)
            db.session.commit()
        for spell in form.fifth_level_spells.data:
            new_spell = CharacterKnownSpells(
                name=spell.title(),
                character_id=character_id,
            )
            db.session.add(new_spell)
            db.session.commit()
        for spell in form.sixth_level_spells.data:
            new_spell = CharacterKnownSpells(
                name=spell.title(),
                character_id=character_id,
            )
            db.session.add(new_spell)
            db.session.commit()
        for spell in form.seventh_level_spells.data:
            new_spell = CharacterKnownSpells(
                name=spell.title(),
                character_id=character_id,
            )
            db.session.add(new_spell)
            db.session.commit()
        for spell in form.eighth_level_spells.data:
            new_spell = CharacterKnownSpells(
                name=spell.title(),
                character_id=character_id,
            )
            db.session.add(new_spell)
            db.session.commit()
        for spell in form.ninth_level_spells.data:
            new_spell = CharacterKnownSpells(
                name=spell.title(),
                character_id=character_id,
            )
            db.session.add(new_spell)
            db.session.commit()
        return redirect(url_for('character_page', character_id=character_id))
    return render_template('spell-selection.html', form=form, character=character_id, all_campaigns=all_campaigns)


@app.route("/character/<int:character_id>/add-action", methods=["POST", "GET"])
def add_character_action(character_id):
    requested_character = Character.query.get(character_id)
    title = "Add Character Action"
    form = forms.AddNewAction()
    if form.validate_on_submit():
        new_action = Actions(
            name=form.name.data,
            description=form.description.data,
            type=form.type.data,
            range=form.range.data,
            target=form.target.data,
            character_id=character_id
        )
        if form.saving_action == "Yes":
            new_action.saving_action = True
            new_action.saving_attribute = form.saving_attribute.data
        else:
            new_action.saving_action = False
        if form.damaging_action == "Yes":
            new_action.damaging_action = True
            new_action.damage_roll_main = form.damage_roll_main.data
            new_action.damage_type_main = form.damage_type_main.data
            new_action.damage_roll_secondary = form.damage_roll_secondary.data
            new_action.damage_type_secondary = form.damage_type_secondary.data
        else:
            new_action.damaging_action = False
        db.session.add(new_action)
        db.session.commit()
        return redirect(url_for('character_page', character_id=character_id))
    return render_template('forms.html', form=form, all_campaigns=all_campaigns,
                           character=requested_character, title=title)


@app.route("/character/<int:character_id>/edit-notes", methods=["POST", "GET"])
def edit_character_notes(character_id):
    requested_character = Character.query.get(character_id)
    form = forms.EditNotes()
    form.notes.data = requested_character.notes
    title = "Edit your notes"
    if form.validate_on_submit():
        requested_character.notes = form.notes.data
        db.session.commit()
        return redirect(url_for('character_page', character_id=character_id))
    return render_template('edit-notes.html', form=form, all_campaigns=all_campaigns,
                           character=requested_character, title=title)


@app.route("/character/<int:character_id>/edit-description", methods=["GET", "POST"])
def edit_character_description(character_id):
    requested_character = Character.query.get(character_id)
    form = forms.EditDescription()
    form.backstory.data = requested_character.backstory
    form.appearance_detailed.data = requested_character.appearance_summary
    if form.validate_on_submit():
        requested_character.backstory = form.backstory.data
        requested_character.appearance_summary = form.appearance_detailed.data
        db.session.commit()
        return redirect(url_for('character_page', character_id=character_id))
    return render_template('edit-backstory-appearance.html', form=form, all_campaigns=all_campaigns,
                           character=requested_character)


@app.route("/character/<int:character_id>/add-item", methods=["GET", "POST"])
def add_character_item(character_id):
    requested_character = Character.query.get(character_id)
    form = forms.AddItem()
    if form.validate_on_submit():
        new_item = Items(
            name=form.name.data,
            category=form.category.data,
            value=form.value.data,
            item_desc=form.item_desc.data,
            character_id=character_id
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('character_page', character_id=character_id))
    return render_template('forms.html', form=form, all_campaigns=all_campaigns,
                           character=requested_character)


if __name__ == '__main__':
    app.run(debug=True)
