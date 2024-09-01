import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Read the CSV data

# Create the Dash app
app = dash.Dash(__name__)

# Apply a dark theme
app.layout = html.Div(style={'backgroundColor': '#111', 'color': '#ccc', 'fontFamily': '"Open Sans", sans-serif', "height": "100vh", "width": "100vw", "top": 0, "left": 0, "position": "absolute"}, children=[
    html.H1(children='System Performance Dashboard', style={'textAlign': 'center'}),

    # Dropdowns for filtering
    html.Div([
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'CPU Usage', 'value': 'CPU_Percent'},
                {'label': 'Memory Usage', 'value': 'Memory_Usage'},
                {'label': 'Network I/O In', 'value': 'Network_IO_In'},
                {'label': 'Network I/O Out', 'value': 'Network_IO_Out'},
                {'label': 'Block I/O Read', 'value': 'Block_IO_Read'},
                {'label': 'Block I/O Write', 'value': 'Block_IO_Write'},
                # Add more options as needed after parsing Block_IO
            ],
            value='CPU_Percent',
            style={'width': '200px', 'margin': '10px'}
        ),
    ], style={'display': 'flex', 'justifyContent': 'center'}),

    dcc.Graph(
        id='main-graph',
    ),

    html.Div(id='min-max-display', style={'textAlign': 'center'}),
])

# Callback to update the main graph and min/max display
@app.callback(
    [Output('main-graph', 'figure'), Output('min-max-display', 'children')],
    [Input('metric-dropdown', 'value'), Input('main-graph', 'relayoutData')]
)
def update_graph(selected_metric, relayoutData):

    # Add '1' before the time unit to create a valid timedelta string
    # time_delta_str = '1' + selected_time_range
    # filtered_df = df[df['Timestamp'] >= df['Timestamp'].max() - pd.Timedelta(time_delta_str)]
    filtered_df = df

    # Create the graph
    fig = px.line(filtered_df, x='Timestamp', y=selected_metric, title=f'{selected_metric} Over Time',
                  color_discrete_sequence=["#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"])  # Demure colors

    fig.layout.template = "plotly_dark"

    # Apply zoom/pan if available
    if relayoutData and 'xaxis.range[0]' in relayoutData:
        fig.update_xaxes(range=[relayoutData['xaxis.range[0]'], relayoutData['xaxis.range[1]']])


    # Calculate and display min/max
    min_val = filtered_df[selected_metric].min()
    max_val = filtered_df[selected_metric].max()
    min_max_text = f'Min: {min_val}, Max: {max_val}'

    return fig, min_max_text


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--data', type=str, help='Path to the data file')
    args = parser.parse_args()

    df = pd.read_csv(args.data)  # Replace 'your_data.csv' with the actual file path

    # Convert 'Timestamp' to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

    # Clean and convert data types for relevant columns
    df['Memory_Usage'] = df['Memory_Usage'].astype(str).str.split(' / ').str[0]
    df['Memory_Usage'] = pd.to_numeric(df['Memory_Usage'].str.replace('MiB', '', regex=False))
    df['Memory_Percent'] = pd.to_numeric(df['Memory_Percent'].str.replace('%', '', regex=False))
    df['CPU_Percent'] = pd.to_numeric(df['CPU_Percent'].str.replace('%', '', regex=False))
    df[['Network_IO_In', 'Network_IO_Out']] = df['Network_IO'].astype(str).str.split(' / ', expand=True)
    df[['Block_IO_Read', 'Block_IO_Write']] = df['Block_IO'].astype(str).str.split(' / ', expand=True)

    app.run_server(debug=True)