

from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///market.db"
db=SQLAlchemy(app)
class Product(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=30),nullable=False)
    price=db.Column(db.Integer(),nullable=False)


@app.route("/")
def homePage():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)

#from datetime import datetime
#year = datetime.now().year
#month = datetime.now().month
#day = datetime.now().day
#hour =datetime.now().hour
#minute=datetime.now().minute


#date=str(day)+"/"+str(month)+"/"+str(year)+"-"+str(hour)+":"+str(minute)
#print(date)









