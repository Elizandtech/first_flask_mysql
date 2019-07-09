from flask import Flask, render_template, request, redirect, flash
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
app = Flask(__name__)
@app.route("/")
def index():
    mysql = connectToMySQL('first_flask')	        # call the function, passing in the name of our db
    friends = mysql.query_db('SELECT * FROM friends;')  # call the query_db function, pass in the query as a string
    print(friends)
    return render_template("index.html", all_friends = friends)

# add validation function
@app.route("/create_friend", methods=["POST"])
def process():
    print(request.form)
    is_valid=True
    if len(request.form['fname'])<=1:
        is_valid=False
        flash("Please enter a first name")
    if len(request.form['lname'])<=1:
        is_valid=False
        flash("Please enter a last name")
    if len(request.form['occ'])<2:
        is_valid=False
        flash("Please enter an occupation, at least 2 characters")
    if not is_valid:
        return redirect('/')
    else:
        print(request.form)
        mysql = connectToMySQL('first_flask')
        query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(occ)s, NOW(), NOW());"
        data = {
            "fn": request.form['fname'],
            "ln": request.form['lname'],
            "occ": request.form['occ']
        }
        new_friend_id = mysql.query_db(query,data)
        flash("Insert friend successful!")
        return redirect('/')

            
if __name__ == "__main__":
    app.run(debug=True)