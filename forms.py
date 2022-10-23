from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

class CreateCampaignForm(FlaskForm):
    title = StringField("Campaign Title", validators=[DataRequired()])
    blurb = CKEditorField("Campaign Summary", validators=[DataRequired()])
    campaign_image = StringField("URL for campaign card image", validators=[DataRequired()])
    page_image = StringField("URL for the campaign page banner", validators=[DataRequired()])
    central_location = StringField("Campaign Location", validators=[DataRequired()])
    submit = SubmitField("Submit Campaign")


class CreateCharacterForm(FlaskForm):
    name = StringField("Character Name", validators=[DataRequired()])
    image = StringField("Character Image Url", validators=[DataRequired()])
    level = IntegerField("Character Level", validators=[DataRequired()])
    strength = IntegerField("Character Strength", validators=[DataRequired()])
    dexterity = IntegerField("Character Dexterity", validators=[DataRequired()])
    constitution = IntegerField("Character Constitution", validators=[DataRequired()])
    wisdom = IntegerField("Character Wisdom", validators=[DataRequired()])
    intelligence = IntegerField("Character Intelligence", validators=[DataRequired()])
    charisma = IntegerField("Character Charisma", validators=[DataRequired()])
    proficiency = IntegerField("Character Proficiency", validators=[DataRequired()])
    submit = SubmitField("Submit Character")


class CreateFactionForm(FlaskForm):
    faction_name = StringField("Name of Faction", validators=[DataRequired()])
    faction_description = CKEditorField("Faction Summary", validators=[DataRequired()])
    submit = SubmitField("Submit Faction")


class CreateLocationForm(FlaskForm):
    place_name = StringField("Name of Location", validators=[DataRequired()])
    summary = CKEditorField("Description of the Location", validators=[DataRequired()])
    image = StringField("Local file location for campaign card image", validators=[DataRequired()])
    campaign = StringField("Enter the name of the campaign for this location:", validators=[DataRequired()])
    submit = SubmitField("Submit Location")


#
# class Factions(db.Model):
#     __tablename__ = "factions"
#     id = db.Column(db.Integer, primary_key=True)
#     campaign = db.Column(db.String, db.ForeignKey("campaigns.title"))
#     faction_name = db.Column(db.String, nullable=True)
#     faction_description = db.Column(db.Text, nullable=True)