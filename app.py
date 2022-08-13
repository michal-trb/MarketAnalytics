# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
import seaborn as sns
from select_data_from_database import DataFromDB

app = Dash(__name__)

df_places = DataFromDB().import_places()

app.layout = html.Div(children=[

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    html.Label('Dropdown'),
    dcc.Dropdown(
        id = "input-places",
        options=[
            {'label': i, 'value': i} for i in list(df_places.place)
        ],
        value=''
    ),
    html.Br(),

    dcc.Graph(
        id='line-graph-market-data'
    )
])
@app.callback(
    Output(component_id='line-graph-market-data', component_property= 'figure'),
    [Input(component_id='input-places', component_property='value')])
def update_graph(input_places):
    df = DataFromDB.select_data(input_places)
    fig = px.line(data_frame=df, x="date", y="m2_value", text="m2_value")
    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)