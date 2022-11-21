from flask import Blueprint, render_template

error_scope=Blueprint("errors",__name__)


@error_scope.app_errorhandler(404)
def page_notfound(error):
    return render_template("404.html"), 404