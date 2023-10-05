from ast import Return
from dash import Dash, html, Input, Output, ctx, dcc, State
from select_data_from_database import DataFromDB
import plotly.graph_objects as go
import plotly.express as px

# CSS styles
styles = {
    'label': {
        'font-weight': 'bold',
        'margin-right': '5px',
        'margin-bottom': '5px',
        'color': '#555',
        'font-size': '24px',
        'font-family': 'Helvetica Neue, Arial, sans-serif',
        'text-transform': 'uppercase'
    },
    'dropdown': {
        'margin-right': '20px',
        'width': '500px',
        'margin-bottom': '10px',
        'background-color': '#fff'
    },
    'button': {
        'margin-right': '10px',
        'margin-top': '20px',
        'background-color': '#4CAF50',
        'color': 'white',
        'border': 'none',
        'padding': '8px 14px',
        'border-radius': '4px',
        'cursor': 'pointer',
        'font-size': '14px'
    },
    'graph_container': {
        'margin-top': '20px'
    }
}

app = Dash(__name__)

df_places = DataFromDB().import_places()
df_areas = DataFromDB().import_areas()
df_transactions = DataFromDB().import_transactions()

province = [
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

app.layout = html.Div(children=[
    html.Label('Wybierz dane:', style=styles['label']),
    dcc.Dropdown(
        id="input-places",
        options=[{'label': i, 'value': i} for i in list(df_places.place)],
        value='',
        multi=True,
        style=styles['dropdown']
    ),
    html.Div(id='container-places', style=styles['graph_container']),
    dcc.Dropdown(
        id="input-areas",
        options=[{'label': i, 'value': i} for i in list(df_areas.area)],
        value='',
        style=styles['dropdown']
    ),
    html.Div(id='container-areas', style=styles['graph_container']),
    dcc.Dropdown(
        id="input-transactions",
        options=[{'label': i, 'value': i} for i in list(df_transactions.transactions)],
        value='',
        style=styles['dropdown']
    ),
    html.Div(id='container-transactions', style=styles['graph_container']),
    html.Button('Mediana cen mieszkań', id='btn-nclicks-1', n_clicks=0, style=styles['button']),
    html.Button('Mediana cen mieszkań oraz zarobków', id='btn-nclicks-2', n_clicks=0, style=styles['button']),
    html.Button('Wartość transakcji', id='btn-nclicks-3', n_clicks=0, style=styles['button']),
    html.Button('Liczba transakcji', id='btn-nclicks-4', n_clicks=0, style=styles['button']),
    html.Button('Powierzchnia użytkowa', id='btn-nclicks-5', n_clicks=0, style=styles['button']),
    html.Div(id='graph-container', style=styles['graph_container'])
])
@app.callback(
    Output('container-places', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks'),
    Input('btn-nclicks-4', 'n_clicks'),
    Input('btn-nclicks-5', 'n_clicks'),
    State('input-places', 'value')
    )
def check_places(btn1, btn2, btn3, btn4, btn5, place_value):
    if not place_value:
        no_place = html.P("Uzupełnij obszar terytorialny")
        return no_place
    else:
        return

@app.callback(
    Output('container-areas', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks'),
    Input('btn-nclicks-4', 'n_clicks'),
    Input('btn-nclicks-5', 'n_clicks'),
    State('input-areas', 'value')
    )
def check_area(btn1, btn2, btn3, btn4, btn5, area_value):
    if not area_value:
        no_area = html.P("Uzupełnij powierzchnię użytkowa lokali mieszkalnych")
        return no_area
    else:
        return

@app.callback(
    Output('container-transactions', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks'),
    Input('btn-nclicks-4', 'n_clicks'),
    Input('btn-nclicks-5', 'n_clicks'),
    State('input-transactions', 'value')
    )
def check_transaction(btn1, btn2, btn3, btn4, btn5, transaction_value):
    if not transaction_value:
        no_transaction = html.P("Uzupełnij rodzaj tranzakcji rynkowych")
        return no_transaction
    else:
        return

@app.callback(
    Output('graph-container', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks'),
    Input('btn-nclicks-4', 'n_clicks'),
    Input('btn-nclicks-5', 'n_clicks'),
    State('input-places', 'value'),
    State('input-areas', 'value'),
    State('input-transactions', 'value')
)
def displayClick(btn1, btn2, btn3, btn4, btn5, place_value, area_value, transaction_value):
    fig = None

    if not place_value:
        return
    if not area_value:
        return
    if not transaction_value:
        return

    if "btn-nclicks-1" == ctx.triggered_id:
        input_transactions = ['ogółem']
        df = DataFromDB.select_data(place_value, area_value, transaction_value, "fact_polish_market_median_m2")
        fig = generate_graph_median_m2(df)
    elif "btn-nclicks-2" == ctx.triggered_id:
        for place in place_value:
            if place.upper() not in province:
                return html.P("Funkcja dotyczy tylko województw")
        else:
            df = DataFromDB.select_data_with_salary(place_value, area_value, transaction_value, "fact_polish_market_median_m2")
            fig = generate_graph_median_m2_salary(df)
    elif "btn-nclicks-3"  == ctx.triggered_id:
        df = DataFromDB.select_data(place_value, area_value, transaction_value, "fact_polish_market_sum_value")
        fig = generate_graph_sum_value(df)
    elif "btn-nclicks-4"  == ctx.triggered_id:
        df = DataFromDB.select_data(place_value, area_value, transaction_value, "fact_polish_market_count")
        fig = generate_graph_count(df)
    elif "btn-nclicks-5"  == ctx.triggered_id:
        df = DataFromDB.select_data(place_value, area_value, transaction_value, "fact_polish_market_count_m2")
        fig = generate_graph_count_m2(df)
    if fig is not None:
        return dcc.Graph(figure=fig) 


def generate_graph_median_m2(df):
    fig = px.line(data_frame=df,
                  x="date",
                  y="value",
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

def generate_graph_median_m2_salary(df):
    fig = go.Figure()

    line_traces = []
    for trace in px.line(data_frame=df,
                          x="date",
                          y="value",
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

    colors = ['blue', 'red', 'green', 'orange']

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

def generate_graph_sum_value(df):
    fig = px.line(data_frame=df,
                  x="date",
                  y="value",
                  title='Wartość lokali mieszkalnych sprzedanych w ramach transakcji rynkowych w zł',
                  symbol='place',
                  color='place',
                  labels={
                      "date": "Data",
                      "value": "Wartość",
                      "place": "Obszar"
                  }
                  )
    fig.update_layout(transition_duration=1000)
    return fig

def generate_graph_count(df):
    fig = px.line(data_frame=df,
                  x="date",
                  y="value",
                  title='Liczba lokali mieszkalnych sprzedanych w ramach transakcji rynkowych',
                  symbol='place',
                  color='place',
                  labels={
                      "date": "Data",
                      "value": "Liczba",
                      "place": "Obszar"
                  }
                  )
    fig.update_layout(transition_duration=1000)
    return fig

def generate_graph_count_m2(df):
    df['value'] = df['value'].str.replace(',', '.').astype(float)
    df_sorted = df.sort_values('value')

    fig = px.line(data_frame=df,
                  x="date",
                  y="value",
                  title='Powierzchnia użytkowa lokali mieszkalnych sprzedanych w ramach transakcji rynkowych',
                  symbol='place',
                  color='place',
                  labels={
                      "date": "Data",
                      "value": "Powierzchnia w m2",
                      "place": "Obszar"
                  }
                  )
    fig.update_layout(transition_duration=1000)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
