# importing modules
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Loading dataset
df = pd.read_csv("csv_file.csv")

# Changing datetime format
df.date_added = pd.to_datetime(df.date_added, infer_datetime_format=True)

# Dropping description column
df = df.drop(['description'], axis = 1)

# Filling missing 'rating' column values
rating={67:'PG',2359:'TV-13',3660:'TV-13',3736:'UR',3737:'UR',3738:'UR',4323:'PG'}
for i, rate in rating.items():
    df.loc[i,'rating']=rate

# Treating 'country' column missing values and splitting on comma
df['country']=df['country'].fillna('United States')
df['country']=df['country'].apply(lambda x: x.split(',')[0])

# Splitting 'listed_in' column on comma
df['listed_in']=df['listed_in'].apply(lambda x: x.split(',')[0])

# Treating 'director', 'cast', 'date_added' missing values
df = df.fillna('Unavailable info')


# Categorising ratings based on age-groups and adding 'rating_ages' column
ratings_ages = {
    'TV-PG': 'Older Kids',
    'TV-MA': 'Adults',
    'TV-Y7-FV': 'Older Kids',
    'TV-Y7': 'Older Kids',
    'TV-14': 'Teens',
    'R': 'Adults',
    'TV-Y': 'Kids',
    'NR': 'Adults',
    'PG-13': 'Teens',
    'TV-G': 'Kids',
    'PG': 'Older Kids',
    'G': 'Kids',
    'UR': 'Adults',
    'NC-17': 'Adults'
}
rating_ages = pd.Series(ratings_ages)
df['rating_ages'] = df['rating'].replace(rating_ages)

# Creating a dataframe for only TV Shows
shows_df = df[df['type'] == 'TV Show']

# Adding a 'show_name' column in 'df' and grouping based on 'release_year' and 'show_name'
title_show = shows_df['title']
df['show_name'] = title_show
df_shows = df[['show_name','release_year','title']].groupby(by=['release_year','show_name']).count().reset_index()
top_10_show = df_shows[['show_name','title']].groupby(by='show_name').sum().sort_values(by='title',ascending=False).reset_index()['show_name'].head(10)

# Grouping based on 'rating' and 'show_name'
df_rating = df[['show_name','rating','title']].groupby(by=['rating','show_name']).count().reset_index()
top_10_rating = df_rating[['show_name','rating']].groupby(by='show_name').sum().sort_values(by='rating',ascending=False).reset_index()['show_name'].head(10)

# Creating a dataframe of only Movies and grouping it by 'rating_ages'
df_plot = df[df['type'] == 'Movie']
df_x = df_plot.groupby(by=["rating_ages"]).size().reset_index(name="counts")

# Creating a dataframe grouped by 'listed_in' along with its count
df_y = df.groupby(by=["listed_in"]).size().reset_index(name="counts")

# Streamlit application begins
st.markdown("""
<style>
body{
        color: #900C3F;
        background-color: #C0C0C0;
    }
</style>
     """, unsafe_allow_html=True)


st.title("Netflix TV Shows and Movies Analysis: ")
st.sidebar.title("Netflix Analysis 2020:")
st.markdown("This application is a Netflix Analysis dashboard:")
st.sidebar.markdown("This application is a Netflix Analysis dashboard:")
st.sidebar.title("TV Shows/Movies")

select = st.sidebar.selectbox('Table/Analysis', ['Dataset','TV Shows', 'Movies'], key = '1')

if not st.sidebar.checkbox('Hide', True, key = '1'):
    if select == 'Dataset':
        st.title('Netflix TV Shows and Movies Dataframe:')
        st.markdown('''This dataset consists of tv shows and movies available on Netflix as of 2019. 
        The dataset is collected from Flixable which is a third-party Netflix search engine. 
        In 2018, they released an interesting report which shows that the number of TV shows on Netflix 
        has nearly tripled since 2010. The streaming service’s number of movies has decreased 
        by more than 2,000 titles since 2010, while its number of TV shows has nearly tripled. 
        It will be interesting to explore what all other insights can be obtained from the same dataset.''')
    
        st.dataframe(df)

    elif select == 'TV Shows':
        st.title('Graphical analysis for TV Shows:')
        st.markdown('Visualising Top 10 Shows based on years: ')
        sunburst_chart1 = px.sunburst(df_shows[(df_shows['show_name'].isin(top_10_show))],
        title='Top 10 shows with year',path=['release_year','show_name'],
        template = 'plotly_dark',
        color = 'show_name',
        values='title')
        st.plotly_chart(sunburst_chart1)

        st.markdown('Visualising Top 10 shows based on rating: ')
        sunburst_chart2 = px.sunburst(df_rating[(df_rating['show_name'].isin(top_10_rating))],
        title='Top 10 shows with ratings',
        path=['rating','show_name'], 
        template = 'plotly_dark', 
        color = 'show_name', 
        values='title')
        st.plotly_chart(sunburst_chart2)

    elif select == 'Movies':
        st.title('Graphical analysis for Movies:')
        st.markdown('Visualising movies watched by different Age Groups:')
        bar1 = px.bar(data_frame=df_x, x="rating_ages", y="counts", color="rating_ages", 
        barmode="group", template = 'plotly_dark')
        st.plotly_chart(bar1)

        st.markdown('Visualising movies based on category:')
        bar2 = px.line(data_frame=df_y, x="listed_in", y="counts",template = 'plotly_dark', height = 700)
        st.plotly_chart(bar2)        
    

