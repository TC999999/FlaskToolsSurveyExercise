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


@app.route("/")
def home_page():
    """Route for the home page"""
    return render_template("home.html", survey=satisfaction_survey)


@app.route("/start/survey", methods=["POST"])
def start_survey():
    """generates a new session and resets response session"""
    session["responses"] = []
    session["question_num"] = 0
    return redirect("/questions/0")


@app.route("/questions")
def question_page():
    """Basic questions page route"""
    if session["question_num"] == len(satisfaction_survey.questions):
        flash("PLEASE GO HOME")
        return redirect("/thanks")
    else:
        return render_template("questions.html", survey=satisfaction_survey)


@app.route("/questions/<question_number>")
def question_num_page(question_number):
    """Manages the redirect and template for the questions route"""
    if session["question_num"] == len(satisfaction_survey.questions):
        return redirect("/thanks")
    elif int(question_number) > len(session["responses"]) or int(question_number) < len(
        session["responses"]
    ):
        flash("USE THE ABOVE BUTTONS TO ANSWER THE QUESTIONS.")
        return redirect("/questions")
    else:
        return redirect("/questions")


@app.route("/response/new", methods=["POST"])
def add_response():
    """Makes a POST request to add a new response to the response list"""
    responses = session["responses"]
    response = request.form["choices"]
    responses.append(response)
    session["responses"] = responses

    question_num = session["question_num"]
    question_num += 1
    session["question_num"] = question_num
    return redirect(f"/questions/{session['question_num']}")


@app.route("/thanks")
def thank_you():
    """Generates the thank you page after the survey and prevents users from skipping to the end"""
    if session["question_num"] != len(satisfaction_survey.questions):
        flash(
            "INVALID SURVEY! PLEASE DON'T SKIP TO THE END BEFORE ANSWERING THE QUESTIONS."
        )
        return redirect("/")
    else:
        return render_template("thanks.html", survey=satisfaction_survey)
