import plotly.express as px
import gensim.downloader as api
from dash import html , Dash ,dcc,Input,Output,State
import pandas as pd
import plotly.express as px
from dash import Dash, html
import dash_cytoscape as cyto
colors = px.colors.qualitative.Plotly

app=Dash(external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

df = pd.read_csv('word_embeddings_2d.csv')


golve = api.load("glove-wiki-gigaword-50")
input_value = 'king'
elements = []
similar_words = [word for word, _ in golve.most_similar(input_value, topn=10)]
similar_words.append(input_value)
similar_words_df = df[df['word'].isin(similar_words)]
    
word_row = similar_words_df[similar_words_df['word'] == input_value].iloc[0]
colors = px.colors.qualitative.Plotly 
for i, row in enumerate(similar_words_df.itertuples()):
    elements.append({'data': {'id': row.word, 'label': row.word, 'color': colors[i % len(colors)]}, 'position': {'x': row.x, 'y': row.y}})

for i in range(0, len(similar_words)):
    if similar_words[i] != input_value:
        elements.append({'data': {'source': input_value, 'target': similar_words[i]}})

app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'margin': 'auto','margin-top':'50px', 'width': '70%', 'padding': '10px', 'background-color': '#f0f0f0', 'border-radius': '15px', 'box-shadow': '0px 0px 15px #888'}, children=[
    html.H2('Word Similarity Graph (GloVe wiki-gigaword-50)', style={'text-align': 'center', 'color': '#555'}),
    html.Div(style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'margin-bottom': '20px'}, children=[
        dcc.Input(id='my-input', type='text', value=None, style={'margin-right': '10px', 'padding': '10px', 'border-radius': '5px'}),
        html.Button('Submit', id='submit-val', n_clicks=0, style={'border-radius': '10px', 'border': 'none', 'background-color': '#007BFF', 'color': 'white', 'cursor': 'pointer'})
    ]),
    html.Div(id='my-div'),
    html.Div(style={'background-color': 'black', 'padding': '10px', 'border-radius': '15px', 'margin-top': '20px'}, children=[
        cyto.Cytoscape(
            id='cytoscape',
            layout={'name': 'cose'},
            style={'width': '100%', 'height': '580px'},
            elements=elements,
            stylesheet=[
                {
                    'selector': 'node',
                    'style': {
                        'background-color': 'data(color)',
                        'label': 'data(label)',
                        'color': 'white',
                        'font-size': '14px',
                        'width': 20,
                        'height': 20,
                    }
                }
            ],
            zoom=0.7,
            pan={'x': 0, 'y': 0}
        )
    ])
])    




@app.callback(
    Output(component_id='cytoscape',component_property= 'elements'),
    State(component_id='my-input', component_property='value'),
    Input(component_id='submit-val',component_property='n_clicks'),

)

def update_graph(input_value, n_clicks=0):
    elements = []
    similar_words = [word for word, _ in golve.most_similar(input_value, topn=10)]
    similar_words.append(input_value)
    similar_words_df = df[df['word'].isin(similar_words)]

    for i, row in enumerate(similar_words_df.itertuples()):
        elements.append({'data': {'id': row.word, 'label': row.word, 'color': colors[i % len(colors)]}, 'position': {'x': row.x, 'y': row.y}})


    for i in range(0, len(similar_words)):
        if similar_words[i] != input_value:
            elements.append({'data': {'source': input_value, 'target': similar_words[i]}})

    return elements
app.run_server(use_reloader=True)   

