from flask import Flask, render_template, request, session
from classes.order import Order
from datafile import filename

app = Flask(__name__)

Order.read(filename + 'Trabalho.db')
prev_option = ""
app.secret_key = 'BAD_SECRET_KEY'

@app.route("/", methods=["GET", "POST"])
def index():
    global prev_option
    butshow, butedit = "enabled", "disabled"
    option = request.args.get("option")

    if option == "edit":
        butshow, butedit = "disabled", "enabled"
    elif option == "delete":
        obj = Order.current()
        Order.remove(obj._id)
        if not Order.previous():
            Order.first()
    elif option == "insert":
        butshow, butedit = "disabled", "enabled"
    elif option == "cancel":
        pass
    elif prev_option == "insert" and option == "save":
        strobj = str(Order.get_id(0))
        strobj += ";" + request.form["order_date"] + ";" + \
                  request.form["quantity"] + ";" + \
                  request.form["partner_id"] + ";" + \
                  request.form["dish_id"]
        obj = Order.from_string(strobj)
        Order.insert(obj._id)
        Order.last()
    elif prev_option == "edit" and option == "save":
        obj = Order.current()
        obj._order_date = request.form["order_date"]
        obj._quantity = int(request.form["quantity"])
        obj._partner_id = request.form["partner_id"]
        obj._dish_id = request.form["dish_id"]
        Order.update(obj._id)
    elif option == "first":
        Order.first()
    elif option == "previous":
        Order.previous()
    elif option == "next":
        Order.nextrec()
    elif option == "last":
        Order.last()
    elif option == "exit":
        return "<h1>Thank you for using this app</h1>"

    prev_option = option
    obj = Order.current()

    if option == "insert" or len(Order.lst) == 0:
        id = 0
        id = Order.get_id(id)
        order_date = ""
        quantity = ""
        partner_id = ""
        dish_id = ""
    else:
        id = obj._id
        order_date = obj._order_date.strftime("%Y-%m-%d")  # Formatar para input date
        quantity = obj._quantity
        partner_id = obj._partner_id
        dish_id = obj._dish_id

    return render_template("order.html",
                           butshow=butshow,
                           butedit=butedit,
                           id=id,
                           order_date=order_date,
                           quantity=quantity,
                           partner_id=partner_id,
                           dish_id=dish_id,
                           ulogin=session.get("user"))

if __name__ == '__main__':
    app.run()
