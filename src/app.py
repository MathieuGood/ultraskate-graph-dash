from dash import *
import plotly.express as px
import pandas as pd
import json


json_file = open("../data/miami_2019.json")
data = json.load(json_file)
json_file.close()


columns = [
    {"name": "Name", "id": "name"},
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
        "division": rider["division"],
        "discipline": rider["discipline"],
        "country": rider["country"],
        "age": rider["age"],
        "hours": rider["hours"][i],
        "miles": rider["miles"][i],
    }
    for rider in data["riders"]
    for i in range(len(rider["hours"]))
]

df = pd.DataFrame(parsed_riders_data)

# Filter df with only name "Mathieu Bon"
# df = df[df["name"] == "Mathieu Bon"]
# df = df[df["country"] == "US"]

print(df)

app = Dash()

app.layout = [
    dcc.Graph(id="graph"),
    dcc.Checklist(
        id="checklist",
        options=[
            {"label": rider["name"], "value": rider["name"]} for rider in data["riders"]
        ],
        value=[rider["name"] for rider in data["riders"]],
        inline=True,
    ),
    dash_table.DataTable(data=parsed_riders_data, columns=columns, page_size=10),
]


@app.callback(
    Output("graph", "figure"),
    Input("checklist", "value"),
)
def update_line_chart(riders):
    mask = df["name"].isin(riders)
    fig = px.line(
        data_frame=df[mask],
        x="hours",
        y="miles",
        color="name",
        title="Rider Stats",
        labels={"hours": "Hours", "miles": "Miles", "name": "Rider"},
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
