# Import packages 

import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Input, Output

# Load and clean data
df = pd.read_csv('/Users/Marcy_Student/Desktop/marcy/DA2025_Lectures/Mod2/data/indian_food.csv')
df=df.dropna()
df.isnull().sum()
df.dtypes
df.head()

df_course= df.groupby('course')[['prep_time','cook_time']].mean().reset_index()
df_course

fig= px.bar(df_course, x='course',y='prep_time', title='prep time by course',template='plotly_dark',color='course')
fig2 = px.bar(df_course, x='course',y='cook_time', title='cook time by course',template='plotly_dark',color='course')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Indian Food Dashboard'

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Dashboard'),class_name='text-center bg-primary bg-light my-5',width= 12)]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure= fig ,id='My_graph'), class_name='bg-light',width=6),
        dbc.Col(dcc.Graph(figure= fig2 ,id='My_graph2'), class_name='bg-light',width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='my_dropdown',
            options=[{'label':course,'value':course} for course in df_course['course'].unique()],
            className='theme-dropdown text-center',
            multi=True,
            placeholder='Select a course',
            searchable= True,
            style={
                'width': '100%',
                'backgroundColor': 'lightwhite',
                'border': '1px solid #ccc',
                'font-weight': 'bold',
                'color':'black'}))
    ]),
    dbc.Row([
        dbc.Col(html.P('This is my dashboard friend, check it out and give me any feedback...N O V A', className='text-right my-5'), width=12)
    ])
],fluid=True)
@app.callback(
    Output('My_graph','figure'),
    Output('My_graph2','figure'),
    Input('my_dropdown','value')
    )

def update_chart(course_selected):
    df_course_f=df_course[df_course['course'].isin(course_selected)] if course_selected else df_course
    fig = px.bar(df_course_f, x='course',y='prep_time', title='Avg prep time by course',template='plotly_dark',color='course')
    fig2 = px.bar(df_course_f,x='course',y='cook_time',title='Avg cook time by course',template='plotly_dark',color='course')
    return fig,fig2

if __name__ == '__main__':
    app.run(debug=True)
