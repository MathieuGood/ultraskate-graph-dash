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
    os.path.dirname(__file__), "..", "data", "miami_2019.json"
)
json_file = open(json_file_path)
data = json.load(json_file)
json_file.close()


parsed_riders_data = parse_event_data(data)
df = pd.DataFrame(parsed_riders_data)

app = Dash(name=__name__, external_scripts=["https://cdn.tailwindcss.com"])

app.layout = PageLayout(data=data, df=df).layout


@app.callback(
    Output("names_checklist", "value"),
    Output("country_dropdown", "value"),
    Output("division_dropdown", "value"),
    Output("discipline_dropdown", "value"),
    Output("age_dropdown", "value"),
    Input("top_10_riders_button", "n_clicks"),
    Input("all_riders_button", "n_clicks"),
    State("names_checklist", "options"),
    prevent_initial_call=True,
)
def update_filters(top_10_clicks, reset_clicks, names_options):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "top_10_riders_button":
        top_10_riders = (
            df[(df["rank"] >= 1) & (df["rank"] <= 10)]["name"].unique().tolist()
        )

        return (
            top_10_riders,
            dash.no_update,
            dash.no_update,
            dash.no_update,
            dash.no_update,
        )
    elif button_id == "all_riders_button":
        return df["name"].unique().tolist(), None, None, None, None

    return dash.no_update


@app.callback(
    Output(component_id="graph", component_property="figure"),
    Input(component_id="names_checklist", component_property="value"),
    Input(component_id="country_dropdown", component_property="value"),
    Input(component_id="division_dropdown", component_property="value"),
    Input(component_id="discipline_dropdown", component_property="value"),
    Input(component_id="age_dropdown", component_property="value"),
)
def update_line_chart(
    riders, selected_countries, selected_divisions, selected_disciplines, selected_ages
):
    filtered_df = df[df["name"].isin(riders)]

    filters = [
        {"name": "country", "content": selected_countries},
        {"name": "division", "content": selected_divisions},
        {"name": "discipline", "content": selected_disciplines},
        {"name": "age", "content": selected_ages},
    ]

    for filter in filters:
        print(f"filter name : {filter['name']}, content: {filter['content']}")
        if filter["content"]:
            print(f"Content in filter {filter['name']} : {filter['content']}")
            if not isinstance(filter["content"], list):
                content = [filter["content"]]
            filtered_df = filtered_df[filtered_df[filter["name"]].isin(content)]
            print(f"df filtered with {filter['name']} filtered_df")

    figure = LineChart(df=filtered_df).figure
    return figure


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=9004)
