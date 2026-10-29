import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


# --------------------------------------------------
# 1. DATA LAYER
# --------------------------------------------------

rng = np.random.default_rng(42)
n = 5000

df = pd.DataFrame({
    "date": pd.to_datetime("2025-01-01")
    + pd.to_timedelta(
        rng.integers(0, 365, n),
        unit="D"
    ),
    "region": rng.choice(
        ["North", "South", "East", "West"],
        n
    ),
    "category": rng.choice(
        ["Electronics", "Clothing", "Home", "Sports"],
        n
    ),
    "units": rng.integers(1, 10, n),
    "unit_price": rng.uniform(10, 200, n).round(2),
})

df["revenue"] = df["units"] * df["unit_price"]


# --------------------------------------------------
# 2. DASHBOARD INITIALIZATION
# --------------------------------------------------

app = Dash(__name__)

REGIONS = sorted(df["region"].unique())
CATEGORIES = sorted(df["category"].unique())

CARD = {
    "flex": "1",
    "padding": "20px",
    "backgroundColor": "white",
    "borderRadius": "10px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
    "textAlign": "center",
}


app.layout = html.Div(
    style={
        "fontFamily": "Arial",
        "backgroundColor": "#F4F6F9",
        "padding": "25px",
    },
    children=[
        html.H1(
            "Interactive Business Dashboard",
            style={
                "textAlign": "center",
                "color": "#1F2937"
            },
        ),

        html.P(
            "Sales and Revenue Analytics",
            style={
                "textAlign": "center",
                "color": "#666"
            },
        ),

        # FILTERS

        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap",
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "marginBottom": "20px",
            },
            children=[
                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "200px"
                    },
                    children=[
                        html.Label("Region"),

                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": r, "value": r}
                                for r in REGIONS
                            ],
                            value=REGIONS,
                            multi=True,
                        ),
                    ],
                ),

                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "200px"
                    },
                    children=[
                        html.Label("Category"),

                        dcc.Dropdown(
                            id="category-filter",
                            options=[
                                {"label": c, "value": c}
                                for c in CATEGORIES
                            ],
                            value=CATEGORIES,
                            multi=True,
                        ),
                    ],
                ),

                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "250px"
                    },
                    children=[
                        html.Label("Date Range"),
                        html.Br(),

                        dcc.DatePickerRange(
                            id="date-filter",
                            min_date_allowed=df["date"].min().date(),
                            max_date_allowed=df["date"].max().date(),
                            start_date=df["date"].min().date(),
                            end_date=df["date"].max().date(),
                            display_format="DD-MM-YYYY",
                        ),
                    ],
                ),
            ],
        ),

        # KPI CARDS

        html.Div(
            id="kpi-row",
            style={
                "display": "flex",
                "gap": "16px",
                "flexWrap": "wrap",
                "marginBottom": "20px",
            },
        ),

        # CHARTS

        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "10px",
                "borderRadius": "10px",
                "marginBottom": "20px",
            },
            children=[
                dcc.Graph(id="trend-chart")
            ],
        ),

        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap"
            },
            children=[
                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "300px",
                        "backgroundColor": "white",
                        "padding": "10px",
                        "borderRadius": "10px",
                    },
                    children=[
                        dcc.Graph(id="category-chart")
                    ],
                ),

                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "300px",
                        "backgroundColor": "white",
                        "padding": "10px",
                        "borderRadius": "10px",
                    },
                    children=[
                        dcc.Graph(id="region-chart")
                    ],
                ),
            ],
        ),
    ],
)


# --------------------------------------------------
# 3. HELPER FUNCTIONS
# --------------------------------------------------

def filter_data(regions, categories, start, end):

    if not start or not end:
        return df.iloc[0:0]

    regions = regions or []
    categories = categories or []

    return df[
        df["region"].isin(regions)
        & df["category"].isin(categories)
        & df["date"].between(
            pd.Timestamp(start),
            pd.Timestamp(end),
        )
    ]


def kpi_card(title, value):

    return html.Div(
        style=CARD,
        children=[
            html.Div(
                title,
                style={"color": "#666"}
            ),

            html.H2(
                value,
                style={"margin": "4px 0 0"}
            ),
        ],
    )


# --------------------------------------------------
# 4. CALLBACKS
# --------------------------------------------------

@app.callback(
    Output("kpi-row", "children"),
    Output("trend-chart", "figure"),
    Output("category-chart", "figure"),
    Output("region-chart", "figure"),

    Input("region-filter", "value"),
    Input("category-filter", "value"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date"),
)

def update_dashboard(regions, categories, start, end):

    d = filter_data(
        regions,
        categories,
        start,
        end
    )

    if d.empty:

        empty_fig = px.scatter(
            title="No data for the selected filters"
        )

        return (
            [
                kpi_card("Total Revenue", "$0.00"),
                kpi_card("Orders", "0"),
                kpi_card("Avg Order Value", "$0.00"),
                kpi_card("Units Sold", "0"),
            ],
            empty_fig,
            empty_fig,
            empty_fig,
        )

    # KPI VALUES

    kpis = [
        kpi_card(
            "Total Revenue",
            f"${d['revenue'].sum():,.2f}"
        ),

        kpi_card(
            "Orders",
            f"{len(d):,}"
        ),

        kpi_card(
            "Avg Order Value",
            f"${d['revenue'].mean():,.2f}"
        ),

        kpi_card(
            "Units Sold",
            f"{d['units'].sum():,}"
        ),
    ]

    # MONTHLY REVENUE TREND

    monthly = (
        d.set_index("date")
        .resample("MS")["revenue"]
        .sum()
        .reset_index()
    )

    fig_trend = px.line(
        monthly,
        x="date",
        y="revenue",
        markers=True,
        title="Monthly Revenue Trend",
        labels={
            "date": "Month",
            "revenue": "Revenue ($)"
        },
        template="plotly_white",
    )

    # REVENUE BY CATEGORY

    by_cat = (
        d.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue")
    )

    fig_cat = px.bar(
        by_cat,
        x="revenue",
        y="category",
        orientation="h",
        title="Revenue by Category",
        labels={
            "category": "Category",
            "revenue": "Revenue ($)"
        },
        template="plotly_white",
    )

    # REVENUE BY REGION

    by_reg = (
        d.groupby("region", as_index=False)["revenue"]
        .sum()
        .sort_values(
            "revenue",
            ascending=False
        )
    )

    fig_reg = px.bar(
        by_reg,
        x="region",
        y="revenue",
        title="Revenue by Region",
        labels={
            "region": "Region",
            "revenue": "Revenue ($)"
        },
        template="plotly_white",
    )

    return (
        kpis,
        fig_trend,
        fig_cat,
        fig_reg
    )


# --------------------------------------------------
# 5. RUN DASHBOARD
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=8050)

