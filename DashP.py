import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Load and preprocess data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv"
df = pd.read_csv(url)
df['Year'] = pd.to_datetime(df['Date']).dt.year
df['Month'] = pd.to_datetime(df['Date']).dt.strftime("%b")

app = dash.Dash(__name__, external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"])

# Additional custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .radio-group {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }
            .radio-group label {
                margin-right: 20px;
            }
            .dropdown-container {
                margin-bottom: 20px;
            }
            .header {
                margin-top: 20px;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div(
    className="container",
    children=[
        html.H1(
            "Australia Wildfire Dashboard",
            className="header",
            style={
                'text-align': 'center',
                'font-size': '40px',
                'color': '#290707'
            }
        ),
        html.Div([
            html.H3("Select Region:"),
            dcc.RadioItems(
                options=[
                    {"label": "New South Wales", "value": "NSW"},
                    {"label": "Northern Territory", "value": "NT"},
                    {"label": "Queensland", "value": "QL"},
                    {"label": "South Australia", "value": "SA"},
                    {"label": "Tasmania", "value": "TA"},
                    {"label": "Victoria", "value": "VI"},
                    {"label": "Western Australia", "value": "WA"}
                ],
                value="NSW",
                id="region",
                inline=True,
                className="radio-group"
            )],
            style={
                "font-size": "20px",
                "color": "#290707",
                'margin-bottom': '20px'
            }
        ),
        html.Div([
            html.H3("Select Year:"),
            dcc.Dropdown(
                options=[{"label": str(year), "value": str(year)} for year in range(2006, 2021)],
                value="2006",
                id="year",
                className="form-control"
            )],
            className="dropdown-container",
            style={
                'font-size': '20px'
            }
        ),
        html.Div([
            html.Div(
                dcc.Graph(
                    id="pie",
                ),
                className="col-md-6"
            ),
            html.Div(
                dcc.Graph(
                    id="bar",
                ),
                className="col-md-6"
            )
        ],
            className="row"
        )
    ]
)

@app.callback(
    [
        Output(component_id="pie", component_property="figure"),
        Output(component_id="bar", component_property="figure")
    ],
    [
        Input(component_id="region", component_property="value"),
        Input(component_id="year", component_property="value")
    ]
)
def update_layout(region, year):
    data = df[(df['Region'] == region) & (df['Year'] == int(year))]
    
    data1 = data.groupby("Month")["Estimated_fire_area"].mean().reset_index()
    fig1 = px.pie(
        data1,
        values='Estimated_fire_area',
        names='Month',
        title=f'{region}: Monthly Average Estimated Fire Area in Year {year}'
    )
    
    data2 = data.groupby("Month")["Count"].sum().reset_index()
    fig2 = px.bar(
        data2,
        x="Month",
        y="Count",
        title=f'{region}: Average Count of Pixels for Presumed Vegetation Fires in Year {year}'
    )
    
    return fig1, fig2

if __name__ == "__main__":
    app.run_server(debug=True)
