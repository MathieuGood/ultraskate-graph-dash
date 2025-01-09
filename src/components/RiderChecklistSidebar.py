from dash import html, dcc
import flag


def RiderChecklistSidebar(className: str, event_data : dict) -> html.Div:

    return html.Div(
        className=className,
        children=[
            dcc.Checklist(
                id="names_checklist",
                className="h-full overflow-y-scroll whitespace-nowrap",
                value=[rider["name"] for rider in event_data["riders"]],
                options=[
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
                ],
            ),
        ],
    )
