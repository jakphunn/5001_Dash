import dash
from dash import dcc, html, Input, Output
from app import app
from apps import scatter_layout, histogram_layout, line_layout, treemap_layout
import dash_bootstrap_components as dbc

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "15rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Hi!", className="display-4"),
        html.Hr(),
        html.P(
            "This is 6610412008's assignment.", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("home", href="/", active="exact"),
                dbc.NavLink("scatter", href="/apps/scatter_layout", active="exact"),
                dbc.NavLink("histogram", href="/apps/histogram_layout", active="exact"),
                dbc.NavLink("treemap", href="/apps/treemap_layout", active="exact"),
                dbc.NavLink("linechart", href="/apps/line_layout", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id = "page-content", style = CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False), sidebar, content
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/scatter_layout':
        return scatter_layout.layout
    if pathname == '/apps/histogram_layout':
        return histogram_layout.layout
    if pathname == '/apps/treemap_layout':
        return treemap_layout.layout
    if pathname == '/apps/line_layout':
        return line_layout.layout
    if pathname == '/':
        return "nothing to see here. please choose from the sidebar :)"

if __name__ == '__main__':
    app.run_server(debug=False)
    
#Exercise
# 1. Change menu3 to another graph (Not histogram)
# 2. Add the 4th menu (menu4) link to line graph
