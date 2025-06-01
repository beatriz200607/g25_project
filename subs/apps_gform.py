from flask import render_template, request, session
from classes.order import Order
from classes.dish import Dish
from classes.deliverypartner import DeliveryPartner
from classes.restaurant import Restaurant
from classes.userlogin import Userlogin

from datetime import date

prev_option = ""

def default_args(cl):
    if cl.__name__ == 'Dish':
        return [0, '', '', 0.0]
    elif cl.__name__ == 'Order':
        return [0, date.today(), 0, 0, 0]
    elif cl.__name__ == 'DeliveryPartner':
        return [0, '', 0.0]
    elif cl.__name__ == 'Restaurant':
        return [0, '', '', '']
    elif cl.__name__ == 'Userlogin':
        return [0, '', '', '']
    else:
        return ['' for _ in cl.att]

def apps_gform(cname=''):
    global prev_option
    ulogin = session.get("user")

    if ulogin is None:
        return render_template("index.html", ulogin=ulogin)

    cl = eval(cname)
    butshow = "enabled"
    butedit = "disabled"
    option = request.form.get("option") or request.args.get("option")

    if prev_option == 'edit' and option == 'save':
        obj = cl.current()
        if obj is not None:
            for i in range(1, len(cl.att)):
                setattr(obj, cl.att[i], request.form.get(cl.att[i], ''))
            cl.update(getattr(obj, cl.att[0]))
        else:
            return f"Erro: Nenhum objeto atual encontrado para a classe '{cname}'"

    else:
        if option == "edit":
            butshow = "disabled"
            butedit = "enabled"

        elif option == "delete":
            obj = cl.current()
            if obj is not None:
                cl.remove(obj.id)
            if not cl.previous():
                cl.first()

        elif option == "first":
            cl.first()

        elif option == "previous":
            cl.previous()

        elif option == "next":
            cl.nextrec()

        elif option == "last":
            cl.last()

        elif option == "exit":
            return render_template("index.html", ulogin=ulogin)

    prev_option = option

    obj = cl.current()
    if obj is None or len(cl.lst) == 0:
        obj = cl(*default_args(cl))  # cria objeto com valores default

    return render_template("gform.html",
                           butshow=butshow,
                           butedit=butedit,
                           cname=cname,
                           obj=obj,
                           att=cl.att,
                           des=cl.des,
                           ulogin=ulogin)
