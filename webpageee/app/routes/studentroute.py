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

student_bp = Blueprint('student', __name__)


@student_bp.route('/student/', methods=['GET', 'POST'])
def students():
    try:
        students =spcall('get_students', param=None)[0][0]
        return render_template('students.html', students=students)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@student_bp.route('/student/add', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        student_name= request.form['student_name'].title()
        course_id = request.form['course_id'].upper()
        
        try:
            if student_name:
                res=spcall('insert_student', (student_name, course_id), commit=True)
                return redirect(url_for('student.students'))
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    courses =spcall('get_courses', param=None)[0][0]

    return render_template('addstudents.html', courses=courses)


@student_bp.route('/student/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    if request.method == 'POST':
        # Handle form data for updating student information
        student_name = request.form['student_name'].title()
        course_id = request.form['course_id'].upper()
        res = spcall('update_student_by_id', (student_id, student_name, course_id), commit=True)
        return redirect(url_for('student.students'))
        
    # Handle GET request to render the edit form
    student =spcall('get_student_by_id', (student_id, ), commit=False)[0][0]
    courses =spcall('get_courses', param=None)[0][0]
    return render_template('editstudent.html', student=student, courses=courses)



@student_bp.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    if request.method == 'DELETE':
        try:
            res = spcall('delete_student_by_id', (student_id, ), commit=True)
            return redirect(url_for('student.students'))
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})


@student_bp.route('/student', methods=['POST'])
def get_student():
    if request.method == 'POST':
        search_query = request.form.get('studentsearch', '')
        res = spcall('get_student_by_id', (search_query, ), commit=False)[0]
        if isinstance(res, str):
            res = [res]  # Convert single string result to a list
        return render_template('students.html', students=res)
