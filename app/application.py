from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import smtplib, os
from dashboards.traits_dashboard import traits_dashboard
from dashboards.breeder_dashboard import breeder_dashboard
from dashboards.dataframes import get_df
from flask_caching import Cache


cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

application = Flask(__name__)

cache.init_app(application)

application.secret_key = 'supersecret'
application.permanent_session_lifetime = timedelta(hours=1)


@cache.cached(timeout=500, key_prefix='get_df')
def get_dataframe():
    return get_df()

df = get_dataframe()

traits_dashboard(application, df)
breeder_dashboard(application, df)

users =[(os.environ['TESTUSER'],os.environ['TESTPASS'])]


@application.route('/', methods=['POST', 'GET'])
def home():

    if request.method == 'POST':

        if request.form['logout'] == 'logout':
            session.pop('email', None)
            return render_template('home.html')

    return render_template('home.html')



@application.route('/login', methods=['POST', 'GET'])
def login():

    if 'email' in session:
        return redirect(url_for("dashboard"))

    elif request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        if (email, password) in users:
            session.permanent = True
            session['email'] = email

            return redirect(url_for("dashboard"))
        else:
            return render_template('login.html')

    return render_template('login.html')


@application.route('/create-account', methods=['POST', 'GET'])
def create_account():

    if 'email' in session:
        return redirect(url_for("dashboard"))

    elif request.method == 'POST':

        return render_template('create-account.html', no_new_users=True)

    return render_template('create-account.html')



@application.route('/contact-us', methods=['POST', 'GET'])
def contact_us():

    if request.method == 'POST':


        fullname = request.form['fullname']
        email = request.form['email']
        message = request.form['message']

        email_contents = f"""\nMessage from {fullname}, reply to email {email}:\n\n{message}"""

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(os.environ['EMAILFROM'], os.environ['EMAILFROMPASS'])
        server.sendmail(os.environ['EMAILFROM'], os.environ['EMAILTO'], email_contents)
        server.quit()

        return render_template('contact-us.html', submitted=True)

    else:

        return render_template('contact-us.html')


@application.route('/privacy', methods=['GET'])
def privacy():

    return render_template('privacy.html')

@application.route('/terms', methods=['GET'])
def terms():

    return render_template('terms.html')



if __name__ == "__main__":
    application.run()
