import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import flask
import psycopg2

server = flask.Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)


colors = {
        'background': 'rgba(190, 231, 233, 0.3)',
        'text': 'rgba(0, 0, 0, 255)'
    }
   
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1("Reddit - KOL Trend",
            style={'textAlign': 'center', 'color': colors['text']}),
    
    html.Div(children='Select a subreddit and a period below',
             style={'textAlign': 'center', 'color': colors['text']}),    
    
    html.Div([
        dcc.Dropdown(id='select_subreddit',
            options=[
                { 'label': "AskReddit", 'value': "AskReddit"},
                { 'label': "pics", 'value': "pics"},
                { 'label': "Music", 'value': "Music"},
                { 'label': "worldnews", 'value': "worldnews"},
                { 'label': "askscience", 'value': "askscience"},
                { 'label': "books", 'value': "books"},
                { 'label': "explainlikeimfive", 'value': "explainlikeimfive"},
                { 'label': "travel", 'value': "travel"},
            ],
            optionHeight=35,
            value="Please Select",
            searchable=True,
            search_value='',
            placeholder='Please select...',
            clearable=True,
            style={'width': "100%"},
            persistence=True,
            persistence_type='memory')],
        style={'width': '45%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Dropdown(id='select_time',
            options=[
                { 'label': "2018-06", 'value': "2018-06"},
                { 'label': "2018-07", 'value': "2018-07"},
                { 'label': "2018-08", 'value': "2018-08"},
                { 'label': "2018-09", 'value': "2018-09"},
                { 'label': "2018-10", 'value': "2018-10"},
            ],
            optionHeight=35,
            value="Please Select",
            searchable=True,
            search_value='',
            placeholder='Please select...',
            clearable=True,
            style={'width': "100%"},
            persistence=True,
            persistence_type='memory')],
        style={'width': '45%', 'float': 'right', 'display': 'inline-block'}),
    
    html.Br(),
    
    html.Button(id='my-button', n_clicks=0, children="Submit"), 
    
    html.Div([
        html.P('Enter an Author ID:'),
        dcc.Input(
            id='author', type='text', value='', debounce=True)],
        style={'textAlign':'right'}),    
   
    html.Div(id='output', style={'display':'flex', 'justify-content':'center'}),
    html.Div(id='links', style={'display':'flex', 'justify-content':'center'})
])    

@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='my-button', component_property='n_clicks')],
    [State(component_id='select_subreddit', component_property='value'),
     State(component_id='select_time', component_property='value')],
    prevent_initial_call = True
)

def update_output(n_clicks, subreddit_name, input_time):
    if(subreddit_name == 'None' or input_time == 'None'):
        return ["oops! Please select first!" + str(n_clicks)]    
    
    try:
        connection = psycopg2.connect(dbname=dbname, user=user, host=host, port=port, password=password)
        cursor = connection.cursor()

        select_Query = "select author, score from submission where subreddit=%s and time=%s order by score desc limit 10;"
        input_search = (subreddit_name, input_time)
    
        cursor.execute(select_Query, input_search)
        rows = cursor.fetchmany(10)
        result_list = [row for row in rows]
    
    except (Exception, psycopg2.Error) as e:
        print(e)
    
    finally:
        if(connection):
            cursor.close()
            connection.close()      
      
        print('\n'.join(map(str, result_list)))
        return html.P(['Top 10 Authors with Interests',
                       html.Ul([html.Li(x[0]+"  |  "+str(x[1])) for x in result_list])])

@app.callback(
    Output('links', 'children'),
    [Input(component_id='author', component_property='value')],
    [State(component_id='select_subreddit', component_property='value'),
     State(component_id='select_time', component_property='value')],
    prevent_initial_call = False
)

def update_author(author_name, subreddit_name, input_time):
    if(len(author_name) == 0):
        return dash.no_update, '{} cannot be empty!'.format(author_name)    

    try:
        connection = psycopg2.connect(dbname=dbname, user=user, host=host, port=port, password=password)
        cursor = connection.cursor()

        select_Query = "select permalink from submission where author=%s and subreddit=%s and time=%s order by score desc limit 10;"
        input_search = (author_name, subreddit_name, input_time)
    
        cursor.execute(select_Query, input_search)
        rows = cursor.fetchmany(10)
        result_list = [row for row in rows]

    except (Exception, psycopg2.Error) as e:
        print (e)
    
    finally:
        if(connection):
            cursor.close()
            connection.close()      

        print('\n'.join(map(str, result_list)))
        return html.P(["Top 10 Posts from this Author", 
                       html.Ul([html.Li("http://www.reddit.com"+str(x)[:-3][2:]) for x in result_list])])
  
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port = 8050)
