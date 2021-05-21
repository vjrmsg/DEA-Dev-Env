from flask import Flask, render_template
import folium

from folium import plugins

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv('.\data_given\RI_CrashData.csv')

df_minor_delay_traffic=df[df['Severity']==1].reset_index(drop=True)
print (df_minor_delay_traffic.shape)
df_minor_delay_traffic.head(2)
#df.shape
df_crashes = pd.read_csv('.\data_given\RI_CrashData.csv')
#df_crashes.groupby('Street')['Side'].apply(lambda x: x.value_counts().head(1)).reset_index(name='COUNT').rename(columns={'level_1': 'Street'})
df_crashes=df_crashes[df_crashes['Latitude'].notna()]
df_crashes=df_crashes[df_crashes['Longitude'].notna()]

df_major_delay_traffic=df[df['Severity']!=1].reset_index(drop=True)
print(df_major_delay_traffic.shape)
df_major_delay_traffic.head(2)

df_minor_delay_traffic1=df_minor_delay_traffic.head(1000)
df_major_delay_traffic1=df_major_delay_traffic.head(1000)

df['Severity'].unique().tolist()
df['Latitude']=df[['Latitude']].astype(float)
df['Longitude']=df[['Longitude']].astype(float)
df=df.dropna(subset=['Latitude', 'Longitude','Street'])
df.isnull().sum()
#Change the Start_Time column to date data tpe.
df['Start_Time']=pd.to_datetime(df['Start_Time'])
df_crashes['Start_Time']=pd.to_datetime(df_crashes['Start_Time'])
df=df[(df['Start_Time']>='2016-01-01')&(df['Start_Time']<='2020-12-31')]
df_crashes=df_crashes[(df_crashes['Start_Time']>='2016-01-01')&(df_crashes['Start_Time']<='2020-12-31')]
df['Hour']=df['Start_Time'].dt.hour
latitude = 41.700001
longitude = -71.500000
df['EVENT'] = df['Severity'].apply(lambda x: 0 if x!=3  else 1)
df['EVENT'].head(10)
df1=df[['Severity','Latitude','Longitude','Street', 'EVENT']]
df1= df1.head(1000)
colordict = {1: 'red', 0: 'yellow'}
df['Start_Time']=pd.to_datetime(df['Start_Time'])
df_crashes['Start_Time']=pd.to_datetime(df_crashes['Start_Time'])
df=df[(df['Start_Time']>='2016-01-01')&(df['Start_Time']<='2020-12-31')]
df_crashes=df_crashes[(df_crashes['Start_Time']>='2016-01-01')&(df_crashes['Start_Time']<='2020-12-31')]

df['Hour']=df['Start_Time'].dt.hour
app = Flask(__name__)

@app.route('/')
def index():
       
        map_test1 = folium.Map(location=[latitude,longitude], zoom_start=7, tiles='Stamen Terrain')
        incidents_accident = folium.map.FeatureGroup()
#latitudes = list(filter(None,df_major_delay_traffic1.Latitude))
#longitudes = list(filter(None,df_major_delay_traffic1.Longitude))
        latitudes = list(df_major_delay_traffic1.Latitude)
        longitudes = list(df_major_delay_traffic1.Longitude)
        labels = list(df_major_delay_traffic1.County)
#df_accident1.head(2)
#for lat, lng, label in zip(latitudes, longitudes, labels):
        for lat, lng, label in zip(latitudes, longitudes, labels,):
     #folium.CircleMarker([lat, lng], popup=label,color='blue',fill=True).add_to(map_test)
            folium.CircleMarker(location=[lat,lng], color='blue',fill=True, popup=label).add_to(map_test1)
# add incidents to map
        map_test1.add_child(incidents_accident)
#map_test1
#MapTest2
       

#create a map centered on RI
#Accident RI details by County

        m=folium.Map(location=[41.700001,-71.500000],tiles="OpenStreetMap" ,zoom_start=12)

#instantiate a mark cluster object for street crashes.
        stcrash=plugins.MarkerCluster().add_to(m)

#Display only crashes where crashes reported in street.

        for lat,lng,st in zip(df_crashes['Latitude'],df_crashes['Longitude'],df_crashes['Street']):
                folium.Marker(
                location=[lat,lng],
                icon=None,
                popup=st
                ).add_to(stcrash)

    #Display the map

        map_test2 = folium.Map(location=[latitude,longitude], zoom_start=8, tiles='OpenStreetMap')
        labels = list(df1.Severity)
        incidents = folium.map.FeatureGroup()
        for lat, lon, traffic_q, label, in zip(df1['Latitude'], df1['Longitude'], df1['EVENT'], labels):
                folium.CircleMarker(
                [lat, lon],
                radius=5,
                popup = (label ),
                color='r',
                key_on = traffic_q,
                threshold_scale=[0,1],
                fill_color=colordict[traffic_q],
                fill=True,
                fill_opacity=0.7
                ).add_to(map_test2)
        map_test2.add_child(incidents)
        ###########################################3

       

        plt.figure(figsize=(6.4,4.8))
        #plt.figure(width=600,height=350)
        s=sns.barplot(data=df.groupby('Hour')['ID'].nunique().reset_index(),x='Hour',y='ID',palette='husl',linewidth=0)
        s.set_title('Hourly Number of reported Crashes in Rhode Island (2016 - 2020)', y=1.02, fontsize=14)
        s.set_xlabel('Hour of Day', fontsize=8, labelpad=15)
        s.set_ylabel('Number of Crashes', fontsize=8, labelpad=15)
        #plt.show()


        plt.savefig('templates/new_plot.png')
        
        map_test1.save('templates/map.html')
        m.save('templates/map2.html')
        map_test2.save('templates/map3.html')
      
        return render_template('index.html')

@app.route('/map')
def map():
    return render_template('map.html')
@app.route('/map2')
def map2():
    return render_template('map2.html')
@app.route('/map3')
def map3():
    return render_template('map3.html')
@app.route('/map4')
def map4():
    #return render_template('map4.html')
     return render_template('map4.html', url='templates/new_plot.png')

if __name__ == '__main__':
        app.run()
  
#if __name__ == '__main__':     
 #    port = int(os.environ.get('PORT', 5000))     
  #   app.run(host='127.0.0.1', port=port)