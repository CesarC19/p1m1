import flask
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import requests
import os
import random
import base64
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from genius import get_lyrics_link
from spotify import get_access_token, get_song_data

app = flask.Flask(__name__)

global artistID

global savedUsername
savedUsername = []

def search(list, savedUsername):
    for i in range(len(list)):
        if list[i] == savedUsername:
            return True
    return False

MARKET = "US"
ARTIST_IDS = [
	"0nmQIMXWTXfhgOBdNzhGOs", #Avenged Sevenfold
	"7jy3rLJdDQY21OgRLCZ9sD", #Foo Fighters
	"6XyY86QOPPrYVGvF9ch6wz", #Linkin Park
]

app.secret_key = b'this is my secret key'
@app.route('/')
def index():
	return flask.render_template("signup.html")

@app.route("/signup",methods=["POST"])
def signup():
	val = flask.request.form["Username"]
	if val == "":
		flask.flash("Invalid username")
		return flask.redirect("/")
		#return flask.render_template("login.html")
	else:
		global savedUsername
		savedUsername.append(val)
		return flask.render_template("login.html")


@app.route("/login",methods=["POST"])
def login():
	val = flask.request.form["Username"]
	if search(savedUsername, val):
		return flask.render_template("artistSelect.html")
		#return flask.redirect("/home")
	else:
		flask.flash("Username not found")
		return flask.render_template("login.html")

@app.route('/artistSelect',methods=["POST"])
def artistSelect():
	val = flask.request.form["artistID"]
	global artistID
	artistID = val

	if val == "":
		flask.flash("Invalid artistID")
		return flask.redirect("/")
	else:
		return flask.redirect("/home")
		#return flask.render_template("index.html", artistID= val)

@app.route('/home')
def home():
	#artist_id = random.choice(ARTIST_IDS)
	global artistID
	artist_id = artistID

	# API calls
	access_token = get_access_token()
	(song_name, song_artist, song_image_url, preview_url) = get_song_data(artist_id, access_token)
	genius_url = get_lyrics_link(song_name)


	return flask.render_template(
    	"index.html",
    	song_name=song_name,
    	song_artist=song_artist,
    	song_image_url=song_image_url,
    	preview_url=preview_url,
    	genius_url=genius_url
    )
	



app.run(
	debug=True
)