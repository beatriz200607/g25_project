from flask import Flask, render_template, request, session
from classes.restaurant import Restaurant
from datafile import filename

app = Flask(__name__)

Restaurant.read(filename + 'Trabalho.db')
prev_option = ""  # Make sure this is initialized
app.secret_key = 'BAD_SECRET_KEY'

@app.route("/", methods=["POST", "GET"])
def index():
    global prev_option
    butshow, butedit = "enabled", "disabled"
    
    # Retrieve the action (edit, delete, etc.)
    option = request.args.get("option")
    
    # Action handling based on option
    if option == "edit":
        butshow, butedit = "disabled", "enabled"
    elif option == "delete":
        obj = Restaurant.current()
        Restaurant.remove(obj.id)
        if not Restaurant.previous():
            Restaurant.first()  # Set to first if no previous exists
    elif option == "insert":
        butshow, butedit = "disabled", "enabled"
    elif option == 'cancel':
        pass
    elif prev_option == 'insert' and option == 'save':
        # Create a new restaurant object
        strobj = str(Restaurant.get_id(0)) + ';' + request.form["name"] + ';' + \
                 request.form["dob"] + ';' + request.form["salary"]
        obj = Restaurant.from_string(strobj)
        Restaurant.insert(obj.id)
        Restaurant.last()
    elif prev_option == 'edit' and option == 'save':
        # Update existing restaurant object
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
    
    # Set the previous option for next iteration
    prev_option = option
    
    # Fetch the current restaurant object to display
    obj = Restaurant.current()
    
    # Default values for insert option or empty list
    if option == 'insert' or len(Restaurant.lst) == 0:
        id = 0
        id = Restaurant.get_id(id)  # Assuming get_id is defined to generate ids
        cuisine = restaurant_name = location = ""
    else:
        id = obj.id
        cuisine = obj.cuisine
        restaurant_name = obj.restaurant_name
        location = obj.location
    
    # Render the template and pass the values
    return render_template("index.html", 
                           butshow=butshow, 
                           butedit=butedit, 
                           id=id,
                           cuisine=cuisine,
                           restaurant_name=restaurant_name,
                           location=location, 
                           ulogin=session.get("user"))  # Ensure 'user' is in the session

if __name__ == '__main__':
    app.run()
