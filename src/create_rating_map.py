# Create a map of the ratings for each genre
import plotly.graph_objects as go
import pandas as pd
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

# df = pd.read_csv('Life expectancy.csv')
# df.head()

# Read data from country_rates.csv
df = pd.read_csv('country_rates.csv')
print(df.head())

# Add column with ISO codes for each country to column "ISO-code" using pycountry
import pycountry

def get_country_code(country_name):
    try:
        return pycountry.countries.get(name=country_name).alpha_3
    except:
        print(country_name, "not found")
        return None

df['ISO-code'] = df['country'].apply(get_country_code)
print(df.head())
print(df["ISO-code"].unique(), len(df["ISO-code"].unique()))

# Create a column description with the country and the number of movies as a string
df['description'] = df['country'] + '<br>' + 'Number of movies: ' + df['number_of_movies'].astype(str)

fig = go.Figure(data=go.Choropleth(
    locations = df['ISO-code'],
    z = df['average_rating'],
    text = df['description'],
    colorscale = 'Inferno',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title = 'Mean rating',
))

fig.update_layout(
    width=1000,
    height=620,
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    title={
        'text': 'Mean movie rating by country',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
    },
    title_font_color='#525252',
    title_font_size=26,
    font=dict(
        family='Heebo', 
        size=18, 
        color='#525252'
    )
)

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