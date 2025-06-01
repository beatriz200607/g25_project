
from flask import Flask, render_template, request, session, redirect, url_for
from flask import jsonify
import json
import os

def ensure_records_file():
    if not os.path.exists('records.json'):
        with open('records.json', 'w') as f:
            json.dump([], f)

import random

from classes.dish            import Dish
from classes.order           import Order
from classes.restaurant      import Restaurant
from classes.deliverypartner import DeliveryPartner
from classes.userlogin       import Userlogin
from classes.record          import Record
from datafile                import filename

from subs.apps_gform           import apps_gform
from subs.apps_subform         import apps_subform
from subs.apps_userlogin       import apps_userlogin
from subs.apps_plotly_monthly  import apps_plotly_monthly
from subs.apps_plotly_cuisine  import apps_plotly_cuisine

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

# Carrega os dados iniciais
Order.read(filename + 'Trabalho.db')
Restaurant.read(filename + 'Trabalho.db')
Dish.read(filename + 'Trabalho.db')
DeliveryPartner.read(filename + 'Trabalho.db')
Userlogin.read(filename + 'business.db')

@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', user='', password='', resul='')

@app.route('/chklogin', methods=['POST'])
def chklogin():
    user     = request.form['user']
    password = request.form['password']
    resul    = Userlogin.chk_password(user, password)
    if resul == 'Valid':
        session['user'] = user
        return redirect(url_for('index'))
    return render_template('login.html', user=user, password='', resul=resul)

@app.route('/index')
def index():
    return render_template('index.html', ulogin=session.get('user'))

@app.route('/Userlogin', methods=['POST', 'GET'])
def userlogin():
    return apps_userlogin()

@app.route('/gform/<cname>', methods=['POST', 'GET'])
def gform(cname):
    return apps_gform(cname)

@app.route('/subform/<cname>', methods=['POST', 'GET'])
def subform(cname):
    return apps_subform(cname)

# Rotas para gráficos interativos
@app.route('/plot/monthly', methods=['GET', 'POST'])
def plot_monthly():
    return apps_plotly_monthly()

@app.route('/plot/cuisine', methods=['GET', 'POST'])
def plot_cuisine():
    return apps_plotly_cuisine()

@app.route('/logoff')
def logoff():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/track', methods=['GET', 'POST'])
def track():
    lat = lng = None
    track_type = track_id = ''
    option = request.args.get('option') or ('track' if request.method == 'POST' else None)

    if option == 'track':
        track_type = request.form.get('track_type')
        track_id   = request.form.get('track_id')
        if track_id and track_id.isdigit():
            random.seed(int(track_id))
            lat = 38.736946 + random.uniform(-0.01, 0.01)
            lng = -9.142685 + random.uniform(-0.01, 0.01)
    elif option == 'exit':
        return '<h1>Obrigado por usar esta aplicação!</h1>'

    return render_template('index_track.html',
                           track_id=track_id,
                           track_type=track_type,
                           lat=lat,
                           lng=lng,
                           ulogin=session.get('user'))

@app.route('/record', methods=['POST'])
def record():
    data = request.get_json()

    try:
        if data['type'] == 'dish':
            entry = Record.add('dish', {
                'name': data['name'],
                'category': data['category'],
                'price': data['price'],
                'restaurant': data['restaurant']
            })
        elif data['type'] == 'suggestion':
            entry = Record.add('suggestion', {
                'name': data['name'],
                'suggestion': data['suggestion']
            })
        else:
            return jsonify({'error': 'Tipo inválido'}), 400

        return jsonify({'status': 'ok'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/suggestions')
def suggestions():
    with open('records.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    # Filtra só os tipos 'suggestion'
    suggestions = [item for item in data if item.get('type') == 'suggestion']
    return render_template('suggestions.html', suggestions=suggestions)
    



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)