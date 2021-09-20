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
from scipy.stats import linregress
from datetime import datetime
import json
from dash import dash_table



def deals_dashboard(flask_app):

    dash_app=dash.Dash(server=flask_app, name="deals_dashboard", url_base_pathname="/deals_dashboard/", external_stylesheets=[dbc.themes.PULSE])

    dash_app.title = "Reptoro"

    engine = create_engine('postgresql://postgres:supersecret@davids-personal-db.cbceh2wuhemk.us-east-2.rds.amazonaws.com:5432/davidpersonal')

    Base = declarative_base()
    session = Session(engine)

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
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("Trait", href="/dashboard", external_link=True),
                        dbc.DropdownMenuItem("Breeder", href="/breeder_dashboard", external_link=True),
                        dbc.DropdownMenuItem("Best Deals", href="/deals_dashboard", external_link=True),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Dashboards",
                    style={"font-size":"18px", "margin-right":"5px"}
                ),
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
        html.H4(children="Create an Account to Unlock All 1,000+ Deals!", style={'text-align': 'center', 'margin-bottom': '25px'}),
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
                     style = {'text-align': 'left'}
                     ), style={'width':'12%', 'padding-left': '10px'}),
            ], style={'width': '100%', 'height':'100%'}),
        html.H5(children="Select a Deal to view it's Comparable Sales", style={'text-align': 'center'}),
        html.Div(dash_table.DataTable(id='deals', selected_cells={'row': 0, 'column': 0}, style_table={'height': '300px', 'overflowY': 'auto'}), style={'height': "100%", 'width': "90%"
            , "padding-top": "15px", 'padding-right': '15px', 'padding-bottom': '15px', 'padding-left': '15px', 'display': 'inline-block'}),

        html.Div(dcc.Graph(id='scatter', figure={}, style={'height': "100%"}), style={'height': "100%", 'width': "55%"
            , "padding-top": "15px", 'padding-right': '15px', 'padding-bottom': '15px', 'padding-left': '15px', 'display': 'inline-block', 'margin-bottom': '30px'}),

        html.Div(dcc.Graph(id='metrics', figure={}, style={'height': "100%"}), style={'height': "40%", 'width': "35%"
            , "padding-top": "15px", 'padding-right': '15px', 'padding-bottom': '15px', 'padding-left': '15px', 'display': 'inline-block', 'margin-bottom': '30px'}),

        dcc.Store(id='dataframe'),
        dcc.Store(id='comp_metrics')
    ], style={'backgroundColor': '#F2F6FC', 'height': "100%", 'text-align': 'center', 'width': '100%'})


    # ------------------------------------------------------------------------------
    # Connect the Plotly graphs with Dash Components
    @dash_app.callback(Output('dataframe', 'data'),
        Input(component_id='type_', component_property='value'),
    )

    def first_query(type_):

        stmt=f"""
            select concat('morphmarket.com', animals.url) as "URL", cast(averages.average/animals.price as integer) as ratio
            , animals.traits as "Traits", animals.price as "Price"
            , cast(averages.average as integer) as "Price of Comparables" from 
            (select url, price, traits from morphmarket.master
            where status = 'for sale' and maturity = 'Baby' and "type" = '{type_}' and price between 5 and 30000) as animals
            inner join
            (select avg(price) as average, traits from morphmarket.master
            where status = 'sold' and maturity = 'Baby' and "type" = '{type_}' and price between 5 and 30000 group by traits
            having count(price) > 3) as averages
            on animals.traits = averages.traits order by ratio desc limit 100;
        """

        df = pd.read_sql(stmt, session.connection())

        return df.to_json(date_format='iso', orient='split')



    @dash_app.callback([Output(component_id='deals', component_property='data'),
    Output(component_id='deals', component_property='columns')],
         Input('dataframe', 'data')
    )

    def deals(data):

        df = pd.read_json(data, orient='split')[['URL', 'Price', 'Price of Comparables', 'Traits']]
        df['Traits'] = df['Traits'].apply(lambda x: x.replace('{','').replace('}','').replace('"','').replace(',',', '))


        return df.to_dict('records'), [{"name": 'URL', "id": 'URL'}
                                        , {"name": 'Price', "id": 'Price'}
                                        , {"name": 'Price of Comparables', "id": 'Price of Comparables'}
                                        , {"name": 'Traits', "id": 'Traits'}]


    @dash_app.callback([Output(component_id='scatter', component_property='figure'), Output(component_id='comp_metrics', component_property='data')],
         [Input('dataframe', 'data'), Input('deals', 'active_cell')
         , Input(component_id='type_', component_property='value')]
    )

    def scatter(data, cell, type_):

        if cell == None: cell = {'row':0}

        df_original = pd.read_json(data, orient='split')

        traits = df_original['Traits'].iloc[cell['row']]

        comp_metrics = (int(df_original['Price of Comparables'].iloc[cell['row']]), int(df_original['Price'].iloc[cell['row']]))

        stmt = select([Animal.url.label('URL'), Animal.price.label('Price'), Animal.last_updated.label('Date Sold')])\
                    .where(and_(Animal.status == 'sold', Animal.maturity == 'Baby'
                        , Animal.type_ == type_, Animal.price.between(5,30000), Animal.traits == traits))

        df = pd.read_sql(stmt, session.connection())

        fig = px.scatter(df, x="Date Sold", y="Price")

        fig.update_yaxes(
        tickprefix="$"
        )

        fig.update_layout(
        title={
        'text': "Comparables",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        margin=dict(
        l=10,
        r=10,
        b=10,
        t=50,
        pad=0)
        )

        return fig, comp_metrics

    
    @dash_app.callback(Output(component_id='metrics', component_property='figure'),
         Input('comp_metrics', 'data')
    )

    def metrics(comp_metrics):

        fig = go.Figure(go.Indicator(
            title = 'Asking Price Compared to Comparables',
            mode = "number+delta",
            value = comp_metrics[1],
            number = {'prefix': "$"},
            delta = {'position': "top", 'reference': comp_metrics[0], 'valueformat': '$'},
            domain = {'x': [0, 1], 'y': [0, 1]}))


        return fig



    return dash_app

