# -*- coding: utf-8 -*-
# @Author: Zachary Priddy
# @Date:   2016-08-29 12:04:59
# @Last Modified by:   Zachary Priddy
# @Last Modified time: 2016-10-13 00:34:55

import json

import requests

from Serenity import API_PATHS, FF_host, FF_port, app
from Serenity.models import *
from flask import jsonify, redirect, render_template, request

from htmlmin.minify import html_minify




@app.route('/')
@login_required
def index():
  return html_minify(render_template("serenity_base.html", title="Base", user=current_user.email))

@login_required
@app.route('/devices')
def page2():
  url = API_PATHS['all_device_status']
  deviceTypes = requests.get(url).json().get('types')
  return html_minify(render_template("devices.html", title="Devices", deviceTypes=deviceTypes))


@login_required
@app.route('/d')
def d():
  url = API_PATHS['all_device_status']
  deviceTypes = requests.get(url).json().get('types')
  return html_minify(render_template("devices.html", title="Devices", deviceTypes=deviceTypes))

@app.route('/c')
def c():
  return "blah"

@app.route('/users')
@login_required
def users_view():
  users = [u.email for u in User.query.all()]
  return html_minify(render_template('users.html', users=users))

@app.route('/tokens')
@login_required
def tokens():
  tokens = [(u.app_name, u.token) for u in AuthToken.query.all()]
  return html_minify(render_template('tokens.html', tokens=tokens))

@app.route('/add_user')
@login_required
def addUser():
  username = request.args.get('username').lower().rstrip()
  password = request.args.get('password')
  add_user(username, password)
  return redirect('/#/users')

@app.route('/remove_user')
@login_required
def removeUser():
  username = request.args.get('username')
  remove_user(username)
  return redirect('/#/users')

@app.route('/get_token')
@login_required
def getToken():
  app_name = request.args.get('app')
  token = add_token(app_name)
  return redirect('/#/tokens')

@app.route('/remove_token')
@login_required
def removeToken():
  token = request.args.get('token')
  remove_token(token)
  return redirect('/#/tokens')

@app.route('/settings')
@login_required
def settingsView():
  return html_minify(render_template('settings.html'))


@app.route('/routines_values')
@login_required
def routinesValues():
  #TODO: This should just be requests.json
  print API_PATHS
  routines = requests.get(API_PATHS['routines']).json()
  print routines
  return jsonify(**routines)
  #routines = collections.OrderedDict(sorted(routines.items(), key=lambda elem: elem[1]['id']))
  #mode = requests.get(API_PATHS['mode']).text.title()
  #return render_template('routines.html', routines=routines, mode=mode)

@app.route('/routines')
@login_required
def routines():
  return html_minify(render_template('routines.html'))

@app.route('/API/translator', methods=['POST'])
@login_required
def api_translator():
  try:
    command = request.json
    print command
    #new_command = {'myCommand':command}
    #url = FF_host + ":" + str(FF_port) + "/manual_command?myCommand=" + str(command)
    url = API_PATHS['command']
    requests.post(url, json=command)
    return "COMMAND SENT"
  except:
    return "UNKNOWN ERROR"

@app.route('/API/alexa', methods=['POST'])
@auth_token_required
def alexaAPI():
  command = request.json
  url = API_PATHS['alexa']
  request.post(url, json=command)

@app.route('/API/views/devices')
@login_required
def device_views():
  url = API_PATHS['device_views']
  try:
    deviceViews = requests.get(url).json()
    return jsonify(deviceViews)
  except:
    return ""

@app.route('/API/status/devices/all')
@login_required
def devices_status_all():
  url = API_PATHS['all_device_status']
  try:
    deviceViews = requests.get(url).json()
    return jsonify(deviceViews)
  except:
    return ""