# Import packages 

import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
# Load and filter the data
df = pd.read_csv('/Users/Marcy_Student/Desktop/marcy/DA2025_Lectures/Mod2/data/sports.csv')
df = df[["sports", "rev_men", "rev_women"]].dropna()
# Pick 5 sports
top5 = ["Basketball", "Tennis", "Soccer", "Volleyball", "Golf"]
#Copying the dataframe to not overwrite the original 
df_5 = df[df["sports"].isin(top5)].copy()
df_5
# Create new column called Total_Revenue that adds up the men and women's revenue columns
df_5["Total_Revenue"] = df['rev_men'] + df['rev_women']
df_5
# Make your pie or scatteplot using plotly 

fig = px.pie(df_5, names='sports', hole=0.2, color='sports',title='Sports repartition',template='plotly_dark')
fig.show()
# Make the App -- DO NOT RUN THIS CELL YET It may give you a "port already in use error if you do"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'MY DASH APP'

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1(children='Revenue Analysis for 5 Sports'), class_name='text-center bg-light my-5', width=10)),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig,id='my_pie',className='bg-light d-flex'), width=20)]),
    dbc.Row([
        dbc.Col(html.Button('JUST DO IT', id='My_button', className='btn-lg my-3'),width='4'),
        dbc.Col(dcc.Slider(0, 4, marks={i: f'Label{i}' for i in range(5)}, value=3))
    ])
])

if __name__ == '__main__':
    app.run(debug=True)