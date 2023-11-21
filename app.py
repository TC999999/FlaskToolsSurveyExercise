from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    session,
)

from surveys import satisfaction_survey

app = Flask(__name__)
app.secret_key = "somethingsomethingisuppose"

qn = 0


@app.route("/")
def home_page():
    """Route for the home page"""
    global qn
    qn = 0
    return render_template("home.html", survey=satisfaction_survey)


@app.route("/start/survey", methods=["POST"])
def start_survey():
    """generates a new session and resets response session"""
    session["responses"] = []
    return redirect("/questions/0")


@app.route("/questions")
def question_page():
    """Basic questions page route"""
    if qn == len(satisfaction_survey.questions):
        flash("PLEASE GO HOME")
        return redirect("/thanks")
    else:
        return render_template("questions.html", survey=satisfaction_survey, qn=qn)


@app.route("/questions/<question_number>")
def question_num_page(question_number):
    """Manages the redirect and template for the questions route"""
    if qn == len(satisfaction_survey.questions):
        return redirect("/thanks")
    elif int(question_number) > len(session["responses"]) or int(question_number) < len(
        session["responses"]
    ):
        flash("USE THE ABOVE BUTTONS TO ANSWER THE QUESTIONS")
        return redirect("/questions")
    else:
        return redirect("/questions")


@app.route("/response/new", methods=["POST"])
def add_response():
    """Makes a POST request to add a new response to the response list"""
    global qn
    responses = session["responses"]
    response = request.form["choices"]
    responses.append(response)
    session["responses"] = responses
    qn += 1
    return redirect(f"/questions/{qn}")


@app.route("/thanks")
def thank_you():
    """Generates the thank you page after the survey and prevents users from skipping to the end"""
    print(session["responses"])
    if qn != len(satisfaction_survey.questions):
        flash("INVALID SURVEY. PLEASE DON'T SKIP TO THE END")
        return redirect("/")
    else:
        return render_template("thanks.html", survey=satisfaction_survey)
