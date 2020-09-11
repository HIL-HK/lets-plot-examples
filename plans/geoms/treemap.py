#!/usr/bin/env python

import squarify
from shapely.geometry import Polygon
import pandas as pd
import geopandas as gpd

from lets_plot import *

def geom_treemap(treemap_aes, treemap_data, **kwargs):
    df = treemap_data.copy()
    
    width = kwargs['width'] if 'width' in kwargs else 1
    height = kwargs['height'] if 'height' in kwargs else 1
    
    aes_value = treemap_aes.as_dict()['value']
    df = df[(~df[aes_value].isna())&(df[aes_value]>0)]
    
    aes_group = 'group_column'
    if 'group' in treemap_aes.as_dict().keys():
        aes_group = treemap_aes.as_dict()['group']
    else:
        df[aes_group] = 'g0'
    
    group_rectangles_df = df.groupby(aes_group).sum()[[aes_value]]
    group_rectangles_df = group_rectangles_df.sort_values(by=aes_value, ascending=False)
    group_rectangles_df['normalized_values'] = squarify.normalize_sizes(group_rectangles_df[aes_value], width, height)
    group_rectangles_df['rectangle'] = [Polygon([(rect['x'], rect['y']), \
                                                 (rect['x'] + rect['dx'], rect['y']), \
                                                 (rect['x'] + rect['dx'], rect['y'] + rect['dy']), \
                                                 (rect['x'], rect['y'] + rect['dy'])]) \
                                        for rect in squarify.squarify(group_rectangles_df['normalized_values'], \
                                                                      0, 0, width, height)]
    
    group_dfs = []
    for group, row in group_rectangles_df.iterrows():
        x, y = row['rectangle'].bounds[0], row['rectangle'].bounds[1]
        group_width, group_height = row['rectangle'].bounds[2] - x, row['rectangle'].bounds[3] - y
        group_df = df[df[aes_group] == group]
        group_df = group_df.sort_values(by=aes_value, ascending=False)
        group_df['normalized_values'] = squarify.normalize_sizes(group_df[aes_value], group_width, group_height)
        group_df['rectangle'] = [Polygon([(rect['x'], rect['y']), \
                                          (rect['x'] + rect['dx'], rect['y']), \
                                          (rect['x'] + rect['dx'], rect['y'] + rect['dy']), \
                                          (rect['x'], rect['y'] + rect['dy'])]) \
                                 for rect in squarify.squarify(group_df['normalized_values'], \
                                                               x, y, group_width, group_height)]
        group_dfs.append(group_df)
    
    gdf = gpd.GeoDataFrame(pd.concat(group_dfs), geometry='rectangle')
    
    return geom_polygon(treemap_aes, data=gdf, **kwargs)