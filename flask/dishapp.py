from flask import Flask, render_template, request, session
from classes.dish import Dish
from datafile import filename

app = Flask(__name__)

Dish.read(filename + 'Trabalho.db')
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
        obj = Dish.current()
        Dish.remove(obj.dish_id)
        if not Dish.previous():
            Dish.first()

    elif option == "insert":
        butshow, butedit = "disabled", "enabled"

    elif option == "cancel":
        pass

    elif prev_option == "insert" and option == "save":
        strobj = str(Dish.get_id(0))
        strobj += ";" + request.form["dish_name"] + ";" + request.form["category"] + ";" + request.form["price"]
        obj = Dish.from_string(strobj)
        Dish.insert(obj.dish_id)
        Dish.last()

    elif prev_option == "edit" and option == "save":
        obj = Dish.current()
        obj._dish_name = request.form["dish_name"]
        obj._category = request.form["category"]
        obj._price = float(request.form["price"])
        Dish.update(obj.dish_id)

    elif option == "first":
        Dish.first()
    elif option == "previous":
        Dish.previous()
    elif option == "next":
        Dish.nextrec()
    elif option == "last":
        Dish.last()
    elif option == "exit":
        return "<h1>Thank you for using this app</h1>"

    prev_option = option
    obj = Dish.current()

    if option == "insert" or len(Dish.lst) == 0:
        id = 0
        id = Dish.get_id(id)
        dish_name = ""
        category = ""
        price = ""
    else:
        id = obj._dish_id
        dish_name = obj._dish_name
        category = obj._category
        price = obj._price

    return render_template("dish.html", 
                           butshow=butshow, 
                           butedit=butedit,
                           id=id,
                           dish_name=dish_name,
                           category=category,
                           price=price,
                           ulogin=session.get("user"))

if __name__ == '__main__':
    app.run()
