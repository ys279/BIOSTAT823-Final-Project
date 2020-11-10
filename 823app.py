import dash
import pandas as pd
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt



session = st.sidebar.selectbox("Which session to Look at?", ["General Trend", "Map", "Rate"])
st.title('🦠 Covid19 Visualization')

if session == "General Trend":
    url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv"
    df = pd.read_csv(url)
    maxr = []
    countrys = list(df.Country.unique())
    for i in countrys:
        maxr.append(df[df.Country == i].Confirmed.diff().max())
    df_inf = pd.DataFrame()
    df_inf["country"] = countrys
    df_inf["Max Infection Rate"] = maxr
    df_inf = df_inf.sort_values("Max Infection Rate",ascending=False).head(10)
    country = df_inf.country.to_list()
   
#sidebar
    st.sidebar.subheader("General trend for Covid19")
    cols = st.sidebar.multiselect('Which country to look at', country, 
                              default = country)
    st.header("Country statistics")
    st.markdown("""\
            The reported number of confirmed, recovered and dead COVID-19 cases by countries that have top10 highest max infection rate.
            """
            """The Infection Rate is the number of people one infected person goes on to infect in a specific area, over a specific time . And can be calculated as the derivative of confirmed cases.Infection Rate is one of the most important features for Covid19  because it tells us how fast COVID is spreading
         
           """     
           )
    variables = ["Confirmed","Recovered", "Deaths"]
    colors = ["steelblue", "orange", "black"]
    value_vars = variables
    SCALE = alt.Scale(domain=variables, range=colors)
    dfm = pd.melt(df.reset_index(), id_vars=["Date"], value_vars=value_vars)
    dfm['order'] = dfm['variable'].replace(
            {val: i for i, val in enumerate(variables[::-1])}
        )

    c = alt.Chart(dfm.reset_index()).mark_bar().properties(height=200).encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("sum(value):Q", title="Cases", scale=alt.Scale(type='linear')),
            color=alt.Color('variable:N', title="Category", scale=SCALE), #, sort=alt.EncodingSortField('value', order='ascending')),
            order='order'
        )
    st.altair_chart(c, use_container_width=True)
    




