from flask import Flask, render_template, request, redirect, jsonify, url_for
import json

app = Flask(__name__, template_folder="templates")

students = [
    {
        'name': 'Test Student',
        'group': '10KN',
        'mark': 5
    }
]

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    return render_template("index.html", stud_count=len(students))

@app.route("/student/list")
def list_students():
    return render_template("list_students.html", students=enumerate(students))

@app.route("/student/add", methods=["GET", "POST"])
def add_student():
    if request.method == "GET":
        return render_template("add-student.html")
    if request.method == "POST":
        attrs = request.form
        if not attrs['mark'].isnumeric(): return 'Error: mark nust be number!<br><button onclick="history.back()">Go Back</button>'
        students.append( {
            'name': attrs['name'],
            'group': attrs['group'],
            'mark': int(attrs['mark'])
        } )
        return redirect(url_for("list_students"))

@app.route("/student/delete/<id>", methods=["POST"])
def delete_student(id):
    students.remove(students[int(id)])
    return redirect(url_for("list_students"))

@app.route("/api/list")
def api_list():
    return jsonify(students)

@app.route("/api/add", methods=["POST"])
def api_add():
    attrs = request.json
    if not "name" in attrs: return jsonify( { 'error': 'no name present' } )
    if not "group" in attrs: return jsonify( { 'error': 'no group present' } )
    if not "mark" in attrs: return jsonify( { 'error': 'no mark present' } )
    if not isinstance(attrs['mark'], int): return jsonify( { 'error': 'mark must be a number' } )
    students.append( {
        'name': attrs['name'],
        'group': attrs['group'],
        'mark': int(attrs['mark'])
    } )
    return jsonify(True)

@app.route("/api/delete/<id>", methods=["POST"])
def api_delete(id):
    students.remove(students[int(id)])
    return jsonify(True)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
