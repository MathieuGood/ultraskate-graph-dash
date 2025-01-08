from dash import *


class PageLayout:
    def __init__(self, data, df):
        self.data = data
        self.df = df
        self.layout = self.build_layout()

    def build_layout(self) -> html.Div:
        return html.Div(
            className="flex h-full h-screen",
            children=[
                # Sidebar
                html.Div(
                    className="bg-gray-100 p-3",
                    children=[
                        dcc.Checklist(
                            id="names_checklist",
                            className="h-full overflow-y-scroll hidden md:block whitespace-nowrap",
                            value=[rider["name"] for rider in self.data["riders"]],
                            options=[
                                {
                                    "label": html.Span(
                                        className="text-xs items-center whitespace-nowrap",
                                        children=[
                                            html.Span(
                                                className="font-bold",
                                                children=f" #{rank_index+1}",
                                            ),
                                            html.Span(
                                                className="",
                                                children=f" {rider['name']}",
                                            ),
                                            html.Span(
                                                className="text-xs italic",
                                                children=f" {rider['miles'][-1]:.1f} miles",
                                            ),
                                        ],
                                    ),
                                    "value": rider["name"],
                                }
                                for rank_index, rider in enumerate(self.data["riders"])
                            ],
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
                                        for country in self.df["country"].unique()
                                    ],
                                    value=[
                                        rider["country"]
                                        for rider in self.data["riders"]
                                    ],
                                ),
                                # Division dropdown
                                dcc.Dropdown(
                                    id="division_dropdown",
                                    placeholder="Division",
                                    options=[
                                        {"label": division, "value": division}
                                        for division in self.df["division"].unique()
                                    ],
                                    value=[
                                        rider["division"]
                                        for rider in self.data["riders"]
                                    ],
                                ),
                                # Discipline dropdown
                                dcc.Dropdown(
                                    id="discipline_dropdown",
                                    placeholder="Discipline",
                                    options=[
                                        {"label": discipline, "value": discipline}
                                        for discipline in self.df["discipline"].unique()
                                    ],
                                    value=[
                                        rider["discipline"]
                                        for rider in self.data["riders"]
                                    ],
                                ),
                                # Age dropdown
                                dcc.Dropdown(
                                    id="age_dropdown",
                                    placeholder="Age",
                                    options=[
                                        {"label": age, "value": age}
                                        for age in self.df["age"].unique()
                                    ],
                                    value=[
                                        rider["age"] for rider in self.data["riders"]
                                    ],
                                ),
                                # Top 10 riders button
                                html.Button(
                                    "Top 10 Riders",
                                    id="top_10_riders_button",
                                    className="bg-blue-500 text-white p-2 rounded",
                                ),
                                # Reset filters button
                                html.Button(
                                    "Reset Filters",
                                    id="reset_filters_button",
                                    className="bg-red-500 text-white p-2 rounded",
                                ),
                            ],
                        ),
                        html.Div(
                            className="w-full h-full",
                            children=[
                                dcc.Graph(id="graph", className="h-full"),
                                # dash_table.DataTable(
                                #     data=parsed_riders_data,
                                #     columns=columns,
                                #     page_size=5,
                                # ),
                            ],
                        ),
                    ],
                ),
            ],
        )


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
