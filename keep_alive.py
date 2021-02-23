from flask import Flask
from threading import Thread
from flask import render_template

app=Flask("")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/quit")
def shutdown():
    quit()
                          

Thread(target=app.run,args=("0.0.0.0",1129)).start()