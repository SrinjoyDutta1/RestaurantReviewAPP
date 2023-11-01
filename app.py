# app.py
from urllib import request
from flask import *
import json
import pymysql
from config import mysql
from flask import flash
import time
app = Flask(__name__)
@app.route("/", methods = ["GET", "POST"]) 
def home():
    return render_template("home.html")

@app.route("/restaurantList", methods = ["GET", "POST"])
def restaurantList():
    zipCode = ""
    if request.method == "POST":
        zipCode = request.form["zipCode"]
        restaurants = find_restaurant(zipCode)
        result = json.loads(restaurants.get_data(as_text=True))
        print(result[1])
    return render_template("restaurantList.html", result = result)
     
@app.route("/addRestaurant", methods = ["GET", "POST"])
def addingRestaurantPage():

    if request.method == "POST":
        
        fullString = request.form["insert restaurant details"]
        array = fullString.split(",")
        restaurants = add_restaurant(array[0], array[1], array[2], array[3], array[4], array[5], array[6])
        
        
    return render_template("addRestaurant.html", result = restaurants)

@app.route("/addReview", methods = ["GET", "POST"])
def addingReviewPage():

    if request.method == "POST":
        
        fullString = request.form["insert review details"]
        array = fullString.split(",")
        restaurants = add_review(array[0], array[1], array[2], array[3])
    return render_template("addRestaurant.html", result = restaurants)

@app.route("/addUser", methods = ["GET", "POST"])
def addUserPage():

    if request.method == "POST":
        
        fullString = request.form["insert user details"]
        array = fullString.split(",")
        restaurants = add_user(array[0], array[1], array[2], array[3], array[4])
    return render_template("addRestaurant.html", result = restaurants)

@app.route("/deleteUser", methods = ["GET", "POST"])
def deleteUserPage():

    if request.method == "POST":
        
        username = request.form["delete user details"]
        response = deleteUser(username)
    return render_template("addRestaurant.html", result = response)

def deleteUser(username) :
    try: 
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user WHERE username =%s", (username,))
        conn.commit()
        cursor.close()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        cursor.close()
        conn.close()
        return "Failed to delete {}".format(username)

def add_user(username, firstname, lastname, email, password):
    try :

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        #user = request.get_json()
        #username = user["username"]
        #firstname = user["firstName"]
        #lastname = user["lastName"]
        #email = user["Email"]
        #password = user["Password"]
        sqlQuery = "insert into user values (%s,%s,%s,%s,%s);"
        bindData = (username, firstname, lastname, email, password)
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        return "was able to add user"
    except Exception as e:
        print(e)
        return "wasn't able to add user"
    finally:
        cursor.close()
        conn.close()

def add_review(username, restaurantId, rating, textReview):
    try :

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        #review = request.get_json()
        #    reviewId = review["reviewId"]
        #    username = review["username"]
        #    restaurantId = review["restaurantId"]
        #    rating = review["rating"]
        #    textReview = review["textReview"]
        #    dateTime = review["dateTime"]
        sqlQuery = "insert into review (username, restaurantId, rating, textReview) values (%s,%s,%s,%s);"
        bindData = (username, restaurantId, rating, textReview)
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        response = "Successfully added review"
        return response
    except Exception as e:
        print(e)
        return "Failed to add Review"
    finally:
        cursor.close()
        conn.close()


def add_restaurant(name, address, zip, email, phone, website, cuisine):
    try :
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
            #print("step2")
            #restaurant = request.get_json()
            #name = restaurant["restaurantName"]
            #address = restaurant["streetAddress"]
            #zip = restaurant["zipCode"]
            #email = restaurant["Email"]
            #phone = restaurant["phoneNumber"]
            #website = restaurant["website"]
            #cuisine = restaurant["cuisineType"]
        sqlQuery = "insert into restaurant values (0 ,%s,%s,%s,%s,%s,%s,%s);"
        bindData = (name, address, zip, email, phone, website, cuisine)
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        response = "The restaurant has been successfully added"
        return response
        

    except Exception as e:
        return "The restaurant was not able to be added"
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
     app.run()


@app.route("/restaurants/<string:id>")
def get_restaurant(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT restaurantId, restaurantName, streetAddress, zipCode, Email,phoneNumber, website, cuisineType FROM Restaurant WHERE restaurantId =%s", id)
        restRow = cursor.fetchone()
        respone = restRow 
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

#@app.route("/restaurants", methods = ['GET'])
def find_restaurant(zipCode):
    try:
        #zipCode = request.args.get("zipCode")
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT restaurantId, restaurantName, streetAddress, zipCode, Email,phoneNumber, website, cuisineType FROM Restaurant WHERE zipCode =%s", zipCode)
        restRow = cursor.fetchall()
        respone = jsonify(restRow)
        #respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()





@app.route('/restaurants/<string:id>', methods = ['DELETE'])
def delete_Restaurant(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM restaurant WHERE restaurantid =%s", (id,))
		conn.commit()
		respone = jsonify('Success')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
          
@app.route("/restaurants/<string:id>", methods = ['PUT'])
def updateRestaurant(id):
    try :
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        print("step1")
        if request.is_json:
            print("step2")
            restaurant = request.get_json()
            name = restaurant["restaurantName"]
            address = restaurant["streetAddress"]
            zip = restaurant["zipCode"]
            email = restaurant["Email"]
            phone = restaurant["phoneNumber"]
            website = restaurant["website"]
            cuisine = restaurant["cuisineType"]
            sqlQuery = "update restaurant set restaurantName = %s, streetAddress = %s, zipCode = %s, Email = %s, phoneNumber = %s, website = %s, cuisineType = %s where restaurantId = %s;"
            bindData = (name, address, zip, email, phone, website, cuisine, id)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify("Success")
            response.status_code = 200

            return response
        else:
            print("step3")
            response = jsonify("Invalid Request")
            print(response)
            response.status_code = 400
            return response


    except Exception as e:
        print(e)
        print("step4")
    finally:
        print("step5")
        cursor.close()
        conn.close()


@app.route("/user/<string:username>")
def get_user(username):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT username, firstName, lastName, Email, Password FROM User WHERE username = %s", username)
        restRow = cursor.fetchone()
        respone = jsonify(restRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 


          

@app.route("/user/update/<string:username>", methods = ['PUT'])
def updateUser(username):
    try :
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.is_json:
            user = request.get_json()
            fname = user["firstName"]
            lname = user["lastName"]
            email = user["email"]
            pw = user["password"]
            sqlQuery = "update user set firstName = %s, lastName = %s, Email = %s, Password = %s where username = %s;"
            bindData = (fname, lname, email, pw, username)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify("Success")
            response.status_code = 200
            print("HI")
            return response
        else:
            response = jsonify("Invalid Request")
            response.status_code = 400
            return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()








@app.route("/review/<string:id>")
def get_Review(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT reviewId, username, restaurantId, rating, textReview, dateTime FROM review WHERE reviewId = %s", id)
        restRow = cursor.fetchone()
        respone = jsonify(restRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 


@app.route('/review/<string:id>', methods = ['DELETE'])
def deleteReview(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM review WHERE reviewId =%s", (id,))
		conn.commit()
		respone = jsonify('Success')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
          

@app.route("/review/update/<string:reviewId>", methods = ['PUT'])
def updateReview(reviewId):
    try :
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.is_json:
            review = request.get_json()
            rating = review["rating"]
            textReview = review["textReview"]
            dateTime = review["dateTime"]
            sqlQuery = "update review set rating = %s, textReview = %s, dateTime = %s where reviewId = %s;"
            bindData = (rating, textReview, dateTime, reviewId)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify("Success")
            response.status_code = 200
            print("HI")
            return response
        else:
            response = jsonify("Invalid Request")
            response.status_code = 400
            return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

