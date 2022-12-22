import pandas as pd
import numpy as np
import math
from joblib import load

import streamlit as st
model=load(filename="model_1.joblib")
def get_recommendation(root,model):
    commons_dict = {}
    for e in model.neighbors(root):
        for e2 in model.neighbors(e):
            if e2==root:
                continue
            if model.nodes[e2]['label']=="MOVIE":
                commons = commons_dict.get(e2)
                if commons==None:
                    commons_dict.update({e2 : [e]})
                else:
                    commons.append(e)
                    commons_dict.update({e2 : commons})
    movies=[]
    weight=[]
    for key, values in commons_dict.items():
        w=0.0
        for e in values:
            w=w+1/math.log(model.degree(e))
        movies.append(key) 
        weight.append(w)
    weight=np.array(weight)
    result = pd.DataFrame({"weight":weight,"movies":movies})
    result.sort_values(by=['weight'],inplace=True,ascending=False)        
    return result[:20];

def show_recommendation(data,df):
    for i in range(0,len(data)):
        temp=df.loc[df["title"]==data["movies"].iloc[i]]
        temp=temp.set_index(pd.Index(temp["title"]))
        name_genre="Title :- "+str(temp["title"].iloc[0])+"\n\n"+"Genre :- "+str(temp["Genre"].iloc[0])
        temp.drop("title",inplace=True,axis=1)
        expander = st.expander(name_genre)
        expander.dataframe(temp.iloc[0].T,use_container_width=True)
    return

def show_details(data,df):
    for i in range(0,len(data)):
        temp=df.loc[df["title"]==data["movies"].iloc[i]]
        temp=temp.set_index(pd.Index(temp["title"]))
        name_genre="Title :- "+str(temp["title"].iloc[0])+"\n\n"+"Genre :- "+str(temp["Genre"].iloc[0])
        temp.drop("title",inplace=True,axis=1)
        expander = st.sidebar.expander(name_genre)
        expander.dataframe(temp.iloc[0].T,use_container_width=True)
    return

df=pd.read_csv("netflix_data.csv")
st.set_page_config(layout="wide")

st.sidebar.title("Movie recommender")
st.sidebar.caption("Help you to find best option to watch next.")
st.sidebar.markdown("Made by [Gautam Jain](https://www.linkedin.com/in/gautam-jain-02baa222a) and [Vipul Jain](https://www.linkedin.com/in/vipul-jain2002)")

st.sidebar.markdown("---")
st.sidebar.header("Describe your past viewed movies")
no_of_movies = st.sidebar.slider("No. of movies you watched", min_value=1, max_value=10, value=5, step=1)
st.sidebar.write("Number of movies :-",no_of_movies)
movies_name = st.sidebar.multiselect("Choose your past views",df["title"], help="Enter the title of past views",max_selections=no_of_movies)
st.sidebar.write("About the movies of you choice:-")
input_data=pd.DataFrame({"movies":movies_name})
show_details(input_data,df)

st.sidebar.markdown("---")
toggle = st.sidebar.checkbox("Toggle Update", value=True, help="Continuously update the recommendations with every change in the app.")
click = st.sidebar.button("Find Recommendations", disabled=bool(toggle))
st.sidebar.markdown("---")

if click or toggle:
     st.title("MOVIE RECOMMENDER")
     movies=[]
     weight=[]
     # data = pd.Series(data=np.array(weight),index=movies)
     data = pd.DataFrame({"weight":weight,"movies":movies})
     st.markdown("---")
     for i in movies_name:
          temp=get_recommendation(i,model)
          data=pd.concat([data,temp])
     data.sort_values(by=["weight"],inplace=True,ascending=False)
     show_recommendation(data[:40],df)
     st.markdown("---")
else:
     st.info("👈  Click on 'Find recommendations' ot turn on 'Toggle Update' to see the color palette.")

st.markdown("Get the code for this [Github](https://www.linkedin.com/in/gautam-jain-02baa222a)")