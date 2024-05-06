from flask import Blueprint, render_template, redirect, flash, jsonify, request, url_for
import sys
import psycopg2

db_connection = psycopg2.connect(
        dbname='rest_api',
        user='postgres',
        password='root12345',
        host='localhost',
    )

def spcall(qry, param, commit=False):
    try:
        cursor = db_connection.cursor()
        cursor.callproc(qry, param)
        res = cursor.fetchall()
        if commit:
            db_connection.commit()
        return res
    except:
        res = [("Error: " + str(sys.exc_info()[0]) +
                " " + str(sys.exc_info()[1]),)]
    return res

course_bp = Blueprint('course', __name__)

@course_bp.route('/course/', methods=['GET', 'POST'])
def courses():
    try:
        courses =spcall('get_courses', param=None)[0][0]
        return render_template('course.html', courses=courses)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500



@course_bp.route('/course/add', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        course_name = request.form['course_name'].title()
        
        try:
            if course_name:
                res = spcall('insert_course', (course_name, ), commit=True)
                return redirect(url_for('course.courses'))
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    return render_template('addcourse.html')


@course_bp.route('/course/update/<int:course_id>', methods=['GET', 'POST'])
def update_course(course_id):
    if request.method == 'POST':
        # Handle form data for updating course information
        course_name = request.form['course_name'].title()
        
        res = spcall('update_course_by_id', (course_id, course_name), commit=True)
        return redirect(url_for('course.courses'))
        
    # Fetch the specific course to be edited
    course = spcall('get_course_by_id', (course_id, ))[0][0]
    return render_template('editcourse.html', course_id=course_id, course=course)


@course_bp.route('/course/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    if request.method == 'DELETE':
        try:
            res = spcall('delete_course_by_id', (course_id, ), commit=True)
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})



@course_bp.route('/course', methods=['POST'])
def get_course():
    if request.method == 'POST':
        search_query = request.form.get('course_search', '')  # Corrected form field name
        res = spcall('get_course_by_id', (search_query, ), commit=False)[0]  # Assuming stored procedure returns a single result
        if isinstance(res, str):
            res = [res]  # Convert single string result to a list
        return render_template('course.html', courses=res)

