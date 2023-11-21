from flask import Flask, render_template, request, redirect, flash

from surveys import satisfaction_survey

app = Flask(__name__)
app.secret_key = "somethingsomethingisuppose"

responses = []

qn = 0


@app.route("/")
def home_page():
    """Route for the home page"""
    global responses, qn
    qn = 0
    responses = []
    return render_template("home.html", survey=satisfaction_survey)


@app.route("/questions")
def question_page():
    """Basic questions page route"""
    if qn == len(satisfaction_survey.questions) and qn == len(responses):
        flash("PLEASE GO HOME")
        return redirect("/thanks")
    else:
        return render_template("questions.html", survey=satisfaction_survey, qn=qn)


@app.route("/questions/<question_number>")
def question_num_page(question_number):
    """Manages the redirect and template for the questions route"""
    # print(responses)
    # print(qn)
    # print(len(responses))
    # print(len(satisfaction_survey.questions))
    if qn == len(satisfaction_survey.questions) and qn == len(responses):
        return redirect("/thanks")
    elif int(question_number) > len(responses) or int(question_number) < len(responses):
        flash("USE THE ABOVE BUTTONS TO ANSWER THE QUESTIONS")
        return redirect("/questions")
    else:
        return redirect("/questions")


@app.route("/response/new", methods=["POST"])
def add_response():
    """Makes a POST request to add a new response to the response list"""
    global qn
    response = request.form["choices"]
    responses.append(response)
    qn += 1
    return redirect(f"/questions/{qn}")


@app.route("/thanks")
def thank_you():
    """Generates the thank you page after the survey and prevents users from skipping to the end"""
    if qn != len(satisfaction_survey.questions):
        flash("INVALID SURVEY. PLEASE DON'T SKIP TO THE END")
        return redirect("/")
    else:
        return render_template(
            "thanks.html", responses=responses, survey=satisfaction_survey
        )
