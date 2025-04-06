#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 18:59:51 2025

@author: sofialourenco
"""

from classes.gclass import Gclass  

class DeliveryPartner(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
   
   
    att = ['_id','_partner_name','_rating']
   
   
    header = 'Delivery Partner'
   
   
    des = ['Id','PartnerName','Rating']
   
   
    def __init__(self, id, partner_name, rating):
        super().__init__()
        id = DeliveryPartner.get_id(id)
        self._id = int(id)
        self._partner_name = str(partner_name)
        self._rating = float(rating)

       
        DeliveryPartner.obj[id] = self
       
 
        DeliveryPartner.lst.append(id)
   
   
    @property
    def id(self):
        return self._id
   
    @id.setter
    def id(self, id):
        self.id = id
   
    @property
    def partner_name(self):
        return self._partner_name

    @partner_name.setter
    def partner_name (self, partner_name):
        self._partner_name = partner_name


    @property
    def rating(self):
        return self._rating


    @rating.setter
    def rating(self, rating):
        self._rating = rating
        
        