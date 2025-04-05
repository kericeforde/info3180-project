from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,FileField,TextAreaField,BooleanField,EmailField,IntegerField,FloatField
from wtforms.validators import InputRequired,Email
from flask_wtf.file import FileField, FileRequired, FileAllowed

class Signup(FlaskForm):
    username=StringField('Username',validators=[InputRequired()])
    password=PasswordField('Password',validators=[InputRequired()])
    name=StringField('Name',validator=[InputRequired()])
    email=EmailField('Email',validator=[InputRequired(),Email])
    photo=FileField('Photo',validator=[FileRequired(message="File is required!"),FileAllowed(['png','jpeg','jpg'])])

class Login(FlaskForm):
     username=StringField('Username',validators=[InputRequired()])
     password=PasswordField('Password',validators=[InputRequired()])

class Profile(FlaskForm):
     description=TextAreaField('Description',validator=[InputRequired()])
     parish=StringField('Parish',validators=[InputRequired()])
     biography=TextAreaField('Biography',validator=[InputRequired()])
     sex=StringField('Sex',validators=[InputRequired(message="Male or Female")])
     race=StringField('Race',validators=[InputRequired()])
     birth_year=IntegerField('Parish',validators=[InputRequired()])
     height=FloatField('Height',validators=[InputRequired()])
     fav_cuisine=StringField('FavCuisine',validators=[InputRequired()])
     fav_school_subject= StringField('FavSchoolSubject',validators=[InputRequired()])
     political=BooleanField('Political')
     religion=BooleanField('Religion')
     family_oriented=BooleanField('Family Oriented')
     