from flask import Flask, render_template, request
import requests
from post import Post
import smtplib

app = Flask(__name__)

response = requests.get("https://api.npoint.io/7bd401c085e58f4beb62")
response.raise_for_status()
blog_data = response.json()

@app.route("/")
def home_page():
    global blog_data
    return render_template("index.html", post_data=blog_data)

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/contact", methods=["POST", "GET"])
def contact_page():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone_num = request.form["phone"]
        msg = request.form["message"]

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user="udemy.test84@gmail.com", password="abcde().")
            connection.sendmail(from_addr="", to_addrs="",
                                msg="Subject:New Message\n\n "
                                    f"Name:{name}\n"
                                    f"Email:{email}\n"
                                    f"Phone: {phone_num}\n"
                                    f"Message: {msg}")

        return render_template("contact.html", msg=True)



    return render_template("contact.html", msg=False)

@app.route("/post/<int:id>")
def post_page(id):
    global blog_data

    post_data = blog_data[id - 1]

    post = Post(title=post_data["title"], subtitle=post_data["subtitle"], body=post_data["body"])

    return render_template("post_page.html", post=post)







if __name__ == "__main__":

    app.run(debug=True)
