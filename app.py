import numpy as np
import pandas as pd
import streamlit as st
import preprocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

df=pd.read_csv('./athlete_events.csv')
region_df=pd.read_csv('./noc_regions.csv')
df=preprocessor.preprocess(df,region_df)
st.sidebar.title("Olympics Analysis")
menu=st.sidebar.radio(
    'Select an Option',('Medal Tally','Overall Analysis', 'Country-Wise Analysis')
)



if menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.header("Overall Tally")
    if selected_year!='Overall' and selected_country=='Overall':
        st.header("Medal Tally in " +str(selected_year)+" Olympics")
    if selected_year=='Overall' and selected_country!='Overall':
        st.header(selected_country + " overall performnace")
    if selected_year!='Overall' and selected_country!='Overall':
        st.header("Performance of "+ selected_country + " in "+ str(selected_year)+" Olympics" )
    st.table(medal_tally)

    


if menu=="Overall Analysis":
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    nations=df['region'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    st.title("Top Statistics")

    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Atheletes")
        st.title(athletes)
    
    nations_over_time=helper.data_over_time(df,'region')
    fig=px.line(nations_over_time, x="Edition" , y="region")
    st.header("Participating nations over the years")
    st.plotly_chart(fig)

    events_over_time=helper.data_over_time(df,'Event')
    fig=px.line(events_over_time, x="Edition" , y="Event")
    st.header("Events over the years")
    st.plotly_chart(fig)


    atheletes_over_time=helper.data_over_time(df,'Name')
    fig=px.line(atheletes_over_time, x="Edition" , y="Name")
    st.header("Atheletes over the years")
    st.plotly_chart(fig)

    st.header("Number of events overtime for each sport")
    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)


if menu=='Country-Wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)
    country_df=helper.year_wise_medal_tally(df,selected_country)
    fig=px.line(country_df, x="Year" , y="Medal")
    st.header(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.header("Top 10 athletes of "+selected_country)

    top_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top_df)

   




    
    





