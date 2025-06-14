from flask import Blueprint, render_template, request, redirect, url_for,flash
from flask_login import login_required, current_user
from .models import Problem, db
import csv
from io import StringIO
from flask import Response

main = Blueprint('main', __name__)

@main.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('home.html')


@main.route('/dashboard')
@login_required
def dashboard():
    platform = request.args.get('platform')
    difficulty = request.args.get('difficulty')
    search = request.args.get('search')

    query = Problem.query.filter_by(user_id=current_user.id)

    if platform:
        query = query.filter_by(platform=platform)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if search:
        query = query.filter(Problem.title.ilike(f"%{search}%"))

    problems = query.all()

    total = len(problems)
    solved = len([p for p in problems if p.status == 'Solved'])
    unsolved = total - solved

    return render_template('dashboard.html', problems=problems, total=total, solved=solved, unsolved=unsolved)


@main.route('/add-problem', methods=['GET', 'POST'])
@login_required
def add_problem():
    if request.method == 'POST':
        title = request.form['title']
        platform = request.form['platform']
        difficulty = request.form['difficulty']
        status = request.form['status']

        new_problem = Problem(
            title=title,
            platform=platform,
            difficulty=difficulty,
            status=status,
            user_id=current_user.id
        )
        db.session.add(new_problem)
        db.session.commit()
        flash("Problem added successfully!", "success")
        return redirect(url_for('main.dashboard'))

    return render_template('add_problem.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_problem(id):
    problem = Problem.query.get_or_404(id)
    if problem.user_id != current_user.id:
        return "Unauthorized", 403

    if request.method == 'POST':
        problem.title = request.form['title']
        problem.platform = request.form['platform']
        problem.difficulty = request.form['difficulty']
        problem.status = request.form['status']
        db.session.commit()
        flash("Problem updated successfully!", "info")
        return redirect(url_for('main.dashboard'))

    return render_template('edit_problem.html', problem=problem)

@main.route('/delete/<int:id>')
@login_required
def delete_problem(id):
    problem = Problem.query.get_or_404(id)
    if problem.user_id != current_user.id:
        return "Unauthorized", 403

    db.session.delete(problem)
    db.session.commit()
    flash("Problem deleted successfully.", "danger")
    return redirect(url_for('main.dashboard'))

@main.route('/export')
@login_required
def export():
    problems = Problem.query.filter_by(user_id=current_user.id).all()

    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Title', 'Platform', 'Difficulty', 'Status'])

    for p in problems:
        cw.writerow([p.title, p.platform, p.difficulty, p.status])

    output = si.getvalue()
    return Response(output, mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=problems.csv"})



@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404