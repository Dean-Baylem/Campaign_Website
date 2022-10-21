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

class Campaign(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer, primary_key=True)
    campaign_image = db.Column(db.String, nullable=False)
    title = db.Column(db.String, unique=True, nullable=False)
    blurb = db.Column(db.Text, nullable=False)
    central_location = db.Column(db.String, nullable=False)
    characters = relationship("Character", back_populates="campaign")
    sub_location_1 = db.Column(db.String)
    sub_location_2 = db.Column(db.String)
    sub_location_3 = db.Column(db.String)


class Character(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"))
    character_image = db.Column(db.String, nullable=False)
    campaign = relationship("Campaign", back_populates="characters")
    name = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    level = db.Column(db.Integer, nullable=True)
    strength = db.Column(db.Integer, nullable=True)
    dexterity = db.Column(db.Integer, nullable=True)
    constitution = db.Column(db.Integer, nullable=True)
    wisdom = db.Column(db.Integer, nullable=True)
    intelligence = db.Column(db.Integer, nullable=True)
    charisma = db.Column(db.Integer, nullable=True)
    proficiency = db.Column(db.Integer, nullable=True)


# class Factions(db.Model):
#     __tablename__ = "factions"
#     id = db.Column(db.Integer, primary_key=True)
#     campaign = db.Column(db.String, db.ForeignKey("campaigns.title"))
#     faction_name = db.Column(db.String, nullable=True)
#     faction_description = db.Column(db.Text, nullable=True)


# db.create_all()


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
            central_location=form.central_location.data,
            sub_location_1=form.sub_location_1.data,
            sub_location_2=form.sub_location_2.data,
            sub_location_3=form.sub_location_3.data,
        )
        db.session.add(new_campaign)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add-campaign.html", form=form)


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

