from flask import Flask, render_template, request, redirect, url_for, session
import pyttsx3

app = Flask(__name__)
app.secret_key = "voicegen_secret"

engine = pyttsx3.init()

USERNAME = "admin"
PASSWORD = "1234"


def speak(text, voice_type, volume, speed):
    engine.setProperty('rate', int(speed))
    engine.setProperty('volume', float(volume))

    voices = engine.getProperty('voices')

    if voice_type == "Male":
        engine.setProperty('voice', voices[0].id)
    elif voice_type == "Female" and len(voices) > 1:
        engine.setProperty('voice', voices[1].id)

    engine.say(text)
    engine.runAndWait()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return "Invalid Credentials ❌"

    return render_template("login.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        text = request.form["text"]
        voice = request.form["voice"]
        volume = request.form["volume"]
        speed = request.form["speed"]

        if text.strip() != "":
            speak(text, voice, volume, speed)

    return render_template("home.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)