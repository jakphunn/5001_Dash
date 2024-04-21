# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from app import app

df = pd.read_csv('https://github.com/chris1610/pbpython/blob/master/data/cereal_data.csv?raw=True')

lineFig = px.line(df, x='sugars',y='rating', color='mfr', title='Rating distribution')

layout = html.Div(children=[

      html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        dcc.Graph(
            id='lineID',
            figure=lineFig
        ),
    
     ], style={'padding': 10, 'flex': 1})