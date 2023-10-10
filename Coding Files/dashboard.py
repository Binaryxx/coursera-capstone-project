# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                            id='site-dropdown',
                                            options = 
                                                [
                                                    {"label": "All Sites", "value": "all"}, 
                                                    {"label": "CCAFS LC-40	", "value": "lc-40"}, 
                                                    {"label": "CCAFS SLC-40	", "value": "slc-40"},
                                                    {"label": "KSC LC-39A	", "value": "lc-39a"},
                                                    {"label": "VAFB SLC-4E	", "value": "slc-4e"},
                                                ],
                                            value = "all", 
                                            placeholder = "Select a Launch Site", 
                                            searchable = True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min = 0,
                                                max = 10000,
                                                step = 1000,
                                                value = [min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    lc_40_df = spacex_df[spacex_df["Launch Site"] == "CCAFS LC-40"].groupby("class", as_index = False).count()
    slc_40_df = spacex_df[spacex_df["Launch Site"] == "CCAFS SLC-40"].groupby("class", as_index = False).count()
    lc_39a_df = spacex_df[spacex_df["Launch Site"] == "KSC LC-39A"].groupby("class", as_index = False).count()
    slc_4e_df = spacex_df[spacex_df["Launch Site"] == "VAFB SLC-4E"].groupby("class", as_index = False).count()

    # return the outcomes piechart for a selected site
    if entered_site == 'all':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Successful Launches by Site')
        return fig
    elif entered_site == 'lc-40':
        fig = px.pie(lc_40_df, values= 'Flight Number', 
        names='class', 
        title='Total Successful Launches by Site LC-40')
        return fig
    elif entered_site == 'slc-40':
        fig = px.pie(slc_40_df, values='Flight Number', 
        names='class', 
        title='Total Successful Launches by Site SLC-40')
        return fig
    elif entered_site == 'lc-39a':
        fig = px.pie(lc_39a_df, values='Flight Number', 
        names='class', 
        title='Total Successful Launches by Site LC-39A')
        return fig
    elif entered_site == 'slc-4e':
        fig = px.pie(slc_4e_df, values='Flight Number', 
        names='class', 
        title='Total Successful Launches by Site SLC-4E')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value"))
              
def get_scatterplot(entered_site, slider_range):
    lc_40_df = spacex_df[spacex_df["Launch Site"] == "CCAFS LC-40"]
    slc_40_df = spacex_df[spacex_df["Launch Site"] == "CCAFS SLC-40"]
    lc_39a_df = spacex_df[spacex_df["Launch Site"] == "KSC LC-39A"]
    slc_4e_df = spacex_df[spacex_df["Launch Site"] == "VAFB SLC-4E"]
    low, high = slider_range

    # return the outcomes scatterplot for a selected site
    if entered_site == 'all':
        mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(spacex_df[mask], x ='Payload Mass (kg)', y = 'class', color = "Booster Version Category") 
        return fig
    elif entered_site == 'lc-40':
        mask = (lc_40_df['Payload Mass (kg)'] > low) & (lc_40_df['Payload Mass (kg)'] < high)
        fig = px.scatter(lc_40_df[mask], x ='Payload Mass (kg)', y = 'class', color = "Booster Version Category")
        return fig
    elif entered_site == 'slc-40':
        mask = (slc_40_df['Payload Mass (kg)'] > low) & (slc_40_df['Payload Mass (kg)'] < high)
        fig = px.scatter(slc_40_df[mask], x ='Payload Mass (kg)', y = 'class', color = "Booster Version Category")
        return fig
    elif entered_site == 'lc-39a':
        mask = (lc_39a_df['Payload Mass (kg)'] > low) & (lc_39a_df['Payload Mass (kg)'] < high)
        fig = px.scatter(lc_39a_df[mask], x ='Payload Mass (kg)', y = 'class', color = "Booster Version Category")
        return fig
    elif entered_site == 'slc-4e':
        mask = (slc_4e_df['Payload Mass (kg)'] > low) & (slc_4e_df['Payload Mass (kg)'] < high)
        fig = px.scatter(slc_4e_df[mask], x ='Payload Mass (kg)', y = 'class', color = "Booster Version Category")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
