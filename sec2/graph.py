from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import random
import pandas as pd

df = px.data.gapminder()

def gen_color(nc):
    col = []
    for _ in range(nc):
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        hex_color = '#{:02x}{:02x}{:02x}'.format(r,g,b)
        col.append(hex_color)
    return col

unique_country = df['country'].unique()
random_color_list = gen_color(len(unique_country))
country_colors = {country: random_color_list[i%len(random_color_list)] for i, country in enumerate(unique_country)}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(
        id='dpdn2', 
        value=['Germany', 'Brazil'], 
        multi=True, 
        options=[{'label': x, 'value': x} for x in df.country.unique()]
    ),
    html.Div([
        dcc.Graph(id='pie-graph', figure={}, className='six columns'),
        dcc.Graph(
            id='my-graph', 
            figure={}, 
            clickData=None, 
            hoverData=None,
            config={
                'staticPlot': False,
                'scrollZoom': True,
                'doubleClick': 'reset',
                'showTips': False,
                'displayModeBar': True,  # Set True to enable modebar
                'watermark': True,
            },
            className='six columns'
        )
    ]),
    dcc.Graph(id='bar-graph', figure={}, className='six columns')
])

@app.callback(
    Output('my-graph', 'figure'),
    Input('dpdn2', 'value')
)
def update_graph(country_chosen):
    dff = df[df.country.isin(country_chosen)]
    fig = px.line(dff, x='year', y='gdpPercap', color='country', hover_data=["lifeExp", "pop", "iso_alpha"],color_discrete_map=country_colors)
    fig.update_traces(mode='lines+markers')
    return fig

@app.callback(
    Output('pie-graph', 'figure'),
    [Input('my-graph', 'hoverData'),
     Input('my-graph', 'clickData'),
     Input('my-graph','selectedData'),
     Input('dpdn2', 'value')]
)
def update_side_graph(hov_data, clk_data, slct_data, country_chosen):
    if hov_data is None:
        dff2 = df[df.country.isin(country_chosen)]
        dff2 = dff2[dff2.year == 1952]
        fig2 = px.pie(dff2, values='pop', names='country', color='country', title='Population for 1952',color_discrete_map=country_colors)
        return fig2
    else:
        dff2 = df[df.country.isin(country_chosen)]
        hov_year = hov_data['points'][0]['x']
        dff2 = dff2[dff2.year == hov_year]
        fig2 = px.pie(dff2, values='pop', names='country', color='country', title=f'Population for: {hov_year}',color_discrete_map=country_colors)
        return fig2

@app.callback(
    Output('bar-graph', 'figure'),
    Input('my-graph', 'selectedData'),
    Input('dpdn2', 'value')
)
def update_bar_chart(selected_data, country_chosen):
    if selected_data is not None:
        selected_country = [point['customdata'][2] for point in selected_data['points']]
        selected_year = [point['x'] for point in selected_data['points']]
        print('data row', selected_country)
        print('year:',selected_year)

        sd_df = pd.DataFrame({
            'country': [df.loc[df['iso_alpha']==country, 'country'].iloc[0] for country in selected_country],
            'year' : selected_year,
            'gdpPercap': [df.loc[(df['iso_alpha']==country)&(df['year']==year), 'gdpPercap'].iloc[0] for country, year in zip(selected_country,selected_year)]
        })

        fig_bar = px.bar(sd_df, x='year', y='gdpPercap', color='country', barmode='group', title='GDP per capita for selected countries',color_discrete_map=country_colors)
        return fig_bar
    return {}

if __name__ == '__main__':
    app.run_server(debug=True)
