#!/usr/bin/env python

from shapely.geometry import Polygon

import numpy as np
import geopandas as gpd

from lets_plot import *

def geom_waffle(waffle_aes, waffle_data, **kwargs):
    def get_cell(x, y):
        cell_width, cell_height = kwargs['cell_shape'] if 'cell_shape' in kwargs else (.9, .9)
        return Polygon([
            ((x + (1 - cell_width) / 2) / chart_width, (y + (1 - cell_height) / 2) / chart_height),
            ((x + (1 - cell_width) / 2) / chart_width, (y + 1 - (1 - cell_height) / 2) / chart_height),
            ((x + 1 - (1 - cell_width) / 2) / chart_width, (y + 1 - (1 - cell_height) / 2) / chart_height),
            ((x + 1 - (1 - cell_width) / 2) / chart_width, (y + (1 - cell_height) / 2) / chart_height),
        ])
    
    chart_width, chart_height = kwargs['chart_shape'] if 'chart_shape' in kwargs else (10, 10)
    grid = np.matrix([[1 for j in range(chart_width)] for i in range(chart_height)])
    if 'grid' in kwargs:
        grid = np.matrix(kwargs['grid'])
        chart_height, chart_width = grid.shape
    N = np.matrix(grid).sum()
    aes_value = waffle_aes.as_dict()['value']
    aes_group = waffle_aes.as_dict()['group']
    waffle_data = waffle_data.sort_values(aes_value, ascending=False).reset_index()
    gdf = gpd.GeoDataFrame({
        'geometry': [get_cell(x, y) for y in range(chart_height - 1, -1, -1) for x in range(chart_width) if grid[chart_height - y - 1, x] == 1],
        aes_group: [elem_type for types_list in [int(round(N * value / waffle_data[aes_value].sum())) * [waffle_data.loc[i, aes_group]] for i, value in waffle_data[aes_value].items()] for elem_type in types_list][:N],
    })

    return geom_polygon(waffle_aes, data=gdf, **kwargs) + coord_fixed(ratio=1)