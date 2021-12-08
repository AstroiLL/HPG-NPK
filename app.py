# Plotly Dash
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

# READ DATA

VERSION = 'HPG-NPK #00'

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
            dbc.Col(html.Div('N', style={'text-align': 'center'}), width={'size': 1, 'offset': 1}),
            dbc.Col(html.Div('P', style={'text-align': 'center'}), width=1),
            dbc.Col(html.Div('K', style={'text-align': 'center'}), width=1),
            dbc.Col(html.Div('Ca', style={'text-align': 'center'}), width=1),
            dbc.Col(html.Div('Mg', style={'text-align': 'center'}), width=1),
            dbc.Col(html.Div('S', style={'text-align': 'center'}), width=1),
            dbc.Col(html.Div('Cl', style={'text-align': 'center'}), width=1),
            dbc.Col(html.Div('EC', style={'text-align': 'center'}), width=1),
        ], style={'margin-top': 20}, align="center",
    ),
    dbc.Row(
        [
            # dbc.Col(html.Div(''), width=1),
            dbc.Col(dbc.Input(id='N', value=220, persistence=True, persistence_type='local'), width={'size': 1, 'offset': 1}),
            dbc.Col(dbc.Input(id='P', value=220, persistence=True, persistence_type='local'), width=1),
            dbc.Col(dbc.Input(id='K', value=220, persistence=True, persistence_type='local'), width=1),
            dbc.Col(dbc.Input(id='Ca', value=220, persistence=True, persistence_type='local'), width=1),
            dbc.Col(dbc.Input(id='Mg', value=220, persistence=True, persistence_type='local'), width=1),
            dbc.Col(dbc.Input(id='S', value=220, persistence=True, persistence_type='local'), width=1),
            dbc.Col(dbc.Input(id='Cl', value=220, persistence=True, persistence_type='local'), width=1),
            dbc.Col(dbc.Input(id='EC', value=220, persistence=True, persistence_type='local'), width=1),
        ], align="center"
    ),
    dbc.Row(
        [
            dbc.Col(html.Div('NO3', style={'text-align': 'right'}), width=1),
            dbc.Col(dbc.Input(id='NO3', value=220, persistence=True, persistence_type='local'), width=1),
            dbc.Col(html.Div('NH4:NO3'), width=1),
            dbc.Col(html.Div(id='NH4NO3_val'), width=1),
            dbc.Col(html.Div(id='N-prop'), width={"order": "last", "offset": 2}),
        ], style={'margin-top': 20}, align="center"
    ),
    dbc.Row(
        [
            dbc.Col(html.Div('NH4', style={'text-align': 'right'}), width=1),
            dbc.Col(dbc.Input(id='NH4', value=20, persistence=True, persistence_type='local'), width=1),
            dbc.Col(dbc.Input(id='NH4NO3', value=0.1, persistence=True, persistence_type='local'), width=1),
            dbc.Col(html.Div(id='NPK'), width={"order": "last", "offset": 2}),
        ], style={'margin-top': 20}, align="center"
    ),
    html.Hr(),
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

""" CALLBACK """

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
    Input('NH4NO3', 'value'),
    ]
)
def update_status(n, p, k, ca, mg, s, cl, ec, nh4no3):
    no3 = n*(1-nh4no3)
    nh4 = n*nh4no3
    n_prop = f'N={n} P={p} K={k} Ca={ca} Mg={mg} S={s} Cl={cl} sPPM={ec//2}'
    npk = f'NPK: {n}-{p}-{k} CaO={ca}% MgO={mg}% SO3={s}%'
    npk_string = f'N={n} NO3={no3} NH4={nh4} P={p} K={k} Ca={ca} Mg={mg} S={s} Cl={cl}'

    return n_prop, npk, npk_string


if __name__ == '__main__':
    app.run_server(port=8055, debug=True)
