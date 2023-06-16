from dash import Dash, html, dash_table, callback, Output, Input, dcc
import pandas as pd
from os import getcwd, path
df = pd.read_parquet(
    path.join(getcwd(), "resumes/resumes.parquet"),
    engine="fastparquet",
)
df.rename(columns={'name': 'city_name'}, inplace=True)
cities_names = df.city_name.unique().tolist()
cities_names.extend(["all"])
filters_columns = df.columns.tolist()
filters_columns.extend("default")
app = Dash(__name__)


app.layout = html.Div(
    children=[
        html.H1(children='Weather info resume', style={'textAlign': 'center'}),
        html.Div(
            [
                dcc.Dropdown(cities_names, 'all', id='city-filter', placeholder="Select a city"),
                dcc.Dropdown(filters_columns, "default", id='order-by-filter', placeholder="Order by"),
                dash_table.DataTable(data=df.to_dict('records'), page_size=20, id="resume-table"),
            ],
            style={
                "padding-top": "2em",
                "padding-bottom": "2em",
                "padding-left": "10em",
                "padding-right": "10em",
            },
        )
    ])


@callback(
    Output('resume-table', 'data'),
    [
        Input('city-filter', 'value'),
        Input('order-by-filter', 'value'),
    ]
)
def update_table(city, order_by):
    if city == "all":
        new_df = df.copy()
    else:
        new_df = df[df.city_name == city]

    if order_by != "default":
        new_df = new_df.sort_values(by=order_by)

    return new_df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
