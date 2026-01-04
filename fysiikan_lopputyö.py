import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from scipy.signal import butter,filtfilt

url1 = "https://raw.githubusercontent.com/niko880/fysiikan-lopputyo/master/Location.csv"

url2 = "https://raw.githubusercontent.com/niko880/fysiikan-lopputyo/master/Linear Acceleration.csv"

df = pd.read_csv(url1)

df2 = pd.read_csv(url2)


st.title('Exercise analysis')

# filter linear acceleration signal
def butter_lowpass_filter(data, cutoff, nyq, order):
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

data = df2['Linear Acceleration y (m/s^2)']
T_tot = df2['Time (s)'].max()
n = len(df2['Time (s)'])

fs = n/T_tot

nyq = fs/2
order = 3
cutoff = 1/0.2

data_filt = butter_lowpass_filter(data,cutoff,nyq,order)

# calculate steps
jaksot = 0
for i in range(n-1):
    if data_filt[i]/data_filt[i+1] < 0:
        jaksot = jaksot + 1/2


st.write("Askelmäärä laskettuna suodatetusta kiihtyvyysdatasta:", jaksot)
#st.write("Keskinopeus on :", df['Speed (m/s)'].mean(),'m/s' )
#st.write("Kokonaismatka on :", df['Distance (km)'].max(),'km' )
#st.write("Askelpituus on :", df['Distance (km)'].max()/jaksot * 1000,'m' )


# draw filtered linear acceleration
df2_filt = df2.copy()
df2_filt['Linear Acceleration y (m/s^2)'] = data_filt

st.line_chart(df2_filt, x = 'Time (s)', y = 'Linear Acceleration y (m/s^2)', y_label = 'Suodatettu y (m/s^2)',x_label = 'Aika(s)')


# draw map from gps signal
start_lat = df['Latitude (°)'].mean()
start_long = df['Longitude (°)'].mean()
map = folium.Map(location = [start_lat,start_long], zoom_start = 14)

folium.PolyLine(df[['Latitude (°)','Longitude (°)']], color = 'red', weight = 3.5, opacity = 1).add_to(map)

st_map = st_folium(map, width=900, height=650)