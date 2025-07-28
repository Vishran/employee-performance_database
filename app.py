import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
from database import get_processed_employee_data

# Load processed data
df = get_processed_employee_data()

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Employee Performance Dashboard"

app.layout = html.Div([
    html.H1("Employee Performance Dashboard", style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='department-filter',
        options=[{'label': dept, 'value': dept} for dept in df['department'].unique()],
        placeholder='Select Department',
        multi=True,
        style={'width': '50%', 'margin': '0 auto'}
    ),

    dcc.Graph(id='kpi-score-chart'),
    dcc.Graph(id='attendance-chart'),
    dcc.Graph(id='appraisal-rating-chart'),

    html.Div([
        html.H3("Top Performer:", style={'color': 'green'}),
        html.P(id='top-performer', style={'fontSize': '20px'}),

        html.H3("Bottom Performer:", style={'color': 'red', 'marginTop': '30px'}),
        html.P(id='bottom-performer', style={'fontSize': '20px'})
    ], style={'textAlign': 'center', 'marginTop': '40px'})
])

@app.callback(
    [Output('kpi-score-chart', 'figure'),
     Output('attendance-chart', 'figure'),
     Output('appraisal-rating-chart', 'figure'),
     Output('top-performer', 'children'),
     Output('bottom-performer', 'children')],
    [Input('department-filter', 'value')]
)
def update_dashboard(selected_departments):
    data = get_processed_employee_data()
    if selected_departments:
        data = data[data['department'].isin(selected_departments)]

    # Charts
    fig1 = px.bar(data, x='name', y='kpi_score', color='department', title='KPI Score by Employee')
    fig2 = px.bar(data, x='name', y='attendance', color='department', title='Attendance by Employee')
    fig3 = px.bar(data, x='name', y='appraisal_rating', color='department', title='Appraisal Rating by Employee')

    # Top/Bottom Performer
    top = data.loc[data['performance_score'].idxmax()]
    bottom = data.loc[data['performance_score'].idxmin()]

    top_text = f"{top['name']} (Score: {top['performance_score']:.2f})"
    bottom_text = f"{bottom['name']} (Score: {bottom['performance_score']:.2f})"

    return fig1, fig2, fig3, top_text, bottom_text

if __name__ == '__main__':
    app.run(debug=True)
