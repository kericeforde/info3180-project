from . import db
from werkzeug.security import generate_password_hash
from datetime import datetime

class Users(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),unique=True)
    password=db.Column(db.String(128),nullable=False)
    name=db.Column(db.String(80),nullable=False)
    email=db.Column(db.String(80),nullable=False)
    photo=db.Column(db.String(128),nullable=False)
    date_joined=db.Column(db.DateTime, default=datetime.now())



    def __init__(self,username,password,name,email,photo):
        self.username=username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.name=name
        self.email=email
        self.photo=photo


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
    
class Profile(db.Model):
      
     id=db.Column(db.Integer,primary_key=True)
     user_id_fk=db.Column(db.Integer,db.ForeignKey(Users.id),nullable=False) 
     description=db.Column(db.String(255),nullable=False)
     parish=db.Column(db.String(80),nullable=False)
     biography=db.Column(db.String(255),nullable=False)
     sex=db.Column(db.String(80),nullable=False)
     race=db.Column(db.String(80),nullable=False)
     birth_year=db.Column(db.Intege,nullable=False)
     height=db.Column(db.Float,nullable=False)
     fav_cuisine=db.Column(db.String(128),nullable=False)
     fav_color=db.Column(db.String(80),nullable=False)
     fav_school_subject=db.Column(db.String(80),nullable=False)
     political=db.Column(db.Boolean,nullable=False)
     religious=db.Column(db.Boolean,nullable=False)
     family_oriented=db.Column(db.Boolean,nullable=False)

     def __init__(self,description,parish,biography,sex,race,birth_year,height,fav_cuisine,fav_color,fav_school_subject,political,religious,family_oriented):
         
       self.description=description
       self.parish=parish
       self.biography=biography
       self.sex=sex
       self.race=race
       self.birth_year=birth_year
       self.height=height
       self.fav_cuisine=fav_cuisine
       self.fav_color=fav_color
       self.fav_school_subject=fav_school_subject
       self.political=political
       self.religious=religious
       self.family_oriented=family_oriented


class Favorite(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id_fk=db.Column(db.Integer,db.ForeignKey(Users.id),nullable=False)
    fav_user_id_fk=db.Column(db.Integer,db.ForeignKey(Profile.id),nullable=False)
