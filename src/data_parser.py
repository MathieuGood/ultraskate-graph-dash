import pandas as pd


def parse_event_data(data: dict) -> pd.DataFrame:
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
            "event_name": data["event_name"],
            "event_duration": data["duration"],
            "utc_start_time": data["utc_start_time"],
            "utc_end_time": data["utc_end_time"],
            "event_started": data["started"],
            "event_finished": data["finished"],
            "elapsed_time": data["elapsed_time"],
        }
        for rider_index, rider in enumerate(data["riders"])
        for i in range(len(rider["hours"]))
    ]
    return pd.DataFrame(parsed_riders_data)
