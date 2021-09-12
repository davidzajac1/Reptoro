from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import os, smtplib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from sqlalchemy import Column, Integer, String, Float, create_engine, Date, and_, text, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import cast, case, func, select
from sqlalchemy.dialects.postgresql import array, ARRAY
from sqlalchemy.orm import Session
import json

application = Flask(__name__)

application.secret_key = 'supersecret'
application.permanent_session_lifetime = timedelta(hours=1)

def create_dash_application(flask_app):

    dash_app=dash.Dash(server=flask_app, name="dashboard", url_base_pathname="/dashboard/", external_stylesheets=[dbc.themes.PULSE])

    engine = create_engine('postgresql://postgres:supersecret@davids-personal-db.cbceh2wuhemk.us-east-2.rds.amazonaws.com:5432/davidpersonal')

    Base = declarative_base()
    session = Session(engine)

    options = json.loads(open('static/options.json', 'r').read())

    convert_to_tuple={'All': (0,1), 'True': (1,2), 'False': (0,2)
        , 'Alls': ('Male', 'Female', 'Unknown'), 'Male': ('Male', 'n')
        , 'Female': ('Female','n'), 'Unknowns': ('Unknown', 'n')}


    class Animal(Base):
        __tablename__ = 'master'
        __table_args__ = {'schema': 'morphmarket'}

        url = Column('url', String)
        breeder_url = Column('breeder_url', String, primary_key=True)
        id_num = Column('id_num', String)
        status = Column('status', String)
        first_posted = Column('first_posted', String)
        last_updated = Column('last_updated', String)
        last_renewed = Column('last_renewed', String)
        date_scraped = Column('date_scraped', Date)
        currency = Column('currency', String)
        price = Column('price', Float)
        title = Column('title', String)
        store = Column('store', String)
        traits = Column('traits', String)
        type_ = Column('type', String)
        sex = Column('sex', String)
        maturity = Column('maturity', String)
        birthday = Column('birthday', String)
        shipping = Column('shipping', String)
        trades = Column('trades', String)
        likes = Column('likes', Float)
        offers = Column('offers', String)
        origin = Column('origin', String)
        proven_breeder = Column('proven_breeder', Float)
        clutch = Column('clutch', String)
        diet = Column('diet', String)
        images = Column('images', String)
        weight = Column('weight', String)
        quantity = Column('quantity', String)
        description = Column('description', String)

    # ------------------------------------------------------------------------------
    # dash_app layout
    dash_app.layout = html.Div([
        html.Div(dbc.NavbarSimple(
            children=[
                html.Div(dbc.NavItem(dbc.NavLink("Home", href="/", external_link=True)), style={"font-size":"18px", "margin-right":"5px"}),
                html.Div(dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard", external_link=True)), style={"font-size":"18px", "margin-right":"5px"}),
                # html.Div(dbc.NavItem(dbc.NavLink("Features", href="/#features", external_link=True)), style={"font-size":"18px", "margin-right":"5px"}),
                # html.Div(dbc.NavItem(dbc.NavLink("Pricing", href="/#pricing", external_link=True)), style={"font-size":"18px", "margin-right":"5px"}),
                # html.Div(dbc.NavItem(dbc.NavLink("FAQ", href="/#faq", external_link=True)), style={"font-size":"18px", "margin-right":"5px"}),
                html.Div(dbc.NavItem(dbc.NavLink("Contact Us", href="/contact-us", external_link=True)), style={"font-size":"18px", "margin-right":"5px"}),
                html.Div(dbc.NavItem(dbc.NavLink("Log In", href="/login", external_link=True)), style={"font-size":"18px", "margin-right":"5px"}),
                html.Div(dbc.NavItem(dbc.NavLink("Create Account", href="/create-account", external_link=True)), style={"font-size":"18px", "margin-right":"5px"}),
            ],
            brand="Reptoro",
            brand_href="/",
            brand_style={"font-size":"30px", "font-weight": "bold"},
            color="black",
            dark=True,
            sticky='top'
            ), style={'margin-bottom':'15px'}),
        html.H4(children="Create an Account to Unlock All 100+ Traits!", style={'text-align': 'center', 'margin-bottom': '25px'}),
        dbc.Row([
        html.H6(children="Type:", style={'padding-left': '12%', 'text-align': 'left'}),
        html.Div(dcc.Dropdown(id="type_",
                     options=[
                         {'label': 'Ball Python', 'value': 'Ball Python'},
                         {'label': 'Leopard Gecko', 'value': 'Leopard Gecko'},
                         {'label': 'Boa Constrictor', 'value': 'Boa Constrictor'},
                         {'label': 'Crested Gecko', 'value': 'Crested Gecko'},
                         {'label': 'Corn Snake', 'value': 'Corn Snake'},
                         {'label': 'Central Bearded Dragon', 'value': 'Central Bearded Dragon'},
                         {'label': 'Reticulated Python', 'value': 'Reticulated Python'},
                         {'label': 'Western Hognose', 'value': 'Western Hognose'},
                            ],
                     multi=False,
                     value="Ball Python",
                     clearable=False,
                     ), style={'width':'12%', 'padding-left': '10px', 'text-align': 'left'}),
        html.H6(children="Trait:", style={'padding-left': '30px', 'text-align': 'left'}),
        html.Div(dcc.Dropdown(id="trait",
                     multi=False,
                     clearable=False,
                     ), style={'width':'12%', 'padding-left': '10px', 'text-align': 'left'}),
        html.H6(children="Sex:", style={'padding-left': '30px', 'text-align': 'left'}),
        html.Div(dcc.Dropdown(id="sex",
                        options=[
                     {"label": "All", "value": "Alls"},
                     {"label": "Male", "value": "Male"},
                     {"label": "Female", "value": "Female"},
                     {"label": "Unknown", "value": "Unknowns"}],
                 multi=False,
                 value="Alls",
                 clearable=False,
                 ), style={'width':'6%', 'padding-left': '10px', 'text-align': 'left'}),
        html.H6(children="Proven Breeder:", style={'padding-left': '30px', 'text-align': 'left'}),
        html.Div(dcc.Dropdown(id="proven_breeder",
                 options=[
                     {"label": "All", "value": "All"},
                     {"label": "True", "value": "True"},
                     {"label": "False", "value": "False"}],
                 multi=False,
                 value="All",
                 clearable=False,
                 ), style={'width':'6%', 'padding-left': '10px', 'text-align': 'left'}),
        html.H6(children="Number of Traits:", style={'padding-left': '30px', 'text-align': 'left'}),
        html.Div(id="trait_range", style={'padding-left': '6px', 'text-align': 'left'}),
        html.Div(dcc.RangeSlider(
            id='num_traits',
            min=0,
            max=10,
            step=1,
            value=[0, 10],
        ), style={'width':'10%', 'text-align': 'left'})], style={'width': '100%', 'height':'100%'}),
        html.Div(dcc.Graph(id='trait_price', figure={}, style={'height': "100%"}), style={'height': "40%", 'width': "45%"
            , "padding-top": "15px", 'padding-right': '15px', 'padding-bottom': '15px', 'padding-left': '15px', 'display': 'inline-block'}),

        html.Div(dcc.Graph(id='3d_plot', figure={}, style={'height': "100%"}), style={'height': "40%", 'width': "45%"
            , "padding-top": "15px", 'padding-right': '15px', 'padding-bottom': '15px', 'padding-left': '15px', 'display': 'inline-block'}),

        html.Div(dcc.Graph(id='breeder_count', figure={}, style={'height': "100%"}), style={'height': "40%", 'width': "45%"
            , "padding-top": "15px", 'padding-right': '15px', 'padding-bottom': '15px', 'padding-left': '15px', 'display': 'inline-block'}),

        html.Div(dcc.Graph(id='table', figure={}, style={'height': "100%"}), style={'height': "40%", 'width': "45%"
            , "padding-top": "15px", 'padding-right': '15px', 'padding-bottom': '15px', 'padding-left': '15px', 'display': 'inline-block'}),


    ], style={'backgroundColor': '#F2F6FC', 'height': "100%", 'text-align': 'center', 'width': '100%'})


    # ------------------------------------------------------------------------------
    # Connect the Plotly graphs with Dash Components
    @dash_app.callback(
         [Output(component_id='trait', component_property='options'),
         Output(component_id='trait', component_property='value')],
        Input(component_id='type_', component_property='value')
    )
    def trait_options(type_):
        return options[type_], options[type_][4]['value']

    @dash_app.callback(
         Output(component_id='trait_range', component_property='children'),
        Input(component_id='num_traits', component_property='value'),
    )
    def trait_range(num_traits):
        trait_range = f"{num_traits[0]}-{num_traits[1]}"
        return trait_range


    @dash_app.callback(
         Output(component_id='trait_price', component_property='figure'),
        [Input(component_id='type_', component_property='value'),
        Input(component_id='trait', component_property='value'),
        Input(component_id='sex', component_property='value'),
        Input(component_id='proven_breeder', component_property='value'),
        Input(component_id='num_traits', component_property='value')]
    )

    def line_and_bar(type_, trait, sex, proven_breeder, num_traits):

        sex = convert_to_tuple[sex]
        proven_breeder = convert_to_tuple[proven_breeder]

        stmt = select([func.count(Animal.url).label('Number Sold')
                       , func.avg(Animal.price).label('Average Price')
                       , cast(func.substr(Animal.last_updated,0,5), Integer).label('Year')])\
                        .where(and_(Animal.status == 'sold'
                                , Animal.type_ == type_
                                , Animal.price < 30000
                               ,Animal.traits.contains(trait)
                               ,Animal.sex.in_(sex)
                               ,Animal.proven_breeder.in_(proven_breeder)
                              , func.array_length(cast(Animal.traits, ARRAY(String)),1).between(num_traits[0], num_traits[1])))\
                        .group_by(cast(func.substr(Animal.last_updated,0,5), Integer))

        df = pd.read_sql(stmt, session.connection())


        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Bar(x=df['Year'], y=df['Number Sold'], name="Number Sold"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Line(x=df['Year'], y=df['Average Price'], name="Average Price"),
            secondary_y=True,
        )
        # Set y-axes titles
        fig.update_yaxes(
            title_text="Number Sold",
            secondary_y=False)
        fig.update_yaxes(
            title_text="Average Price",
            secondary_y=True,
            tickprefix="$"
        )


        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1),
            margin=dict(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=0)
        )

        return fig



    @dash_app.callback(
         Output(component_id='breeder_count', component_property='figure'),
        [Input(component_id='type_', component_property='value'),
        Input(component_id='trait', component_property='value'),
        Input(component_id='sex', component_property='value'),
        Input(component_id='proven_breeder', component_property='value'),
        Input(component_id='num_traits', component_property='value')]
    )

    def pie_chart(type_, trait, sex, proven_breeder, num_traits):

        sex = convert_to_tuple[sex]
        proven_breeder = convert_to_tuple[proven_breeder]

        stmt = select([Animal.breeder_url.label('Breeder'), func.count(Animal.url).label('Number Sold') ])\
                        .where(and_(Animal.status == 'sold'
                        , Animal.type_ == type_
                        , Animal.price < 30000
                       ,Animal.traits.contains(trait)
                       ,Animal.sex.in_(sex)
                       ,Animal.proven_breeder.in_(proven_breeder)
                      , func.array_length(cast(Animal.traits, ARRAY(String)),1).between(num_traits[0], num_traits[1])))\
                        .group_by(Animal.breeder_url)

        df = pd.read_sql(stmt, session.connection())

        fig = go.Figure(data=[go.Pie(labels=df['Breeder'], values=df['Number Sold'], hole=.6)])

        fig.update_traces(textposition='inside')

        fig.update_layout(margin=dict(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=0)
        )

        fig.update_traces(hoverinfo='label+percent', textinfo='value')

        fig.update_layout(legend_title_text='Breeder')

        return fig



    @dash_app.callback(
         Output(component_id='3d_plot', component_property='figure'),
        [Input(component_id='type_', component_property='value'),
        Input(component_id='trait', component_property='value'),
        Input(component_id='sex', component_property='value'),
        Input(component_id='proven_breeder', component_property='value'),
        Input(component_id='num_traits', component_property='value')]
    )

    def chart_3d(type_, trait, sex, proven_breeder, num_traits):

        sex = convert_to_tuple[sex]
        proven_breeder = convert_to_tuple[proven_breeder]

        stmt = select([Animal.url, Animal.price.label('Price'), cast(Animal.last_updated, Date).label('Sold'), Animal.maturity.label('Maturity')
                       , (cast(Animal.last_updated, Date) - cast(Animal.first_posted, Date)).label('Days on Market')])\
                        .where(and_(Animal.status == 'sold'
                        , Animal.type_ == type_
                        , Animal.price < 30000
                       ,Animal.traits.contains(trait)
                       ,Animal.sex.in_(sex)
                       ,Animal.proven_breeder.in_(proven_breeder)
                      , func.array_length(cast(Animal.traits, ARRAY(String)),1).between(num_traits[0], num_traits[1])))

        df = pd.read_sql(stmt, session.connection())

        fig = px.scatter_3d(df, x='Sold', y='Days on Market', z='Price',
                  color='Maturity')

        fig.update_layout(margin=dict(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=0)
        )

        fig.update_layout(scene = dict(xaxis = dict(tickformat='%Y', nticks=4, title='Date Sold'), yaxis = dict(nticks=4), zaxis = dict(tickprefix = '$', nticks=4)),xaxis_title='Date Sold')

        fig.update_traces(marker=dict(size=3))

        return fig


    @dash_app.callback(
         Output(component_id='table', component_property='figure'),
        [Input(component_id='type_', component_property='value'),
        Input(component_id='trait', component_property='value'),
        Input(component_id='sex', component_property='value'),
        Input(component_id='proven_breeder', component_property='value'),
        Input(component_id='num_traits', component_property='value')]
    )

    def table(type_, trait, sex, proven_breeder, num_traits):

        sex = convert_to_tuple[sex]
        proven_breeder = convert_to_tuple[proven_breeder]

        stmt = select([("morphmarket.com" + Animal.url).label('URL'), Animal.price.label('Price')
                    , (cast(Animal.last_updated, Date) - cast(Animal.first_posted, Date)).label('Days on Market')])\
                    .where(and_(Animal.status == 'sold'
                    , Animal.price != None
                    , Animal.price < 30000
                    , Animal.type_ == type_
                   ,Animal.traits.contains(trait)
                   ,Animal.sex.in_(sex)
                   ,Animal.proven_breeder.in_(proven_breeder)
                  , func.array_length(cast(Animal.traits, ARRAY(String)),1).between(num_traits[0], num_traits[1])))\
                    .order_by(Animal.price.desc()).limit(50)

        df = pd.read_sql(stmt, session.connection())


        fig = go.Figure(data=[go.Table(columnwidth = [130,30,30],
        header=dict(values=list(df.columns)),
        cells=dict(values=[df['URL'], df['Price'], df['Days on Market']]))
                   ])

        fig.update_layout(margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0)
        )

        return fig

    return dash_app




create_dash_application(application)

users =[('test@gmail.com','testpass')]


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

        if request.form['logout'] == 'logout':
            session.pop('email', None)
            return redirect('/')

        else:
            fullname = request.form['fullname']
            email = request.form['email']
            message = request.form['message']

            email_contents = f"""\nMessage from {fullname}, reply to email {email}:\n\n{message}"""

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('dmznotifications@gmail.com', '1Ogsy#13notifications')
            server.sendmail('dmznotifications@gmail.com', 'davidzajac1996@gmail.com', email_contents)
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
    application.run(debug=True)
