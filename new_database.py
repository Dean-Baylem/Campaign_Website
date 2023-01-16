# Attempt to improve the Database and tables to improve user input for character creation and then to set up the
# character sheet page for dynamic use and updating.

import datetime

from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_wtf import FlaskForm
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
from functools import wraps
import forms
from server import db

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# --------------- Connect to database ------------------

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///campaign_manager.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
    players = relationship("Player", back_populates="campaign") # !!! Change to Many to Many !!!
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
    campaign = relationship("Campaign", back_populates="players") # !!! Change to Many to Many !!!


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
    spell_ability = Column(String) # All of these will be updated after a player changes the level of the character.
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
    armor = relationship("Armor")
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
    subrace_features = relationship("SubraceFeatures", back_populates="subrace")
    race_id = Column(Integer, ForeignKey("character_races.id"))
    race = relationship("CharacterRaces", back_populates="subraces")


class SubraceFeatures(db.Model):
    __tablename__ = "sub_race_features"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    feature_desc = Column(Text)
    subrace_id = Column(Integer, ForeignKey("subraces.id"))
    subrace = relationship("Subraces", back_populates="subrace_features")


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
    other_weapons = Column(Text)

    strength_save = Column(Boolean, default=False)
    dexterity_save = Column(Boolean, default=False)
    constitution_save = Column(Boolean, default=False)
    intelligence_save = Column(Boolean, default=False)
    wisdom_save = Column(Boolean, default=False)
    charisma_save = Column(Boolean, default=False)
    spellcaster = Column(Boolean)

    num_skills = Column(Integer)
    num_tools = Column(Integer)
    start_equipment = Column(Text)

    class_features = relationship("ClassFeatures")
    subclass_features = relationship("SubclassFeatures")


class ClassFeatures(db.Model):
    __tablename__ = "class_features"
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("character_classes.id")) # Remember to have a class option in
                                                                   # the form that then fills the id out
    class_level = Column(Integer, nullable=False)
    optional = Column(Boolean)
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
    classes = Column(String) # Have this entered with each seperated by ',' then use split to get the list when needed
    name = Column(String)
    cast_time = Column(String)
    verbal = Column(Boolean)
    somatic = Column(Boolean)
    material = Column(Boolean)
    material_desc = Column(Text)
    concentration = Column(Boolean)
    attack_type = Column(String)
    range = Column(Integer)
    target = Column(String)
    spell_desc = Column(Text)
    spell_level = Column(Integer)
    spell_school = Column(String)
    duration = Column(String)
    attack_spell = Column(Boolean)
    save_spell = Column(Boolean)
    save_type = Column(String)
    ritual = Column(Boolean)
    primary_damage_die = Column(Integer)
    number_primary_die = Column(Integer)
    primary_higher_level_extra_die = Column(Integer)
    primary_damage_type = Column(String)
    secondary_damage_die = Column(Integer)
    number_secondary_die = Column(Integer)
    secondary_higher_level_extra_die = Column(Integer)
    secondary_damage_type = Column(String)
    cantrip_damage_die_1 = Column(Integer)
    cantrip_damage_die_2 = Column(Integer)
    cantrip_damage_die_3 = Column(Integer)
    cantrip_damage_die_4 = Column(Integer)


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
    character_id = Column(Integer, ForeignKey("characters.id"))


class Items(db.Model):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    value = Column(Integer)
    item_desc = Column(Text)
    character_id = Column(Integer, ForeignKey("characters.id"))


# db.create_all()
