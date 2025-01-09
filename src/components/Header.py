from dash import html, get_asset_url


def Header(className : str) -> html.Div:

    return html.Div(
        className=className,
        children=[
            html.Img(className="h-8 w-8", src=get_asset_url("longboard.svg")),
            html.Span(
                className="text-2xl font-bold",
                children=f"Ultraskate Buddy",
            ),
        ],
    )
