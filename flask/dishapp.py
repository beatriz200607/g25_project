from flask import Flask, render_template, request, session
from classes.dish import Dish
from datafile import filename

app = Flask(__name__)

Dish.read(filename + 'Trabalho.db')
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
        obj = Dish.current()
        Dish.remove(obj.id)
        if not Dish.previous():
            Dish.first()
    elif option == "insert":
        butshow, butedit = "disabled", "enabled"
    elif option == 'cancel':
        pass
    elif prev_option == 'insert' and option == 'save':
        strobj = str(Dish.get_id(0))
        strobj = strobj + ';' + request.form["name"] + ';' + \
        request.form["dob"] + ';' + request.form["salary"]
        obj = Dish.from_string(strobj)
        Dish.insert(obj.id)
        Dish.last()
    elif prev_option == 'edit' and option == 'save':
        obj = Dish.current()
        obj.name = request.form["name"]
        obj.dob = request.form["dob"]
        obj.salary = float(request.form["salary"])
        Dish.update(obj.id)
    elif option == "first":
        Dish.first()
    elif option == "previous":
        Dish.previous()
    elif option == "next":
        Dish.nextrec()
    elif option == "last":
        Dish.last()
    elif option == 'exit':
        return "<h1>Thank you for using this app</h1>"
    prev_option = option
    obj = Dish.current()
    if option == 'insert' or len(Dish.lst) == 0:
        id = 0
        id = Dish.get_id(id)
        name = category = price = ""
    else:
        id = obj.id
        name = obj.name
        category = obj.category
        price = obj.price
    return render_template("index.html", butshow=butshow, butedit=butedit, 
                    id=id,name = name,category=category,price=price, 
                    ulogin=session.get("user"))
        
if __name__ == '__main__':
    app.run()