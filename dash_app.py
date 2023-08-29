import numpy as np
import pandas as pd
import xlrd
import io
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import base64

import mysql.connector


def gerar_link(link):
    try:
        link = int(link)
        return link
    except:
        inicio, fim = link.find('tnr')+3, link.find('aspx')-1
        link = link[inicio:fim]
        link = int(link)
        return link

app = dash.Dash(__name__,
external_stylesheets=[dbc.themes.CYBORG,'https://drive.google.com/uc?export=download&id=1M1XOtesUvdBHVoEkM9HGXt9Z83c2iXxi'], #'https://drive.google.com/uc?export=download&id=1M1XOtesUvdBHVoEkM9HGXt9Z83c2iXxi',
title = 'Calculadora Global Chess')

app.layout = html.Div(
    style={
        'position': 'relative',  # Ensure relative positioning for contained elements
        'overflow': 'hidden',    # Hide any overflow beyond the viewport
        'width': '100vw',
        'height': '100vh',
    },
    children=[html.Div(
            style={
                'position': 'absolute',  # Position the background container absolutely
                'top': 0,
                'left': 0,
                'width': '100%',
                'height': '100%',
                'background-image': 'url("https://www.globalchess.com.br/images/2022/04/22/gclogo_figura.png")',
                'background-size': 'cover',
                'background-position': 'center',
                'z-index': -1,  # Place the background behind other content
            }
        ),html.Div(
    children=[dcc.Download(id="download-excel"),
    dcc.Store(id='output-store'),
    html.Meta(
        name='viewport',
        content='width=device-width, initial-scale=1.0'
        ),
    html.H1(
    children='Calculadora Global Chess',
    style={
            'textAlign': 'center',
            'color':'#013A51'
        }
    ),
    html.Div([dbc.Row([
        dbc.Col([
        dbc.Input(id="input-1", placeholder="Digite o Primeiro Link", type="text")
        ],width = 'auto'),
        dbc.Col([
        dbc.Input(id="input-2", placeholder="Digite o Segundo Link", type="text")
        ],width = 'auto')
    ])],style = {"display": "flex",
                    "justify-content": "center",
                    "margin-bottom":"10px"}),
     html.Div([dbc.Button(
                        "Calcular",
                        id="botao",
                        n_clicks=0
                            )],style={
                    "display": "flex",
                    "justify-content": "center",
                    "margin-bottom":"10px"
                }),


    html.Div([dbc.Row([dbc.Col([html.Div(children=[""], id='output-3',style={
                    "display": "flex",
                    "justify-content": "center",
                    "width":"100%"
                })],width = 'auto'),
            dbc.Col([html.Div(children=[''], id='output-4',style={
                    "display": "flex",
                    "justify-content": "center",
                }),
     html.Div(children=[''], id='output-5',style={
                    "display": "flex",
                    "justify-content": "center",
                }),
                html.Div(children=[''], id='output-6',style={
                    "display": "flex",
                    "justify-content": "center",
                })],width = 'auto')])],style={
                    "display": "flex",
                    "justify-content": "center",
                })
    ],  style={
                'position': 'relative',  # Ensure relative positioning for content
                'z-index': 1,            # Place content above background
                'height': '100%',
                'width': '100%',
                'overflow': 'scroll',    # Enable scrolling for content
            }
    )])


# @app.callback(
#     Output('output', 'children'),
#     [Input('upload-data-1', 'filename')]
# )
# def atualizar_nome(filename):
#     if filename is None:
#         return 'Selecione um arquivo'
#     return filename


# @app.callback(
#     Output('output-2', 'children'),
#     [Input('upload-data-2', 'filename')]
# )
# def atualizar_nome_2(filename):
#     if filename is None:
#         return 'Selecione um arquivo'
#     return filename


@app.callback(
    Output('output-3', 'children'),
    Output('output-store', 'data'),
    Output('botao', 'n_clicks'),
    Output('output-4', 'children'),
    Output('output-6', 'children'),
    [Input('botao', 'n_clicks')],
    [Input('input-1', 'value')],
    [Input('input-2', 'value')]

)
def calcular_vencedores(cliques, tabela_1, tabela_2):

    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    triggering_input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggering_input_id != 'botao':
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update




    # if tabela_1 is None:
    #     return 'Selecione o primeiro arquivo'
    # if tabela_2 is None:
    #     return 'Selecione o segundo arquivo'
    # if cliques == 0:
    #     return 'Aperte o botão'

    # content_type, content_string = tabela_1.split(',')
    # decoded = base64.b64decode(content_string)
    # planilha = pd.read_excel(io.BytesIO(decoded))

    # inicio = (planilha[planilha['Da base de dados do torneio do Chess-Results http://chess-results.com']=='Rk.'].index.values) + 1
    # inicio = int(inicio)
    # fim = (planilha[planilha['Da base de dados do torneio do Chess-Results http://chess-results.com']=='Anotação'].index.values) - 1
    # fim = int(len(planilha) - fim)

    # base = pd.read_excel(io.BytesIO(decoded), skiprows=inicio, skipfooter=fim)
    query = "SELECT * FROM classificacao_{};".format(int(gerar_link(tabela_1)))
    db_connection = mysql.connector.connect(user='GlobalChessDatab',password='pedro100',host='GlobalChessDatabases.mysql.pythonanywhere-services.com',database='GlobalChessDatab$default')
    base = pd.read_sql(query, con=db_connection)


    base = base[['Nome','Clube/Cidade','Pontos']]

    query = "SELECT Nome,`Clube/Cidade`  FROM tnr{} where `Nome.1` = 'não emparceirado' ;".format(int(gerar_link(tabela_1)))
    db_connection = mysql.connector.connect(user='GlobalChessDatab',password='pedro100',host='GlobalChessDatabases.mysql.pythonanywhere-services.com',database='GlobalChessDatab$default')
    base_negativos = pd.read_sql(query, con=db_connection)
    base_negativos['Pontos'] = -1
    base_negativos['Clube/Cidade'] = base_negativos['Clube/Cidade'].str.upper()


    base['Clube/Cidade'] = base['Clube/Cidade'].str.upper()
    base = base.groupby('Clube/Cidade').head(5)

    base = pd.concat([base, base_negativos], axis=0)

    # content_type, content_string = tabela_2.split(',')
    # decoded = base64.b64decode(content_string)
    # planilha = pd.read_excel(io.BytesIO(decoded))

    # inicio = (planilha[planilha['Da base de dados do torneio do Chess-Results http://chess-results.com']=='Rk.'].index.values) + 1
    # inicio = int(inicio)
    # fim = (planilha[planilha['Da base de dados do torneio do Chess-Results http://chess-results.com']=='Anotação'].index.values) - 1
    # fim = int(len(planilha) - fim)

    # base2 = pd.read_excel(io.BytesIO(decoded), skiprows=inicio, skipfooter=fim)

    query = "SELECT * FROM classificacao_{};".format(int(gerar_link(tabela_2)))
    db_connection = mysql.connector.connect(user='GlobalChessDatab',password='pedro100',host='GlobalChessDatabases.mysql.pythonanywhere-services.com',database='GlobalChessDatab$default')
    base2 = pd.read_sql(query, con=db_connection)


    base2 = base2[['Rk.','Nome','Clube/Cidade','Pontos']]
    base2['Clube/Cidade'] = base2['Clube/Cidade'].str.upper()
    base2 = base2.groupby('Clube/Cidade').head(5)

    query = "SELECT Nome,`Clube/Cidade`  FROM tnr{} where `Nome.1` = 'não emparceirado' ;".format(int(gerar_link(tabela_2)))
    db_connection = mysql.connector.connect(user='GlobalChessDatab',password='pedro100',host='GlobalChessDatabases.mysql.pythonanywhere-services.com',database='GlobalChessDatab$default')
    base_negativos = pd.read_sql(query, con=db_connection)
    base_negativos['Pontos'] = -1
    base_negativos['Clube/Cidade'] = base_negativos['Clube/Cidade'].str.upper()

    base2 = pd.concat([base2, base_negativos], axis=0)


    base = pd.concat([base, base2], axis=0)
    base_store = base
    base_store = base_store.sort_values(by = 'Pontos', ascending = False).drop_duplicates(subset='Nome', keep='last').reset_index(drop=True)

    base = base.groupby('Clube/Cidade')['Pontos'].sum().reset_index().sort_values(by = 'Pontos', ascending = False)

    unique_values = base['Clube/Cidade'].drop_duplicates().tolist()

    dropdown_escolas = dbc.Select(
                        id='dropdown',
                        options=unique_values,
                        value=unique_values[0],
                        size='sm',
                        style={
                            'width': '100%',
                            "justify-content": "center"
                        },
                    )



    store_data = {'data_key': base_store.to_dict("records")}
    n_clicks_button = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    base.rename(columns={'Clube/Cidade': 'Escola'}, inplace=True)


    return (dbc.Table.from_dataframe(base, striped=True, bordered=True, hover=True,color = 'primary',size = 'sm'),store_data, n_clicks_button, dropdown_escolas, dbc.Button("Download",
                        id="download",
                        n_clicks=0,
                        color = 'success',
                        style = {"width":"100%"}
                            ))

@app.callback(
    Output('output-5', 'children'),
    [Input('dropdown', 'value')],
    [Input('output-store', 'data')]
)

def outra_tabela(value, data):
    if data is None:
        return "Data is None"

    if 'data_key' not in data:
        return "'data_key' not found in data"

    df = pd.DataFrame(data['data_key'])
    df_filtered = df[df['Clube/Cidade'] == value]
    df_filtered = df_filtered[['Nome','Pontos']].sort_values('Pontos',ascending = False)
    return dbc.Table.from_dataframe(df_filtered, striped=True, bordered=True, hover=True, color='primary', size='sm')

@app.callback(
    Output("download-excel", "data"),
    [Input("download", "n_clicks")],
    [Input('output-store', 'data')]
)
def download_excel(n_clicks, data):
    if n_clicks is None or n_clicks == 0:
        return None

    df = pd.DataFrame(data['data_key'])

    df = df.groupby('Clube/Cidade')['Pontos'].sum().reset_index().sort_values(by = 'Pontos', ascending = False)

    df.rename(columns={'Clube/Cidade': 'Escola'}, inplace=True)

    return dcc.send_data_frame(df.to_csv, "Pontuação Por Escola.csv")


if __name__ == '__main__':
    app.run_server(debug=True)
