import datetime
from new_database import Campaign, Player, Location, LocationComments, Armor, Actions, Faction, FactionComments, \
    NPC, SessionReview, SessionReviewComments, ScheduledSession, HouseRule, Character, CharacterClasses, \
    CharacterRaces, RacialFeatures, SubclassFeatures, SubraceFeatures, ClassFeatures, Spells, Backgrounds, \
    BackgroundFeatures, BackgroundIdeals, BackgroundTraits, BackgroundBonds, BackgroundFlaws, \
    Weapons, Items
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


# ------------------------ Routes ----------------------------

@app.route("/test")
def test_page():
    return render_template("test.html")


@app.route("/")
def home():
    campaigns = Campaign.query.all()
    return render_template('index.html', all_campaigns=campaigns,
                           logged_in=current_user.is_authenticated)


@app.route("/campaigns")
def campaigns():
    campaigns = Campaign.query.all()
    return render_template('campaigns.html', all_campaigns=campaigns,
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


@app.route('/<campaign_id>/session-review/<review_id>', methods=["GET", "POST"])
def session_review_page(campaign_id, review_id):
    campaigns = Campaign.query.all()
    requested_campaign = Campaign.query.get(campaign_id)
    requested_review = SessionReview.query.get(review_id)
    print(requested_campaign.title)
    return render_template("session_review.html", campaign=requested_campaign, review=requested_review,
                           all_campaigns=campaigns, logged_in=current_user.is_authenticated)


@app.route("/login", methods=["GET", "POST"])
def login():
    campaigns = Campaign.query.all()
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
                           all_campaigns=campaigns, image=image, title=title, subtitle=subtitle)


@app.route("/character-hub", methods=["GET", "POST"])
def character_hub():
    campaigns = Campaign.query.all()
    if not current_user.is_authenticated:
        flash("Please login or register to create characters")
        return redirect(url_for('login'))
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


@app.route('/contact-us', methods=["GET", "POST"])
def contact_page():
    form = forms.ContactMe()
    campaigns = Campaign.query.all()
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
    return render_template('forms.html', form=form, all_campaigns=campaigns,
                           logged_in=current_user.is_authenticated, image=image,
                           title='Cast Message', subtitle=subtitle, classes="contact-form")


@app.route('/schedule')
def schedule_page():
    campaigns = Campaign.query.all()
    return render_template('schedule.html', all_campaigns=campaigns, logged_in=current_user.is_authenticated)

# ------------------------ Form Routes for DB -----------------------------


@app.route("/register", methods=["GET", "POST"])
def register_player():
    form = forms.CreateNewPlayerForm()
    # campaigns = Campaign.query.all()
    image = 'https://img.freepik.com/free-photo/top-view-beautiful-rpg-still-life-items_23-2149282425.jpg?w=1800&t=st=1668923891~exp=1668924491~hmac=1a144e548bff837473f7442b48915694068909663936c7cc36c77c7dc4166142'
    title = "Register"
    subtitle = "Welcome to Dungeon Delvers Incorportated"
    if form.validate_on_submit():
        # if Player.query.filter_by(username=form.username.data).first():
        #     flash("You have already signed up with that username. Please login")
        #     return redirect(url_for('login'))

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
                           image=image, title=title, subtitle=subtitle)
# all_campaigns=campaigns !!!! Remember to add back for the footer!!

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
            appearance_summary=form.appearance_summary.data,
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
            alignment=form.alignment.data,
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
        new_campaign.dm_img = request.files[form.dm_img.name]
        db.session.add(new_campaign)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("forms.html", form=form,  logged_in=current_user.is_authenticated)


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
    return render_template("forms.html", form=form, logged_in=current_user.is_authenticated)



if __name__ == '__main__':
    app.run(debug=True)
