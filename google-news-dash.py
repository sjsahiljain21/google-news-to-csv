import feedparser
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], prevent_initial_callbacks=True)

# Create server variable with Flask server object for use with gunicorn
# server = app.server


app.layout = html.Div([

    dbc.Row(
        dbc.Col(html.H1("Google News API"),  style = {'textAlign': 'center'}),
    ),

    html.Br(),
    html.Br(),

    dbc.Row(
        [
        
        dbc.Col(html.Div(dbc.Input(id = 'keywords', placeholder = 'Enter Keyword - eg. SaaS', type = 'text'))),
        
        dbc.Col(dcc.Dropdown(id='dropdown-time',
         options=[
            {'label': 'Anytime', 'value': ''},
            {'label': 'Past hour', 'value': '%20when%3A1h'},
            {'label': 'Past 24 hour', 'value': '%20when%3A1d'},
            {'label': 'Past week', 'value': '%20when%3A7d'},
            {'label': 'Past year', 'value': '%20when%3A1y'},
            ],
            value='IN',
            clearable=False,
         )),

         dbc.Col(dcc.Dropdown(id='dropdown-country',
    options=[
        {'label': 'India', 'value': 'IN'},
        {'label': 'Malaysia', 'value': 'MY'},
        {'label': 'Singapore', 'value': 'SG'},
        {'label': 'United States', 'value': 'US'},
        {'label': 'Australia', 'value': 'AU'},
        # {'label': 'Botswana', 'value': 'SF'},
        # {'label': 'Canada', 'value': 'SF'},
        # {'label': 'Ethiopia', 'value': 'SF'},
        # {'label': 'Ghana', 'value': 'SF'},
        # {'label': 'Indonesia', 'value': 'SF'},
        # {'label': 'Ireland', 'value': 'SF'},
        # {'label': 'Israel', 'value': 'SF'},
        # {'label': 'Kenya', 'value': 'SF'},
        # {'label': 'Namibia', 'value': 'SF'},
        # {'label': 'New Zealand', 'value': 'SF'},
        # {'label': 'Nigeria', 'value': 'SF'},
        # {'label': 'Pakistan', 'value': 'SF'},
        # {'label': 'Philippines', 'value': 'SF'},
        # {'label': 'South Africa', 'value': 'SF'},
        # {'label': 'Tanzania', 'value': 'SF'},
        # {'label': 'Uganda', 'value': 'SF'},
        # {'label': 'United Kingdom', 'value': 'SF'},
        # {'label': 'Zimbabwe', 'value': 'SF'},
    ],
    value='IN',
    clearable=False,
)), 
    ]), 

dbc.Button('Submit', id='submit-button', outline=True, color="success"),
html.Br(),
html.Br(),
dcc.Loading(children=[html.Div(id='table')], type="default"),
html.Br(),
html.Br(),
dcc.Loading(children=[html.Div(dcc.Graph(id='bar-chart', figure={}))], type="default")
])

@app.callback(Output('table', 'children'),
              [Input('submit-button', 'n_clicks')],
             [State('keywords', 'value'),
             State('dropdown-time', 'value'),
             State('dropdown-country', 'value')])

def update_table(n_clicks, keywords_value, dropdown_time_value, dropdown_country_value):
    if len(keywords_value.split()) == 1:
        NewsFeed = feedparser.parse('https://news.google.com/rss/search?q={}{}&hl=en-{}&gl={}&ceid={}:en'.format(keywords_value,dropdown_time_value, dropdown_country_value, dropdown_country_value, dropdown_country_value))
        entry = NewsFeed.entries
        df = pd.json_normalize(entry)
        df_col = df[['link', 'title', 'published', 'source.href', 'source.title']]
        df_col.columns = ['Link', 'Headline', 'PublishedAt', 'Domain', 'Publication']

        # data=news_df_merged_1.to_dict('records')
    else:
        keywords_value = keywords_value.split()
        keywords_value = "%20".join(keywords_value)
        NewsFeed = feedparser.parse('https://news.google.com/rss/search?q={}{}&hl=en-{}&gl={}&ceid={}:en'.format(keywords_value,dropdown_time_value, dropdown_country_value, dropdown_country_value, dropdown_country_value))
        entry = NewsFeed.entries
        df = pd.json_normalize(entry)
        df_col = df[['link', 'title', 'published', 'source.href', 'source.title']]
        df_col.columns = ['Link', 'Headline', 'PublishedAt', 'Domain', 'Publication']
        # data=news_df_merged_1.to_dict('records')
        # columns=[{"name": i, "id": i} for i in df.columns]
    return dash_table.DataTable( 
            columns=[{"name": i, "id": i} for i in df_col.columns],
            data=df_col.to_dict('records'),
            filter_action = 'native',
            sort_action = 'native',
            sort_mode = 'single',
            page_current = 0,
            page_size = 10,
            style_cell={                # ensure adequate header width when text is shorter than cell's text
                    'minWidth': 95, 'maxWidth': 95, 'width': 95
                },
            style_data={                # overflow cells' content into multiple lines
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
            export_format="csv")

@app.callback(Output('bar-chart', 'figure'),
              [Input('submit-button', 'n_clicks')],
             [State('keywords', 'value'),
             State('dropdown-time', 'value'),
             State('dropdown-country', 'value')])

def update_graphs(n_clicks, keywords_value, dropdown_time_value, dropdown_country_value):
    if len(keywords_value.split()) == 1:
        NewsFeed = feedparser.parse('https://news.google.com/rss/search?q={}{}&hl=en-{}&gl={}&ceid={}:en'.format(keywords_value,dropdown_time_value, dropdown_country_value, dropdown_country_value, dropdown_country_value))
        entry = NewsFeed.entries
        df = pd.json_normalize(entry)
        df_col_bar = df[['link', 'title', 'published', 'source.href', 'source.title']]
        df_col_bar.columns = ['Link', 'Headline', 'PublishedAt', 'Domain', 'Publication']
        df_col_groupby = df_col_bar[['Publication']].value_counts().reset_index()
        df_col_groupby.columns = ['Publications', 'Count']
        fig = px.bar(df_col_groupby, x='Publications', y='Count')

    else:
        keywords_value = keywords_value.split()
        keywords_value = "%20".join(keywords_value)
        NewsFeed = feedparser.parse('https://news.google.com/rss/search?q={}{}&hl=en-{}&gl={}&ceid={}:en'.format(keywords_value,dropdown_time_value, dropdown_country_value, dropdown_country_value, dropdown_country_value))
        entry = NewsFeed.entries
        df = pd.json_normalize(entry)
        df_col_bar = df[['link', 'title', 'published', 'source.href', 'source.title']]
        df_col_bar.columns = ['Link', 'Headline', 'PublishedAt', 'Domain', 'Publication']
        df_col_groupby = df_col_bar[['Publication']].value_counts().reset_index()
        df_col_groupby.columns = ['Publications', 'Count']
        fig = px.bar(df_col_groupby, x='Publications', y='Count')
    return fig

if __name__ == '__main__':
    app.run(debug=True)
