from flask import (
    Flask,
    session,
    redirect,
    url_for,
    request,
    render_template,
    jsonify,
    make_response,
)
from markupsafe import escape
import datetime
import pymysql
import pymysql.cursors
import json
from DBUtils.PersistentDB import PersistentDB

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
# Don't worry, we'll change this before we go to production
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def connect_db():
    return PersistentDB(
        creator=pymysql,
        host="hotel-site.coakcauk3jpi.us-east-1.rds.amazonaws.com",
        user="admin",
        password="sateesh_mane_its_insane",
        autocommit = True,
        db="hotelsite",
        cursorclass=pymysql.cursors.DictCursor,
    )


def get_db():
    if not hasattr(app, "db"):
        app.db = connect_db()
    return app.db.connection()


cursor = get_db().cursor()
sql = "SELECT * FROM accounts"
cursor.execute(sql)
data = cursor.fetchone()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["curr_date"] = request.form["set_date"]
        return redirect(url_for("index"))
    if "username" in session and "curr_date" in session:
        # we need to do a check to see if this user is a hotel manager or a customer.
        cursor0 = get_db().cursor()
        sql0 = "select userid, usertype from accounts where login = %s"
        cursor0.execute(sql0, session["username"])
        rows0 = cursor0.fetchone()
        session["usertype"] = rows0["usertype"]
        session["userid"] = rows0["userid"]
        if rows0["usertype"] == "customer":
            cursor = get_db().cursor()
            sql = "select gfirst,glast,hname,roomnum,bookid,date_format(checkin,'%%m-%%d-%%Y'),date_format(checkout,'%%m-%%d-%%Y'),address from accounts,hotel,booking,room where login= %s and accounts.userid=booking.userid and booking.roomid=room.roomid and room.hotelid=hotel.hotelid and checkout > %s"
            cursor.execute(sql, (session["username"], session["curr_date"]))
            rows = cursor.fetchall()
            return render_template(
                "index.j2",
                username=session["username"],
                curr_date=session["curr_date"],
                reservations=rows,
            )
        if rows0["usertype"] == "host":
            cursor0 = get_db().cursor()
            sql0 = "select chainid from hchain where cuserid=%s"
            cursor0.execute(sql0,(session["userid"]))
            rows0 = cursor0.fetchall()
            session["chainid"] = rows0[0]["chainid"]
            cursor = get_db().cursor()
            sql = "select hchain.chainid,bookid,userid,booking.roomid,date_format(checkin,'%%m-%%d-%%Y'),date_format(checkout,'%%m-%%d-%%Y'),hname from booking,room,hotel,hchain where booking.roomid = room.roomid and room.hotelid = hotel.hotelid and hotel.chainid = hchain.chainid and hchain.cuserid = %s and checkout > %s"
            cursor.execute(sql, (session["userid"], session["curr_date"]))
            rows = cursor.fetchall()
            return render_template(
                "index.j2",
                username=session["username"],
                curr_date=session["curr_date"],
                reservations=rows,
            )
    if "curr_date" in session:
        return render_template("index.j2", curr_date=session["curr_date"])
    return """
        <form method="post">
            <input type="date" id="start" name="set_date" min="2015-01-01" max="2100-12-31" value="2020-06-06">
            <p><input type=submit value=set_date>
        </form>
    """


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username and password:
            cursor = get_db().cursor()
            sql = "SELECT * FROM accounts WHERE login = %s AND pass = %s"
            cursor.execute(sql, (username, password))
            if cursor.fetchone():
                session["username"] = username
                print(username + " has logged in")
                return redirect(url_for("index"))
            else:
                return "Incorrect Username and/or Password!"
        else:
            return "Please enter Username and Password!"
    if "username" in session:
        return redirect(url_for("index"))
    return render_template("login.j2")


@app.route("/logout")
def logout():
    # remove the curr_date from the session if it's there
    if "username" in session:
        print(session["username"] + " has logged out")
        session.pop("username", None)
    session.pop("curr_date", None)
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        gfirst = request.form["firstname"]
        glast = request.form["lastname"]
        if username and password:
            cursor = get_db().cursor()
            sql = "SELECT login FROM accounts WHERE login = %s"
            cursor.execute(sql, (username))
            if cursor.fetchone():
                return "A user has already chosen that username, please try again"
            else:
                cursor2 = get_db().cursor()
                sql2 = "INSERT INTO accounts (gfirst,glast,login, pass, usertype) VALUES (%s,%s,%s,%s,'customer')"
                cursor2.execute(sql2, (gfirst, glast, username, password))
                get_db().commit()
                return redirect(url_for("index"))
        else:
            return "Please enter Username and Password!"
    return render_template("register.j2")


@app.route("/map")
def mapp():  # Two p so we don't overwrite python map function
    if "curr_date" not in session:
        return redirect(url_for("index"))
    cursor = get_db().cursor()
    sql = "SELECT hname,ycoord,xcoord FROM hotel"
    cursor.execute(sql)
    rows = cursor.fetchall()
    if "username" in session:
        return render_template(
            "map.j2", hotel_locations=rows, username=session["username"]
        )
    else:
        return render_template("map.j2", hotel_locations=rows)


@app.route("/hotel/<hotelid>")
def hotel_page(hotelid):
    if "curr_date" not in session:
        return redirect(url_for("index"))
    cursor = get_db().cursor()
    sql = "SELECT hname, phone, address, xcoord, ycoord from hotel where hotelid = %s"
    cursor.execute(sql, (hotelid))
    rows = cursor.fetchall()
    if rows:
        cursor2 = get_db().cursor()
        # currently available rooms.
        #sql2 = "SELECT distinct room.roomid,format(price,2),roomnum,rType,capacity from room,booking where hotelid = %s and room.roomid not in (select roomid from booking where checkin <= %s AND checkout >= %s)"
        # list all rooms
        sql2 = "SELECT room.roomid,format(price,2),roomnum,rType,capacity from room,hotel where hotel.hotelid= %s and room.hotelid = hotel.hotelid"
        cursor2.execute(sql2, (hotelid))
        rows2 = cursor2.fetchall()
        return render_template("hotel.j2", hotelinfo=rows, availrooms=rows2)
    else:
        return "Error 404: This hotel does not exist"


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        cursor = get_db().cursor()
        # TODO: FIX THIS SEARCH!
        # sql = "SELECT count(*),hotel.hotelid,hname from room,hotel where room.roomid not in (select roomid from booking WHERE (checkin <= %s AND checkout >= %s ) OR (checkin < %s AND checkout >= %s) OR ( %s <= checkin AND %s >= checkin)) and ( hname like %s or address like %s ) and hotel.hotelid = room.hotelid and room.capacity >= %s AND price >= %s AND price <= %s group by hotel.hotelid"
        sql = "select count(*),hotel.hotelid,hname,format(min(price),2) from hotel,room where roomid not in (select roomid from booking where (checkin<= %s AND checkout >= %s) OR (checkin < %s AND checkout >= %s) OR (%s <= checkin AND %s >= checkin)) and (hname like %s or address like %s) AND room.hotelid=hotel.hotelid and room.capacity >= %s AND price >= %s AND price <= %s group by hotelid;"
        cursor.execute(
            sql,
            (
                request.form["checkin"],
                request.form["checkin"],
                request.form["checkout"],
                request.form["checkout"],
                request.form["checkin"],
                request.form["checkout"],
                "%" + request.form["keywords"] + "%",
                "%" + request.form["keywords"] + "%",
                request.form["roomtype"],
                request.form["min_price"],
                request.form["max_price"],
            ),
        )
        rows = cursor.fetchall()
        return render_template("search.j2", availrooms=rows)

    if "curr_date" not in session:
        return redirect(url_for("index"))
    return render_template("search.j2")


@app.route("/makebooking/<roomid>", methods=["GET", "POST"])
def makebooking(roomid):
    if request.method == "POST":
        # sanity check
        cursor = get_db().cursor()
        # checkin checkin checkout checkout checkin checkout
        # https://stackoverflow.com/questions/29213183/sql-query-to-search-for-room-availability
        sql = "SELECT bookid from booking WHERE ((checkin <= %s AND checkout >= %s ) OR (checkin < %s AND checkout >= %s) OR ( %s <= checkin AND %s >= checkin)) AND roomid=%s"
        cursor.execute(
            sql,
            (
                request.form["checkin"],
                request.form["checkin"],
                request.form["checkout"],
                request.form["checkout"],
                request.form["checkin"],
                request.form["checkout"],
                roomid,
            ),
        )
        rows = cursor.fetchall()
        if datetime.datetime.strptime(
            request.form["checkin"], "%Y-%m-%d"
        ) > datetime.datetime.strptime(request.form["checkout"], "%Y-%m-%d"):
            return "Invalid dates! try again!"
        if rows:
            return "Sorry, this room is booked on the days which you have specified. Please try again!"
        else:
            cursor1 = get_db().cursor()
            sql1 = "INSERT INTO booking (userid,roomid,checkin,checkout) values (%s,%s,%s,%s)"
            cursor1.execute(
                sql1,
                (
                    session["userid"],
                    roomid,
                    request.form["checkin"],
                    request.form["checkout"],
                ),
            )
            get_db().commit()
            return redirect(url_for("index"))
    else:
        if "curr_date" not in session:
            return redirect(url_for("index"))
        if "username" not in session:
            return redirect(url_for("login"))
        cursor = get_db().cursor()
        sql = "SELECT roomid from room where roomid = %s"
        cursor.execute(sql, (roomid))
        rows = cursor.fetchone()
        if rows:
            return render_template("makebooking.j2")
        else:
            return "This roomid is invalid. Please try again!"


@app.route("/cancelbooking/<bookingid>", methods=["GET", "POST"])
def cancelbooking(bookingid):
    if request.method == "POST":
        cursor = get_db().cursor()
        sql = "DELETE FROM booking WHERE bookid=%s and userid = %s"
        cursor.execute(sql, (bookingid,session['userid']))
        get_db().commit()
        return redirect(url_for("index"))
    else:
        if "curr_date" not in session:
            return redirect(url_for("index"))
        cursor = get_db().cursor()
        sql = "SELECT bookid from booking where bookid = %s and userid = %s"
        cursor.execute(sql, (bookingid,session['userid']))
        rows = cursor.fetchone()
        if rows:
            return render_template("cancelbooking.j2")
        else:
            return "This bookingid is invalid. Please try again!"


@app.route("/makehotel", methods=["POST"])
def makehotel():
    cursor = get_db().cursor()
    sql = "SELECT xcoord, ycoord from hotel where xcoord = %s and ycoord = %s"
    cursor.execute(sql, (request.form["xcoord"], request.form["ycoord"]))
    if not cursor.fetchone():
        cursor2 = get_db().cursor()
        sql2 = "INSERT into hotel (chainid,hname,phone,xcoord,ycoord,address) values (%s,%s,%s,%s,%s,%s)"
        cursor2.execute(
            sql2,
            (
                session["chainid"],
                request.form["hname"],
                request.form["phone"],
                request.form["xcoord"],
                request.form["ycoord"],
                request.form["address"],
            ),
        )
        get_db().commit()
        # get the id of the newly inserted hotel.
        cursor3 = get_db().cursor()
        sql3 = "SELECT hotelid from hotel where xcoord = %s and ycoord = %s"
        cursor3.execute(sql3, (request.form["xcoord"], request.form["ycoord"]))
        rows = cursor3.fetchone()
        # build the rooms
        for i in range(int(request.form["num_dlx"])):
            cursor4 = get_db().cursor()
            sql4 = "INSERT into room (hotelid,price,roomnum,rType,capacity) values (%s, %s, %s, 'delux', 2)"
            cursor4.execute(sql4, (rows["hotelid"], request.form["price_dlx"], i))
            get_db().commit()
        for i in range(int(request.form["num_std"])):
            cursor4 = get_db().cursor()
            sql4 = "INSERT into room (hotelid,price,roomnum,rType,capacity) values (%s, %s, %s, 'standard', 1)"
            cursor4.execute(sql4, (rows["hotelid"], request.form["price_std"], i))
            get_db().commit()
    else:
        return "Sorry there is a hotel with those coordinates. Please try again!"

    return redirect(url_for("index"))
