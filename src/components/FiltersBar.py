from dash import html, dcc
import pandas as pd
import flag


def FiltersBar(
    className: str, event_data: dict, df: pd.DataFrame, data_filenames: list[str]
) -> html.Div:
    filter_dropdown_classname = "text-xs md:text-sm"
    return html.Div(
        className=className,
        children=[
            # Country dropdown
            dcc.Dropdown(
                id="country_dropdown",
                className=filter_dropdown_classname,
                placeholder="Country",
                options=[
                    {
                        "label": [
                            html.Span(
                                className="whitespace-nowrap",
                                children=f"{flag.flag(country)} {country}",
                            ),
                        ],
                        "value": country,
                    }
                    for country in df["country"].unique()
                ],
                value=[rider["country"] for rider in event_data["riders"]],
            ),
            # Division dropdown
            dcc.Dropdown(
                id="division_dropdown",
                className=filter_dropdown_classname,
                placeholder="Division",
                options=[
                    {"label": division, "value": division}
                    for division in df["division"].unique()
                ],
                value=[rider["division"] for rider in event_data["riders"]],
            ),
            # Discipline dropdown
            dcc.Dropdown(
                id="discipline_dropdown",
                className=filter_dropdown_classname,
                placeholder="Discipline",
                options=[
                    {"label": discipline, "value": discipline}
                    for discipline in df["discipline"].unique()
                ],
                value=[rider["discipline"] for rider in event_data["riders"]],
            ),
            # Age dropdown
            dcc.Dropdown(
                id="age_dropdown",
                className=filter_dropdown_classname,
                placeholder="Age",
                options=[{"label": age, "value": age} for age in df["age"].unique()],
                value=[rider["age"] for rider in event_data["riders"]],
            ),
            # Top 10 riders button
            html.Button(
                "Top 10",
                id="top_10_riders_button",
                className="text-xs md:text-sm bg-blue-500 text-white p-1 md:p-2 rounded",
            ),
            # All riders button
            html.Button(
                "All Riders",
                id="all_riders_button",
                className="text-xs md:text-sm bg-red-500 text-white p-2 rounded",
            ),
            # Event dropdown
            dcc.Dropdown(
                id="event_dropdown",
                className=filter_dropdown_classname,
                placeholder="Event",
                options=[
                    {
                        "label": [
                            html.Span(
                                className="whitespace-nowrap",
                                children=f"{
                                    " ".join(filename.capitalize().rstrip(".json").split("_"))
                                    }",
                            ),
                        ],
                        "value": filename,
                    }
                    for filename in data_filenames
                ],
                value=data_filenames[-1],
            ),
        ],
    )
