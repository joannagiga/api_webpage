function deleteCourse(button) {
    var course_id = button.getAttribute('course-id');
   
    if (confirm("Are you sure you want to delete this course?")) {
        fetch(`/course/${course_id}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success === true) {
                window.location.reload();
            } else {
                console.error("Error: " + data.error);
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });        
    }
}

function deleteStudent(button) {
    var stud_ID = button.getAttribute('student-id');
    if (confirm("Are you sure you want to delete this student?")) {
        fetch(`/student/${stud_ID}`, {
            method: 'DELETE',

        }).then(response => response.json())
        .then(data => {
            if (data.success === true) {
                window.location.reload();
            } else {
                console.error("Error: " + data.error);
            }
        });        
    }
    window.location.reload();
}
function editStudent(studentID, firstName, lastName, gender, courseCode, yearLevel, imageUrl) {
    // Fill in the form fields with the student's information
    document.getElementById('editStudentID').value = studentID;
    document.getElementById('editFirstName').value = firstName;
    document.getElementById('editLastName').value = lastName;
    document.getElementById('editGender').value = gender;
    document.getElementById('editCourseCode').value = courseCode;
    document.getElementById('editYearLevel').value = yearLevel;

    // Show the edit form
    document.getElementById('editForm').style.display = 'block';
}

function cancelEdit() {
    // Hide the edit form
    document.getElementById('editForm').style.display = 'none';
}

