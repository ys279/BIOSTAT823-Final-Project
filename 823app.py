
import pandas as pd
import streamlit as st
import altair as alt



session = st.sidebar.selectbox("Which session to Look at?", ["General Trend", "Map", "Covid Rate in US"])
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
    selection = st.selectbox("which country to look at:", country)
    df = df[df["Country"] == selection]
    variables = ["Confirmed","Recovered", "Deaths"]
    colors = ["steelblue", "orange", "black"]
    value_vars = variables
    SCALE = alt.Scale(domain=variables, range=colors)
    dfm = pd.melt(df.reset_index(), id_vars=["Date"], value_vars=value_vars)
    dfm['order'] = dfm['variable'].replace(
            {val: i for i, val in enumerate(variables[::-1])}
        )

    c = alt.Chart(dfm.reset_index()).mark_bar().properties(height=400,width = 350).encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("sum(value):Q", title="Cases", scale=alt.Scale(type='linear')),
            color=alt.Color('variable:N', title="Category", scale=SCALE), 
            order='order'
        )
   
    st.altair_chart(c , use_container_width=True)

if session == "Covid Rate in US":
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
    trend = ["All","active","Confirmed", "Deaths"]
    st.header("Active,Confirmed, Death Cases in US for Covid19:")
    col = st.selectbox('Which trend in US to look at', trend)
    df_us1 = df_us1.loc[:,["Date","active","Confirmed", "Deaths"]]
    colors = ["steelblue", "red","black","yellow"]
    SCALE = alt.Scale(domain=trend, range=colors)
    dfu1 = pd.melt(df_us1.reset_index(), id_vars=["Date"], value_vars=["active","Confirmed", "Deaths"])
    if col == trend[0]:
        dfu1 = dfu1
    else:
        dfu1 = dfu1[dfu1['variable']==col]
    
    c3 = alt.Chart(dfu1.reset_index()).mark_line().properties(height=400,width = 350).encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("value:Q", title="Cases", scale=alt.Scale(type='linear')),
            color=alt.Color('variable:N', title="Category", scale=SCALE)
            
        )
    st.altair_chart(c3 , use_container_width=True)
    with st.beta_expander("See explanation"):
         st.markdown("""
         Notice that the Death Rate has stabilized to a fixed rate but it is above zero a lot. We still need to take more actions to reduce mortality. Survive Rate is increasing recently which is a good trend.
         """)
    
    
    
    
    
    
