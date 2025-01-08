from dash import *
from app_layout import PageLayout
import plotly.express as px
import pandas as pd
import json
import os

from components.LineChart import LineChart
from data_parser import parse_event_data


json_file_path = os.path.join(
    os.path.dirname(__file__), "..", "data", "miami_2019.json"
)
json_file = open(json_file_path)
data = json.load(json_file)
json_file.close()


parsed_riders_data = parse_event_data(data)
df = pd.DataFrame(parsed_riders_data)

app = Dash(external_scripts=["https://cdn.tailwindcss.com"])

app.layout = PageLayout(data=data, df=df).layout


@app.callback(
    Output(component_id="graph", component_property="figure"),
    [
        Input(component_id="names_checklist", component_property="value"),
        Input(component_id="country_dropdown", component_property="value"),
        Input(component_id="division_dropdown", component_property="value"),
        Input(component_id="discipline_dropdown", component_property="value"),
        Input(component_id="age_dropdown", component_property="value"),
    ],
)
def update_line_chart(
    riders, selected_countries, selected_divisions, selected_disciplines, selected_ages
):
    filtered_df = df[df["name"].isin(riders)]

    if selected_countries:
        if not isinstance(selected_countries, list):
            selected_countries = [selected_countries]
        filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

    if selected_divisions:
        if not isinstance(selected_divisions, list):
            selected_divisions = [selected_divisions]
        filtered_df = filtered_df[filtered_df["division"].isin(selected_divisions)]

    if selected_disciplines:
        if not isinstance(selected_disciplines, list):
            selected_disciplines = [selected_disciplines]
        filtered_df = filtered_df[filtered_df["discipline"].isin(selected_disciplines)]

    if selected_ages:
        if not isinstance(selected_ages, list):
            selected_ages = [selected_ages]
        filtered_df = filtered_df[filtered_df["age"].isin(selected_ages)]

    figure = LineChart(df=filtered_df).figure
    return figure


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
