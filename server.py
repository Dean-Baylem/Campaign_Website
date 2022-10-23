from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_wtf import FlaskForm
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, declarative_base
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
from functools import wraps
import forms

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# Connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///campaign_manager.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




# Making database tables: string, text, integers.

# Testing relationships with simple tables

class Campaign(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    characters = relationship("Character", back_populates="campaign")
    locations = relationship("Location", back_populates="campaign")
    factions = relationship("Faction", back_populates="campaign")
    players = relationship("Player", back_populates="campaign")
    campaign_image = db.Column(db.String)
    page_image = db.Column(db.String)
    blurb = db.Column(db.Text)
    central_location = db.Column(db.String)

class Character(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    character_image = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    level = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    constitution = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    charisma = db.Column(db.Integer)
    proficiency = db.Column(db.Integer)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"))
    campaign = relationship("Campaign", back_populates="characters")
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    player = relationship("Player", back_populates="characters")

class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String, nullable=True)
    characters = relationship("Character", back_populates="player")
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"))
    campaign = relationship("Campaign", back_populates="players")

class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    place_name = db.Column(db.String)
    summary = db.Column(db.Text)
    image = db.Column(db.String)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"))
    campaign = relationship("Campaign", back_populates="locations")


class Faction(db.Model):
    __tablename__ = "factions"
    id = db.Column(db.Integer, primary_key=True)
    faction_name = db.Column(db.String(100))
    faction_description = db.Column(db.Text)
    faction_image = db.Column(db.String)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"))
    campaign = relationship("Campaign", back_populates="factions")

db.create_all()


@app.route("/")
def home():
    campaigns = Campaign.query.all()
    return render_template('index-template-version.html', all_campaigns=campaigns)


@app.route("/campaign")
def campagin():
    return render_template('campaign_page.html')


@app.route("/campaign/<story_id>", methods=["GET", "POST"])
def campaign_page(story_id):
    character_id = 1
    requested_campaign = Campaign.query.get(story_id)
    requested_character = Character.query.get(character_id)
    return render_template("campaign_page.html", campaign=requested_campaign, character=requested_character)


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
        )
        db.session.add(new_campaign)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add-campaign.html", form=form)

@app.route("/new-location", methods=["GET", "POST"])
def add_new_location():
    form = forms.CreateLocationForm()
    if form.validate_on_submit():
        new_location = Location(
            place_name=form.place_name.data,
            summary=form.summary.data,
            image=form.image.data,
            campaign=form.campaign.data,
        )

        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add-location.html", form=form)


@app.route("/new-character", methods=["GET", "POST"])
def add_new_character():
    form = forms.CreateCharacterForm()
    if form.validate_on_submit():
        new_character = Character(
            character_image=form.image.data,
            name=form.name.data,
            level=form.level.data,
            strength=form.strength.data,
            dexterity=form.dexterity.data,
            constitution=form.constitution.data,
            wisdom=form.wisdom.data,
            intelligence=form.intelligence.data,
            charisma=form.charisma.data,
            proficiency=form.proficiency.data,
        )
        db.session.add(new_character)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add-character.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)

