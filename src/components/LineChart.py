import pandas as pd
import plotly.express as px


class LineChart:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.figure = self.build_figure()

    def build_figure(self):
        fig = px.line(
            data_frame=self.df,
            x="hours",
            y="miles",
            color="name",
            labels={"hours": "Hours", "miles": "Miles", "name": "Rider"},
        )

        fig.update_layout(showlegend=False)

        for rider in self.df["name"].unique():
            rider_df = self.df[self.df["name"] == rider]
            fig.add_annotation(
                x=rider_df["hours"].iloc[-1],
                y=rider_df["miles"].iloc[-1],
                text=rider,
                showarrow=True,
                font=dict(size=12, color="black"),
                align="center",
                # xshift=60,
            )

        return fig
