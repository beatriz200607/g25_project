from flask import Flask, render_template, request, session
from classes.deliverypartner import DeliveryPartner
from datafile import filename

app = Flask(__name__)

DeliveryPartner.read(filename + 'Trabalho.db')
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
        obj = DeliveryPartner.current()
        DeliveryPartner.remove(obj.id)
        if not DeliveryPartner.previous():
            DeliveryPartner.first()

    elif option == "insert":
        butshow, butedit = "disabled", "enabled"

    elif option == "cancel":
        pass

    elif prev_option == "insert" and option == "save":
        strobj = str(DeliveryPartner.get_id(0))
        strobj += ";" + request.form["partner_name"] + ";" + request.form["rating"]
        obj = DeliveryPartner.from_string(strobj)
        DeliveryPartner.insert(obj.id)
        DeliveryPartner.last()

    elif prev_option == "edit" and option == "save":
        obj = DeliveryPartner.current()
        obj._partner_name = request.form["partner_name"]
        obj._rating = float(request.form["rating"])
        DeliveryPartner.update(obj.id)

    elif option == "first":
        DeliveryPartner.first()
    elif option == "previous":
        DeliveryPartner.previous()
    elif option == "next":
        DeliveryPartner.nextrec()
    elif option == "last":
        DeliveryPartner.last()
    elif option == "exit":
        return "<h1>Thank you for using this app</h1>"

    prev_option = option
    obj = DeliveryPartner.current()

    if option == "insert" or len(DeliveryPartner.lst) == 0:
        id = 0
        id = DeliveryPartner.get_id(id)
        partner_name = ""
        rating = ""
    else:
        id = obj._id
        partner_name = obj._partner_name
        rating = obj._rating

    return render_template("deliverypartner.html", 
                           butshow=butshow, 
                           butedit=butedit,
                           id=id,
                           partner_name=partner_name,
                           rating=rating,
                           ulogin=session.get("user"))

if __name__ == '__main__':
    app.run()
