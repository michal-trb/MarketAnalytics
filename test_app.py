import pytest
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from app import generate_graph_count
from app import generate_graph_median_m2
from app import generate_graph_count_m2
from app import generate_graph_median_m2_salary
from app import generate_graph_sum_value

data = {
        "date": pd.date_range(start='1/1/2020', periods=4),
        "value": [1, 2, 3, 4],
        "place": ["place1", "place2", "place1", "place2"]
    }
data_for_count_m2 = {
        "date": pd.date_range(start='1/1/2020', periods=4),
        "value": ["1.2", "2.2", "3.3", "4.4"],
        "place": ["place1", "place2", "place1", "place2"]
    }
    
def test_generate_graph_median_m2():    
    df = pd.DataFrame(data)
    result = generate_graph_median_m2(df)
    assert isinstance(result, go.Figure), "Returned object is not a go.Figure instance."
    assert len(result.data) == len(df['place'].unique()), "The number of traces does not match the expected number."
    assert result.layout.transition.duration == 1000, "Layout transition duration is not as expected."

def test_generate_graph_median_m2_salary():
    data_salary = {
        "date": pd.date_range(start='1/1/2020', periods=4),
        "value": [1, 2, 3, 4],
        "place": ["place1", "place2", "place1", "place2"],
        "salary_brutto": [5000, 6000, 7000, 8000]
    }
    df = pd.DataFrame(data_salary)
    result = generate_graph_median_m2_salary(df)
    assert isinstance(result, go.Figure), "Returned object is not a go.Figure instance."
    assert len(result.data) == 2 * len(df['place'].unique()), "The number of traces does not match the expected number."  
    expected_colors = ['blue', 'red']
    for i, data in enumerate(result.data):
        if i < len(df['place'].unique()):
            continue  
        assert data.marker.color == expected_colors[i % len(expected_colors)], f"Unexpected color for trace {i}."

def test_generate_graph_sum_value():
    df = pd.DataFrame(data)
    result = generate_graph_sum_value(df)
    assert isinstance(result, go.Figure), "Returned object is not a go.Figure instance."
    assert len(result.data) == len(df['place'].unique()), "The number of traces does not match the expected number."  
    assert result.layout.transition.duration == 1000, "Layout transition duration is not as expected."


def test_generate_graph_count():
    df = pd.DataFrame(data)
    result = generate_graph_count(df)
    assert isinstance(result, go.Figure), "Returned object is not a go.Figure instance."
    assert len(result.data) == len(df['place'].unique()), "The number of traces does not match the expected number."
    assert result.layout.transition.duration == 1000, "Layout transition duration is not as expected."

def test_generate_graph_count_m2():
    df = pd.DataFrame(data_for_count_m2)
    result = generate_graph_count_m2(df)

    assert isinstance(result, go.Figure), "Returned object is not a go.Figure instance."
    assert len(result.data) == len(df['place'].unique()), "The number of traces does not match the expected number."
    assert result.layout.transition.duration == 1000, "Layout transition duration is not as expected."

