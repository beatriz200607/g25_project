
from classes.gclass import Gclass  
from datetime import datetime, date

class Order(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
   
    att = ['_id', '_order_date', '_quantity', '_partner_id', '_dish_id']
    header = 'Order'
    des = ['Id', 'Order_Date', 'Quantity', 'Partner_Id', 'Dish_Id']
   
    def __init__(self, id, order_date, quantity, partner_id, dish_id):
        super().__init__()
        id = Order.get_id(id)
        self._id = id

        # ✅ Tratamento robusto da data
        if isinstance(order_date, str):
            try:
                self._order_date = datetime.strptime(order_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Formato de data inválido. Use 'YYYY-MM-DD'.")
        elif isinstance(order_date, datetime):
            self._order_date = order_date.date()
        elif isinstance(order_date, date):
            self._order_date = order_date
        else:
            raise ValueError("order_date deve ser uma string 'YYYY-MM-DD', datetime ou date.")

        self._quantity = int(quantity)
        self._partner_id = partner_id
        self._dish_id = dish_id
       
        Order.obj[self._id] = self
        Order.lst.append(self._id)

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
        if isinstance(order_date, str):
            self._order_date = datetime.strptime(order_date, "%Y-%m-%d").date()
        elif isinstance(order_date, datetime):
            self._order_date = order_date.date()
        elif isinstance(order_date, date):
            self._order_date = order_date
        else:
            raise ValueError("order_date deve ser string 'YYYY-MM-DD', datetime ou date.")

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        self._quantity = quantity
        
    @property 
    def partner_id(self):
        return self._partner_id
    
    @property 
    def dish_id(self):
        return self._dish_id
