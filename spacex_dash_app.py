# Importar las librerías necesarias
import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px

# Cargar los datos desde el archivo CSV
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Preparar las opciones del Dropdown para los sitios de lanzamiento
launch_sites_options = [{'label': 'All Sites', 'value': 'ALL'}]
launch_sites_options += [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Definir el layout de la aplicación
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),
    
    dcc.Dropdown(
        id='site-dropdown',
        options=launch_sites_options,
        value='ALL',
        placeholder="Select a launch site",
        searchable=True
    ),
    
    html.Div([
        dcc.Graph(id='success-pie-chart')
    ]),
    
    html.Div([
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            marks={i: f'{i} Kg' for i in range(0, 11000, 1000)},
            value=[min_payload, max_payload]
        )
    ], style={'padding': '20px'}),
    
    html.Div([
        dcc.Graph(id='success-payload-scatter-chart')
    ])
])

# Callback para el gráfico de pastel
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, names='Launch Site', title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', title=f'Total Launches for Site {selected_site}')
    return fig

# Callback para el gráfico de dispersión
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    fig = px.scatter(
        filtered_df, 
        x='Payload Mass (kg)', 
        y='class', 
        color="Booster Version Category",
        title='Correlation between Payload and Success for selected Site'
    )
    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
