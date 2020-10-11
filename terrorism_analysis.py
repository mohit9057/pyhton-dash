#importing libraries 
import pandas as pd                                                   #its used to import nad processing on data
import webbrowser as wb                                               #its used to open web browser
import dash                                                           #its used to use dash functionatlities
import dash_core_components as dcc                                    #its used to use dash core components
import dash_html_components as html                                   #its used to use html components
import plotly.express as px                                           #its used to use plotly express functionalities
import plotly.graph_objects as go                                     #its used to use plotly graph object functionalities
from dash.dependencies import Input as i , Output as o                #its used to take input and give output internally     
from dash.exceptions import PreventUpdate                             # its used for exception handling
 
#global variables              
app = dash.Dash()

def load_data():
    database_name = "global_terror.csv"                              #it stores the file nme in variable
    
    global df
    df = pd.read_csv(database_name)                                  #its used to read csv file
    
    global month_list
    month = {
         "January":1,
         "February": 2,
         "March": 3,
         "April":4,
         "May":5,
         "June":6,
         "July": 7,
         "August":8,
         "September":9,
         "October":10,
         "November":11,
         "December":12
         }
    month_list = [{"label" : key , "value" : values} for key , values in month.items()]
    
    global date_list
    date_list = [x for x in range(1,32)]
    
    global region_list
    region_list = [{"label" : str(regionn) , "value" : str(regionn)} for regionn in sorted(df['region_txt'].unique().tolist() ) ] #here regionn is loop vriable
    
    global country_list
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
    
    global state_list
    state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()
    
    global city_list
    city_list = df.groupby("provstate")["city"].unique().apply(list).to_dict()
    
    global attacktype_list
    attacktype_list =  [{"label" : str(attack__type) , "value" : str(attack__type)} for attack__type in sorted(df['attacktype1_txt'].unique().tolist() ) ]
    #here attack__type is loop vriable 
    
    global year_list
    year_list = sorted(df['iyear'].unique().tolist() )
    
    global year_dict
    year_dict = {str(year) : str(year) for year in year_list }
    
    # chart dropdown options
    global chart_dropdown_values
    chart_dropdown_valuess = {
                             "Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
                          
    chart_dropdown_values = [{"label" : keys , "value" : values } for keys, values in chart_dropdown_valuess.items()]
    
    #open the default web browser when run code
def open_browser():
    wb.open_new('http://127.0.0.1:4051/')
    
#layput of your page
def create_app_ui():
    #create ui of the webpage here
    main_layout = html.Div([
            html.H1("Terrorism Analysis eith Insight " , id = 'Main_Title' , style = 'align:center'),
            dcc.Tabs(id = 'Tabs' , value = 'Map',children = [
                    dcc.Tab(id = 'Map tool' , label = 'Map tool' , value = 'Map' , children = [
                            dcc.Tabs(id = 'subtabs', value = 'WorldMap', children = [
                                    dcc.Tab(id = 'World' , label = 'World Map Tool' , value = 'WorldMap'),                
                                    dcc.Tab(id = 'India' , label = 'India Map Tool' , value = 'IndiaMap')
                                    ]),#subtabs close
    dcc.Dropdown(
            id = 'month',
            options = month_list,
            multi = True,
            placeholder = 'Select Month'
            ), #month dropdown close
            
    dcc.Dropdown(
            id = 'date',
            multi = True,
            placeholder = 'Select Day'
            ),#day dropdown close
            
          dcc.Dropdown(
                id='region-dropdown', 
                options=region_list,
                placeholder='Select Region',
                multi = True
                  ),#region dropdown closed
          dcc.Dropdown(
                id='country-dropdown',
                options = [{"label": "All" , "value":"All"}],
                placeholder='Select Country',
                multi = True
                  ),#Country dropdown closed
          dcc.Dropdown(
                id='state-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select State or Province',
                multi = True
                  ),#state dropdown closed
          dcc.Dropdown(
                id='city-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select City',
                multi = True
                  ),#City dropdown closed
          dcc.Dropdown(
                id='attacktype-dropdown', 
                options= attacktype_list,
                placeholder='Select Attack Type',
                multi = True
                  ),#Attack type dropdown closed

          html.H5('Select the Year', id='year_title'),
          dcc.RangeSlider(
                    id='year-slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                      ),# Year Slider closed
        
          html.Br()#make space between components
    ]),#maptool tab close
      dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart", children=[
          dcc.Tabs(id = "subtabs2", value = "WorldChart",children = [
              dcc.Tab(label="World Chart tool", id="WorldC", value="WorldChart"),          
            dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart")
            ]),#tabs close of subtab2
            dcc.Dropdown(id="Chart_Dropdown", options = chart_dropdown_values, placeholder="Select option", value = "region_txt"), 
            html.Br(),
            html.Br(),
            html.Hr(),
            dcc.Input(id="search", placeholder="Search Filter"),#it creates a search box
            html.Hr(),
            html.Br(),
            dcc.RangeSlider(
                    id='cyear_slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                      ),#slider close
                  html.Br(),
    
                           ]),#dcc.Tab of Chart close
    
                    ]),# Tabs close
            
            html.Div(id = "graph-object", children ="Graph will be shown here")
            
            ])#Div close
            
    return main_layout

#callbacks of your page
    
@app.callback(
        o('graph-object', 'children'),#giving output
    [ #collecting inputs
    i("Tabs", "value"),
    i('month', 'value'),
    i('date', 'value'),
    i('region-dropdown', 'value'),
    i('country-dropdown', 'value'),
    i('state-dropdown', 'value'),
    i('city-dropdown', 'value'),
    i('attacktype-dropdown', 'value'),
    i('year-slider', 'value'), 
    i('cyear_slider', 'value'), 
    
    i("Chart_Dropdown", "value"),
    i("search", "value"),
    i("subtabs2", "value")
    ]#input close
    )#callback close


def update_app_ui(Tabs, month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value,chart_year_selector, chart_dp_value, search,
                   subtabs2):
    fig = None
     
    if Tabs == "Map":
        print("Data Type of month value = " , str(type(month_value)))
        print("Data of month value = " , month_value)
        
        print("Data Type of Day value = " , str(type(date_value)))
        print("Data of Day value = " , date_value)
        
        print("Data Type of region value = " , str(type(region_value)))
        print("Data of region value = " , region_value)
        
        print("Data Type of country value = " , str(type(country_value)))
        print("Data of country value = " , country_value)
        
        print("Data Type of state value = " , str(type(state_value)))
        print("Data of state value = " , state_value)
        
        print("Data Type of city value = " , str(type(city_value)))
        print("Data of city value = " , city_value)
        
        print("Data Type of Attack value = " , str(type(attack_value)))
        print("Data of Attack value = " , attack_value)
        
        print("Data Type of year value = " , str(type(year_value)))
        print("Data of year value = " , year_value)
        #checking values by printing them and their datatypes
        
        # year_filter
        year_range = range(year_value[0], year_value[1]+1)
        new_df = df[df["iyear"].isin(year_range)]
        
        # month_filter
        if month_value==[] or month_value is None:
            pass
        else:
            if date_value==[] or date_value is None:
                new_df = new_df[new_df["imonth"].isin(month_value)]
            else:
                new_df = new_df[new_df["imonth"].isin(month_value)
                                & (new_df["iday"].isin(date_value))]
        # region, country, state, city filter
        if region_value==[] or region_value is None:
            pass
        else:
            if country_value==[] or country_value is None :
                new_df = new_df[new_df["region_txt"].isin(region_value)]
            else:
                if state_value == [] or state_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value))]
                else:
                    if city_value == [] or city_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))]
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))&
                        (new_df["city"].isin(city_value))]
                        
        if attack_value == [] or attack_value is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)] 
        
        
         # You should always set the figure for blank, since this callback 
         # is called once when it is drawing for first time        
        mapFigure = go.Figure()
        if new_df.shape[0]:
            pass
        else: 
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
            
        
        mapFigure = px.scatter_mapbox(new_df,
          lat="latitude", 
          lon="longitude",
          color="attacktype1_txt",
          hover_name="city", 
          hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
          zoom=1
          )                       
        mapFigure.update_layout(mapbox_style="open-street-map",
          autosize=True,
          margin=dict(l=0, r=0, t=25, b=20),
          )
          
        fig = mapFigure

    elif Tabs=="Chart":
        fig = None
        
        year_range_c = range(chart_year_selector[0], chart_year_selector[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        
        
        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
        if chart_dp_value is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
        
        
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp_value])
            
            chart_df.loc[0] = [0, 0,"No data"]
        fig = px.area(chart_df, x="iyear", y ="count", color = chart_dp_value),
        
    return dcc.Graph(figure = fig)

@app.callback(
  o("date", "options"),
  [i("month", "value")])
def update_date(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option

@app.callback([o("region-dropdown", "value"),
               o("region-dropdown", "disabled"),
               o("country-dropdown", "value"),
               o("country-dropdown", "disabled")],
              [i("subtabs", "value")])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c



@app.callback(
    o('country-dropdown', 'options'),
    [i('region-dropdown', 'value')])
def set_country_options(region_value):
    option = []
    # Making the country Dropdown data
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    o('state-dropdown', 'options'),
    [i('country-dropdown', 'value')])
def set_state_options(country_value):
  # Making the state Dropdown data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]
@app.callback(
    o('city-dropdown', 'options'),
    [i('state-dropdown', 'value')])
def set_city_options(state_value):
  # Making the city Dropdown data
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]

# Flow of your Project
def main():
  load_data()                                                        #calling load_data function
  
  open_browser()                                                      #calling open_browser function
  
  global app
  app.layout = create_app_ui()                                        #calling creat_app_ui function
  
  app.title = "Terrorism Analysis with Insights" #its app title

  app.run_server(port = 4051) # it runs our code at server port 4051

  print("This would be executed only after the script is closed")
  #assign df and app value to none for stop running and clear data
  global df
  df = None 
  app = None


if __name__ == '__main__':
    main() #it calls main function


            
                
