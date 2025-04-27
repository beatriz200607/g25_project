#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 19:04:27 2025

@author: sofialourenco
"""

from classes.gclass import Gclass  
import datetime

class Restaurant(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
   
   
    att = ['_id','_cuisine','_restaurant_name','_location']
   
   
    header = 'Restaurant'
   
   
    des = ['Id','Cuisine','Name','Location']
   
   
    def __init__(self, id, cuisine, restaurant_name, location):
        super().__init__()
        id = Restaurant.get_id(id)
        self._id = id
        self._cuisine = str(cuisine)
        self._restaurant_name = str(restaurant_name)
        self._location = location        
       
        Restaurant.obj[id] = self
       
 
        Restaurant.lst.append(id)
   
   
    @property
    def id(self):
        return self._id
   
    @id.setter
    def restaurant_id(self, id):
        self._id = id
   
    @property
    def cuisine(self):
        return self._cuisine

    @cuisine.setter
    def cuisine (self, cuisine):
        self._cuisine = cuisine


    @property
    def restaurants_name(self):
        return self._restaurants_name


    @restaurants_name.setter
    def restaurants_name(self, restaurants_name):
        self._restaurants_name = restaurants_name


    @property
    def location(self):
        return self._location
 
    @location.setter
    def location(self, location):
        self._location = location