from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField, \
    SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

# Plan!


class CreateNewCharacter(FlaskForm):
    # darkvision = IntegerField("Please write down your darkvision in ft") - Based on race / abilities / etc
    submit = SubmitField("Submit Character")


class NameAndBackground(FlaskForm):
    campaign = SelectField("Please select which campaign this character is part off", choices=campaigns,
                           validators=[DataRequired()])
    level = IntegerField("Character Level", validators=[DataRequired()])
    name = StringField("Character Name", validators=[DataRequired()])
    race = StringField("Character Race", validators=[DataRequired()])
    character_class = StringField("Character Class", validators=[DataRequired()])
    alignment = StringField("Character Alignment", validators=[DataRequired()])
    background = StringField("Character Background", validators=[DataRequired()])
    appearance_summary = StringField("Short description of character appearance (up to 150 characters)",
                                     validators=[DataRequired()])
    character_image = StringField("Character Image URL", validators=[DataRequired()])
    token = StringField("Character Token URL", validators=[DataRequired()])


class AbilityScores(FlaskForm):
    strength = IntegerField("Character Strength", validators=[DataRequired()])
    dexterity = IntegerField("Character Dexterity", validators=[DataRequired()])
    constitution = IntegerField("Character Constitution", validators=[DataRequired()])
    wisdom = IntegerField("Character Wisdom", validators=[DataRequired()])
    intelligence = IntegerField("Character Intelligence", validators=[DataRequired()])
    charisma = IntegerField("Character Charisma", validators=[DataRequired()])


class SkillsAndBonuses(FlaskForm):
    skills = SelectMultipleField("Please select which skills you are proficient with", choices=all_skills)
    languages = CKEditorField("Please write down which languages you know. Please use bullet points")
    tool_proficiencies = CKEditorField("Please write down you tool proficiencies. Please use bullet points")
    # saves = SelectMultipleField("Please select which saves you are proficient with", choices=all_saves) - Based on Class


class Personality(FlaskForm):
    personality_traits = CKEditorField("Personality Traits", validators=[DataRequired()])
    ideals = StringField("Character Ideals", validators=[DataRequired()])
    bonds = StringField("Character Bonds", validators=[DataRequired()])
    flaws = StringField("Character Flaws", validators=[DataRequired()])

class ActionsNotesFeatures(FlaskForm):
    description = CKEditorField("Character Description", validators=[DataRequired()])
    backstory = CKEditorField("Character Backstory", validators=[DataRequired()])