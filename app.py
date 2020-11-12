
import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import timedelta, datetime,date

session = st.sidebar.selectbox("Which session to Look at?", ["General Trend", "Map", "Covid19 in US"])
st.title('🦠 Covid19 Visualization')

if session == "General Trend":
    url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv"
    df = pd.read_csv(url)
    
    maxr = []
    countrys = list(df.Country.unique())
    for i in countrys:
        maxr.append(df[df.Country == i].Confirmed.diff().max())
    df_inf = pd.DataFrame()
    df_inf["countryy"] = countrys
    df_inf["Max Infection Rate"] = maxr
    df_inf = df_inf.sort_values("Max Infection Rate",ascending=False).head(10)
    country = df_inf.countryy.to_list()
   
#sidebar
    st.sidebar.subheader("General death,recover and confirmed cases trend for Covid19")
    st.sidebar.subheader("General cases or Incident/infection Rate among countries")
    s2 = st.sidebar.selectbox(
            "Choose cases or rate",
             ["cases","rate"]
        )
    st.header("Country statistics")
    st.markdown("""\
            The reported number of confirmed, recovered and dead COVID-19 cases by countries that have top10 highest max infection rate.
            """
            """The Infection Rate is the number of people one infected person goes on to infect in a specific area, over a specific time . And can be calculated as :  
            
            The derivative of Confirmed cases  
            
            Infection Rate is one of the most important features for Covid19  because it tells us how fast COVID is spreading.
         
           """     
           )
    c1 = alt.Chart(df_inf).properties(width=150,height = 300).mark_bar().encode(
            x=alt.X("Max Infection Rate:Q", title="Max Infection Rate"),
            y=alt.Y("countryy:N", title="Countries", sort=None),
            color=alt.Color('countryy:N', title="Country"),
        tooltip=[alt.Tooltip('countryy:N', title='Country'), 
                     alt.Tooltip('Max Infection Rate:Q', title='Max Infection Rate'),
                     alt.Tooltip('inhabitants:Q', title='Inhabitants [mio]')]
                     )
    st.altair_chart(c1, use_container_width=True)
    selection = st.selectbox("Which country to look at:", country)
    df = df[df["Country"] == selection]
    variables = ["Confirmed","Recovered", "Deaths"]
    colors = ["steelblue", "orange", "black"]
    value_vars = variables
    SCALE = alt.Scale(domain=variables, range=colors)
    dfm = pd.melt(df.reset_index(), id_vars=["Date"], value_vars=value_vars)
    dfm['order'] = dfm['variable'].replace(
            {val: i for i, val in enumerate(variables[::-1])}
        )
    if s2 == "cases":
        c = alt.Chart(dfm.reset_index()).mark_bar().properties(height=400,width = 350).encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("sum(value):Q", title="Cases", scale=alt.Scale(type='linear')),
            color=alt.Color('variable:N', title="Category", scale=SCALE), 
            order='order'
        )
   
        st.altair_chart(c , use_container_width=True)
    else:
        df["Infection Rate"] = df.Confirmed.diff()
        df["Incident Rate"] = df.Confirmed/1000
        df = df.loc[:,["Date","Infection Rate","Incident Rate"]]
        dfr = pd.melt(df.reset_index(), id_vars=["Date"], value_vars=["Infection Rate","Incident Rate"])
        SCALE = alt.Scale(domain= ["Infection Rate","Incident Rate"], range= ["steelblue", "orange"])
        c_r = alt.Chart(dfr.reset_index()).mark_line().properties(height=400,width = 350).encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("value:Q", title="Rate", scale=alt.Scale(type='linear')),
            color=alt.Color('variable:N', title="Category", scale=SCALE)
        )
   
        st.altair_chart(c_r , use_container_width=True)
        

if session == "Covid19 in US":
    url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv"
    df = pd.read_csv(url)
    
    
    df_us = df[df.Country == "US"]
    df_us["infection rate"] = df_us["Confirmed"].diff()
    df_us["death rate"] = 100*df_us["Deaths"].values/df_us["Confirmed"]
    df_us["survive rate"] =100*df_us["Recovered"].values/df_us["Confirmed"]
    rate = ["death rate","survive rate"]
    df_us = df_us.loc[:,["Date","death rate","survive rate"]]
    colors = ["steelblue", "red"]
    SCALE = alt.Scale(domain=rate, range=colors)
    
    st.sidebar.subheader("Death and Survive rate in US for Covid19")
    cols = st.sidebar.multiselect('Which feature to look at', rate, 
                              default = rate)
    st.header("US statistics")
    st.markdown("""\
            From the first General Trend Page, we know that US has the most severe cases worldwid. This page will foucus on visualization covid in US. Death and Survive rates help us understand the severity of Covid19, identify at-risk populations, and evaluate quality of healthcare in US.
            """
            """Death/Survived Rate can be calculated as :  
            
            Number of Death/Survived in US / Number of Confirmed cases in US
            """     
           )
    dfu = pd.melt(df_us.reset_index(), id_vars=["Date"], value_vars=["death rate","survive rate"])
    dfu = dfu[dfu['variable'].isin(cols)]
    c2 = alt.Chart(dfu.reset_index()).mark_line().properties(height=400,width = 350).encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("value:Q", title="Percent", scale=alt.Scale(type='linear')),
            color=alt.Color('variable:N', title="Category", scale=SCALE)
        )
   
    st.altair_chart(c2 , use_container_width=True)
    with st.beta_expander("See explanation"):
         st.markdown("""
         Notice that the Death Rate has stabilized to a fixed rate but it is above zero a lot. We still need to take more actions to reduce mortality. Survive Rate is increasing recently which is a good trend.
         """)
    df_us1 = df[df.Country == "US"]
    df_us1["active"] = df_us1.Confirmed - (df_us1.Deaths + df_us1.Recovered)
    trend = ["active","Confirmed", "Deaths"]
    st.sidebar.subheader("Active,Confirmed, Death Cases in US for Covid19:")
    col = st.sidebar.multiselect('Which Cases in US to look at', trend, 
                              default = trend)
    df_us1 = df_us1.loc[:,["Date","active","Confirmed", "Deaths"]]
    colors = ["steelblue", "red","black"]
    SCALE = alt.Scale(domain=trend, range=colors)
    dfu1 = pd.melt(df_us1.reset_index(), id_vars=["Date"], value_vars=["active","Confirmed", "Deaths"])
    dfu1 = dfu1[dfu1['variable'].isin(col)]
    
    c3 = alt.Chart(dfu1.reset_index()).mark_line().properties(height=400,width = 350).encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("value:Q", title="Cases", scale=alt.Scale(type='linear')),
            color=alt.Color('variable:N', title="Category", scale=SCALE)
            
        )
    st.altair_chart(c3 , use_container_width=True)
    with st.beta_expander("See explanation"):
         st.markdown("""
         Notice that in US, the confirmed cases is extremly high which need us to make more attention to this.Though the death cases is not very high, the active cases is still a lot which means it is hard to fully recovered.
         """)

if session == "Map":
    st.sidebar.subheader("Pick A Map")
    mapplots = st.sidebar.selectbox("Maps", ["Daily updated","Spread of COVID-19"])
    current_time = datetime.now()-timedelta(days=1)
    if current_time.hour < 13:
        current_time = datetime.now()-timedelta(days=2)
    today = current_time.strftime("%m-%d-%Y")
    px.set_mapbox_access_token('pk.eyJ1IjoibW9sdW9zaXJpdXMiLCJhIjoiY2toOTlvenZrMGEzNzJwcjFzbjNuaG42eSJ9.glsH-yMcr1tmNxlzHDsCpQ')
    
    ##spread animated
    if mapplots == "Spread of COVID-19":
        ##data cleaning and merge
        confirmed_global='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        death_global = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
        recover_global = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
        confirmed = pd.read_csv(confirmed_global)
        death = pd.read_csv(death_global)
        recover = pd.read_csv(recover_global)
        dates = confirmed.columns[4:]
        confirmed_df = confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                              value_vars=dates, var_name='Date', value_name='Confirmed')
        deaths_df = death.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                       value_vars=dates, var_name='Date', value_name='Deaths')
        recovered_df = recover.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                       value_vars=dates, var_name='Date', value_name='Recovered')
        recovered_df = recovered_df[recovered_df['Country/Region']!='Canada']
        full_table = confirmed_df.merge(right=deaths_df, how='left',
                                        on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long'])
        full_table = full_table.merge(right=recovered_df, how='left',
                                      on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long'])
        full_table['Date'] = [d.split()[0] for d in full_table['Date']]
        full_table['Recovered'] = full_table['Recovered'].fillna(0)

        ship_rows = full_table['Province/State'].str.contains('Grand Princess') | full_table['Province/State'].str.contains('Diamond Princess') | full_table['Country/Region'].str.contains('Diamond Princess') | full_table['Country/Region'].str.contains('MS Zaandam')

        full_table = full_table[~(ship_rows)]


        
        #full_table = pd.read_csv('https://raw.githubusercontent.com/ys279/BIOSTAT823-Final-Project/xiangwenmo/covid19_merged1108.csv')
        full_table['Date_datetype'] = pd.to_datetime(full_table['Date'])
        def date_range(start_date, end_date):
            return (full_table['Date_datetype'] > start_date) & (full_table['Date_datetype']<end_date)
        #default graph
        
        
        start_date = st.sidebar.text_input('Start date (no late than 2020/1/22)',"2020-03-22")
        end_date = st.sidebar.text_input('End date', "2020-05-03")
        
   
        st.sidebar.subheader("check the box only after you select both Start and End Date")
        if st.sidebar.checkbox("Show me the spread ", value=True):
            mask = date_range(start_date, end_date)
            animate = px.scatter_mapbox(full_table[mask],lat="Lat", lon="Long",
                                        animation_frame = 'Date', animation_group = 'Country/Region',
                                        color="Confirmed", size="Confirmed",
                                        color_continuous_scale=px.colors.sequential.RdBu, 
                                        size_max=70, zoom=0.7, hover_name='Country/Region',
                                        hover_data = ['Confirmed', 'Deaths', 'Recovered'],
                                        title = 'Spread of COVID-19 from {start} to {end}'.format(start = start_date, end = end_date)
                                       )
            animate.update_layout(autosize = False, height = 600, width = 800)
        
            st.plotly_chart(animate)
     
    #daily data
    def read_daily_data(url):
        df = pd.read_csv(url)
        df = df.dropna(axis=0, subset=['Lat'])
        df = df.fillna(0)
        df['Active'] = df['Active'].astype(int)
        df[df['Active'] < 0] = 0
        return df
    
    ##global daily update
    if mapplots == "Daily updated":
        g_or_us = st.sidebar.selectbox("Global or U.S.", ["Global", "U.S."])
        daily_global = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}.csv'.format(today)
        daily_us = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/{}.csv'.format(today)
        if g_or_us == "Global":
            st.sidebar.subheader("Which information you would like to know:")
            active = st.sidebar.checkbox("Active Cases", value = True)
            ratio = st.sidebar.checkbox("Case-Fatality Ratio")
            
            g_df = read_daily_data(daily_global)
            date, time = g_df.iloc[0,4].split()
            g_df["Province_State"].replace(0, '', inplace = True)
            g_df['Regions'] = g_df[["Province_State", "Country_Region"]].astype(str).apply(lambda x: " ".join(x), axis = 1)
            if active:
                g_f = px.scatter_mapbox(g_df,  
                                        lat="Lat", lon="Long_",     
                                        color="Active", size="Active",
                                        color_continuous_scale=px.colors.sequential.Jet, 
                                        size_max=40, zoom=0.8,center={"lat": 26.978, "lon": -10.249},
                                        hover_data=["Confirmed"],hover_name='Regions'
                                       )
                g_f.update_layout(title=f'COVID-19 Global Active cases by country. Date: {date}',
                                  autosize = False, height = 550, width = 800
                                 )
                
                st.plotly_chart(g_f)
            if ratio:
                #calculate ratio
                g_df["Case-Fatality Ratio"] = (g_df["Deaths"]/g_df["Confirmed"])*100
                g_df["Case-Fatality Ratio"] = g_df["Case-Fatality Ratio"].fillna(0)
                #calculate ratio for each state of US and change Lat and Long corresponding only to each state
                us_df = pd.read_csv(daily_us)
                us_df["Case-Fatality Ratio"] = (us_df["Deaths"]/us_df["Confirmed"])*100
                for state in us_df.Province_State:
                    g_df["Lat"] = np.where((g_df.Province_State == state),us_df[us_df["Province_State"] == state].Lat.values,g_df['Lat'])
                    g_df["Long_"] = np.where((g_df.Province_State == state),us_df[us_df["Province_State"] == state].Long_.values,g_df['Long_'])
                    g_df['Case-Fatality Ratio'] = np.where((g_df.Province_State == state),us_df[us_df["Province_State"] == state].iloc[:,-1].values,g_df['Case-Fatality Ratio'])
                g_df = g_df.drop("Case_Fatality_Ratio", axis = 1)
                
                r_f = px.scatter_mapbox(g_df, lat="Lat", lon="Long_",     
                                        color="Case-Fatality Ratio", zoom=0.8,  
                                        center={"lat": 26.978, "lon": -10.249},
                                        hover_data=["Case-Fatality Ratio"],hover_name='Regions')
                r_f.update_layout(title=f'COVID-19 Global Case-Fatality Rate by country. Date: {date}',
                                  autosize = False, height = 550, width = 800
                                 )
                st.plotly_chart(r_f)
    

        if g_or_us == "U.S.": 
            st.sidebar.subheader("Which information you would like to know:")
            active = st.sidebar.checkbox("Active", value = True)
            death = st.sidebar.checkbox("Death", value = True)
            #daily_us = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/{}.csv'.format(today)
            us_df = read_daily_data(daily_us)
            date, time = us_df.iloc[0,2].split()
            if active:
                a_f = px.scatter_mapbox(us_df, lat="Lat", lon="Long_",
                                        color="Active", size="Active",
                                        color_continuous_scale=px.colors.sequential.Jet,
                                        size_max=40,
                                        zoom=2.94, 
                                        center={"lat": 38.5266, "lon": -96.72},              
                                        hover_data=["Confirmed"],
                                        hover_name='Province_State')
                a_f.update_layout(title=f'COVID-19 US Active cases by state. Date: {date}',
                                 autosize = False, height = 500, width = 800)
                st.plotly_chart(a_f)
            if death:
                us_state_abbrev = {
                    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO',
                    'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
                    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
                    'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 
                    'Mississippi': 'MS','Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 
                    'New Hampshire': 'NH', 'New Jersey': 'NJ','New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 
                    'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
                    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
                    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
                    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}
                indexNames = us_df[ us_df['ISO3'] != 'USA' ].index 
                us_df.drop(indexNames , inplace=True)
                us_df = us_df.dropna(axis=0, subset=['Lat'])
                us_df['Province_State'] = us_df['Province_State'].map(us_state_abbrev).fillna(us_df['Province_State'])
                d_f = go.Figure(data=go.Choropleth(
                    locations=us_df['Province_State'], # Spatial coordinates
                    z = us_df['Deaths'].astype(int), # Data to be color-coded
                    locationmode = 'USA-states', # set of locations match entries in `locations`
                    colorscale = 'Reds'))
                d_f.update_layout(
                    title_text = f'COVID-19 Deaths by State, Date: {date}',
                    geo_scope='usa', # limite map scope to USA
                    autosize = False, height = 500, width = 800
                )
            
                st.plotly_chart(d_f)

    
    
    
