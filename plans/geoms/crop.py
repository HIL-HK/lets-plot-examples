#!/usr/bin/env python

import requests
from io import BytesIO
from PIL import Image, ImageDraw
import shapely
import numpy as np

from lets_plot import geom_image

def get_geom_mask(geom, width, height):
    polygon = list(geom.exterior.coords)
    im_mask = Image.new('1', (width, height), 0)
    ImageDraw.Draw(im_mask).polygon(polygon, outline=1, fill=1)
    return im_mask

def get_geom_image(geom, image):
    origin = (int(geom.bounds[0]), int(geom.bounds[1]))
    total_width, total_height = int(geom.bounds[2]), int(geom.bounds[3])
    width, height = total_width - origin[0], total_height - origin[1]
    geom = shapely.affinity.scale(geom, 1, -1)
    geom = shapely.affinity.translate(geom, xoff=-origin[0], yoff=-origin[1])
    image_rgba = image.resize((width, height))
    if (geom.type == 'Polygon'):
        im_mask = get_geom_mask(geom, width, height)
    elif (geom.type == 'MultiPolygon'):
        mask_arrays = [np.asarray(get_geom_mask(subgeom, width, height)) for subgeom in geom]
        im_mask = Image.fromarray(np.logical_xor.reduce(mask_arrays))
    else:
        im_mask = Image.new('1', (width, height), 0)
    image_rgba.putalpha(im_mask)
    image_rgba = image_rgba.transform((total_width, total_height), \
                                      method=Image.EXTENT, \
                                      data=(-int(origin[0]), 0, image_rgba.width, total_height))
    return image_rgba

def get_stub_image(geometry):
    return geom_image(image_data=np.array([[[0, 0, 0, 0]]]))

def get_geom_crop(geometry, image_url):
    if image_url:
        try:
            image_rgba = get_geom_image(geometry, Image.open(BytesIO(requests.get(image_url).content)))
            return geom_image(image_data=np.asarray(image_rgba))
        except:
            return get_stub_image(geometry)
    else:
        return get_stub_image(geometry)

def geom_crop(crop_aes, crop_data, **kwargs):
    aes_geometry = crop_aes.as_dict()['geometry']
    aes_image_url = crop_aes.as_dict()['url']
    result = get_geom_crop(crop_data.iloc[0][aes_geometry], crop_data.iloc[0][aes_image_url])
    for i in range(1, crop_data.shape[0]):
        result += get_geom_crop(crop_data.iloc[i][aes_geometry], crop_data.iloc[i][aes_image_url])
    return result