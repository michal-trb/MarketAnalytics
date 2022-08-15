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

    html.Label('Wybierz dane:'),
    dcc.Dropdown(
        id = "input-places",
        options=[
            {'label': i, 'value': i} for i in list(df_places.place)
        ],
        value='POLSKA',
        multi=True
    ),
    html.Br(),

    dcc.Graph(
        id='line-graph-market-data'
    ),
    html.Div(children='''
       Dane pochodzą z GUS.
       
   ''')
])
@app.callback(
    Output(component_id='line-graph-market-data', component_property= 'figure'),
    [Input(component_id='input-places', component_property='value')])
def update_graph(input_places):
    if bool(input_places):
        df = DataFromDB.select_data(input_places)
        fig = px.line(data_frame=df,
                      x="date",
                      y="m2_value",
                      text="m2_value",
                      title='Mediana cen za 1 m2 lokali mieszkalnych sprzedanych w ramach transakcji rynkowych',
                      symbol='place',
                      color='place',
                      labels={
                          "date": "Data",
                          "m2_value": "Cena m2",
                          "place": "Obszar"
                      }
                      )
        fig.update_layout(transition_duration=1000)

    else:
        fig = px.line()
        fig.update_layout(transition_duration=1000)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)