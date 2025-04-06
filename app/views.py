"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort,send_from_directory,jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash,generate_password_hash
from app.forms import Login
from app.forms import Signup
from app.forms import Profiles
from app.models import Users
from app.models import Profile
from app.models import Favorite
import os
from datetime import datetime
from sqlalchemy import func



###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


#Create an account
@app.route('/api/register',methods=['GET','POST'])
def register():
    form=Signup()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        name=form.name.data
        email=form.email.data
        photo=form.photo.data
        
        #Saving image to uploads folder
        photoname = secure_filename(photo.filename)  # Secure the filename
        path = os.path.join(app.config['UPLOAD_FOLDER'],photoname)  
        photo.save(path)

        #Saving from data to database table Users
        
        existingUser = Users.query.filter_by(username=username).first()
        if existingUser:
            return jsonify({'error':'Username already exists!'})
        else:
            users=Users(username=username,password=generate_password_hash(password,method='pbkdf2:sha256'),name=name,email=email,photo=photoname)
            db.session.add(users)
            db.session.commit()
            return jsonify({'message':'Account Created Successfully!'}),201
    return jsonify({'errors':form_errors(form)}),400

#Login user
@app.route('/api/auth/login',methods=['GET','POST'])
def login():
    form=Login()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
          
        user = Users.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user) 
            return jsonify({"message":"Login Successful!"})
        return(jsonify({'message':'Incorrect Login: Username or password may be incorrect'}))
    return jsonify({'errors':form_errors(form)}),400

#Logout user
@app.route('/api/auth/logout',methods=['GET','POST'])
@login_required
def logout():
    """Logs out the user ."""
    logout_user()  
    return jsonify({"message":"Logout Successful!"})

@app.route("/api/photo/<filename>")
def getphoto(filename):
   return send_from_directory(os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"]), filename)

#Get profiles
@app.route('/api/profiles',methods=['GET'])
@login_required
def get_profiles():
  
    if not current_user.profiles or len(current_user.profiles) == 0:
        return jsonify({"error": "You must create a profile to view others."}), 403

    
    profiles = Users.query.join(Profile).filter(Users.id != current_user.id).all()

    profilelist = []
    for user in profiles:
        
        profilelist.append({
            "id": user.id,
            "photo": f"/api/photo/{user.photo}",
            "name": user.name
            #Do you think we should add some profile details?
            })

    return jsonify({"profiles": profilelist}), 200

#Create profile
@app.route('/api/profiles',methods=['POST'])
@login_required
def add_profile():

    form=Profiles()
    
    if form.validate_on_submit():

        if len(current_user.profiles) >= 3:
            return jsonify({"message": "You can only create up to 3 profiles."}), 403

        description= form.description.data
        parish=form.parish.data
        biography=form.biography.data
        sex=form.sex.data
        race=form.race.data
        birth=form.birth_year.data
        height=form.height.data
        cuisine=form.fav_cuisine.data
        color=form.fav_color.data
        subject=form.fav_school_subject.data
        political=form.political.data
        religious=form.religious.data
        family=form.family_oriented.data

        profile=Profile(description=description,parish=parish,biography=biography,sex=sex,race=race,birth_year=birth,height=height,fav_cuisine=cuisine,fav_color=color,fav_school_subject=subject,political=political,religious=religious,family_oriented=family,user_id_fk=current_user.id)
        
        db.session.add(profile)
        db.session.commit()

        return jsonify({"message":"Profile created successfully!"}),201
    return jsonify({'errors':form_errors(form)}),400

#Get one profile details by id
@app.route('/api/profiles/<int:profile_id>', methods=['GET'])
@login_required
def get_profile(profile_id):
    if not current_user.profiles or len(current_user.profiles) == 0:
        return jsonify({"error": "You must create a profile to view others."}), 403

    profile = Profile.query.get(profile_id)
   
    user = Users.query.get(profile.user_id_fk)

    return jsonify({
        "profile_id": profile.id,
        "userid": profile.user_id_fk,
        "name": user.name,
        "photo": f"/api/photo/{user.photo}",
        "description": profile.description,
        "parish": profile.parish,
        "biography": profile.biography,
        "sex": profile.sex,
        "race": profile.race,
        "birth_year": profile.birth_year,
        "height": profile.height,
        "fav_cuisine": profile.fav_cuisine,
        "fav_color": profile.fav_color,
        "fav_school_subject": profile.fav_school_subject,
        "political": profile.political,
        "religious": profile.religious,
        "family_oriented": profile.family_oriented
    }), 200

#Add user to favorites for logged in user
@app.route('/api/profiles/<int:user_id>/favorite', methods=['POST'])
@login_required
def addfavorite(user_id):
    if user_id == current_user.id:
        return jsonify({"error": "You cannot favorite your own profile."}), 400
    
    existFav = Favorite.query.filter_by(user_id_fk=current_user.id, fav_user_id_fk=user_id).first()
    if existFav:
        return jsonify({"message": "This profile is already in your favorites."}), 200

  
    newfav = Favorite(user_id_fk=current_user.id, fav_user_id_fk=user_id)
    db.session.add(newfav)
    db.session.commit()

    
    return jsonify({"message": "Profile added to favorites!"}), 201

#Get a list of all profiles that match a specific criteria.
@app.route('/api/profiles/matches/<int:profile_id>', methods=['GET'])
@login_required
def get_matches(profile_id):
    
    currentprofile = Profile.query.get(profile_id)
   
    currentuser = Users.query.get(currentprofile.user_id_fk)
    
    
    other_profiles = Profile.query.filter(Profile.id != profile_id).all()

    
    matching_profiles = []

    
    for profile in other_profiles:
        
        if profile.user_id_fk == currentuser.id:
            continue
        
        
        age_diff = abs(currentuser.birth_year - profile.birth_year)
        if age_diff > 5:
            continue
        
       
        height_diff = abs(currentuser.height - profile.height)
        if height_diff < 3 or height_diff > 10:
            continue
        
       
        matching_fields = 0
        if currentprofile.fav_cuisine.lower() == profile.fav_cuisine.lower():
            matching_fields += 1
        if currentprofile.fav_color.lower() == profile.fav_color.lower():
            matching_fields += 1
        if currentprofile.fav_school_subject.lower() == profile.fav_school_subject.lower():
            matching_fields += 1
        if currentprofile.political == profile.political:
            matching_fields += 1
        if currentprofile.religious == profile.religious:
            matching_fields += 1
        if currentprofile.family_oriented == profile.family_oriented:
            matching_fields += 1
        
        if matching_fields >= 3:
           
            user = Users.query.get(profile.user_id_fk)
            matching_profiles.append({
                "profile_id": profile.id,
                "user_id": profile.user_id_fk,
                "name": user.name,
                "photo": f"/api/photo/{user.photo}",
                "age": currentprofile.birth_year,
                "height": profile.height,
                "fav_cuisine": profile.fav_cuisine,
                "fav_color": profile.fav_color,
                "fav_school_subject": profile.fav_school_subject,
                "political": profile.political,
                "religious": profile.religious,
                "family_oriented": profile.family_oriented
            })

   
    return jsonify({"matching_profiles": matching_profiles}), 200


  

#Search for profiles by name, birth year, sex, race, or any combination of these four (4) fields; and return JSON results
@app.route('/api/search', methods=['GET'])
@login_required
def search():
    
    name = request.args.get('name', default='', type=str)
    birth_year = request.args.get('birth_year', default='', type=int)
    sex = request.args.get('sex', default='', type=str)
    race = request.args.get('race', default='', type=str)

    currentUserProfiles = [profile.id for profile in current_user.profiles] if current_user.profiles else []

    query = Profile.query

    if name:
        query = query.filter(Users.name.ilike(f"%{name}%"))
    if birth_year:
        query = query.filter(Profile.birth_year == birth_year)
    if sex:
        query = query.filter(Profile.sex.ilike(f"%{sex}%"))
    if race:
        query = query.filter(Profile.race.ilike(f"%{race}%"))

    if currentUserProfiles:
        query = query.filter(Profile.id.notin_(currentUserProfiles))

    profiles = query.all()

    profilelist = []
    for profile in profiles:
        user = Users.query.get(profile.user_id_fk)
        profilelist.append({
            "profile_id": profile.id,
            "user_id": profile.user_id_fk,
            "name": user.name,
            "photo": f"/api/photo/{user.photo}",
            "sex": profile.sex,
            "birth_year": profile.birth_year,
            "race": profile.race,
            "biography": profile.biography
        })

    return jsonify({"profiles": profilelist}), 200

#Get Details of a user
@app.route('/api/users/<int:user_id>', methods=['GET'])
@login_required
def getuserdetails(user_id):
    
    user=Users.query.get(user_id)

    return jsonify({"id":user.id,"username":user.username,"name":user.name,"email":user.email,"photo":f"/api/photo/{user.photo}","date_join":user.date_joined})


#Get users that a user has favoured. 
@app.route('/api/users/<int:user_id>/favourites', methods=['GET'])
@login_required
def getFav(user_id):
    sort_by = request.args.get('sort', default='name', type=str)

    favs = Favorite.query.filter(Favorite.user_id_fk == user_id).all()

    if not favs:
        return jsonify({"message": "No favorites found"}), 404

    fav_users = []
    
    for fav in favs:
        profile = Profile.query.filter_by(id=fav.fav_user_id_fk).first()
        if profile:
            user = Users.query.get(profile.user_id_fk)
            if user:
                age = datetime.now().year - profile.birth_year
                fav_users.append({
                    "name": user.name,
                    "parish": profile.parish,
                    "age": age,
                    "photo": f"/api/photo/{user.photo}"
                })

    
    if sort_by == 'name':
        fav_users.sort(key=lambda x: x['name'].lower())
    elif sort_by == 'parish':
        fav_users.sort(key=lambda x: x['parish'].lower())
    elif sort_by == 'age':
        fav_users.sort(key=lambda x: x['age'])

    return jsonify({"favorites": fav_users}), 200


       
#Get the top N favoured users based on the number of times they were favoured

@app.route('/api/users/favourites/<int:N>', methods=['GET'])
@login_required
def getTopFavs(N):
    sort_by = request.args.get('sort', default='fav_count', type=str)

  
    fav_counts = db.session.query(
        Favorite.fav_user_id_fk,
        func.count(Favorite.fav_user_id_fk).label('fav_count')
    ).group_by(Favorite.fav_user_id_fk).all()

    top_fav_users = []
    for fav in fav_counts:
        profile = Profile.query.get(fav.fav_user_id_fk)
        if profile:
            user = Users.query.get(profile.user_id_fk)
            if user:
                age = datetime.now().year - profile.birth_year 
                top_fav_users.append({
                    "name": user.name,
                    "parish": profile.parish,
                    "age": age,
                    "photo": f"/api/photo/{user.photo}",
                    "fav_count": fav.fav_count
                })

   
    if sort_by == 'name':
        top_fav_users.sort(key=lambda x: x['name'].lower())
    elif sort_by == 'parish':
        top_fav_users.sort(key=lambda x: x['parish'].lower())
    elif sort_by == 'age':
        top_fav_users.sort(key=lambda x: x['age'])
    else:
    
        top_fav_users.sort(key=lambda x: x['fav_count'], reverse=True)

    return jsonify({"top_favorites": top_fav_users[:N]}), 200

@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(Users).filter_by(id=id)).scalar()

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404