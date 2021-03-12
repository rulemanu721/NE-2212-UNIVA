from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return "Flask running"

if __name__=="__main__":
    app.run(port=3000, debug=True)


