import os
import time

from flask import (
	Flask, 
	Response, 
	jsonify, 
	make_response,
	render_template, 
	request, 
	redirect, 
	url_for,
	send_from_directory, 
)

from config import Config

cf = Config()


app = Flask(cf.APP_NAME, static_url_path="/static/")

app.config['FLASK_SECRET'] = cf.FLASK_SECRET    

os.environ['TZ'] = 'Europe/Berlin'
time.tzset()