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

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# --------------- Connect to database ------------------

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///campaign_manager.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --------------- Setup Login Manager -----------------

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_player(player_id):
    return Player.query.get(player_id)


skills = ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History",
          "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception",
          "Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"]

# ---------------- Database Tables --------------------


class Campaign(db.Model):
    __tablename__ = "campaign"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    characters = relationship("Character", back_populates="campaign")
    locations = relationship("Location", back_populates="campaign")
    factions = relationship("Faction", back_populates="campaign")
    players = relationship("Player", back_populates="campaign")
    npcs = relationship("NPC", back_populates="campaign")
    sessions = relationship("ScheduledSession", back_populates="campaign")
    sessionreview = relationship("SessionReview", back_populates="campaign")

    campaign_image = Column(String)
    page_image = Column(String)
    blurb = Column(Text)
    central_location = Column(String)
    region_summary = Column(Text)
    faction_summary = Column(Text)


class Player(UserMixin, db.Model):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    email = Column(String(100))
    password = Column(String, nullable=False)
    characters = relationship("Character", back_populates="player")
    sessionreview = relationship("SessionReview", back_populates="player")
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="players")


class Character(db.Model):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    
    # ----------- Character Details -------------
    name = Column(String(100))
    character_image = Column(String(250), nullable=False)
    token = Column(String(250))
    race = Column(String(50), nullable=False)
    character_class = Column(String(150), nullable=False)
    background = Column(String(50), nullable=False)
    personality_traits = Column(String, nullable=False)
    ideals = Column(String, nullable=False)
    bonds = Column(String, nullable=False)
    flaws = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    backstory = Column(Text, nullable=False)
    notes = Column(Text)
    traits_and_features = Column(Text)
    inventory = Column(Text)
    

    # ----------- Character Stats ----------------
    level = Column(Integer, nullable=False)
    strength = Column(Integer, nullable=False)
    dexterity = Column(Integer, nullable=False)
    constitution = Column(Integer, nullable=False)
    wisdom = Column(Integer, nullable=False)
    intelligence = Column(Integer, nullable=False)
    charisma = Column(Integer, nullable=False)

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
    strength_save = Column(Boolean, default=False)
    dexterity_save = Column(Boolean, default=False)
    constitution_save = Column(Boolean, default=False)
    intelligence_save = Column(Boolean, default=False)
    wisdom_save = Column(Boolean, default=False)
    charisma_save = Column(Boolean, default=False)
    init_bonus = Column(Integer, default=0)
    ac_bonus = Column(Integer, default=0)
    ac_override = Column(Integer, default=0)

    # ------ Skllls, languages and senses --------

    languages = Column(Text, default="Common")
    darkvision = Column(Integer, default=0)
    blindsight = Column(Integer, default=0)
    tremorsense = Column(Integer, default=0)
    truesight = Column(Integer, default=0)
    tool_proficiencies = Column(Text)

    # ------------- Table Relationships ------------
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="characters")
    player_id = Column(Integer, ForeignKey("players.id"))
    player = relationship("Player", back_populates="characters")
    actions = relationship("CharacterActions")


class CharacterActions(db.Model):
    __tablename__ = "action"
    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    type = Column(String(50), nullable=False) # Drop down in table generation
    damaging_action = Column(Boolean, default=True, nullable=False) # True or False in table
    saving_action = Column(Boolean, default=False, nullable=False)
    saving_attribute = Column(String(50))
    range = Column(String(50))
    target = Column(String(50))
    damage_roll_main = Column(String(50))
    damage_type_main = Column(String(50))
    damage_roll_secondary = Column(String(50))
    damage_type_secondary = Column(String(50))
    ac_bonus = Column(Integer)
    ac_override = Column(Integer)
    character_id = Column(Integer, ForeignKey("characters.id"))


class NPC(db.Model):
    __tablename__ = "npc"
    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)
    npc_image = Column(String, nullable=False)
    npc_description = Column(Text, nullable=False)
    npc_history = Column(Text, nullable=False)
    npc_notes = Column(Text, nullable=False)

    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="npcs")
    faction = Column(String(250))


class Location(db.Model):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)

    place_name = Column(String)
    summary = Column(Text)
    image = Column(String)
    notes = Column(Text)

    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="locations")


class Faction(db.Model):
    __tablename__ = "factions"
    id = Column(Integer, primary_key=True)

    faction_name = Column(String(100))
    faction_description = Column(Text)
    faction_image = Column(String)
    faction_notes = Column(Text)

    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="factions")


class UpcomingCampaign(db.Model):
    __tablename__ = "upcoming_campaign"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    timeslot = Column(String(300), nullable=False)
    image = Column(String, nullable=False)
    premise = Column(Text, nullable=False)
    registered_players = Column(Integer, nullable=False)


class ScheduledSession(db.Model):
    __tablename__ = "scheduledsession"
    id = Column(Integer, primary_key=True)
    day = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    time = Column(String(50), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="sessions")


class SessionReview(db.Model):
    __tablename__ = "sessionreview"
    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    subtime = Column(String(500))
    body = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())

    player_id = Column(Integer, ForeignKey("players.id"))
    player = relationship("Player", back_populates="sessionreview")

    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="sessionreview")


# db.create_all()

# ------------------------ Routes ----------------------------


@app.route("/")
def home():
    campaigns = Campaign.query.all()
    return render_template('index.html', all_campaigns=campaigns,
                           logged_in=current_user.is_authenticated)


@app.route("/campaign/<story_id>", methods=["GET", "POST"])
def campaign_page(story_id):
    campaigns = Campaign.query.all()
    requested_campaign = Campaign.query.get(story_id)
    if current_user.is_authenticated:
        requested_character = current_user.characters
    else:
        requested_character = None
    return render_template("campaign_page.html", campaign=requested_campaign,
                           characters=requested_character, logged_in=current_user.is_authenticated,
                           campaign_id=int(story_id), all_campaigns=campaigns,)


@app.route("/login", methods=["GET", "POST"])
def login():
    campaigns = Campaign.query.all()
    form = forms.LoginForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        player = Player.query.filter_by(email=email).first()
        if check_password_hash(player.password, password):
            login_user(player)
            return redirect(url_for('home'))
    return render_template("forms.html", form=form, logged_in=current_user.is_authenticated, all_campaigns=campaigns,)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# ------------------------ Form Routes for DB -----------------------------


@app.route("/register", methods=["GET", "POST"])
def register_player():
    form = forms.CreateNewPlayerForm()
    if form.validate_on_submit():
        new_player = Player()
        new_player.username = request.form["username"]
        new_player.email = request.form["email"]
        new_player.password = generate_password_hash(
            password=request.form["password"],
            method='pbkdf2:sha256',
            salt_length=8
        )
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("forms.html", form=form)


@app.route("/new-character", methods=["GET", "POST"])
@login_required
def add_new_character():
    campaigns = Campaign.query.all()
    trait_form = forms.CharacterNameAndTraits()
    backstory_form = forms.CharacterBackstory()
    stats_form = forms.CharacterStats()
    profs_form = forms.CharacterProfs()
    if profs_form.validate_on_submit():
        new_character = Character(
            character_image=trait_form.character_image.data,
            name=trait_form.name.data,
            token=trait_form.token.data,
            race=trait_form.race.data,
            character_class=trait_form.character_class.data,
            background=trait_form.background.data,
            personality_traits=trait_form.personality_traits.data,
            ideals=trait_form.ideals.data,
            bonds=trait_form.bonds.data,
            flaws=trait_form.flaws.data,
            description=trait_form.description.data,
            backstory=backstory_form.backstory.data,
            notes=backstory_form.notes.data,
            traits_and_features=backstory_form.traits_and_features.data,
            level=stats_form.level.data,
            strength=stats_form.strength.data,
            dexterity=stats_form.dexterity.data,
            constitution=stats_form.constitution.data,
            wisdom=stats_form.wisdom.data,
            intelligence=stats_form.intelligence.data,
            charisma=stats_form.charisma.data,
            # skills - This one has to be used with a loop to get each prof
            # Saves - Same as above
            languages=profs_form.languages.data,
            darkvision=profs_form.darkvision.data,
            tool_proficiencies=profs_form.tool_proficiencies.data,
        )
        # for skill in profs_form.skills:
        #     char_skill = skill.lower()
        #     if char_skill in skills:
        #         new_character.char_skill = True
        if trait_form.campaign.data == "GoS":
            new_character.campaign_id = 1
        if trait_form.campaign.data == "CoS":
            new_character.campaign_id = 2
        if trait_form.campaign.data == "LotST":
            new_character.campaign_id = 3
        new_character.player_id = current_user.id
        db.session.add(new_character)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("character-creation-form.html", trait_form=trait_form, backstory_form=backstory_form,
                           stats_form=stats_form, profs_form=profs_form,
                           logged_in=current_user.is_authenticated, all_campaigns=campaigns,)


@app.route("/new-location", methods=["GET", "POST"])
def add_new_location():
    form = forms.CreateLocationForm()
    if form.validate_on_submit():
        new_location = Location(
            place_name=form.place_name.data,
            summary=form.summary.data,
            image=form.image.data,
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
    return render_template("forms.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/new-campaign", methods=["GET", "POST"])
def add_new_campaign():
    form = forms.CreateCampaignForm()
    if form.validate_on_submit():
        new_campaign = Campaign(
            title=form.title.data,
            blurb=form.blurb.data,
            campaign_image=form.campaign_image.data,
            page_image=form.page_image.data,
            central_location=form.central_location.data,
            region_summary=form.region_summary.data,
            faction_summary=form.faction_summary.data
        )
        db.session.add(new_campaign)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("forms.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/new-faction", methods=["GET", "POST"])
def add_new_faction():
    form = forms.CreateFactionForm()
    if form.validate_on_submit():
        new_faction = Faction(
            faction_name=form.faction_name.data,
            faction_description=form.faction_description.data,
            faction_image=form.faction_image.data
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

if __name__ == '__main__':
    app.run(debug=True)

