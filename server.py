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


# ------------- Character Functions ---------------------


def prof_bonus(requested_character):
    if requested_character.level < 5:
        return 2
    elif requested_character.level < 9:
        return 3
    elif requested_character.level < 13:
        return 4
    elif requested_character.level < 16:
        return 5
    else:
        return 6


def ability_bonus(stat):
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


app = Flask(__name__)
app.jinja_env.globals.update(ability_bonus=ability_bonus)
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


skills = ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History",
          "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception",
          "Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"]


# ---------------- Database Tables --------------------


class Campaign(db.Model):
    __tablename__ = "campaign"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    subtitle = Column(String(500), nullable=False)
    campaign_image = Column(String, nullable=False)
    page_image = Column(String, nullable=False)
    blurb = Column(Text, nullable=False)
    central_location = Column(String, nullable=False)
    region_summary = Column(Text, nullable=False)
    faction_summary = Column(Text, nullable=False)

    characters = relationship("Character", back_populates="campaign")
    locations = relationship("Location", back_populates="campaign")
    factions = relationship("Faction", back_populates="campaign")
    players = relationship("Player", back_populates="campaign")
    npcs = relationship("NPC", back_populates="campaign")
    sessions = relationship("ScheduledSession", back_populates="campaign")
    sessionreview = relationship("SessionReview", back_populates="campaign")
    house_rules = relationship("HouseRule")


class HouseRule(db.Model):
    __tablename__ = "house_rules"
    id = Column(Integer, primary_key=True)
    character_creation = Column(Text)
    homebrew = Column(Text)
    special = Column(Text)
    races = Column(Text)
    source_material = Column(Text)
    third_party_material = Column(Text)
    campaign_id = Column(Integer, ForeignKey("campaign.id"))


class Player(UserMixin, db.Model):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
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
    alignment = Column(String(50), nullable=False)
    appearance_summary = Column(String(300), nullable=False)
    personality_traits = Column(String, nullable=False)
    ideals = Column(String, nullable=False)
    bonds = Column(String, nullable=False)
    flaws = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    backstory = Column(Text, nullable=False)
    notes = Column(Text)
    copper = Column(Integer)
    silver = Column(Integer)
    electum = Column(Integer)
    gold = Column(Integer)
    platinum = Column(Integer)

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
    spells = relationship("Spells")
    features = relationship("CharacterFeatures")
    inventory = relationship("CharacterInventory")


class CharacterActions(db.Model):
    __tablename__ = "action"
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


class Spells(db.Model):
    __tablename__ = "spell"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    cast_time = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    range = Column(Integer)  # Note to leave blank for self
    verbal = Column(Boolean, default=True, nullable=False)
    somatic = Column(Boolean, default=True, nullable=False)
    material = Column(Boolean, default=True, nullable=False)
    material_list = Column(String(100))
    level = Column(Integer, nullable=True)
    school = Column(String(50), nullable=True)
    duration = Column(String(50), nullable=True)
    concentration = Column(Boolean, nullable=True)
    damaging = Column(Boolean, nullable=True)
    saving = Column(Boolean, nullable=True)
    save_type = Column(String(50))  # Drop down list for options.
    damage_roll_main = Column(String(50))
    damage_type_main = Column(String(50))
    damage_roll_secondary = Column(String(50))
    damage_type_secondary = Column(String(50))
    ritual = Column(Boolean, default=False, nullable=True)
    character_id = Column(Integer, ForeignKey("characters.id"))


class CharacterFeatures(db.Model):
    __tablename__ = "feature"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    source = Column(String(50), nullable=True)  # have this as drop-down in list
    description = Column(Text, nullable=True)
    character_id = Column(Integer, ForeignKey("characters.id"))


class CharacterInventory(db.Model):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    number_owned = Column(Integer, nullable=True)
    value = Column(String(50))
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
    preview = Column(String(300))
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="sessions")


class SessionReview(db.Model):
    __tablename__ = "sessionreview"
    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    subtitle = Column(String(500))
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
                           campaign_id=int(story_id), all_campaigns=campaigns)


@app.route('/rules/<campaign_id>', methods=["GET", "POST"])
def rules_page(campaign_id):
    requested_campaign = Campaign.query.get(campaign_id)
    return render_template("rules.html", campaign=requested_campaign)



@app.route("/login", methods=["GET", "POST"])
def login():
    campaigns = Campaign.query.all()
    form = forms.LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        player = Player.query.filter_by(username=username).first()
        if check_password_hash(player.password, password):
            login_user(player)
            return redirect(url_for('home'))
    return render_template("forms.html", form=form, logged_in=current_user.is_authenticated, all_campaigns=campaigns)


@app.route("/character-hub", methods=["GET", "POST"])
@login_required
def character_hub():
    campaigns = Campaign.query.all()
    return render_template("character-hub.html", logged_in=current_user.is_authenticated, all_campaigns=campaigns)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/character/<character_id>', methods=["GET", "POST"])
def character_page(character_id):
    campaigns = Campaign.query.all()
    requested_character = Character.query.get(character_id)
    prof = prof_bonus(requested_character)
    return render_template("character-page.html", character=requested_character,
                           all_campaigns=campaigns, prof=prof, logged_in=current_user.is_authenticated)



# ------------------------ Form Routes for DB -----------------------------


@app.route("/register", methods=["GET", "POST"])
def register_player():
    form = forms.CreateNewPlayerForm()
    if form.validate_on_submit():
        new_player = Player()
        new_player.username = request.form["username"]
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
    form = forms.CreateNewCharacter()
    if form.validate_on_submit():
        new_character = Character(
            character_image=form.character_image.data,
            name=form.name.data,
            token=form.token.data,
            race=form.race.data,
            character_class=form.character_class.data,
            background=form.background.data,
            personality_traits=form.personality_traits.data,
            ideals=form.ideals.data,
            bonds=form.bonds.data,
            flaws=form.flaws.data,
            description=form.description.data,
            player_id=current_user.id,
            backstory=form.backstory.data,
            notes=form.notes.data,
            traits_and_features=form.traits_and_features.data,
            level=form.level.data,
            strength=form.strength.data,
            dexterity=form.dexterity.data,
            constitution=form.constitution.data,
            wisdom=form.wisdom.data,
            intelligence=form.intelligence.data,
            charisma=form.charisma.data,
            languages=form.languages.data,
            darkvision=form.darkvision.data,
            tool_proficiencies=form.tool_proficiencies.data,
        )
        if form.campaign.data == "GoS":
            new_character.campaign_id = 1
        if form.campaign.data == "CoS":
            new_character.campaign_id = 2
        if form.campaign.data == "LotST":
            new_character.campaign_id = 3
        # Saves - Same as above
        for skill in form.skills.data:
            if skill == "Acrobatics":
                new_character.acrobatics = True
            if skill == "Atheltics":
                new_character.athletics = True
            if skill == "Arcana":
                new_character.arcana = True
            if skill == "Deception":
                new_character.deception = True
            if skill == "History":
                new_character.history = True
            if skill == "Insight":
                new_character.insight = True
            if skill == "Intimidation":
                new_character.intimidation = True
            if skill == "Investigation":
                new_character.investigation = True
            if skill == "Medicine":
                new_character.medicine = True
            if skill == "Nature":
                new_character.nature = True
            if skill == "Perception":
                new_character.perception = True
            if skill == "Performance":
                new_character.performance = True
            if skill == "Persuasion":
                new_character.persuasion = True
            if skill == "Religion":
                new_character.religion = True
            if skill == "Sleight of Hand":
                new_character.sleight_of_hand = True
            if skill == "Stealth":
                new_character.stealth = True
            if skill == "Survival":
                new_character.survival = True
        for save in form.saves.data:
            if save == "Strength":
                new_character.strength_save = True
            if save == "Dexterity":
                new_character.dexterity_save = True
            if save == "Constitution":
                new_character.constitution_save = True
            if save == "Wisdom":
                new_character.wisdom_save = True
            if save == "Intelligence":
                new_character.intelligence_save = True
            if save == "Charisma":
                new_character.charisma_save = True
        db.session.add(new_character)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("forms.html", form=form,
                           logged_in=current_user.is_authenticated, all_campaigns=campaigns, )


@app.route("/new-location", methods=["GET", "POST"])
@admin_only
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


@app.route("/add-npc", methods=["GET", "POST"])
@admin_only
def add_new_npc():
    form = forms.NPCForm()
    if form.validate_on_submit():
        new_npc = NPC(
            name=form.name.data,
            npc_image=form.npc_image.data,
            npc_description=form.npc_description.data,
            npc_history=form.npc_history.data,
            npc_notes=form.npc_notes.data,
            faction=form.faction.data
        )
        if form.campaign.data == "GoS":
            new_npc.campaign_id = 1
        if form.campaign.data == "CoS":
            new_npc.campaign_id = 2
        if form.campaign.data == "LotST":
            new_npc.campaign_id = 3
        db.session.add(new_npc)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("forms.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/new-campaign", methods=["GET", "POST"])
@admin_only
def add_new_campaign():
    form = forms.CreateCampaignForm()
    if form.validate_on_submit():
        new_campaign = Campaign(
            title=form.title.data,
            subtitle=form.subtitle.data,
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
@admin_only
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
