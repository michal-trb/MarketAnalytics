# -*- coding: utf-8 -*-
from dash import Dash, html, Input, Output, ctx, dcc, State
from select_data_from_database import DataFromDB
import plotly.graph_objects as go
import plotly.express as px

app = Dash(__name__)

df_places = DataFromDB().import_places()
wojewodztwa = [
    "DOLNOŚLĄSKIE", 
    "KUJAWSKO-POMORSKIE", 
    "LUBELSKIE", 
    "LUBUSKIE", 
    "ŁÓDZKIE", 
    "MAŁOPOLSKIE", 
    "MAZOWIECKIE",
    "OPOLSKIE", 
    "PODKARPACKIE", 
    "PODLASKIE", 
    "POMORSKIE", 
    "ŚLĄSKIE", 
    "ŚWIĘTOKRZYSKIE", 
    "WARMIŃSKO-MAZURSKIE",
    "WIELKOPOLSKIE", 
    "ZACHODNIOPOMORSKIE"
]

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
    html.Button('Mediana cen mieszkań', id='btn-nclicks-1', n_clicks=0),
    html.Button('Mediana cen mieszkań oraz zarobków', id='btn-nclicks-2', n_clicks=0),
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
        # Sprawdzamy, czy każde słowo w places jest w liście województw
        for place in input_places:
            if place.upper() not in wojewodztwa:
                return "Funkcja dotyczy tylko województw"
        else:
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
    # Tworzenie wykresu typu Scatter
    fig = go.Figure()

    # Iterowanie po liście elementów data i dodawanie wykresów typu Line
    line_traces = []
    for trace in px.line(data_frame=df,
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
                          }).data:
        line_traces.append(trace)
        fig.add_trace(trace)

        # Zdefiniowanie listy kolorów
    colors = ['blue', 'red', 'green', 'orange']

        # Dodawanie wykresu typu Scatter
    for i, c in enumerate(df['place'].unique()):
        scatter_trace = go.Scatter(
            x=df[df['place'] == c]['date'],
            y=df[df['place'] == c]['salary_brutto'],
            mode='markers',
            text=df[df['place'] == c]['salary_brutto'],
            name='wynagrodzenie w obszarze: ' + c,
            hovertext=df[df['place'] == c]['place'],
            marker=dict(
                size=5,
                symbol='square',
                color=colors[i % len(colors)]
            )
        )
        line_traces.append(scatter_trace)
        fig.add_trace(scatter_trace)


    return fig



if __name__ == '__main__':
    app.run_server(debug=True)