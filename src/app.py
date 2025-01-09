from dash import Dash, Input, Output, State, ctx, dcc
import dash
from components.PageLayout import PageLayout
from components.PxLineChart import PxLineChart
from utils.parsing_utils import parse_event_data
from utils.path_utils import events_files
from utils.json_utils import get_event_data_from_json


event_data = get_event_data_from_json(events_files[-1])
df = parse_event_data(event_data)


app = Dash(name=__name__, external_scripts=["https://cdn.tailwindcss.com"])

app.layout = PageLayout(event_data=event_data, df=df, data_filenames=events_files)


@app.callback(
    Input("event_dropdown", "value"),
)
def on_event_update(selected_event):
    print(">>>>>>> ON EVENT UPDATE")
    if selected_event:
        print(selected_event)
        # event_data = get_event_data_from_json(selected_event)
        # df = parse_event_data(event_data)


@app.callback(
    Output("graph", "figure"),
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
def on_filter_update(
    riders,
    selected_countries,
    selected_divisions,
    selected_disciplines,
    selected_ages,
    top_10_clicks,
    all_riders_clicks,
    names_options,
):
    print(">>>>>>> ON FILTER UPDATE")
    print(ctx.triggered_id)

    filtered_df = df.copy()

    # Click on the names checklist
    if ctx.triggered_id == "names_checklist":
        filtered_df = filtered_df[filtered_df["name"].isin(riders)]
        return PxLineChart(df=filtered_df), riders, None, None, None, None

    # Click on one of the buttons
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "top_10_riders_button":
            filtered_df = df[(df["rank"] >= 1) & (df["rank"] <= 10)]
            top_10_riders = filtered_df["name"].unique().tolist()
            figure = PxLineChart(df=filtered_df)
            return figure, top_10_riders, None, None, None, None

        elif button_id == "all_riders_button":
            all_riders = filtered_df["name"].unique().tolist()
            return PxLineChart(df=filtered_df), all_riders, None, None, None, None

    # Apply filters
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

    updated_checklist_values = filtered_df["name"].unique().tolist()

    return (
        PxLineChart(df=filtered_df),
        updated_checklist_values,
        dash.no_update,
        dash.no_update,
        dash.no_update,
        dash.no_update,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=9004)
