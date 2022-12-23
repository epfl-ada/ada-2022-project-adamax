from dash import Dash, dcc, html
import plotly.express as px
from base64 import b64encode
import io
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import json
import pandas as pd

app = Dash(__name__)

buffer = io.StringIO()

# Download data from genre_rates.json
with open('genre_rates.json') as f:
    data = json.load(f)

# Read all the rows from data and create a dataframe with three columns (genre, year, rate)
df = pd.DataFrame(columns=['genre', 'year', 'rate'])
for genre in data:
    for movie in data[genre]:
        df = df.append({'genre': genre, 'year': movie[0], 'rate': movie[1]}, ignore_index=True)


# Create a plotly figure for a lineplot
fig = px.line(df, x='year', y='rate', color='genre')

# Hide all the lines
fig.for_each_trace(lambda trace: trace.update(visible="legendonly"))

# Add buttons for selecting and deselecting all the lines
fig.update_layout(dict(updatemenus=[
                        dict(
                            type = "buttons",
                            direction = "left",
                            buttons=list([
                                dict(
                                    args=["visible", "legendonly"],
                                    label="Deselect All",
                                    method="restyle"
                                ),
                                dict(
                                    args=["visible", True],
                                    label="Select All",
                                    method="restyle"
                                )
                            ]),
                            pad={"r": 10, "t": 10},
                            showactive=False,
                            x=1,
                            xanchor="right",
                            y=1.1,
                            yanchor="top"
                        ),
                    ]
              ))

fig.write_html(buffer)

html_bytes = buffer.getvalue().encode()
encoded = b64encode(html_bytes).decode()

app.layout = html.Div([
    html.H4('Simple plot export options'),
    html.P("↓↓↓ try downloading the plot as PNG ↓↓↓", style={"text-align": "right", "font-weight": "bold"}),
    dcc.Graph(id="graph", figure=fig),
    html.A(
        html.Button("Download as HTML"), 
        id="download",
        href="data:text/html;base64," + encoded,
        download="plotly_graph.html"
    )
])


app.run_server(debug=True, port=9000)