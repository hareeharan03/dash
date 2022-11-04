import dash_bootstrap_components as dbc
#Basic Libraries
import pandas as pd
import numpy as np 

#Visualization libraries
import plotly.figure_factory as ff 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly import tools
import plotly.express as px

import dash
import plotly.graph_objs as go
from jupyter_dash import JupyterDash

#Statistical libraries an ML

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

second_data=pd.read_csv("Super_store_preprocessed.csv")

#set the assets_folder location to the assets folder which contains css files

app = dash.Dash(__name__, prevent_initial_callbacks=True,meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H2('Superstore Sales Dashboard', style={'margin-bottom': '0px', 'color': 'black'})

        ], className='one-third column', id = 'title1'),

html.Div([
            html.H4('Region', className='fix_label', style= {'color': 'black'}),
 dcc.Checklist( id="checklist",
                        options=['South', 'West', 'Central', 'East'],
                        value=['South', 'West', 'Central', 'East'],
                        inline=True,style={'text-align': 'center', 'color': 'black'},
                       className='dcc_compon'),

        ], className='one-half column', id = 'title2')

    ], id='header', className='row flex-display', style={'margin-bottom': '25px'}),

    # Number statistics & number of accidents each day

html.Div([
          html.Div([
            html.Div(id = 'text1'),
            ], className='create_container3 three columns'),
          html.Div([
            html.Div(id = 'text2'),
            ], className='create_container3 three columns'),
          html.Div([
            html.Div(id = 'text3'),
            ], className='create_container3 three columns'),
          html.Div([
            html.Div(id = 'text4'),
            ], className='create_container3 three columns'),
        ], className='row flex-display'),

    html.Div([
        html.Div([
                    
            dcc.Graph(id='graph', config={'displayModeBar': 'hover'},
                      style={'height': '350px'})

        ], className='create_container2 eight columns', style={'height': '400px'}),



html.Div([
          html.Div([
      
            dcc.Graph(id='pie', config={'displayModeBar': 'hover'},
                      style={'height': '450px'})

])

        ], className='create_container2 four columns', style={'height': '400px'}),

    ], className='row flex-display'),

    html.Div([


html.Div([

            dcc.Graph(id = 'funnel', config={'displayModeBar': 'hover'},
                      style={'height': '350px','offset': 0}),

        ], className='create_container2 five columns'),

        html.Div([

dcc.RadioItems(id = 'radio_items2',
                       labelStyle = {'display': 'inline-block'},
                       value='Sales',
                       options = [{'label': 'Sales', 'value': 'Sales'},
                                  {'label': 'Profit', 'value': 'Profit'}],
                           style={'text-align': 'center', 'color': 'black'},
                       className='dcc_compon'),

            dcc.Graph(id = 'line', config={'displayModeBar': 'hover'},
                      style={'height': '350px','offset': 1}),

        ], className='create_container2 nine columns'),


    ], className='row flex-display'),
     
  html.Div([
            
            html.Div([

            dcc.Graph(id = 'bar_chart', config={'displayModeBar': 'hover'},
                      style={'height': '350px'}),
            

        ], className='create_container2 twelve columns'),
               
     ],className='row flex-display'),

html.Div([
            
            html.Div([

            dcc.Graph(id = 'top_state', config={'displayModeBar': 'hover'},
                      style={'height': '350px'}),
            

        ], className='create_container2 six columns'),

        html.Div([

            dcc.Graph(id = 'discount', config={'displayModeBar': 'hover'},
                      style={'height': '350px'}),
            

        ], className='create_container2 six columns'),
               
     ],className='row flex-display'),

html.Div([
            
            html.Div([

            dcc.Graph(id = 'compare', config={'displayModeBar': 'hover'},
                      style={'height': '350px'}),
            

        ], className='create_container2 twelve columns'),
               
     ],className='row flex-display'),


], id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


@app.callback(
    Output("graph", "figure"),
    Input("checklist", "value"))
def update_line_chart(Region):
    mask = second_data.Region.isin(Region)
    fig = px.scatter(second_data, x=second_data[mask].groupby('State').sum()['Sales'],
                 y=second_data[mask].groupby('State').sum()['Profit'],
                 labels={"x":"Sales","y":"Profit","size":"Quantity","color":"state"},
                 size=second_data[mask].groupby('State').sum()['Quantity'],
                 color=second_data[mask].groupby('State').sum().index,
                 hover_name=second_data[mask].groupby(["State"]).sum().index,
                 #hover_data=second_data[mask].groupby('State').sum(),
                 log_x=True, size_max=50
                 )
    fig['layout']=go.Layout(title='<b>Sales & Profits by States',
                        titlefont=dict(size=16),paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(title='Sales $',titlefont=dict(size=10)),
                        yaxis=dict(title='Profits $',titlefont=dict(size=10)))
    fig.update_layout(margin = dict(t=50, b=50, l=25, r=25))

    return fig

@app.callback(
    Output("line", "figure"),
    Input("checklist", "value"),
    Input("radio_items2", "value"))
def update_line(Region,radio_items2):
    mask1 = second_data.Region.isin(Region)
    temp = second_data[mask1].groupby(by=['Sub-Category']).sum().sort_values(by='Sales',ascending=False).reset_index()
    temp2 = second_data[mask1].groupby(by=['Sub-Category']).sum().sort_values(by='Profit',ascending=False).reset_index()
    if radio_items2=="Sales":
      fig_s = px.bar(temp, x='Sub-Category', y='Sales',
                     labels={"x":"Sub-Category","y":"Sales $"},
            color='Sales',height=400)
      fig2=fig_s
      fig2['layout']=go.Layout(title='<b>Sales & Profits by Sub-Category',
                        titlefont=dict(size=16),paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        margin = dict(t=50, b=50, l=25, r=25),
                        xaxis=dict(title='Sub-Category',titlefont=dict(size=10)),
                        yaxis=dict(title='Sales $',titlefont=dict(size=10)))
    elif radio_items2 == 'Profit':
      fig_p = px.bar(temp2, x='Sub-Category', y='Profit',
                     labels={"x":"Sub-Category","y":"Sales $"},
            color='Profit',height=400)
      fig2=fig_p
      fig2['layout']=go.Layout(title='<b>Sales & Profits by Sub-Category',
                        titlefont=dict(size=16),paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        margin = dict(t=50, b=50, l=25, r=25),
                        xaxis=dict(title='Sub-Category',titlefont=dict(size=10)),
                        yaxis=dict(title='Profits $',titlefont=dict(size=10)))
    return fig2


@app.callback(
    Output("funnel", "figure"),
    Input("checklist", "value"),)
def update_funnel(Region):
    mask2 = second_data.Region.isin(Region)
    from plotly import graph_objects as go
    Category_profit=second_data[mask2].groupby("Category").sum()["Profit"].reset_index()
    Category_sales=second_data[mask2].groupby("Category").sum()["Sales"].reset_index()
    funnel_Data=pd.concat([Category_profit,Category_sales["Sales"]],axis=1)
    funnel_Data=funnel_Data.sort_values(by="Sales",ascending=False).reset_index()
    funnel_Data

    fig = go.Figure()

    fig.add_trace(go.Funnel(
        name = 'Sales',
        y = ['Office Supplies','Furniture', 'Technology'],
        x = [funnel_Data["Sales"][0],funnel_Data["Sales"][1],funnel_Data["Sales"][2]]))

    fig.add_trace(go.Funnel(
        name = 'Profit',
        orientation = "h",
        y = ['Office Supplies','Furniture', 'Technology'],
        x = [funnel_Data["Profit"][0],funnel_Data["Profit"][1],funnel_Data["Profit"][2]],
        textposition = "inside"))
    fig.update_layout(title='<b>Sales & Profits by Category',height=400,width=400,paper_bgcolor='rgba(0,0,0,0)',titlefont=dict(size=16),
                        plot_bgcolor='rgba(0,0,0,0)',margin = dict(t=50, b=50, l=25, r=25))
    return fig

@app.callback(
    Output("bar_chart", "figure"),
    Input("checklist", "value"),)
def update_funnel(Region):
    mask3 = second_data.Region.isin(Region)
    df2 = second_data[mask3].groupby(["Ship Mode","Category",'Sub-Category','Segment'])['Sales'].sum().reset_index()
    fig = px.bar(df2, x = 'Sub-Category', y = 'Sales',facet_col="Ship Mode", color='Segment',)
    fig.update_layout(title='<b>Sales with Sub-Category,segment,Ship Mode',barmode='group',paper_bgcolor='rgba(0,0,0,0)',titlefont=dict(size=16),
                        plot_bgcolor='rgba(0,0,0,0)',margin = dict(t=50, b=50, l=25, r=25))
    return fig


@app.callback(Output('text1', 'children'),
              [Input('checklist','value')])
def update_graph(Region):
    mask4 = second_data.Region.isin(Region)
    profit_f=second_data[mask4].groupby("Region").sum()["Profit"].reset_index()
    profit=profit_f["Profit"].sum()

    return [

        html.H6(children='Profit',
                style={'textAlign': 'center',
                       'color': 'black'}),

        html.P('${0:,.2f}'.format(profit),
               style={'textAlign': 'center',
                      'color': '#19AAE1',
                      'fontSize': 15,
                      'margin-top': '-10px'})

    ]

@app.callback(Output('text2', 'children'),
              [Input('checklist','value')])
def update_graph(Region):
    mask5 = second_data.Region.isin(Region)
    sales_f=second_data[mask5].groupby("Region").sum()["Sales"].reset_index()
    sales=sales_f["Sales"].sum()

    return [

        html.H6(children='Sales',
                style={'textAlign': 'center',
                       'color': 'black'}),

        html.P('${0:,.2f}'.format(sales),
               style={'textAlign': 'center',
                      'color': '#19AAE1',
                      'fontSize': 15,
                      'margin-top': '-10px'})

    ]

@app.callback(Output('text3', 'children'),
              [Input('checklist','value')])
def update_graph(Region):
    mask6 = second_data.Region.isin(Region)
    discount_f=second_data[mask6].groupby("Region").mean()["Discount"].reset_index()
    discount=discount_f["Discount"].mean()

    return [

        html.H6(children='Discount',
                style={'textAlign': 'center',
                       'color': 'black'}),

        html.P('{0:,.2f}%'.format(discount*100),
               style={'textAlign': 'center',
                      'color': '#19AAE1',
                      'fontSize': 15,
                      'margin-top': '-10px'})

    ]

@app.callback(Output('text4', 'children'),
              [Input('checklist','value')])
def update_graph(Region):
    mask7 = second_data.Region.isin(Region)
    Quantity_f=second_data[mask7].groupby("Region").sum()["Quantity"].reset_index()
    Quantity=Quantity_f["Quantity"].sum()

    return [

        html.H6(children='Quantity',
                style={'textAlign': 'center',
                       'color': 'black'}),

        html.P('{:,.2f}'.format(Quantity),
               style={'textAlign': 'center',
                      'color': '#19AAE1',
                      'fontSize': 15,
                      'margin-top': '-10px'})

    ]

@app.callback(Output('pie', 'figure'),
              [Input('checklist','value')])
def update_graph(Region):
    mask6 = second_data.Region.isin(Region)

    labels = ['Consumer', 'Corporate', 'Home Office']

    # Create subplots: use 'domain' type for Pie subplot
    segmentt=second_data[mask6].groupby("Segment")["Sales"].sum().reset_index()
    a=segmentt["Sales"][0]
    b=segmentt["Sales"][2]
    c=segmentt["Sales"][2]
    labels =labels
    values = [a,b,c]

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6)])
    fig.update_layout(
        title_text="<b>Segment by sales",paper_bgcolor='rgba(0,0,0,0)',titlefont=dict(size=16),
                        plot_bgcolor='rgba(0,0,0,0)',margin = dict(t=50, b=50, l=25, r=25))
                        
    return fig


@app.callback(Output('top_state', 'figure'),
              [Input('checklist','value')])
def update_graph(Region):
      mask6 = second_data.Region.isin(Region)
      top_state_sales = second_data[mask6].groupby('State')['Sales'].sum().sort_values(ascending=False).head(10)
      top_state_sales = top_state_sales.reset_index()

      #Generating the labels which will show the sales value in K figure
      top_state_sales['SalesK'] = ['$ '+str(round(int(v)/1000))+' K' for v in top_state_sales.Sales]
      #print(top_state_sales)

      top_state_profit = second_data[mask6].groupby(by='State').sum().sort_values(by='Sales',ascending=False).head(10)['Profit']
      top_state_profit = top_state_profit.reset_index()

      #Generating the labels which will show the sales value in K figure
      top_state_profit['ProfitK'] = ['$ '+str(round(int(v)/1000))+' K' for v in top_state_profit.Profit]
      #print(top_state_profit)

      fig = go.Figure(data = [go.Bar(
                  x=top_state_profit.Profit,
                  y=top_state_profit.State,
                  name="Profit",
                  orientation='h',
                  text = top_state_profit.ProfitK,
                  textposition='auto',
                  texttemplate='<b>%{text}',
                  width=0.5,

      ),go.Bar(
                  x=top_state_sales.Sales,
                  y=top_state_sales.State,
                  name="Sales",
                  orientation='h',
                  text = top_state_sales.SalesK,
                  textposition='auto',
                  texttemplate='<b>%{text}',
                  width=0.5,

      )])


      fig.update_layout(dict(yaxis_categoryorder = 'total ascending',
                        title={
                              'text': "<b>Top 10 States in Sales and Profit",
                              },
                          xaxis_title="Sales in $",
                          yaxis_title="States",titlefont=dict(size=16),
                          barmode='group',paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',margin = dict(t=50, b=50, l=25, r=25)))

      return fig

@app.callback(Output('compare', 'figure'),
              [Input('checklist','value')])
def update_graph(Region):
      mask6 = second_data.Region.isin(Region)

      discount_mean=second_data[mask6].groupby("Sub-Category").mean()["Discount"]
      sales=second_data[mask6].groupby("Sub-Category").sum()["Sales"]
      profit=second_data[mask6].groupby("Sub-Category").sum()["Profit"]

      # use specs parameter in make_subplots function
      # to create secondary y-axis
      fig = make_subplots(specs=[[{"secondary_y": True}]])

      # plot a bar chart by specifying the x and y values
      # Use add_trace function to specify secondary_y axes.
      fig.add_trace(
        go.Bar(x=sales.index,
                  y=sales,
                  name='Sales'),
        secondary_y=False)

      fig.add_trace(
      go.Scatter(x=discount_mean.index,
                  y=discount_mean,
                  name='discount_mean'),
        secondary_y=True)

      # Use add_trace function and specify secondary_y axes = True.
      fig.add_trace(
      go.Bar(x=profit.index,
                  y=profit,
                  name='profit'),
        secondary_y=False)



      # Adding title text to the figure
      fig.update_layout(
        title_text="<b>Sales and profit with discount",titlefont=dict(size=16),
                            barmode='group',paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',margin = dict(t=50, b=50, l=25, r=25)
      )

      # Naming x-axis
      fig.update_xaxes(title_text="Sub-Category")

      # Naming y-axes
      fig.update_yaxes(title_text="<b>Sales & Profit $</b> Y - axis ", secondary_y=False)
      fig.update_yaxes(title_text="<b>Discount</b> Y - axis ", secondary_y=True)
      return fig

@app.callback(Output('discount', 'figure'),
              [Input('checklist','value')])
def update_graph(Region):
      mask7 = second_data.Region.isin(Region)
                            
      temp = second_data.groupby('Region').sum().sort_values('Sales',ascending=False)

      fig = go.Figure(data = [go.Bar(
                        x=temp.index,
                        y=temp['Sales'],
                        name="Sales",

            ),go.Bar(
                        x=temp.index,
                        y=temp['Profit'],
                        name="Profit",


            )])
      fig.update_layout(dict(title='<b>Sales with Region',yaxis_categoryorder = 'total ascending',titlefont=dict(size=16),
                                xaxis_title="Region",
                                yaxis_title="Sales $",
                                barmode='group',paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)',margin = dict(t=50, b=50, l=25, r=25)))

      return fig


if __name__ == '__main__':
    app.run_server(debug=True)
