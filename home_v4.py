import pandas as pd
import datetime
import time
import dash
import inflect
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

p = inflect.engine()
app = dash.Dash(__name__,static_folder='static')
#app.scripts.config.serve_locally=True

my_css_url = "https://www.w3schools.com/w3css/4/w3.css"
app.css.append_css({
    "external_url": my_css_url
})
app.scripts.append_script({"external_url":"https://cdn.plot.ly/plotly-latest.min.js"})

timeseries_df = pd.read_csv('BitcoinPrice.csv').dropna()
timeseries_df['date'] = timeseries_df['date'].map(lambda x: datetime.datetime.strptime(x, '%m/%d/%Y'))
timeseries_df = timeseries_df.sort_values(by='date').reset_index(drop=True)
going_up = timeseries_df[timeseries_df['date']==max(timeseries_df['date'])].reset_index(drop=True).loc[0,'move']
confidence = int(round(timeseries_df[timeseries_df['date']==max(timeseries_df['date'])].reset_index(drop=True).loc[0,'confidence']*100))
if going_up == 1:
    color_style_class = 'w3-text-green'
    img_src = 'static/uparrow_anim.gif'
else:
    color_style_class = 'w3-text-red'
    img_src = 'static/downarrow_anim.gif'
print('going_up=',going_up)
print('img_src=',img_src)

from_dt = (max(timeseries_df['date']) - datetime.timedelta(6)).strftime("%Y-%m-%d")
to_dt = max(timeseries_df['date']).strftime("%Y-%m-%d")
filter_df = timeseries_df[(timeseries_df['date']>=from_dt) & (timeseries_df['date']<=to_dt)]
filter_df2 = filter_df.reset_index(drop=True)
marks_vals={'{}'.format(filter_df2['date'].index[filter_df2['date'] == val].tolist()[0]):\
            '{}'.format(str(val)[:10]) for val in filter_df2['date']}
marks_vals2={'{}'.format(filter_df2['date'].index[filter_df2['date'] == val].tolist()[0]):\
             '' for val in filter_df2['date']}

def update_global_vars(fr_dt,t_dt):
    global marks_vals,marks_vals2,from_dt,to_dt
    from_dt = datetime.datetime.strptime(fr_dt,'%Y-%m-%d')
    to_dt = datetime.datetime.strptime(t_dt,'%Y-%m-%d')
    filter_df = timeseries_df[(timeseries_df['date']>=from_dt) & (timeseries_df['date']<=to_dt)]
    filter_df2 = filter_df.reset_index(drop=True)
    marks_vals={'{}'.format(filter_df2['date'].index[filter_df2['date'] == val].tolist()[0]): '{}'.format(str(val)[:10]) for val in filter_df2['date']}
    marks_vals2={'{}'.format(filter_df2['date'].index[filter_df2['date'] == val].tolist()[0]):\
             '' for val in filter_df2['date']}

app.layout = html.Div(children=[ #Main Container
    html.Link(href='/static/mycss.css', rel='stylesheet'),
    html.Div(id="my-header",children=[ #Header
        html.Label('KEEP CALM AND HODL??',style={'font-face':'monospace','font-size':'48px','color':'white','font-style':'italic'})
    ],style={'padding-left':'150px','padding-top':'10px'}), # Header

    html.Div(children=[ #Two column container
        
        html.Div(children=[ #w3-cell-row 1 ### ROW 1 ####
        
            html.Div(children=[ #column 1 ### SECTION 1 ####
                html.Div(children=[
                    html.Div('Tomorrow\'s Prediction',className=color_style_class,style={'margin-right':'20px','margin-top':'60px','font-size':'24px','float':'left'}),
                    html.Img(src=img_src,style={'margin-left':'10px','width':'100px','height':'150px','margin-bottom':'20px','float':'left'}),
                    html.Div(children=[
                            html.Label(str(confidence)+'%'+' Confidence',className=color_style_class,style={'margin-left':'20px','font-size':'24px'})
                    ],style={'padding-top':'60px'}),
                ],className='',style={'margin-left':'17%'})
            ],className='w3-cell',style={}), # column 1 ENDS

        ],className='w3-cell-row w3-margin'), #w3-cell-row 1 ENDS

        html.Div(children=[ #w3-cell-row 2 ### ROW 2 ####
        
            html.Div(children=[ #column 1 ### SECTION 3 ####
                html.Div(children=[
                        html.Label(children='Social Media Buzz on ',className=color_style_class),
                        html.Label(id='my-wctitle',children='',className='w3-text-black'),
                        html.Label(children=' (Use Slider to change)',className=color_style_class)
                ],className='w3-panel w3-padding',style={'text-align':'center','text-shadow':'1px 1px 0 #444;','font-weight':'bold'}),
                html.Div(id='my-slider-parent',children=[
                    dcc.Slider(id='my-dtslider',
                                min=0,
                                max=len(marks_vals2)-1,
                                marks=marks_vals2,
                                value=0,
                            )
                ],style={'margin-left':'50px','margin-right':'50px','margin-bottom':'0px'}),
                html.Div(children=[
                    html.Div(children=[
                        html.Label(id='my-slider-leftval',children='',style={'padding-left':'10px','font-size':'12px'})
                    ],style={'width':'50%','float':'left','text-align':'left'}),
                    html.Div(children=[
                        html.Label(id='my-slider-rightval',children='',style={'padding-right':'30px','font-size':'12px'})
                    ],style={'width':'50%','text-align':'right','position':'absolute'}),
                ]),
                html.A(html.Img(id='my-wordcloud',src='static/wordcloud.png',\
                                style={'margin-left':'35px','width':'470px','height':'340px','background-color':'white'}),\
                                href='#',title='Click for Details')
            ],className='w3-cell w3-half'), # column 1 ENDS
    
            html.Div(children=[ #column 2 ### SECTION 4 ####
                #html.Div('Accuracy',className=color_style_class+' w3-panel w3-padding w3-margin',style={'text-shadow':'1px 1px 0 #444;','font-weight':'bold'}),
            
                html.Div(children=[
                    html.Div([
                        html.Div('Past Performance',className=color_style_class+' w3-panel w3-padding w3-margin',style={'text-shadow':'1px 1px 0 #444;','font-weight':'bold'}),
                        html.Div(children=[
                            html.Div(children=[
                                    dcc.DatePickerRange(
                                        id='my-datepicker',
                                        minimum_nights = 5,
                                        start_date_placeholder_text="From Date",
                                        end_date_placeholder_text="To Date",
                                        start_date=from_dt,
                                        end_date=to_dt,
                                        display_format='MMM Do, YY',
                                        max_date_allowed=to_dt,
                                        min_date_allowed='2016-01-01',
                                    )
                            ],style={'width':'100%'}),
                        ],style={'margin-left':'35px'})
                    ],style={})
                    #dcc.Input(id='my-tmp',value='', type='text')
                ],className=''),
            
                html.Div(children=[
                    dcc.Graph( #Graph
                        id='my-timeseries',
                        config={'displayModeBar': False}
                    ) #Graph
                ],style={'margin-left':'35px'},className='')
            ],className='w3-cell w3-half'), # column 2 ENDS

        ],className='w3-cell-row') #we-cell-row 2 ENDS

    ],className='w3-container w3-block'),# Two column container
    html.Br(),
    html.Br()
])#Main Container
                    
                    
@app.callback(
        dash.dependencies.Output('my-slider-parent', 'children'),
        [dash.dependencies.Input('my-datepicker', 'start_date'),
         dash.dependencies.Input('my-datepicker', 'end_date')])
def update_slider_parent(fr_dt,t_dt):
    fr_dt = fr_dt[:10]
    t_dt = t_dt[:10]
    update_global_vars(fr_dt,t_dt)
    return [dcc.Slider(id='my-dtslider',
                                min=0,
                                max=len(marks_vals2)-1,
                                marks=marks_vals2,
                                value=0,
                            )]

@app.callback(
        dash.dependencies.Output('my-timeseries', 'figure'),
        [dash.dependencies.Input('my-datepicker', 'start_date'),
         dash.dependencies.Input('my-datepicker', 'end_date')])
def update_timeseries(fr_dt,t_dt):
    fr_dt = fr_dt[:10]
    t_dt = t_dt[:10]
    from_dt = datetime.datetime.strptime(fr_dt,'%Y-%m-%d')
    to_dt = datetime.datetime.strptime(t_dt,'%Y-%m-%d')
    filter_df = timeseries_df[(timeseries_df['date']>=from_dt) & (timeseries_df['date']<=to_dt)]
    return {
            'data': [go.Scatter(
                    x=filter_df['date'],
                    y=filter_df['move'],
                    mode='lines+markers',
                    line={'width': 4.0, 'color': 'orange'},
                    marker={'size':6,'color':'black'}
            )],
            'layout':go.Layout(
                    margin={'l': 60, 'b': 30, 't': 20, 'r': 50},
                    height=340,width=470,
                    yaxis={'tickvals' : [0,1],'ticktext' : ['Miss','Hit']}
                )
    }

@app.callback(
    dash.dependencies.Output('my-wordcloud', 'src'),
    [dash.dependencies.Input('my-dtslider', 'value')])
def update_wordcloud(dt):
    pos = str(dt)
    fname = 'static/wc' + marks_vals[pos][5:7] + marks_vals[pos][8:10] + marks_vals[pos][:4] + '.png'
    return fname

@app.callback(
    dash.dependencies.Output('my-wctitle', 'children'),
    [dash.dependencies.Input('my-dtslider', 'value')])
def update_wcheader(dt):
    pos = str(dt)
    date_val = datetime.datetime.strptime(marks_vals[pos],'%Y-%m-%d')
    date_val = date_val.strftime("%b") + ' ' + p.ordinal(date_val.day) + ', ' + str(date_val.year)[2:]
    hdr = date_val
    return hdr

@app.callback(
    dash.dependencies.Output('my-slider-leftval', 'children'),
    [dash.dependencies.Input('my-datepicker', 'start_date')])
def update_slider_leftval(fr_dt):
    fr_dt = datetime.datetime.strptime(fr_dt,'%Y-%m-%d')
    left_val = fr_dt.strftime("%b") + ' ' + p.ordinal(fr_dt.day) + ', ' + str(fr_dt.year)[2:]
    return left_val

@app.callback(
    dash.dependencies.Output('my-slider-rightval', 'children'),
    [dash.dependencies.Input('my-datepicker', 'end_date')])
def update_slider_rightval(t_dt):
    t_dt = datetime.datetime.strptime(t_dt,'%Y-%m-%d')
    right_val = t_dt.strftime("%b") + ' ' + p.ordinal(t_dt.day) + ', ' + str(t_dt.year)[2:]
    return right_val
    
if __name__ == '__main__':
    app.run_server(debug=True,port=8053)