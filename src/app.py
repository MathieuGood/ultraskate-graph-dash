from dash import Dash, dcc, html, Input, Output, State, callback_context
import dash
from app_layout import PageLayout
import plotly.express as px
import pandas as pd
import json
import os

from components.LineChart import LineChart
from data_parser import parse_event_data


json_file_path = os.path.join(
    os.path.dirname(__file__), "..", "data", "miami_2024.json"
)
json_file = open(json_file_path)
data = json.load(json_file)
json_file.close()


parsed_riders_data = parse_event_data(data)
df = pd.DataFrame(parsed_riders_data)

app = Dash(name=__name__, external_scripts=["https://cdn.tailwindcss.com"])

app.layout = PageLayout(data=data, df=df).layout


@app.callback(
    Output(component_id="graph", component_property="figure"),
    Output("names_checklist", "value"),
    Output("country_dropdown", "value"),
    Output("division_dropdown", "value"),
    Output("discipline_dropdown", "value"),
    Output("age_dropdown", "value"),
    Input("names_checklist", "value"),
    Input("country_dropdown", "value"),
    Input("division_dropdown", "value"),
    Input("discipline_dropdown", "value"),
    Input("age_dropdown", "value"),
    Input("top_10_riders_button", "n_clicks"),
    Input("all_riders_button", "n_clicks"),
    State("names_checklist", "options"),
    prevent_initial_call=True,
)
def update_graph_and_checklist(
    riders,
    selected_countries,
    selected_divisions,
    selected_disciplines,
    selected_ages,
    top_10_clicks,
    all_riders_clicks,
    names_options,
):
    context = dash.callback_context
    filtered_df = df.copy()

    if context.triggered_id == "names_checklist":
        filtered_df = filtered_df[filtered_df["name"].isin(riders)]

        figure = LineChart(df=filtered_df).figure
        return figure, riders, None, None, None, None

    if context.triggered:
        button_id = context.triggered[0]["prop_id"].split(".")[0]
        if button_id == "top_10_riders_button":
            filtered_df = df[(df["rank"] >= 1) & (df["rank"] <= 10)]
            top_10_riders = filtered_df["name"].unique().tolist()
            figure = LineChart(df=filtered_df).figure
            return figure, top_10_riders, None, None, None, None

        elif button_id == "all_riders_button":
            all_riders = filtered_df["name"].unique().tolist()
            figure = LineChart(df=filtered_df).figure
            return figure, all_riders, None, None, None, None

    filters = [
        {"col_name": "country", "content": selected_countries},
        {"col_name": "division", "content": selected_divisions},
        {"col_name": "discipline", "content": selected_disciplines},
        {"col_name": "age", "content": selected_ages},
    ]

    for filter in filters:
        if filter["content"]:
            if not isinstance(filter["content"], list):
                content = [filter["content"]]
            else:
                content = filter["content"]
            filtered_df = filtered_df[filtered_df[filter["col_name"]].isin(content)]

    figure = LineChart(df=filtered_df).figure

    updated_checklist_values = filtered_df["name"].unique().tolist()

    return (
        figure,
        updated_checklist_values,
        dash.no_update,
        dash.no_update,
        dash.no_update,
        dash.no_update,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=9004)
