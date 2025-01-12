from dash import Dash, Input, Output, State, ctx, html
import flag
import dash
from components.PageLayout import PageLayout
from components.PxLineChart import PxLineChart
from utils.parsing_utils import parse_event_data
from utils.path_utils import events_files
from utils.json_utils import get_event_data_from_json


app = Dash(name=__name__, external_scripts=["https://cdn.tailwindcss.com"])


event_data = get_event_data_from_json(events_files[-1])
df = parse_event_data(event_data)


app.layout = PageLayout(event_data=event_data, df=df, data_filenames=events_files)


def get_riders_list_from_df(df) -> list[str]:
    return df["name"].unique().tolist()


@app.callback(
    Output("graph", "figure", allow_duplicate=True),
    Output("names_checklist", "options"),
    Output("names_checklist", "value", allow_duplicate=True),
    Output("country_dropdown", "options"),
    Output("country_dropdown", "value", allow_duplicate=True),
    Output("division_dropdown", "options"),
    Output("division_dropdown", "value", allow_duplicate=True),
    Output("discipline_dropdown", "options"),
    Output("discipline_dropdown", "value", allow_duplicate=True),
    Output("age_dropdown", "options"),
    Output("age_dropdown", "value", allow_duplicate=True),
    Input("event_dropdown", "value"),
    prevent_initial_call=True,
)
def on_event_update(selected_event):
    print(">>>>>>> ON EVENT UPDATE")
    if selected_event:
        print(selected_event)
        event_data = get_event_data_from_json(selected_event)
        df = parse_event_data(event_data)
        figure = PxLineChart(df=df)

        names_options = [
            {
                "label": html.Span(
                    className="text-xs lg:text-sm whitespace-nowrap",
                    children=[
                        html.Span(
                            className="font-bold w-4",
                            children=f" #{rank_index+1}",
                        ),
                        html.Span(
                            className="",
                            children=f" {flag.flag(rider['country'])}",
                        ),
                        html.Span(
                            className="",
                            children=f" {rider['name']}",
                        ),
                        html.Span(
                            className="text-xs italic align-right",
                            children=f" {rider['miles'][-1]:.1f} miles",
                        ),
                    ],
                ),
                "value": rider["name"],
            }
            for rank_index, rider in enumerate(event_data["riders"])
        ]
        names_value = [rider["name"] for rider in event_data["riders"]]
        print(f"names value for new dataset : {names_value}")

        country_options = [
            {"label": country, "value": country} for country in df["country"].unique()
        ]
        country_value = [rider["country"] for rider in event_data["riders"]]

        division_options = [
            {"label": division, "value": division}
            for division in df["division"].unique()
        ]
        division_value = [rider["division"] for rider in event_data["riders"]]

        discipline_options = [
            {"label": discipline, "value": discipline}
            for discipline in df["discipline"].unique()
        ]
        discipline_value = [rider["discipline"] for rider in event_data["riders"]]

        age_options = [{"label": age, "value": age} for age in df["age"].unique()]
        age_value = [rider["age"] for rider in event_data["riders"]]

        return (
            figure,
            names_options,
            names_value,
            country_options,
            country_value,
            division_options,
            division_value,
            discipline_options,
            discipline_value,
            age_options,
            age_value,
        )


@app.callback(
    Output("graph", "figure"),
    Output("names_checklist", "value", allow_duplicate=True),
    Output("country_dropdown", "value"),
    Output("division_dropdown", "value"),
    Output("discipline_dropdown", "value"),
    Output("age_dropdown", "value"),
    Input("event_dropdown", "value"),
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
    selected_event,
    selected_riders,
    selected_countries,
    selected_divisions,
    selected_disciplines,
    selected_ages,
    top_10_clicks,
    all_riders_clicks,
    names_options,
) -> tuple[PxLineChart, list[str], list[str], list[str], list[str], list[str]]:
    print(">>>>>>> ON FILTER UPDATE")
    print("Triggered by", ctx.triggered_id)

    print(f"Selected event : {selected_event}")
    if ctx.triggered_id == "event_dropdown":
        event_data = get_event_data_from_json(selected_event)
        df = parse_event_data(event_data)
        filtered_df = df[(df["rank"] >= 1) & (df["rank"] <= 10)]
        top_10_riders_selected = get_riders_list_from_df(filtered_df)
        figure = PxLineChart(df=filtered_df)
        return figure, top_10_riders_selected, None, None, None, None

    event_data = get_event_data_from_json(selected_event)
    df = parse_event_data(event_data)

    filtered_df = df.copy()

    # Click on the names checklist
    if ctx.triggered_id == "names_checklist":
        filtered_df = filtered_df[filtered_df["name"].isin(selected_riders)]
        return PxLineChart(df=filtered_df), selected_riders, None, None, None, None

    # Click on one of the buttons
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "top_10_riders_button":
            filtered_df = df[(df["rank"] >= 1) & (df["rank"] <= 10)]
            top_10_riders_selected = get_riders_list_from_df(filtered_df)
            figure = PxLineChart(df=filtered_df)
            return figure, top_10_riders_selected, None, None, None, None

        elif button_id == "all_riders_button":
            all_riders_selected = get_riders_list_from_df(df)
            return (
                PxLineChart(df=filtered_df),
                all_riders_selected,
                None,
                None,
                None,
                None,
            )

    # Apply filters
    filters = [
        {"col_name": "country", "content": selected_countries},
        {"col_name": "division", "content": selected_divisions},
        {"col_name": "discipline", "content": selected_disciplines},
        {"col_name": "age", "content": selected_ages},
    ]

    for filter in filters:
        if filter["content"]:
            content = (
                filter["content"]
                if isinstance(filter["content"], list)
                else [filter["content"]]
            )
            filtered_df = filtered_df[filtered_df[filter["col_name"]].isin(content)]

    updated_checklist_values = filtered_df["name"].unique().tolist()
    print(f"updated selected names after filters : {updated_checklist_values}")

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
