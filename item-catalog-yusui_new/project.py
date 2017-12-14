from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, GameItem, User
from flask import session as login_session
import random
import string
import datetime
import os
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from functools import wraps

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Game Category Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///categorygamewithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# =====================
# The Google OAuth connection part, don't modify unless necessary
# =====================
# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Create connection between client and Google OAuth
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    # request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user \
        is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


# Define a login wrapper to remind user to log-in if necessary
def login_required(f):
    @wraps(f)
    def decorated_function(*arg, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*arg, **kwargs)
    return decorated_function


# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# =====================
# The main portion of this project, including all the paths and functions
# =====================
# Show all category
@app.route('/')
@app.route('/category/')
def showCategory():
    categories = session.query(Category).order_by(asc(Category.name))
    games = session.query(GameItem).order_by(desc(GameItem.date)).limit(5)
    if 'username' not in login_session:
        return render_template(
            'public_categories.html',
            categories=categories,
            games=games
        )
    else:
        return render_template(
            'private_categories.html',
            categories=categories,
            games=games
        )


# Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
@login_required
def newCategory():
    # if 'username' not in login_session:
        # return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategory'))
    else:
        return render_template('newCategory.html')


# Edit a category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
@login_required
def editCategory(category_id):
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedCategory.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized \
        to edit this category. Please create your own category in order to \
        edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showCategory'))
    else:
        return render_template('editCategory.html', category=editedCategory)


# Delete a category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_id):
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if categoryToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not \
        authorized to delete this category. Please create your own \
        category in order to delete.');}</script><body \
        onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template(
            'deleteCategory.html',
            category=categoryToDelete
        )


# Show a category game
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/game/')
def showGame(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    games = session.query(GameItem).filter_by(
        category_id=category_id).all()
    original_categories = session.query(Category).order_by(asc(Category.name))
    if 'username' not in login_session:
        return render_template(
            'public_gamelist.html',
            games=games,
            categories=original_categories,
            category=category,
            creator=creator
        )
    else:
        return render_template(
            'user_gamelist.html',
            games=games,
            categories=original_categories,
            category=category,
            creator=creator
        )


# Show a specific game item
@app.route('/category/<int:category_id>/game/<int:game_id>/')
def showGameItem(category_id, game_id):
    category = session.query(Category).filter_by(id=category_id).one()
    game = session.query(GameItem).filter_by(
        id=game_id).one()
    creator = getUserInfo(game.user_id)
    if 'username' not in login_session \
            or creator.id != login_session['user_id']:
        return render_template(
            'public_game_item.html',
            game=game,
            creator=creator
        )
    else:
        return render_template(
            'private_game_item.html',
            game=game,
            creator=creator
        )


# Create a new game
@app.route('/category/<int:category_id>/game/new/', methods=['GET', 'POST'])
def newGameItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    categories = session.query(Category).order_by(asc(Category.name))
    if request.method == 'POST':
        newGame = GameItem(
            name=request.form['name'],
            description=request.form['description'],
            date=datetime.datetime.now(),
            official_website=request.form['website'],
            category=session.query(Category).
            filter_by(name=request.form['category']).one(),
            user_id=login_session['user_id'])
        session.add(newGame)
        session.commit()
        flash('New Game %s Item Successfully Created' % (newGame.name))
        return redirect(url_for('showCategory'))
    else:
        return render_template(
            'newgameitem.html',
            category_id=category_id,
            categories=categories
        )


# Edit the game content, only authrized user is allowed
@app.route(
    '/category/<int:category_id>/game/<int:game_id>/edit',
    methods=['GET', 'POST']
)
def editGameItem(category_id, game_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedGame = session.query(GameItem).filter_by(id=game_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    categories = session.query(Category).order_by(asc(Category.name))
    if login_session['user_id'] != editedGame.user_id:
        return "<script>function myFunction() {alert('You are not \
        authorized to edit this game. Please create your \
        own game.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedGame.name = request.form['name']
        if request.form['description']:
            editedGame.description = request.form['description']
        if request.form['category']:
            editedGame.category = session.query(Category).\
                filter_by(name=request.form['category']).one()
        if request.form['website']:
            editedGame.official_website = request.form['website']
        editedGame.date = datetime.datetime.now()
        session.add(editedGame)
        session.commit()
        flash('Game Item Successfully Edited')
        return redirect(url_for('showGame', category_id=category_id))
    else:
        return render_template(
            'editgameitem.html',
            categories=categories,
            category_id=category_id,
            game_id=game_id,
            game=editedGame
        )


# Delete a game, only authrized user is allowed
@app.route(
    '/category/<int:category_id>/game/<int:game_id>/delete',
    methods=['GET', 'POST']
)
def deleteGameItem(category_id, game_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    gameToDelete = session.query(GameItem).filter_by(id=game_id).one()
    if login_session['user_id'] != gameToDelete.user_id:
        return "<script>function myFunction() {alert('You are not authorized \
        to delete menu items to this category. Please create your own \
        category in order to delete \
        items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(gameToDelete)
        session.commit()
        flash('Game Item Successfully Deleted')
        return redirect(url_for('showGame', category_id=category_id))
    else:
        return render_template(
            'deletegameitem.html',
            category_id=category_id,
            game=gameToDelete
        )


# =====================
# The JSON part, the follwing JSON endpoints are open to public
# =====================
# JSON endpoints to view all category
@app.route('/category/JSON')
def categorysJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


# JSON endpoints to view games in a specific category
@app.route('/category/<int:category_id>/game/JSON')
def categoryGameJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    games = session.query(GameItem).filter_by(
        category_id=category_id).all()
    return jsonify(GameItems=[i.serialize for i in games])


# JSON endpoints to view a specific game
@app.route('/category/<int:category_id>/game/<int:game_id>/JSON')
def gameItemJSON(category_id, game_id):
    game = session.query(GameItem).filter_by(id=game_id).one()
    return jsonify(GameItem=game.serialize)

# =====================
# The main function, don't modify unless changing forwarding port
# =====================
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
