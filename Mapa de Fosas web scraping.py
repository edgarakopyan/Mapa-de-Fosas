#######################################################################
##### CODE FOR SCRAPPING MAPA DE FOSAS ################################
#######################################################################

# Original link:
# https://mapadefosas.mjusticia.es/exovi_externo/CargarMapaFosas.htm

# Upload the necessary packages
import pandas as pd
import requests as req
from scrapy import Selector

# Not the tedious part. I have used specific URL combining :
# 1) rss format to get a parseable file
# 2) EPSG:4326 geolocation as this includes all of Spain.
# This is taken from: https://spatialreference.org/ref/epsg/4326/
# 3) Different layers (all in all 6 of them) which are available from
# https://mapadefosas.mjusticia.es/geoserver/wms?request=
# GetCapabilities&service=WMS
# For each layer I first made a list, then a pandas Series and finally made a
# Dataframe and specified type in each
# dataframe to make merging easier
# The numbers for loops were made experimentally: I ran with larger number
# (10 000) and would see how many NONEs I have.
# from this I got the optimal number to put in the range for the for loop

trial4 = req.get("https://mapadefosas.mjusticia.es/geoserver/wms?LAYERS=VALLE&\
    SRS=EPSG:4326&FORMAT=application/rss+xml&TRANSPARENT=true&SERVICE= \
    WMS&VERSION=1.1.1&REQUEST=GetMap&EXCEPTIONS=application/vnd. \
    ogc.se_inimage&BBOX=-10.12451171875,34.287109375,5.12451171875, \
    45.712890625&WIDTH=694&HEIGHT=520").content
VALLE = [Selector(text = trial4).xpath('//rss/channel/item//point').get()]
VALLE1 = pd.Series(VALLE)
VALLE2 = pd.DataFrame(VALLE1)
VALLE2['type'] = 'VALLE'

# NOTE: THIS ONE COUNTS BURIALS WITH SEVERAL TYPES
trial7 = req.get("https://mapadefosas.mjusticia.es/geoserver/wms?LAYERS=exovi:\
    OV_VISTA_4326_AGRUPADAS&SRS=EPSG:4326&FORMAT=application/rss+xml&\
    TRANSPARENT=true&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&EXCEPTIONS=\
    application/vnd.ogc.se_inimage&BBOX=-10.12451171875,34.287109375,\
    5.12451171875,45.712890625&WIDTH=694&HEIGHT=520").content
MULTI = []
for i in range(1,959):
    MULTI.append(Selector(text = trial7).xpath(
    '//rss/channel/item[{}]//point'.format(i)).get())
MULTI1 = pd.Series(MULTI)
MULTI2 = pd.DataFrame(MULTI1)
MULTI2['type'] = 'MULTI'

trial8 = req.get("https://mapadefosas.mjusticia.es/geoserver/wms?LAYERS=exovi:\
    OV_VISTA_4326_INTERVENIDA&SRS=EPSG:4326&FORMAT=application/\
    rss+xml&TRANSPARENT=true&SERVICE=WMS&VERSION=1.1.1&REQUEST=\
    GetMap&EXCEPTIONS=application/vnd.ogc.se_inimage&BBOX=-10.12451171875,\
    34.287109375,5.12451171875,45.712890625&WIDTH=694&HEIGHT=520").content
ROJA = []
for i in range(1,474):
    ROJA.append(Selector(text = trial8).xpath('//rss/channel/item[{}]//point'\
    .format(i)).get())
ROJA1 = pd.Series(ROJA)
ROJA2 = pd.DataFrame(ROJA1)
ROJA2['type'] = 'ROJA'

trial9 = req.get("https://mapadefosas.mjusticia.es/geoserver/wms?LAYERS=exovi:\
    OV_VISTA_4326_NOINTERV&SRS=EPSG:4326&FORMAT=application/rss+xml&TRANSPARENT\
    =true&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&EXCEPTIONS=application/vnd.\
    ogc.se_inimage&BBOX=-10.12451171875,34.287109375,5.12451171875,\
    45.712890625&WIDTH=694&HEIGHT=520").content
VERDE = []
for i in range(1,1203):
    VERDE.append(Selector(text = trial9).xpath('//rss/channel/item[{}]//point'\
    .format(i)).get())
VERDE1 = pd.Series(VERDE)
VERDE2 = pd.DataFrame(VERDE1)
VERDE2['type'] = 'VERDE'

trial10 = req.get("https://mapadefosas.mjusticia.es/geoserver/wms?LAYERS=\
    exovi:OV_VISTA_4326_PROSPECTADA&SRS=EPSG:4326&FORMAT=application/\
    rss+xml&TRANSPARENT=true&SERVICE=WMS&VERSION=1.1.1&REQUEST=\
    GetMap&EXCEPTIONS=application/vnd.ogc.se_inimage&BBOX=-10.12451171875,\
    34.287109375,5.12451171875,45.712890625&WIDTH=694&HEIGHT=520").content
BLANCA = []
for i in range(1,247):
    BLANCA.append(Selector(text = trial10).xpath(\
    '//rss/channel/item[{}]//point'.format(i)).get())
BLANCA1 = pd.Series(BLANCA)
BLANCA2 = pd.DataFrame(BLANCA1)
BLANCA2['type'] = 'BLANCA'

trial11 = req.get("https://mapadefosas.mjusticia.es/geoserver/wms?LAYERS=\
    exovi:OV_VISTA_4326_RELAC_VALLE&SRS=EPSG:4326&FORMAT=application/\
    rss+xml&TRANSPARENT=true&SERVICE=WMS&VERSION=1.1.1&REQUEST=\
    GetMap&EXCEPTIONS=application/vnd.ogc.se_inimage&BBOX=-10.12451171875,\
    34.287109375,5.12451171875,45.712890625&WIDTH=694&HEIGHT=520").content
AMARILLA = []
for i in range(1,500):
    AMARILLA.append(Selector(text = trial11).xpath(\
    '//rss/channel/item[{}]//point'.format(i)).get())
AMARILLA1 = pd.Series(AMARILLA)
AMARILLA2 = pd.DataFrame(AMARILLA1)
AMARILLA2['type'] = 'AMARILLA'

# Finally making the dataframe
frames = [BLANCA2, AMARILLA2, VERDE2, ROJA2, VALLE2, MULTI2]
result = pd.concat(frames)
result = result.reset_index(drop = True)
# Clearing position variable from useless strings and dividing into
# long/lat locations
for i in range(0, result.shape[0]):
    result[0].iloc[i] = result[0].iloc[i].replace("<point>", "" ).replace(\
    "</point>", "")
result[['Latitude', 'Longtitude']] = result[0].str.split(" ", expand = True)
result = result.drop(columns = 0)
# Saving the dataset
result.to_csv('Mapa_de_fosas.csv')
