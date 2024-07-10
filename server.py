from flask import Flask, render_template, redirect, url_for
from forms import TeamForm, ProjectForm
from model import User, Team, Project, connect_to_db, db

app = Flask(__name__)

app.secret_key = "keep this secret"

user_id = 1

@app.route("/")
def home():
    team_form = TeamForm()
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)
    
    return render_template("home.html", team_form = team_form, project_form = project_form)

@app.route('/info')
def view_team_projects():
    user = User.query.get(user_id)
    teams = user.teams
    team_form = TeamForm()  # Assuming TeamForm is imported correctly
    project_form = ProjectForm()  # Assuming ProjectForm is imported correctly
    return render_template("info.html", teams=teams, team_form=team_form, project_form=project_form)

@app.route("/add-team", methods=["POST"])
def add_team():
    team_form = TeamForm()
    
    if team_form.validate_on_submit():
        team_name = team_form.team_name.data
        new_team = Team(team_name, user_id)
        db.session.add(new_team)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route('/add-project', methods=["POST"])
def add_project():
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)
    
    if project_form.validate_on_submit():
        project_name = project_form.project_name.data
        description = project_form.description.data
        completed = project_form.completed.data
        team_id = project_form.team_selection.data
        
        new_project = Project(project_name, description, team_id, completed=completed)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))
    
@app.route("/delete-team/<int:team_id>", methods=["POST"])
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    return redirect(url_for("view_team_projects"))

@app.route("/delete-project/<int:project_id>", methods=["POST"])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("view_team_projects"))

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)