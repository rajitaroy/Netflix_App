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

# Creating a dataframe of only Movies
df_plot = df[df['type'] == 'Movie']

# Streamlit application begins
st.title("Netflix TV Shows and Movies Analysis: ")
st.sidebar.title("Netflix Analysis 2020:")
st.markdown("This application is a Netflix Analysis dashboard:")
st.sidebar.markdown("This application is a Netflix Analysis dashboard:")
st.sidebar.title("TV Shows/Movies")

select = st.sidebar.selectbox('Table/Analysis', ['Dataset','TV Shows', 'Movies'], key = '1')

if not st.sidebar.checkbox('Hide', True, key = '1'):
    if select == 'Dataset':
        st.title('Netflix TV Shows and Movies Dataframe:')
        st.markdown('This is the entire table:')
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
        fig1 = plt.figure(figsize=(30,15))
        plt.style.use('dark_background')
        cp_rating = sns.countplot(x = 'rating_ages', data = df_plot)
        plt.xlabel('Ratings',fontsize = 30)
        plt.ylabel('Count', fontsize = 30)
        for p in cp_rating.patches:
            cp_rating.annotate(str(p.get_height()), 
            xy=(p.get_x() + p.get_width() / 2, p.get_height()),
            ha='center', va='bottom', fontsize = 25)
        plt.grid(linestyle = '-.')
        st.pyplot(fig1)

        st.markdown('Visualising movies based on category:')
        fig2 = plt.figure(figsize=(10,25))
        plt.style.use('dark_background')
        cp_standup = sns.countplot(y = 'listed_in', data = df)
        plt.xlabel('Count',fontsize = 20)
        plt.ylabel('Category', fontsize = 20)
        for p in cp_standup.patches:
            width = p.get_width()
            plt.text(5+p.get_width(), p.get_y()+0.55*p.get_height(),
            '{:1.2f}'.format(width),ha='left',va='center')
        st.pyplot(fig2)
        
    

