from flask import Flask, render_template, request, session
from classes.restaurant import Restaurant
from datafile import filename

app = Flask(__name__)

Restaurant.read(filename + 'Trabalho.db')
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
        obj = Restaurant.current()
        Restaurant.remove(obj.id)
        if not Restaurant.previous():
            Restaurant.first()
    elif option == "insert":
        butshow, butedit = "disabled", "enabled"
    elif option == 'cancel':
        pass
    elif prev_option == 'insert' and option == 'save':
        strobj = str(Restaurant.get_id(0))
        strobj = strobj + ';' + request.form["name"] + ';' + \
        request.form["dob"] + ';' + request.form["salary"]
        obj = Restaurant.from_string(strobj)
        Restaurant.insert(obj.id)
        Restaurant.last()
    elif prev_option == 'edit' and option == 'save':
        obj = Restaurant.current()
        obj.name = request.form["name"]
        obj.dob = request.form["dob"]
        obj.salary = float(request.form["salary"])
        Restaurant.update(obj.id)
    elif option == "first":
        Restaurant.first()
    elif option == "previous":
        Restaurant.previous()
    elif option == "next":
        Restaurant.nextrec()
    elif option == "last":
        Restaurant.last()
    elif option == 'exit':
        return "<h1>Thank you for using this app</h1>"
    prev_option = option
    obj = Restaurant.current()
    if option == 'insert' or len(Restaurant.lst) == 0:
        id = 0
        id = Restaurant.get_id(id)
        cuisine = restaurant_name = location = ""
    else:
        id = obj.id
        cuisine = obj.cuisine
        restaurant_name = obj.restaurant_name
        location = obj.location
    return render_template("index.html", butshow=butshow, butedit=butedit, 
                    id=id,cuisine = cuisine,restaurant_name=restaurant_name,location=location, 
                    ulogin=session.get("user"))
        
if __name__ == '__main__':
    app.run()