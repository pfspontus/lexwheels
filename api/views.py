"""
API views
"""
from flask import abort
from flask import jsonify


def define(api_page, models):
    @api_page.route('/owner/<int:id>')
    def owner(id):
        owner = models.get_owner(id)
        if owner:
            return owner.as_dict()
        return abort(404)

    @api_page.route('/owners')
    def owners():
        owners = [o.as_dict() for o in models.get_all_owners()]
        return jsonify(owners)
