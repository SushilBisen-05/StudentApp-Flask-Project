from flask import Flask
app=Flask(__name__)

@app.route("/")
def home():
    return "<h1> Welcome to Flask <h1>"

@app.route("/index")
def index():
    return "<h1> Welcome to Flask in Maharashtra <h1>"

@app.route("/song")
def song():
    return "<h1> Welcome to Flask in Nagpur <h1>"

if __name__ == '__main__':
    app.run(debug=True)

