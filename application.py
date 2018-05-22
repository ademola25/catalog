#!/usr/bin/python
from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash, g
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from functools import wraps
from database_setup import Category, Base, SpaItem, User
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Category in Spa Application"

# Connecting  to the  Database and create database session
engine = create_engine('sqlite:///spa_category.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# conecting through google plus
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

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
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

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
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response





# Login required
def login_required(f):
    @wraps(f)
    def y(*args, **kwargs):
        if 'user_id' not in login_session:
            return redirect(url_for('showLogin'))
        return f(*args, **kwargs)
    return y


# JSON APIs to view Spa Category Information
@app.route('/spacategory/<int:categories_id>/spaitem/JSON')
def spaCategoryJSON(categories_id):
    categories = session.query(Category).filter_by(id=categories_id).one()
    items = session.query(SpaItem).filter_by(
        categories_id=categories_id).all()
    return jsonify(SpaItems=[i.serialize for i in items])


@app.route('/spacategory/<int:categories_id>/spaitem/<int:spa_item_id>/JSON')
def spaItemJSON(categories_id, spa_item_id):
    Spa_Item = session.query(SpaItem).filter_by(id=spa_item_id).one()
    return jsonify(Spa_Item=Spa_Item.serialize)


@app.route('/spacategory/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])

# Show all spa categories
@app.route('/')
@app.route('/spacategory/')
def showCategory():
    categories = session.query(Category).all()
    items = session.query(SpaItem).order_by(SpaItem.id.desc())
    if 'username' not in login_session:
        return render_template('publicspacategory.html', categories=categories, items=items)
    else:
        return render_template('spacategory.html', categories=categories, items=items)


#show spa items
@app.route('/spacategory/<int:categories_id>/')
@app.route('/spacategory/<int:categories_id>/spaitem/')
def showSpaItem(categories_id):
    categories = session.query(Category).filter_by(id=categories_id).one()
    category = session.query(Category).all()
    creator = getUserInfo(categories.user_id)
    items = session.query(SpaItem).filter_by(categories_id=categories.id).order_by(SpaItem.id.desc())
    return render_template('publicspaitem.html', categories=categories, items=items, category=category, creator=creator)

# READ- specifying some item from the spa items
@app.route('/spacategories/<int:categories_id>/spaitem/<int:spa_item_id>/')
def showItemDetails(categories_id, spa_item_id):
    """returns category item"""
    categories = session.query(Category).filter_by(id=categories_id).one()
    items = session.query(SpaItem).filter_by(id=spa_item_id).one()
    creator = getUserInfo(categories.user_id)
    if 'username' not in login_session:
        return render_template('public_itemdetails.html', categories=categories, items=items, creator=creator)
    else:
        return render_template('item_details.html', categories=categories, items=items, creator=creator)

# create new spa item
@app.route('/spacategory/spaitem/new', methods=['GET', 'POST'])
@login_required
def newSpaItem():
    if request.method == 'POST':
            newItem = SpaItem(
            name=request.form['name'],
            description=request.form['description'],
            categories_id=request.form['categories_id'],
            user_id=login_session['user_id'])
            session.add(newItem)
            session.commit()
            flash('New Spa %s Item Successfully Created' % (newItem.name))
            return redirect(url_for('showCategory'))
    else:
        return render_template('newspaitem.html')
# Edit a spa item
@app.route('/spacategory/<int:categories_id>/spaitem/<int:spa_item_id>/edit', methods=['GET', 'POST'])
@login_required
def editSpaItem(categories_id, spa_item_id):
    editedItem = session.query(SpaItem).filter_by(id=spa_item_id).one()
    categories = session.query(Category).all()
    #check if the logged in user is the owner of item
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('Spa Item Successfully Updated')
        return redirect(url_for('showSpaItem', categories_id=categories_id, spa_item_id=spa_item_id))
    else:

        return render_template('editspaitem.html', item=editedItem, categories_id=categories_id, spa_item_id=spa_item_id, categories=categories)
# Delete a spa item
@app.route('/spacategory/<int:categories_id>/spaitem/<int:spa_item_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteSpaItem(categories_id, spa_item_id):
    categories = session.query(Category).filter_by(id=categories_id).one()
    itemToDelete = session.query(SpaItem).filter_by(id=spa_item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Spa Item Successfully Deleted')
        return redirect(url_for('showCategory', categories_id=categories_id))
    else:
        return render_template('deleteSpaitem.html', categories_id=categories_id, spa_item_id=spa_item_id, item=itemToDelete)

# Disconnect from Google
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("Successfully logged out.")
        return redirect(url_for('showCategory'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategory'))



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
