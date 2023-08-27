from flask import Flask,abort,redirect,render_template,jsonify,session,url_for,request,flash
from src.components.data_ingestion import DataIngestion
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from src.utils import sqli_connect
import numpy as np
from src.exception import CustomException
import json
import os


app = Flask(__name__)

load_dotenv()
appConf = {
    "OAUTH2_CLIENT_ID": os.getenv('OAUTH2_CLIENT_ID'),
    "OAUTH2_CLIENT_SECRET": os.getenv('OAUTH2_CLIENT_SECRET'),
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": os.getenv('FLASK_SECRET'),
    "FLASK_PORT": 5000
}

app.secret_key = appConf.get("FLASK_SECRET")
oauth = OAuth(app)

oauth.register(
    "myApp",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'{appConf.get("OAUTH2_META_URL")}',
)

#======================================= Home ========================================#
@app.route('/')
def home():
    return render_template('home.html',session=session.get('person'))

#====================================== Google Authentication ========================#
@app.route("/sign-in-google")
def googleCallback():
    # fetch access token and id token using authorization code
    token = oauth.myApp.authorize_access_token()
    session["person"] = token
    return redirect(url_for("base"))

@app.route("/google-login")
def google_login():
    if "person" in session:
        abort(404)
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))

@app.route("/logout")
def logout():
    session.pop("person", None)
    return render_template('home.html',session=session.get("person"))  

#====================================== Login ===================================#
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('name')
        password = request.form.get('password')
    conn = sqli_connect('database')
    cursor = conn.cursor()
    query = "SELECT username, password from user101 where username='{u}' and password='{p}';".format(u=username,p=password)
    rows = cursor.execute(query)
    rows = rows.fetchall()
    if len(rows) == 1:
        token = {'userinfo':{'name':username}}
        session['person'] = token
        return render_template('base.html',session=session.get('person'))
    else:
        message_alert = "Invalid username and password"
        flash(message_alert)
        return render_template('login.html')

#====================================== Register ===================================#
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('login.html')  
    else:
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
    if password == confirm_password:   
        conn = sqli_connect('database')
        cursor = conn.cursor()     
        query = "INSERT INTO user101 VALUES('{u}','{e}','{p}');".format(u=username,e=email,p=password)
        try:
            cursor.execute(query)
            conn.commit()
            conn.close()
            flash("Registered Successfully")
            return render_template('login.html')
        except Exception as e:
            flash("User already exist")
            return render_template('login.html')
    else:
        flash("Check confirm password")
        return render_template('login.html')  

#====================================== Dashboard ===================================#  
@app.route('/base')
def base():
    data_obj = DataIngestion()
    data = data_obj.initiate_data_ingestion()

    # pi chart info
    pi_values = list(data['online_order'].value_counts().values)
    total_count = pi_values[0] + pi_values[1]
    pi_data = {
        "labels": ["Online", "Offline"],
        "values": [int(pi_values[0]), int(pi_values[1])],
        "percentages": [round(int(pi_values[0])/total_count * 100), round(int(pi_values[1])/total_count * 100)]
    }

    # bar plot
    bar_details = data.groupby('name')
    bar_data = bar_details['votes'].agg(np.sum).sort_values(ascending = False)[:5]
    bar_label = list(bar_data.index)
    bar_values = list(bar_data.values)
    for index in range(len(bar_values)):
        bar_label[index] = str(bar_label[index])
        bar_values[index] = int(bar_values[index]) 

    #restaurant types
    types = data['rest_type'].value_counts().head(20)
    types_label = list(types.index)
    types_values = list(types.values) 
    for index in range(len(types)):
        types_label[index] = str(types_label[index])
        types_values[index] = int(types_values[index]) 

    # cuisines plot
    cuisines = data['cuisines'].value_counts()[:5]
    cuisines_labels = list(cuisines.index)
    cuisines_values = list(cuisines.values)
    for index in range(len(cuisines_values)):
        cuisines_labels[index] = str(cuisines_labels[index])
        cuisines_values[index] = int(cuisines_values[index])   

    # locations
    location = data['location'].value_counts()[:5]
    loc_label = list(location.index)  
    loc_values = list(location.values)
    for index in range(len(loc_values)):
        loc_label[index] = str(loc_label[index])
        loc_values[index] = int(loc_values[index])       
    return render_template('base.html',session = session.get('person'),pi_data=json.dumps(pi_data),bar_label=json.dumps(bar_label),bar_values=json.dumps(bar_values),types_label=json.dumps(types_label),types_values=json.dumps(types_values),cuisines_labels=json.dumps(cuisines_labels),cuisines_values=json.dumps(cuisines_values),loc_label=json.dumps(loc_label),loc_values=json.dumps(loc_values))   

@app.route('/show_div')
def show_div():
    return jsonify(success=True)    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)