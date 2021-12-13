# Plotly Dash
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output

# READ DATA

VERSION = 'HPG-NPK #02'

# LAYOUT

tab1_content = [
    # Header
    dbc.Row(
        [
            dbc.Col(html.H5('Макропрофиль в мг/л (ppm)')),
            dbc.Col(html.H6('Рассчет макропрофилей и навесок солей')),
            dbc.Col(dbc.Button('Help', id="Help", color="primary", outline=True), align="end"),
        ]
        # , style={'margin-bottom': 40}
    ),
    dbc.Row(
        [
            dbc.Col(html.Div('N', className='zag'), width={'size': 1, 'offset': 1}),
            dbc.Col(html.Div('P', className='zag'), width=1),
            dbc.Col(html.Div('K', className='zag'), width=1),
            dbc.Col(html.Div('Ca', className='zag'), width=1),
            dbc.Col(html.Div('Mg', className='zag'), width=1),
            dbc.Col(html.Div('S', className='zag'), width=1),
            dbc.Col(html.Div('Cl', className='zag'), width=1),
            dbc.Col(html.Div('EC', className='zag'), width=1),
        ], style={'margin-top': 20}, align="center",
    ),
    dbc.Row(
        [
            # dbc.Col(html.Div(''), width=1),
            dbc.Col(
                dbc.Input(
                    id='N', value=220.0, type="number", step=0.1, min=0.1, max=300, persistence=True,
                    persistence_type='local'
                ), width={'size': 1, 'offset': 1}
            ),
            dbc.Col(dbc.Input(id='P', value=40, persistence=True, persistence_type='local'), width=1),
            dbc.Col(dbc.Input(id='K', value=300, persistence=True, persistence_type='local'), width=1),
            dbc.Col(dbc.Input(id='Ca', value=150, persistence=True, persistence_type='local'), width=1),
            dbc.Col(dbc.Input(id='Mg', value=50, persistence=True, persistence_type='local'), width=1),
            dbc.Col(dbc.Input(id='S', value=40, persistence=True, persistence_type='local'), width=1),
            dbc.Col(dbc.Input(id='Cl', value=0, persistence=True, persistence_type='local'), width=1),
            dbc.Col(dbc.Input(id='EC', value=2, persistence=True, persistence_type='local'), width=1),
        ], align="center"
    ),
    dbc.Row(
        [
            dbc.Col(html.Div('NO3', style={'text-align': 'right'}), width=1),
            dbc.Col(
                dbc.Input(
                    id='NO3', type="number", step=0.1, value=0, min=0, max=300, persistence=True,
                    persistence_type='local'
                    ), width=1
                ),
            dbc.Col(html.Div('NH4:NO3'), width=1),
            dbc.Col(html.Div(id='NH4NO3_val'), width=1),
            dbc.Col(html.Div(id='N-prop'), width={"order": "last", "offset": 1}),
        ], style={'margin-top': 20}, align="center"
    ),
    dbc.Row(
        [
            dbc.Col(html.Div('NH4', style={'text-align': 'right'}), width=1),
            dbc.Col(
                dbc.Input(
                    id='NH4', type="number", step=0.1, value=0, min=0, max=300, persistence=True,
                    persistence_type='local'
                    ), width=1
                ),
            dbc.Col(
                dbc.Input(
                    id='NH4NO3', type="number", step=0.01, value=0, min=0, max=0.5, persistence=True,
                    persistence_type='local'
                ), width=1
            ),
            dbc.Col(html.Div(id='NPK'), width={"order": "last", "offset": 2}),
        ], style={'margin-top': 20}, align="center"
    ),
    # html.Hr(),
    # dash layout code
    html.Div(className='gap'),
    html.Div(className='li'),
    html.Div(className='gap'),
    html.Div(className='li'),
    dbc.Row(
        [
            dbc.Alert(id='NPK-string', color="dark"),
        ], style={'margin-top': 20}
    ),
]
tab2_content = []
tab3_content = [html.Div('2021, HPG-NPK калькулятор.'),
                html.Div('astroill@gmail.com')]

app = dash.Dash(
    # __name__, external_stylesheets=[dbc.themes.GRID]
    __name__, external_stylesheets=[dbc.themes.FLATLY]
)

app.layout = html.Div(
    [
        # interval_reload,
        # Header
        dbc.Row(
            html.H1(VERSION),
            style={'margin-bottom': 40}
        ),
        dbc.Row(
            [
                dbc.Tabs(
                    [
                        dbc.Tab(tab1_content, label='Macro'),
                        dbc.Tab(tab2_content, label='Micro'),
                        dbc.Tab(tab3_content, label='About'),
                    ]
                )
            ],
            style={'margin-bottom': 40}
        ),
    ],
    style={'margin-left': '80px', 'margin-right': '80px'}
)


def isnoneto0(x):
    return 0 if x is None else x


# CALLBACKS
@app.callback(
    [Output('NO3', 'max'),
     Output('NH4', 'max'),
     ],
    [Input('N', 'value'),
     ]
)
def update_max(n):
    return n, n/2


@app.callback(
    [Output('NO3', 'value'),
     Output('NH4', 'value'),
     Output('NH4NO3', 'value'),
     ],
    [Input('N', 'value'),
     Input('NO3', 'value'),
     Input('NH4', 'value'),
     Input('NH4NO3', 'value'),
     ]
)
def update_NH4NO3(n, no3, nh4, nh4no3):
    if n is None or no3 is None or nh4 is None or nh4no3 is None:
        return dash.no_update, dash.no_update, dash.no_update
    ctx = dash.callback_context
    # print(ctx.triggered)
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    # print(no3, nh4, nh4no3)
    if trigger_id == "NO3":
        # if no3 is None:
        #     no3 = n * (1 - nh4no3)
        nh4no3 = 1 - (no3 / n)
        nh4 = n * nh4no3
        return dash.no_update, round(nh4, 1), round(nh4no3, 2)
    if trigger_id == "NH4":
        # if nh4 is None:
        #     nh4 = n * nh4no3
        nh4no3 = nh4 / n
        no3 = n * (1 - nh4no3)
        return round(no3, 1), dash.no_update, round(nh4no3, 2)
    no3 = n * (1 - nh4no3)
    nh4 = n * nh4no3
    return round(no3, 1), round(nh4, 1), dash.no_update


@app.callback(
    [Output('N-prop', 'children'),
     Output('NPK', 'children'),
     Output('NPK-string', 'children')],
    [Input('N', 'value'),
     Input('P', 'value'),
     Input('K', 'value'),
     Input('Ca', 'value'),
     Input('Mg', 'value'),
     Input('S', 'value'),
     Input('Cl', 'value'),
     Input('EC', 'value'),
     Input('NH4', 'value'),
     Input('NO3', 'value'),
     ]
)
def update_status(n, p, k, ca, mg, s, cl, ec, nh4, no3):
    # nh4no3 = float(nh4no3)
    # no3 = n * (1 - nh4no3)
    # nh4 = n * nh4no3
    try:
        n_prop = f'N={n} P={p} K={k} Ca={ca} Mg={mg} S={s} Cl={cl} sPPM={ec / 2}'
        npk = f'NPK: {n:.0f}-{p}-{k} CaO={ca}% MgO={mg}% SO3={s}%'
        npk_string = f'N={n} NO3={no3:.1f} NH4={nh4:.1f} P={p} K={k} Ca={ca} Mg={mg} S={s} Cl={cl}'
    except:
        n_prop = 'Error inputing'
        npk = 'Error inputing'
        npk_string = 'Error inputing'

    return n_prop, npk, npk_string


if __name__ == '__main__':
    app.run_server(port=8055, debug=True)
