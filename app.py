from flask import (
    Flask,
    render_template,
    redirect,
    jsonify,
    request,
    abort,
    url_for,
    make_response
)
from flaskext.versioned import Versioned
from flask_mongoengine import *
from mongoengine.errors import (
    DoesNotExist,
    NotUniqueError
)
from flask_login import UserMixin, LoginManager, login_required, login_user
from flask_login import logout_user, current_user
from flask_cors import CORS
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
import datetime
import random
import string
import bcrypt
import json
from urllib.parse import quote
from pymongo import MongoClient
from functools import wraps
from flask import request, Response
from bson.json_util import dumps
from pymongo.errors import ServerSelectionTimeoutError
import os
import uuid

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = [
    {
        'db':  'MEDRECPRO',
        'host':  'localhost',
        'port':  27017,
        'alias':  'MEDRECMAIN',

    }
]
app.config['SECRET_KEY'] = "secret key is here !!!"
versioned = Versioned(app)
db = MongoEngine()
CORS(app, origins='http://localhost:8080', supports_credentials=True)

'''
=======================================================================================
ADMIN SECTION

1. scaling servers
2. choosing algorithm split
=======================================================================================
'''


# def check_auth(username, password):
#     """This function is called to check if a username /
#     password combination is valid.
#     """
#     return username == 'admin' and password == 'secret'

# def authenticate():
#     """Sends a 401 response that enables basic auth"""
#     return Response(
#     'Could not verify your access level for that URL.\n'
#     'You have to login with proper credentials', 401,
#     {'WWW-Authenticate': 'Basic realm="Login Required"'})

# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#         if not auth or not check_auth(auth.username, auth.password):
#             return authenticate()
#         return f(*args, **kwargs)
#     return decorated


'''
=======================================================================================

ADMIN SECTION ENDS HERE

=======================================================================================
'''

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user):
    return User.objects.get(id=user)


def login_required(role="developer"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if not current_user.check_role(role):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


class User(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    email = db.StringField(max_length=255, required=True)
    password = db.StringField(max_length=255, required=True)
    api_key = db.UUIDField(binary=False, default=uuid.uuid4)
    notifications = db.DictField(default={'email': False})

    def __unicode__(self):
        return self.id

    def check_role(self, role):
        print("Check for ", role)
        if role in self.roles:
            # print(role, " is assigned correctly")
            return True
        return False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'email'],
        'ordering': ['-created_at'],
        'strict': False,
        "db_alias": "MEDRECMAIN"
    }


def genStatusCode(code, message):
    data = {
        'status': code,
        'message': message
    }
    resp = jsonify(data)
    resp.status_code = 400
    return resp

# def add_api(data = {}):
#     api_key = current_user.api_key
#     data['api_key'] = str(api_key)
#     return data


@app.route("/")
def api_start():  # creating a function api_root which returns some txt to url
    # try:
    #     if current_user:
    #         email = current_user.email
    #         return render_template('index.html')
    # except:
    return render_template('index.html')


'''
=============================================================================
New Admin section
=============================================================================
'''

ALLOWED_USER_ROLES = ['admin', 'developer']


@app.route('/admin')
@login_required(role="admin")
def admin_home():
    return render_template('admin.html', title='Admin')


@app.route('/protected/<path:filename>')
@login_required(role="admin")
def protected(filename):

    return send_from_directory(
        os.path.join(app.instance_path, 'protected'),
        filename
    )


# setting another route /messages methods as post
@app.route('/admin/users', methods=['POST', 'GET'])
@login_required(role="admin")
def Users_admin():  # creating a function api_signup which gives a json data when a form is submitted in url

    if request.method == 'POST':

        data = request.get_json()

        try:
            data = User.objects.get(email=data['email'])
            return jsonify({'status': False, 'message': 'User already exist with that mail'})
        except DoesNotExist:
            unhashed_pass = data['password'].encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_pass = bcrypt.hashpw(unhashed_pass, salt)
            # response = requests.get(app.config['MASTER_API_URL']+'/api/user')
            # response = response.json()
            user_obj = User(email=data['email'], slackid=data['slackid'])
            # user_obj = User(slackid=data['slackid'])
            user_obj.set_password(data['password'])
            user_obj.save()
        return jsonify({'status': True})

    elif request.method == 'GET':
        try:
            users = User.objects().exclude('password', 'api_key')
            return jsonify({'status': True, 'users': users})
        except Exception as e:
            raise e
        return jsonify({'status': False})

    else:
        return genStatusCode(404, "Invalid")


@app.route('/admin/user/roles', methods=['GET'])
@login_required(role="admin")
def get_allowed_roles():
    return jsonify(roles=ALLOWED_USER_ROLES, status=True)


@app.route('/admin/users/<uid>', methods=['PATCH', 'DELETE'])
@login_required(role="admin")
def Update_users(uid):

    if request.method == 'PATCH':

        data = request.get_json()

        try:
            d = User.objects.get(uid=uid)
            d.slackid = data.get('slackid')
            d.roles = data.get('roles')
            d.save()
            return jsonify({'status': True})

        except DoesNotExist:
            return jsonify({'status': False, 'message': 'User not found'})

    elif request.method == 'DELETE':

        try:
            data = request.get_json()
            d = User.objects.get(uid=uid)
            try:
                if d.email == current_user.email:
                    logout_user()
            except Exception as e:
                pass
            d.delete()
            return jsonify(status=True)

        except Exception as e:
            raise e
    else:
        return genStatusCode(404, "Invalid")


@app.route('/admin/allusers', methods=['GET'])
@login_required(role="admin")
def userall():
    try:
        users = all_users()
        return jsonify({'status': True, 'users': users})
    except Exception as e:
        raise e
        return jsonify({'status': False})

# @app.route('/admin/user/delete', methods=['POST'])
# @login_required(role="admin")
# def delete_user():
#     try:
#         data = request.get_json()
#         email = data.get('email')
#         user = User.objects.get(email=email)

#         response = requests.delete(app.config['MASTER_API_URL']+'/api/user', json = {'api_key':str(user.api_key)})
#         response = response.json()

#         if response.get('status') == True:
#             try:
#                 if user.email == current_user.email:
#                     logout_user()
#             except Exception as e:
#                 pass
#             user.delete()
#             return jsonify(status=True)
#         return jsonify(status=False)
#     except Exception as e:
#         raise e


@app.route('/admin/dashboard/statistics', methods=['GET'])
@login_required(role="admin")
def admin_dashboard():
    try:
        data = request.args
        req_stat = data.get('stat_type')
        span_type = data.get('span_type')
        span_count = data.get('span_count')

        data = {"stat_type": req_stat, "span": {
            "type": span_type, "count": span_count}}
        response = requests.get(
            app.config['MASTER_API_URL']+'/api/statistics', json=data)
        response = response.json()

        return jsonify(status=True, stat=response.get('stat'))
    except Exception as e:
        raise e


'''
=======================================================================================

ADMIN SECTION ENDS HERE

=======================================================================================
'''


# setting another route /messages methods as post
@app.route('/login', methods=['POST'])
def api_login():  # creating a function api_message which gives a json data when a form is submitted in url
    data = request.get_json()

    try:
        user = User.objects.get(email=data['email'])
        if user.validate_login(user.password, data['password']):
            user_obj = User.objects.get(id=user.id)
            login_user(user_obj)
            return jsonify({'status': True})
    except DoesNotExist:
        return jsonify({'status': False, 'message': 'You have entered wrong Email or Password'})
    return jsonify({'status': False})


@app.route('/users/all', methods=['GET'])
def get_all_users():
    try:
        users = all_users()
        return jsonify({'status': True, 'users': users})
    except Exception as e:
        raise e
        return jsonify({'status': False})


@app.route("/logout", methods=['GET'])
def api_logout():
    logout_user()
    return redirect(url_for('api_start'))


@app.route('/dashboard')  # setting another route /messages methods as post
@login_required(role="developer")
def project_home():  # creating a function api_message which gives a json data when a form is submitted in url
    if current_user:
        email = current_user.email
        return render_template('index.html', email=email)
    return render_template('index.html', email=None)


'''
====================================================================
Login Section Ends
====================================================================
'''


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8991)
