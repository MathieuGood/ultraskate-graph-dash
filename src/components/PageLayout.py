from dash import html, dcc, get_asset_url
import pandas as pd

from components.FiltersBar import FiltersBar
from components.GraphArea import GraphArea
from components.Header import Header
from components.RiderChecklistSidebar import RiderChecklistSidebar


def PageLayout(event_data: dict, df: pd.DataFrame, data_filenames: list[str]):

    return html.Div(
        className="flex h-full h-screen overflow-hidden",
        children=[
            # Header
            # Header(className="flex bg-blue-500 text-white p-3 h-12"),
            # Sidebar
            RiderChecklistSidebar(
                className="bg-gray-100 p-3 hidden lg:flex border-2 rounded shadow-lg m-1",
                event_data=event_data,
            ),
            # Filters & Graph
            html.Div(
                className="w-screen flex flex-col",
                children=[
                    FiltersBar(
                        className="filters grid grid-cols-6 gap-2 p-4",
                        event_data=event_data,
                        df=df,
                        data_filenames=data_filenames,
                    ),
                    GraphArea(className="flex w-full h-full"),
                ],
            ),
        ],
    )


columns = [
    {"name": "Rank", "id": "rank"},
    {"name": "Name", "id": "name"},
    {"name": "Mileage", "id": "current_mileage"},
    {"name": "Division", "id": "division"},
    {"name": "Discipline", "id": "discipline"},
    {"name": "Country", "id": "country"},
    {"name": "Age", "id": "age"},
    {"name": "Time", "id": "hours"},
    {"name": "Miles", "id": "miles"},
]
