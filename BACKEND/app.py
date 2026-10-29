from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_db_connection

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Smart Campus Assistant Backend is running!",
        "status": "success"
    })


@app.route("/api/faculty", methods=["GET"])
def get_faculty():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            faculty_name,
            department,
            building,
            floor,
            room_no,
            email
        FROM faculty
    """)

    faculty = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(faculty)


@app.route("/api/faculty/search", methods=["GET"])
def search_faculty():
    name = request.args.get("name", "").strip()

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            faculty_name,
            department,
            building,
            floor,
            room_no,
            email
        FROM faculty
        WHERE faculty_name LIKE %s
    """, (f"%{name}%",))

    faculty = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(faculty)


@app.route("/api/classrooms", methods=["GET"])
def get_classrooms():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            room_no,
            building,
            floor,
            source
        FROM classrooms
    """)

    classrooms = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(classrooms)


@app.route("/api/labs", methods=["GET"])
def get_labs():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            lab_room_no,
            building,
            floor,
            source
        FROM labs
    """)

    labs = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(labs)


@app.route("/api/offices", methods=["GET"])
def get_offices():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            office,
            building,
            floor,
            timing,
            services,
            source
        FROM offices
    """)

    offices = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(offices)


@app.route("/api/departments", methods=["GET"])
def get_departments():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            department,
            hod,
            room_no,
            email,
            source
        FROM departments
    """)

    departments = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(departments)


@app.route("/api/admin-services", methods=["GET"])
def get_admin_services():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            block_name,
            department_room,
            services_provided,
            source
        FROM admin_services
    """)

    services = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(services)


@app.route("/api/dt-seating", methods=["GET"])
def get_dt_seating():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            floor,
            faculty_name,
            room_cabin_no,
            source_sheet,
            source_row
        FROM dt_seating_plan
    """)

    seating = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(seating)

@app.route("/api/search")
def search():
    q = request.args.get("q", "").strip()

    if not q:
        return jsonify([])

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    search = f"%{q}%"
    results = []

    # =========================
    # FACULTY
    # =========================
    cursor.execute("""
        SELECT
            'Faculty' AS type,
            faculty_name AS name,
            CONCAT(
                department,
                ' — ',
                building,
                ', Floor ',
                floor,
                ', Room ',
                room_no
            ) AS detail,
            room_no AS code
        FROM faculty
        WHERE
            faculty_name LIKE %s
            OR department LIKE %s
            OR building LIKE %s
            OR floor LIKE %s
            OR room_no LIKE %s
            OR email LIKE %s
    """, (search, search, search, search, search, search))

    results.extend(cursor.fetchall())


    # =========================
    # CLASSROOMS
    # =========================
    cursor.execute("""
        SELECT
            'Classroom' AS type,
            room_no AS name,
            CONCAT(
                building,
                ', Floor ',
                floor
            ) AS detail,
            room_no AS code
        FROM classrooms
        WHERE
            room_no LIKE %s
            OR building LIKE %s
            OR floor LIKE %s
    """, (search, search, search))

    results.extend(cursor.fetchall())


    # =========================
    # LABS
    # =========================
    cursor.execute("""
        SELECT
            'Lab' AS type,
            lab_room_no AS name,
            CONCAT(
                building,
                ', Floor ',
                floor
            ) AS detail,
            lab_room_no AS code
        FROM labs
        WHERE
            lab_room_no LIKE %s
            OR building LIKE %s
            OR floor LIKE %s
    """, (search, search, search))

    results.extend(cursor.fetchall())


    # =========================
    # OFFICES
    # =========================
    cursor.execute("""
        SELECT
            'Office' AS type,
            office AS name,
            CONCAT(
                building,
                ', Floor ',
                floor,
                ' — ',
                services
            ) AS detail,
            office AS code
        FROM offices
        WHERE
            office LIKE %s
            OR building LIKE %s
            OR floor LIKE %s
            OR services LIKE %s
    """, (search, search, search, search))

    results.extend(cursor.fetchall())


    # =========================
    # DEPARTMENTS
    # =========================
    cursor.execute("""
        SELECT
            'Department' AS type,
            department AS name,
            CONCAT(
                'HOD: ',
                hod,
                ' — Room ',
                room_no
            ) AS detail,
            room_no AS code
        FROM departments
        WHERE
            department LIKE %s
            OR hod LIKE %s
            OR room_no LIKE %s
            OR email LIKE %s
    """, (search, search, search, search))

    results.extend(cursor.fetchall())


    cursor.close()
    conn.close()

    return jsonify(results)

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )