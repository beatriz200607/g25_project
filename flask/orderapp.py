from flask import Flask, render_template, request, session
from classes.order import Order
from datafile import filename

app = Flask(__name__)

Order.read(filename + 'Trabalho.db')
prev_option = ""
app.secret_key = 'BAD_SECRET_KEY'

@app.route("/", methods=["post","get"])
def index():
    global prev_option
    butshow, butedit = "enabled", "disabled"
    option = request.args.get("option")
    if option == "edit":
        butshow, butedit = "disabled", "enabled"
    elif option == "delete":
        obj = Order.current()
        Order.remove(obj.id)
        if not Order.previous():
            Order.first()
    elif option == "insert":
        butshow, butedit = "disabled", "enabled"
    elif option == 'cancel':
        pass
    elif prev_option == 'insert' and option == 'save':
        strobj = str(Order.get_id(0))
        strobj = strobj + ';' + request.form["name"] + ';' + \
        request.form["dob"] + ';' + request.form["salary"]
        obj = Order.from_string(strobj)
        Order.insert(obj.id)
        Order.last()
    elif prev_option == 'edit' and option == 'save':
        obj = Order.current()
        obj.name = request.form["name"]
        obj.dob = request.form["dob"]
        obj.salary = float(request.form["salary"])
        Order.update(obj.id)
    elif option == "first":
        Order.first()
    elif option == "previous":
        Order.previous()
    elif option == "next":
        Order.nextrec()
    elif option == "last":
        Order.last()
    elif option == 'exit':
        return "<h1>Thank you for using this app</h1>"
    prev_option = option
    obj = Order.current()
    if option == 'insert' or len(Order.lst) == 0:
        id = 0
        id = Order.get_id(id)
        order_date = quantity = ""
    else:
        id = obj.id
        order_date = obj.order_date
        quantity = obj.quantity
       
    return render_template("index.html", butshow=butshow, butedit=butedit, 
                    id=id,order_date = order_date,quantityh=quantity, 
                    ulogin=session.get("user"))
        
if __name__ == '__main__':
    app.run()

