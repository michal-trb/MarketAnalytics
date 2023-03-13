from dash import Dash, html, Input, Output, ctx, dcc, State
from select_data_from_database import DataFromDB
import plotly.express as px

app = Dash(__name__)

df_places = DataFromDB().import_places()

app.layout =  html.Div(children=[
    html.Label('Wybierz dane:'),
    dcc.Dropdown(
        id="input-places",
        options=[
            {'label': i, 'value': i} for i in list(df_places.place)
        ],
        value='POLSKA',
        multi=True
    ),
    html.Br(),
    html.Button('Wykres 1', id='btn-nclicks-1', n_clicks=0),
    html.Button('Wykres 2', id='btn-nclicks-2', n_clicks=0),
    html.Br(),
    html.Div(id='graph-container')
])

@app.callback(
    Output('graph-container', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    [State(component_id='input-places', component_property='value')]
)

def displayClick(btn1, btn2, input_places):
    fig = None
    if "btn-nclicks-1" == ctx.triggered_id:
        df = DataFromDB.select_data(input_places)
        fig = generate_graph_1(df)
    elif "btn-nclicks-2" == ctx.triggered_id:
        df = DataFromDB.select_data(input_places)
        fig = generate_graph_2(df)
    if fig is not None:
        return dcc.Graph(figure=fig)  # Wrap the Plotly figure object inside dcc.Graph


def generate_graph_1(df):
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
    return fig

def generate_graph_2(df):
    fig = px.line(data_frame=df,
                 x="place",
                 y="m2_value",
                 title='Mediana cen za 1 m2 lokali mieszkalnych sprzedanych w ramach transakcji rynkowych',
                 labels={
                     "place": "Obszar",
                     "m2_value": "Cena m2"
                 }
                 )
    fig.update_layout(transition_duration=1000)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)