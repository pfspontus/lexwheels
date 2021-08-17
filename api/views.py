"""
API views
"""
from flask import abort
from flask import jsonify


def define(api_page, models):
    @api_page.route('/owner/<int:id>')
    def owner(id):
        try:
            return models.get_owner(id).name
        except IndexError:
            return abort(404)

    @api_page.route('/owners')
    def owners():
        return jsonify([o.name for o in models.get_all_owners()]) # jsonify(models.get_all_owners())
