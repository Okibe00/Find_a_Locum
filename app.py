from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.profession import Profession
import uuid


app = Flask(__name__)

app.url_map.strict_slashes = False


@app.teardown_appcontext
def _reload(t):
    '''reload db'''
    storage.close()

@app.route("/form")
def _form():
    '''display job form'''
    return render_template("form.html")

@app.route("/about")
def about():
    '''display the about page'''
    return render_template('about.html')


@app.route("/contact")
def contact():
    '''display the about page'''
    return render_template('contact.html')


@app.route("/state")
def welcome():
    '''
    print a list of states
    '''
    states = storage.all(State)
    return render_template("state.html", states=states)


@app.route("/state/<id>")
def find_state(id):
    '''return the state with passed id'''
    state = storage.search(id, "State")
    if state:
        return render_template("find_state.html", state=state)
    else:
        return "<h2>Not Found</h2>"


@app.route("/home")
def home_page():
    '''display home page'''
    states = storage.all(State)
    prof = storage.all(Profession)
    return render_template(
                "home.html", states=states, profs=prof, uuid=uuid.uuid4
            )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
