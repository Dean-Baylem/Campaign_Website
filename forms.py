from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

class CreateCampaignForm(FlaskForm):
    title = StringField("Campaign Title", validators=[DataRequired()])
    blurb = CKEditorField("Campaign Summary", validators=[DataRequired()])
    campaign_image = StringField("URL for campaign card image", validators=[DataRequired()])
    central_location = StringField("Campaign Location", validators=[DataRequired()])
    sub_location_1 = StringField("Side locations", validators=[DataRequired()])
    sub_location_2 = StringField("Side locations", validators=[DataRequired()])
    sub_location_3 = StringField("Side locations", validators=[DataRequired()])
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


#
# class Factions(db.Model):
#     __tablename__ = "factions"
#     id = db.Column(db.Integer, primary_key=True)
#     campaign = db.Column(db.String, db.ForeignKey("campaigns.title"))
#     faction_name = db.Column(db.String, nullable=True)
#     faction_description = db.Column(db.Text, nullable=True)