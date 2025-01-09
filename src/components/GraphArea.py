from dash import html, dcc


def GraphArea(className: str) -> html.Div:
    return html.Div(
        className=className,
        children=dcc.Graph(
            id="graph",
            className="w-full h-full",
            config={"displayModeBar": False},
            responsive=True,
        ),
    )
