import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from scipy.stats import linregress
from datetime import datetime
import json



def breeder_dashboard(flask_app, df0):

    dash_app=dash.Dash(server=flask_app, name="breeder_dashboard", url_base_pathname="/breeder_dashboard/", external_stylesheets=[dbc.themes.PULSE])

    dash_app.title = "Reptoro"

    breeder_options = json.loads(open('static/breeders.json', 'r').read())

    # ------------------------------------------------------------------------------
    # dash_app layout
    dash_app.layout = html.Div([
        html.Div(dbc.NavbarSimple(
            children=[
                html.Div(dbc.NavItem(dbc.NavLink("Traits Dashboard", href="/dashboard", external_link=True)), style={"font-size":"18px", "margin-right":"5px"}),
                html.Div(dbc.NavItem(dbc.NavLink("Breeders Dashboard", href="/breeder_dashboard", external_link=True)), style={"font-size":"18px", "margin-right":"5px"}),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("Home", href="/", external_link=True),
                        dbc.DropdownMenuItem("Create an Account", href="/create-account", external_link=True),
                        dbc.DropdownMenuItem("Contact Us", href="/contact-us", external_link=True),
                        dbc.DropdownMenuItem("Login", href="/login", external_link=True),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="More",
                    style={"font-size":"18px", "margin-right":"5px"}
                ),
            ],
            brand="Reptoro",
            brand_external_link=True,
            brand_href= '/',
            brand_style={"font-size":"30px", "font-weight": "bold"},
            color="black",
            dark=True,
            sticky='top'
            ), style={'margin-bottom':'15px'}),
        html.H4(children="Create an Account to Unlock All 8,000+ Breeders!", style={'text-align': 'center', 'margin-bottom': '25px'}),
        dbc.Row([
        html.H6(children="Breeder:", style={'padding-left': '12%', 'text-align': 'left'}),
        html.Div(dcc.Dropdown(id="breeder",
                    options=breeder_options,
                     multi=False,
                     value="nerd",
                     clearable=False,
                     ), style={'width':'20%', 'padding-left': '10px', 'text-align': 'left'}),
            ], style={'width': '100%', 'height':'100%'}),
        html.Div(dcc.Graph(id='bar_revenue', figure={}, style={'height': "100%"}), style={'height': "100%", 'width': "45%"
            , "padding-top": "15px", 'padding-right': '15px', 'padding-bottom': '15px', 'padding-left': '15px', 'display': 'inline-block'}),

        html.Div(dcc.Graph(id='pie_count', figure={}, style={'height': "100%"}), style={'height': "100%", 'width': "45%"
            , "padding-top": "15px", 'padding-right': '15px', 'padding-bottom': '15px', 'padding-left': '15px', 'display': 'inline-block'}),

        html.Div(dcc.Graph(id='scatter', figure={}, style={'height': "100%"}), style={'height': "40%", 'width': "90%"
            , "padding-top": "15px", 'padding-right': '15px', 'padding-bottom': '15px', 'padding-left': '15px', 'display': 'inline-block', 'margin-bottom': '30px'}),

        dcc.Store(id='dataframe')
    ], style={'backgroundColor': '#F2F6FC', 'height': "100%", 'text-align': 'center', 'width': '100%'})


    # ------------------------------------------------------------------------------
    # Connect the Plotly graphs with Dash Components
    @dash_app.callback(Output('dataframe', 'data'),
        Input(component_id='breeder', component_property='value'),
    )

    def first_query(breeder):

        df = df0
        df = df[['price', 'last_updated', 'type', 'breeder_url']]
        df = df.dropna()
        df = df[df['breeder_url'] == breeder]
        df = df.rename(columns={'price': 'Price', 'last_updated': 'Sold', 'type': 'Type'})

        return df.to_json(date_format='iso', orient='split')


    @dash_app.callback(Output(component_id='scatter', component_property='figure'),
         Input('dataframe', 'data')
    )

    def scatter(data):

        df = pd.read_json(data, orient='split')[['Price', 'Sold', 'Type']]
        df = df.rename(columns={'Sold': 'Date Sold'})


        fig = px.scatter(df, x="Date Sold", y="Price", color='Type')

        fig.update_yaxes(
        tickprefix="$"
        )

        fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1),
        legend_title_text=None,
        margin=dict(
        l=10,
        r=10,
        b=10,
        t=10,
        pad=0)
        )

        return fig


    @dash_app.callback(
         Output(component_id='bar_revenue', component_property='figure'),
         Input('dataframe', 'data')
    )

    def bar(data):

        df = pd.read_json(data, orient='split')[['Price', 'Sold']]
        df['Year'] = pd.to_datetime(df['Sold']).dt.year
        df = df.drop(columns='Sold')
        df = df.groupby('Year').agg('sum')
        df = df.reset_index()
        df = df.rename(columns={'Price': 'Revenue'}).sort_values('Year')
        df['Forecast'] = 'Data'

        forecast = linregress(df['Year'][:-1], df['Revenue'][:-1])
        this_year_forecast = forecast[1] + forecast[0] * datetime.now().year
        if this_year_forecast > df['Revenue'].iloc[-1]:
            df = df.append({'Year': datetime.now().year
                            , 'Revenue': this_year_forecast - df['Revenue'].iloc[-1]
                            , 'Forecast': 'Forecast'}, ignore_index=True)
        next_year_forecast = forecast[1] + forecast[0] * (datetime.now().year + 1)
        if next_year_forecast > 0:
            df = df.append({'Year': datetime.now().year + 1
                                , 'Revenue': next_year_forecast
                                , 'Forecast': 'Forecast'}, ignore_index=True)

        fig = px.bar(df, x='Year', y='Revenue', color='Forecast')

        fig.update_yaxes(
        tickprefix="$"
        )


        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1),
            legend_title_text=None,
            margin=dict(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=0)
        )

        return fig


    @dash_app.callback(
         Output(component_id='pie_count', component_property='figure'),
        Input('dataframe', 'data')
    )

    def pie_chart(data):

        df = pd.read_json(data, orient='split')[['Type', 'Price', 'Sold']]
        df = df[pd.to_datetime(df['Sold']).dt.year == (datetime.now().year - 1)].drop(columns='Sold')
        df = df.groupby('Type').agg('count')
        df = df.reset_index()
        df = df.rename(columns={'Price': 'Number Sold'})


        fig = go.Figure(data=[go.Pie(labels=df['Type'], values=df['Number Sold'], hole=.6)])

        fig.update_traces(textposition='inside')

        fig.update_layout(margin=dict(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=0)
        )

        fig.update_traces(hoverinfo='label+percent', textinfo='value')

        fig.update_layout(legend_title_text=f"{datetime.now().year - 1} Number of Animals Sold")

        return fig



    return dash_app

