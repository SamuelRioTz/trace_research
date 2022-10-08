#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import requests
import json
from rasta.gpx import GpxParser
import polyline
import matplotlib.pyplot as plt
from rasta.rasta_kepler import RastaKepler # Optional


# In[2]:


def __process_gpx_file(file_name):
    """A wrapper function to read a GPX file and provide a df according to meili.
    """
    gpx_instance = GpxParser(file_name, calculate_distance=True)
    # Extract our data in a dataframe
    df = gpx_instance.data
    df= df.drop(["altitude","time", "distance"], axis=1)
    df['time'] = df.index 
    df = df.rename(columns={"longitude": "lon", "latitude": "lat"})
    return df #, html_path, vis

def create_meli_req(df_trip):
    """Returns the body for meili for its request.
    """
    # Providing needed data for the body of Meili's request
    meili_coordinates = df_trip.to_json(orient='records')
    meili_head = '{"shape":'
    meili_tail = ""","search_radius": 150, "shape_match":"map_snap", "costing":"pedestrian", "format":"osrm"}"""
    meili_request_body = meili_head + meili_coordinates + meili_tail
    return meili_request_body


# In[3]:


# Get the gpx trajectory (can be recorded from your phone)
df_trip = __process_gpx_file(r"./mini.gpx")
df_trip.head(5)


# In[4]:


# Providing headers to the request
meili_request_body = create_meli_req(df_trip)
headers = {'Content-type': 'application/json'}
trace_url = "http://localhost:8002/trace_attributes"


# In[7]:


# Sending a request yo meili and transform data
r = requests.post(trace_url, data=str(meili_request_body), headers=headers)
response_text = r.json()
# Following are the keys in the response
print(response_text.keys())


# In[8]:


# For now, just extract the matched points
matched_df = pd.DataFrame()
matched_df["lat"] = [i[0] for i in polyline.decode(response_text['shape'], 6)]
matched_df["lon"] = [i[1] for i in polyline.decode(response_text['shape'], 6)]
matched_df.head()
response_text['shape']


# In[17]:


plt.scatter(df_trip["lat"], df_trip["lon"], s=15, c='k', label='before', alpha=0.5)
plt.scatter(matched_df["lat"], matched_df["lon"], s=2, c='r', label='after')
plt.legend()


# In[12]:


MAPBOX_API_KEY = 'pk.eyJ1IjoibGVvZ2lnYSIsImEiOiJjazgxeGV2MjMwYjg3M2xwY2duMXlncDI5In0.MADt3h9xfTjNOpu-_OvbYg'
visualizer = RastaKepler(api_key=MAPBOX_API_KEY,
                         style="Dark")
visualizer.add_data(data=df_trip, names="Before")
visualizer.add_data(data=matched_df, names="After")


# In[13]:


visualizer.map.height = 800
visualizer.map


# In[11]:


response_text["edges"]



# In[ ]:




