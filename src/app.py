from dash import *
import plotly.express as px
import pandas as pd
import json
import os


json_file_path = os.path.join(
    os.path.dirname(__file__), "..", "data", "miami_2019.json"
)
json_file = open(json_file_path)
data = json.load(json_file)
json_file.close()


columns = [
    {
        "name": "Rank",
        "id": "rank",
    },
    {"name": "Name", "id": "name"},
    {"name": "Mileage", "id": "current_mileage"},
    {"name": "Division", "id": "division"},
    {"name": "Discipline", "id": "discipline"},
    {"name": "Country", "id": "country"},
    {"name": "Age", "id": "age"},
    {"name": "Time", "id": "hours"},
    {"name": "Miles", "id": "miles"},
]

parsed_riders_data = [
    {
        "name": rider["name"],
        "rank": rider_index + 1,
        "pace": "",
        "current_mileage": rider["miles"][-1],
        "current_hours": rider["hours"][-1],
        "division": rider["division"],
        "discipline": rider["discipline"],
        "country": rider["country"],
        "age": rider["age"],
        "hours": rider["hours"][i],
        "miles": rider["miles"][i],
    }
    for rider_index, rider in enumerate(data["riders"])
    for i in range(len(rider["hours"]))
]


df = pd.DataFrame(parsed_riders_data)


# Converts hours to hours and minutes
def convert_hours_to_hours_minutes(hours):
    hours = int(hours)
    minutes = (hours % 1) * 60
    return f"{hours}h {minutes}m"


app = Dash(external_scripts=["https://cdn.tailwindcss.com"])

app.layout = html.Div(
    className="flex h-full h-screen",
    children=[
        # Sidebar
        html.Div(
            className="bg-red-100",
            children=[
                dcc.Checklist(
                    id="names_checklist",
                    options=[
                        {
                            "label": f" #{rank_index+1} {rider['name']} {rider["miles"][-1]:.1f} miles",
                            "value": rider["name"],
                        }
                        for rank_index, rider in enumerate(data["riders"])
                    ],
                    value=[rider["name"] for rider in data["riders"]],
                    className="h-full overflow-y-scroll hidden md:block",
                ),
            ],
        ),
        # Main content
        html.Div(
            className="w-full flex flex-col",
            children=[
                html.Div(
                    className="filters grid grid-cols-4 gap-2 p-4",
                    children=[
                        # Country dropdown
                        dcc.Dropdown(
                            id="country_dropdown",
                            placeholder="Country",
                            options=[
                                {"label": country, "value": country}
                                for country in df["country"].unique()
                            ],
                            value=[rider["country"] for rider in data["riders"]],
                        ),
                        # Division dropdown
                        dcc.Dropdown(
                            id="division_dropdown",
                            placeholder="Division",
                            options=[
                                {"label": division, "value": division}
                                for division in df["division"].unique()
                            ],
                            value=[rider["division"] for rider in data["riders"]],
                        ),
                        # Discipline dropdown
                        dcc.Dropdown(
                            id="discipline_dropdown",
                            placeholder="Discipline",
                            options=[
                                {"label": discipline, "value": discipline}
                                for discipline in df["discipline"].unique()
                            ],
                            value=[rider["discipline"] for rider in data["riders"]],
                        ),
                        # Age dropdown
                        dcc.Dropdown(
                            id="age_dropdown",
                            placeholder="Age",
                            options=[
                                {"label": age, "value": age}
                                for age in df["age"].unique()
                            ],
                            value=[rider["age"] for rider in data["riders"]],
                        ),
                    ],
                ),
                dcc.Graph(id="graph"),
                dash_table.DataTable(
                    data=parsed_riders_data,
                    columns=columns,
                    page_size=5,
                ),
            ],
        ),
    ],
)


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

    return build_line_chart_figure(filtered_df)


def build_line_chart_figure(df: pd.DataFrame):
    return px.line(
        data_frame=df,
        x="hours",
        y="miles",
        color="name",
        title="Rider Stats",
        labels={"hours": "Hours", "miles": "Miles", "name": "Rider"},
    )


if __name__ == "__main__":
    app.run(debug=True)
