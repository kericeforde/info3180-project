"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from functools import wraps
from flask import request, jsonify
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from app.forms import Login
import jwt
from app.forms import Signup
from sqlalchemy.orm import joinedload
from app.forms import Profiles
from app.models import Users
from app.models import Profile
from app.models import Favorite
import os
from datetime import datetime
from sqlalchemy import func
from flask_wtf.csrf import generate_csrf


###
# Routing for  application.
###

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


# Create an account
@app.route('/api/register', methods=['GET', 'POST'])
def register():
    form = Signup()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data
        email = form.email.data
        photo = form.photo.data

        # Saving image to uploads folder
        photoname = secure_filename(photo.filename)  # Secure the filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], photoname)
        photo.save(path)

        # Saving from data to database table Users

        existingUser = Users.query.filter_by(username=username).first()
        if existingUser:
            return jsonify({
                "success": False,
                "errors": {
                    "username": ["Username already exists!"]
                }
            }), 409

        # Save image to uploads folder
        photoname = secure_filename(photo.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photoname)
        photo.save(photo_path)

        # Add user to database
        user = Users(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'), name=name, email=email, photo=photoname
                     )
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Account Created Successfully!"
        }), 201

    return jsonify({
        "success": False,
        "errors": form_errors(form)
    }), 400

# Login user


@app.route('/api/auth/login', methods=['GET', 'POST'])
def login():
    form = Login()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            # Generate a JWT token
            token = jwt.encode({"user_id": user.id},
                               app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({"success": True, "message": "Login Successful!", "token": token, "user_id": user.id}), 200
        else:

            return jsonify({
                "success": False,
                "errors": {
                    "login": ["Incorrect Login: Username or password may be incorrect"]
                }
            }), 401

    return jsonify({
        "success": False,
        "errors": form_errors(form)
    }), 400

# Logout user


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization').split(" ")[1]
    try:
        decoded_token = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if decoded_token['user_id'] == current_user.id:
            """Logs out the user ."""
            # logout_user()
            return jsonify({"success": True, "message": "Logout Successful!"})
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/photo/<filename>")
def getphoto(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"]), filename)


@app.route('/api/profiles', methods=['GET'])
@login_required
def get_last_four_profiles():
    if not current_user.profiles:
        return jsonify({"error": "You must create a profile to view others."}), 403

    token = request.headers.get('Authorization').split(" ")[1]
    try:
        decoded_token = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if decoded_token['user_id'] == current_user.id:
            current_profile_ids = [
                profile.id for profile in current_user.profiles]

            query = Profile.query.options(joinedload(Profile.user))

            if current_profile_ids:
                query = query.filter(Profile.id.notin_(current_profile_ids))

            profiles = query.order_by(Profile.id.desc()).all()

            profilelist = [
                {
                    "profile_id": profile.id,
                    "user_id": profile.user_id_fk,
                    "name": profile.user.name,
                    "photo": f"/api/photo/{profile.user.photo}",
                    "sex": profile.sex,
                    "birth_year": profile.birth_year,
                    "race": profile.race,
                    "biography": profile.biography
                }
                for profile in profiles
            ]

            return jsonify({"profiles": profilelist}), 200
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Create profile
@app.route('/api/profiles', methods=['POST'])
@login_required
def add_profile():
    token = request.headers.get('Authorization').split(" ")[1]

    try:
        decoded_token = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
        print(decoded_token)
        if decoded_token['user_id'] == current_user.id:

            form = Profiles()

            if form.validate_on_submit():

                if len(current_user.profiles) >= 3:
                    return jsonify({"message": "You can only create up to 3 profiles."}), 403

                description = form.description.data
                parish = form.parish.data
                biography = form.biography.data
                sex = form.sex.data
                race = form.race.data
                birth = form.birth_year.data
                height = form.height.data
                cuisine = form.fav_cuisine.data
                color = form.fav_color.data
                subject = form.fav_school_subject.data
                political = form.political.data
                religious = form.religious.data
                family = form.family_oriented.data

                profile = Profile(description=description, parish=parish, biography=biography, sex=sex, race=race, birth_year=birth, height=height, fav_cuisine=cuisine,
                                  fav_color=color, fav_school_subject=subject, political=political, religious=religious, family_oriented=family, user_id_fk=current_user.id)

                db.session.add(profile)
                db.session.commit()

            return jsonify({"message": "Profile created successfully!"}), 201
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({'errors': form_errors(form)}), 400


# Get one profile details by id
@app.route('/api/profiles/<int:profile_id>', methods=['GET'])
@login_required
def get_profile(profile_id):
    token = request.headers.get('Authorization').split(" ")[1]
    try:

        decoded_token = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if decoded_token['user_id'] == current_user.id:
            if not current_user.profiles or len(current_user.profiles) == 0:
                return jsonify({"error": "You must create a profile to view others."}), 403

            profile = Profile.query.get(profile_id)

            user = Users.query.get(profile.user_id_fk)

            return jsonify({
                "profile_id": profile.id,
                "user_id": profile.user_id_fk,
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
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Add user to favorites for logged in user
@app.route('/api/profiles/<int:user_id>/favorite', methods=['POST'])
@login_required
def addfavorite(user_id):
    token = request.headers.get('Authorization').split(" ")[1]
    try:
        decoded_token = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if decoded_token['user_id'] == current_user.id:
            if user_id == current_user.id:
                return jsonify({"error": "You cannot favorite your own profile."}), 400

            existFav = Favorite.query.filter_by(
                user_id_fk=current_user.id, fav_user_id_fk=user_id).first()
            if existFav:
                return jsonify({"message": "This user is already in your favorites."}), 200

            newfav = Favorite(user_id_fk=current_user.id, fav_user_id_fk=user_id)
            db.session.add(newfav)
            db.session.commit()

            return jsonify({"message": "Profile added to favorites!"}), 201
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get a list of all profiles that match a specific criteria.


@app.route('/api/profiles/matches/<int:profile_id>', methods=['GET'])
@login_required
def get_matches(profile_id):
    token = request.headers.get('Authorization').split(" ")[1]
    try:
        decoded_token = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if decoded_token['user_id'] == current_user.id:

            currentprofile = Profile.query.get(profile_id)

            currentuser = Users.query.get(currentprofile.user_id_fk)

            other_profiles = Profile.query.filter(Profile.id != profile_id).all()
            print(other_profiles)
            matching_profiles = []

            for profile in other_profiles:
                
                if profile.user_id_fk == currentuser.id:
                    continue

                age_diff = abs(currentprofile.birth_year - profile.birth_year)
                print(age_diff)
                print("here")
                if age_diff > 5:
                    continue

                height_diff = abs(currentprofile.height - profile.height)
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
                
                print(matching_fields)
                if matching_fields >= 3:

                    user = Users.query.get(profile.user_id_fk)
                    matching_profiles.append({
                        "profile_id": profile.id,
                        "user_id": profile.user_id_fk,
                        "name": user.name,
                        "photo": f"/api/photo/{user.photo}",
                        "birth_year": currentprofile.birth_year,
                        "height": profile.height,
                        "fav_cuisine": profile.fav_cuisine,
                        "fav_color": profile.fav_color,
                        "fav_school_subject": profile.fav_school_subject,
                        "political": profile.political,
                        "religious": profile.religious,
                        "family_oriented": profile.family_oriented
                    })

            return jsonify({"matching_profiles": matching_profiles}), 200
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Search for profiles by name, birth year, sex, race, or any combination of these four (4) fields; and return JSON results
@app.route('/api/search', methods=['GET'])
@login_required
def search():
    if not current_user.profiles or len(current_user.profiles) == 0:
        return jsonify({"error": "You must create a profile to view others."}), 403

    token = request.headers.get('Authorization').split(" ")[1]
    try:
        decoded_token = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if decoded_token['user_id'] == current_user.id:

            name = request.args.get('name', default='', type=str)
            birth_year = request.args.get('birth_year', default='', type=int)
            sex = request.args.get('sex', default='', type=str)
            race = request.args.get('race', default='', type=str)

            currentUserProfiles = [
                profile.id for profile in current_user.profiles] if current_user.profiles else []

            query = db.session.query(Profile).join(
                Users, Profile.user_id_fk == Users.id)

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

            if not any([name, birth_year, sex, race]):
                # query = query.order_by(Profile.id.desc()).limit(4)
                return jsonify({"error": "Search bar is empty."}), 403

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
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get Details of a user


@app.route('/api/users/<int:user_id>', methods=['GET'])
@login_required
def get_user_details(user_id):
    token = request.headers.get('Authorization').split(" ")[1]
    try:
        decoded_token = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if decoded_token['user_id'] == current_user.id:
            # Check if the user exists
            user = Users.query.get(user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404

            # Get all profiles for the user
            profiles = Profile.query.filter_by(user_id_fk=user.id).all()
            if not profiles:
                return jsonify({"error": "Profiles not found"}), 404

            # Prepare the list of profile data to return
            profiles_data = []
            for profile in profiles:
                profiles_data.append({
                    "profile_id": profile.id,
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
                })

            # Return user and all associated profiles
            return jsonify({
                "user_id": user.id,
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "photo": f"/api/photo/{user.photo}",
                "profiles": profiles_data,
                "date_joined": user.date_joined.strftime("%Y-%m-%d"),
            }), 200
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/users/<int:user_id>/favourites', methods=['GET'])
@login_required
def get_favourites(user_id):
    token = request.headers.get('Authorization').split(" ")[1]
    try:
        decoded_token = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if decoded_token['user_id'] == current_user.id:
            sort_by = request.args.get('sort', default='name', type=str)
            favs = Favorite.query.filter_by(user_id_fk=user_id).all()

            fav_users = []

            for fav in favs:

                profile = Profile.query.filter_by(
                    user_id_fk=fav.fav_user_id_fk).first()

                if profile and profile.user_id_fk != user_id:
                    user = Users.query.get(profile.user_id_fk)
                    if user:
                        age = datetime.now().year - profile.birth_year
                        fav_users.append({
                            "name": user.name,
                            "parish": profile.parish,
                            "age": age,
                            "profile_id": profile.id,
                            "user_id": user.id,
                            "photo": f"/api/photo/{user.photo}"
                        })

            if sort_by == 'name':
                fav_users.sort(key=lambda x: x['name'].lower())
            elif sort_by == 'parish':
                fav_users.sort(key=lambda x: x['parish'].lower())
            elif sort_by == 'age':
                fav_users.sort(key=lambda x: x['age'])

            return jsonify({"favorites": fav_users}), 200
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/users/favourites/<int:N>', methods=['GET'])
@login_required
def getTopFavs(N):
    token = request.headers.get('Authorization').split(" ")[1]
    try:
         decoded_token = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
         if decoded_token['user_id'] == current_user.id:
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
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500



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
