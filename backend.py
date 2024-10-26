from flask import Flask, request, render_template, redirect, url_for, flash
from dotenv import dotenv_values

context = dotenv_values(".env")

app = Flask(__name__, static_folder="docs", static_url_path="")
app.secret_key = context["flask_secret_key"]


@app.route("/contact", methods=["GET", "POST"])
def submit_form():
    contactFirstName = request.form.get("contact-first-name")
    contactLastName = request.form.get("contact-last-name")
    contactEmail = request.form.get("contact-email")
    contactNumber = request.form.get("contact-number")
    message = request.form.get("message")

    flash("Your message has been sent!", "success")
    return redirect(url_for("contact"))


app.run(debug=True)
