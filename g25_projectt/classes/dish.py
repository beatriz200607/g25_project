#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 19:00:25 2025

@author: sofialourenco
"""

from classes.gclass import Gclass  
import datetime

class Dish(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
   
    att = ['dish_id', '_dish_name', '_category', '_price']
   
    header = 'Dish'
   
    des = ['Dish_Id', 'DishName', 'Category', 'Price']
   
    def __init__(self, dish_id, dish_name, category, price):
        super().__init__()
        dish_id = Dish.get_id(dish_id)
        self._dish_id = dish_id
        self._dish_name = dish_name
        self._categoty = category
        self._price = price
      
        Dish.obj[self._dish_id] = self
        Dish.lst.append(self._dish_id)
   
    @property
    def dish_id(self):
        return self._dish_id
   
    @dish_id.setter
    def dish_id(self,dish_id):
        self._dish_id = dish_id
   
    @property
    def dish_name(self):
        return self._dish_name

    @dish_name.setter
    def dish_name(self, dish_name):
        self._dish_name = dish_name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category
    @property
    def price(self):
        return self._price
    @price.setter
    def price(self, price):
        self._price = price
    
    @property 
    def price (self):
        return self._price