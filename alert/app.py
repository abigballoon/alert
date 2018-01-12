from flask import Flask, request, session, g, redirect, url_for

app = Flask(__name__) # create the application instance :)

@app.route('/')
def hello():
    # return "name"
    return ','.join(
        [
            request.user.username,
            request.user.email,
            request.user.name,
        ]
    )
