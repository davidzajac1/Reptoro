import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import json


def traits_dashboard(flask_app, df0):

    dash_app=dash.Dash(server=flask_app, name="dashboard", url_base_pathname="/dashboard/", external_stylesheets=[dbc.themes.PULSE])

    dash_app.title = "Reptoro"

    options = json.loads(open('static/options.json', 'r').read())

    convert_to_tuple={'All': (0,1), 'True': (1,2), 'False': (0,2)
        , 'Alls': ('Male', 'Female', 'Unknown'), 'Male': ('Male', 'n')
        , 'Female': ('Female','n'), 'Unknowns': ('Unknown', 'n')}

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
        html.Div(dcc.Graph(id='trait_price', figure={}, style={'height': "100%"}), style={'height': "300px", 'width': "90%"
            , "padding-top": "15px", 'padding-right': '15px', 'padding-bottom': '15px', 'padding-left': '15px', 'display': 'inline-block'}),

        html.Div(dcc.Graph(id='3d_plot', figure={}, style={'height': "100%"}), style={'height': "40%", 'width': "45%"
            , "padding-top": "15px", 'padding-right': '15px', 'padding-bottom': '15px', 'padding-left': '15px', 'display': 'inline-block', 'margin-bottom': '30px'}),

        html.Div(dcc.Graph(id='breeder_count', figure={}, style={'height': "100%"}), style={'height': "40%", 'width': "45%"
            , "padding-top": "15px", 'padding-right': '15px', 'padding-bottom': '15px', 'padding-left': '15px', 'display': 'inline-block', 'margin-bottom': '30px'}),
        dcc.Store(id='dataframe')
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

    @dash_app.callback(Output('dataframe', 'data'),
        [Input(component_id='type_', component_property='value'),
        Input(component_id='trait', component_property='value'),
        Input(component_id='sex', component_property='value'),
        Input(component_id='proven_breeder', component_property='value'),
        Input(component_id='num_traits', component_property='value')]
    )

    def first_query(type_, trait, sex, proven_breeder, num_traits):

        sex = convert_to_tuple[sex]
        proven_breeder = convert_to_tuple[proven_breeder]
        
        df = df0
        df = df[df['type'] == type_]
        df = df[df['traits'].str.contains(trait) == True]
        df = df[df['sex'].isin(sex)]
        df = df[df['proven_breeder'].isin(proven_breeder)]
        df['num_traits'] = df['traits'].str.count(',') + 1
        df = df[df['num_traits'] >= num_traits[0]]
        df = df[df['num_traits'] <= num_traits[1]]
        df = df[['url', 'breeder_url', 'last_updated','price', 'maturity', 'Days on Market']]

        return df.to_json(date_format='iso', orient='split')


    @dash_app.callback(
         Output(component_id='trait_price', component_property='figure'),
         Input('dataframe', 'data')
    )

    def line_and_bar(data):

        df = pd.read_json(data, orient='split')[['price', 'last_updated']]
        df['Year'] = pd.to_datetime(df['last_updated']).dt.year
        df = df.drop(columns='last_updated')
        df = df.groupby('Year').agg({'price': ['mean', 'count']})
        df.columns = df.columns.droplevel(0)
        df = df.reset_index()
        df = df.rename(columns={'count': 'Number Sold', 'mean': 'Average Price'}).sort_values('Year')


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
        Input('dataframe', 'data')
    )

    def pie_chart(data):

        df = pd.read_json(data, orient='split')[['url', 'breeder_url']]
        df = df.groupby('breeder_url').agg('count')
        df = df.reset_index()
        df = df.rename(columns={'breeder_url': 'Breeder', 'url': 'Number Sold'})


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
         Input('dataframe', 'data')
    )

    def chart_3d(data):

        df = pd.read_json(data, orient='split')[['last_updated', 'price', 'maturity', 'Days on Market']]
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        df = df.rename(columns={"price": "Price", "maturity": "Maturity", "last_updated": "Sold"})

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


    return dash_app

