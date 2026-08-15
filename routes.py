from flask import Blueprint, render_template, redirect

from lib.content import load_content
from lib.decorators.state_machine_decorator import with_state_machine
from forms.home import HomeForm


bp = Blueprint("main", __name__)


@bp.route("/", methods=("GET", "POST"))
@with_state_machine
def home(state_machine):
    form = HomeForm()
    if form.validate_on_submit():
        state_machine.continue_from_initial()
        return redirect(state_machine.route_for_current_state)
    return render_template("home.html", form=form, content=load_content())


@bp.route("/first-page/")
def first_page():
    return render_template("first-page.html", content=load_content())


@bp.route("/health")
def health():
    # Dependency-free by design: answers "can this process serve HTTP?",
    # nothing more. Keep template renders and service calls out of it.
    return {"status": "ok"}
