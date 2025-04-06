#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 19:01:53 2025

@author: sofialourenco
"""

from classes.gclass import Gclass  
from datetime import datetime, date

class Order(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
   
    att = ['_id', '_order_date', '_quantity','_partner_id','_dish_id']
   
    header = 'Order'
   
    des = ['Id', 'Order_Date', 'Quantity', 'Partner_Id','Dish_Id']
   
    def __init__(self, id, order_date, quantity,partner_id,dish_id):
        super().__init__()
        id = Order.get_id(id)
        ano, mes, dia = map(int, order_date.split("-"))
        self._id = id
        self._order_date = date(ano, mes, dia)
        self._quantity = int(quantity)
        self._partner_id = partner_id
        self._dish_id = dish_id 
       
        Order.obj[self.__id] = self
        Order.lst.append(self.__id)
   
    @property
    def id(self):
        return self._id
   
    @id.setter
    def id(self, id):
        self._id = id
   
    @property
    def order_date(self):
        return self._order_date

    @order_date.setter
    def order_date(self, order_date):
        self._order_date = order_date

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        self._quantity = quantity
        
    @property 
    def partner_id (self):
        return self._partner_id
    
    @property 
    def dish_id (self):
        return self._dish_id
