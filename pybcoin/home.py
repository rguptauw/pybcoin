import pandas as pd
import datetime
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


app = dash.Dash(__name__,static_folder='static')
#app.scripts.config.serve_locally=True

my_css_url = "https://www.w3schools.com/w3css/4/w3.css"
app.css.append_css({
    "external_url": my_css_url
})
app.scripts.append_script({"external_url":"https://cdn.plot.ly/plotly-latest.min.js"})


timeseries_df = pd.read_csv('BitcoinPrice.csv')
timeseries_df['date'] = timeseries_df['date'].map(lambda x: datetime.datetime.strptime(x, '%m/%d/%Y'))
from_dt = datetime.datetime.strptime('2018-05-01','%Y-%m-%d')
to_dt = time.strftime("%Y-%m-%d")
filter_df = timeseries_df[(timeseries_df['date']>=from_dt) & (timeseries_df['date']<=to_dt)]

app.layout = html.Div(children=[ #Main Container
    html.Link(href='/static/mycss.css', rel='stylesheet'),
    html.Div(id="my-header",children=[ #Header
        #html.Div('KEEP CALM AND HODL',className='w3-container w3-orange w3-padding w3-margin w3-card-4 w3-round'),
        
        #html.Img(src='static/bitcoin_banner2.jpg',style={'height':'150px'})
        html.Label('KEEP CALM AND HODL??',style={'font-face':'monospace','font-size':'48px','color':'white','font-style':'italic'})
    ],style={'padding-left':'150px','padding-top':'10px'}), # Header

    html.Div(children=[ #Two column container
        
        html.Div(children=[ #w3-cell-row 1 ### ROW 1 ####
        
            html.Div(children=[ #column 1 ### SECTION 1 ####
                html.Div('Today\'s Prediction',className=' w3-panel w3-text-green w3-padding w3-margin',style={'text-shadow':'1px 1px 0 #444;','font-weight':'bold'}),
                html.Img(src='static/uparrow.png',style={'margin-left':'100px','width':'100px','height':'150px','margin-bottom':'20px'}),
                html.H1('75%',style={'position':'absolute','left':'250px','top':'200px','color':'rgb(198,223,75)'})
            ],className='w3-cell w3-half'), # column 1 ENDS
    
            html.Div(children=[ #column 2 ### SECTION 2 ####
                html.Div([
                    html.Div('Past Performance',className=' w3-panel w3-text-green w3-padding w3-margin',style={'text-shadow':'1px 1px 0 #444;','font-weight':'bold'}),
                    html.Div(children=[
                        html.Div(children=[
                                html.Label('From Date',style={'color':'white'}),
                                html.Br(),
                                dcc.Input(id='my-fromdt',value='2018-05-01', type='date'),
                        ],style={'float':'left'}),
                        html.Div(children=[
                                html.Label('To Date',style={'color':'white'}),
                                html.Br(),
                                dcc.Input(id='my-todt',value=time.strftime("%Y-%m-%d"), type='date')
                        ])
                    ],style={'margin-left':'35px'})
                ],style={'margin-top':'100px'})
                #dcc.Input(id='my-tmp',value='', type='text')
            ],className='w3-cell w3-half'), # column 2 ENDS

        ],className='w3-cell-row'), #w3-cell-row 1 ENDS

        html.Div(children=[ #w3-cell-row 2 ### ROW 2 ####
        
            html.Div(children=[ #column 1 ### SECTION 3 ####
                html.Div('Social Media Buzz!',className=' w3-panel w3-text-green w3-padding w3-margin',style={'text-shadow':'1px 1px 0 #444;','font-weight':'bold'}),
                html.Img(src='static/wordcloud.png',style={'margin-left':'35px','width':'470px','height':'340px','background-color':'white'})
            ],className='w3-cell w3-half'), # column 1 ENDS
    
            html.Div(children=[ #column 2 ### SECTION 4 ####
                html.Div('Daily Predicted Price',className=' w3-panel w3-text-green w3-padding w3-margin',style={'text-shadow':'1px 1px 0 #444;','font-weight':'bold'}),
                html.Div(children=[
                    dcc.Graph( #Graph
                        id='my-timeseries',
                        config={'displayModeBar': False},
                        figure={
                            'data': [go.Scatter(
                                    x=filter_df['date'],
                                    y=filter_df['price'],
                                    mode='line',
                                    line={'width': 1.0, 'color': 'black'}
                            )],
                            'layout':go.Layout(
                                    margin={'l': 40, 'b': 90, 't': 20, 'r': 20},
                                    height=340,width=470
                                )
                        }
                    ) #Graph
                ],style={'margin-left':'35px'},className='')
            ],className='w3-cell w3-half'), # column 2 ENDS

        ],className='w3-cell-row') #we-cell-row 2 ENDS

    ],className='w3-container w3-block'),# Two column container
    html.Br(),
    html.Br()
    #html.Link('Illustration Credit: Vecteezy.com',href='https://www.Vecteezy.com/')
])#Main Container

@app.callback(
    #dash.dependencies.Output('id-timeseries', 'figure'),
    dash.dependencies.Output('my-timeseries', 'figure'),
    [dash.dependencies.Input('my-fromdt', 'value'),
     dash.dependencies.Input('my-todt', 'value')])
def update_timeseries(from_dt,to_dt):
    from_dt = datetime.datetime.strptime(from_dt,'%Y-%m-%d')
    to_dt = datetime.datetime.strptime(to_dt,'%Y-%m-%d')
    filtered_df = timeseries_df[(timeseries_df['date']>=from_dt) & (timeseries_df['date']<=to_dt)]
    return {
            'data': [go.Scatter(
                    x=filtered_df['date'],
                    y=filtered_df['price'],
                    mode='lines+markers',
                    line={'width': 4.0, 'color': 'orange'},
                    marker={'size':6,'color':'black'}
            )],
            'layout':go.Layout(
                    margin={'l': 60, 'b': 30, 't': 20, 'r': 50},
                    height=340,width=470
                )
    }

if __name__ == '__main__':
    app.run_server(debug=True,port=8052)