# Plotly Dash
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

# READ DATA

VERSION = 'HPG-NPK #00'

# create category
# bins = [0, 0.8, 1.2, 100]
# names = ['small', 'similar', 'bigger']
# df['StarSize'] = pd.cut(df['RSTAR'], bins, labels=names)

# LAYOUT

options = [{'label': i, 'value': i} for i in [15, 30, 60, 120, 240]]
wvwma_selector = html.Div(
    [
        dbc.Label("WVWMA"),
        dcc.Dropdown(
            id='wvwma-selector',
            options=options,
            value=[],
            multi=True,
            persistence=True, persistence_type='local',
        )]
)
sma_selector = html.Div(
    [
        dbc.Label("SMA"),
        dcc.Dropdown(
            id='sma-selector',
            options=options,
            value=[],
            multi=True,
            persistence=True, persistence_type='local',
        )]
)

vol_level_selector = dcc.RangeSlider(
    id='vol-level-slider',
    min=0,
    max=100,
    value=[0, 100],
    # allowCross=False,
    # pushable=1,
    tooltip={'always_visible': True, 'placement': 'bottom'},
    persistence=True, persistence_type='local',
)
refresh = dbc.Row(
    [
        dbc.Col(dbc.Button('Refresh', id="refresh", color="primary", outline=True), width=1),
        dbc.Col(dcc.Loading(html.Div(id='out-btc'))),
        dbc.Col(html.Div(id='out-dump'), width=0),
    ], justify="start",
)
interval_reload = dcc.Interval(
    id='interval-reload',
    interval=60000,  # in milliseconds
    n_intervals=0
)

app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.FLATLY]
)

app.layout = html.Div(
    [
        interval_reload,
        dbc.Row(
            html.H1(VERSION),
            style={'margin-bottom': 40}
        ),
        dbc.Row(
            [
                dbc.Col(wvwma_selector),
                dbc.Col(sma_selector),
            ],
            style={'margin-bottom': 40}
        ),
        dbc.Row(
            html.Div(refresh),
            style={'margin-bottom': 40}
        ),
        dbc.Row(
            [
                html.Div(vol_level_selector),
                html.Div(id='btc-chart')
            ],
            style={'margin-bottom': 40}
        )
    ],
    style={'margin-left': '80px', 'margin-right': '80px'}
)

""" CALLBACK """


# @app.callback(
#     Output(component_id='out-dump', component_property='children'),
#     [Input(component_id='refresh', component_property='n_clicks'),
#      # Input(component_id='vol-level-slider', component_property='value'),
#      Input('interval-reload', 'n_intervals')]
# )
# def update_df(n, nn):
#     cry.load(limit=LIMIT)
#     return ' '


@app.callback(
    [Output(component_id='out-btc', component_property='children')],
    [Input(component_id='refresh', component_property='n_clicks'),
     Input(component_id='vol-level-slider', component_property='value'),
     Input('interval-reload', 'n_intervals'),
     Input(component_id='wvwma-selector', component_property='value'),
     Input(component_id='sma-selector', component_property='value')]
)
def update_status(n, range_vol_level, nn, wvwma_select, sma_select):
    html1 = [html.Div('N= P= K=', className='header_plots')]

    return html1


if __name__ == '__main__':
    app.run_server(port=8055, debug=True)
