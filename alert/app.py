from flask import Flask, request, session, g, redirect, url_for

app = Flask(__name__) # create the application instance :)

@app.route('/')
def hello():
    return "hello"