from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for pic in data:
        if pic.get('id') == id:
            return jsonify(pic), 200
    abort(404)


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    if not picture:
        return {"message": "Invalid input"}, 400

    # Duplicate detection by 'id'
    posted_id = picture.get('id')
    if posted_id is not None:
        for pic in data:
            if pic.get('id') == posted_id:
                return jsonify({"Message": f"picture with id {posted_id} already present"}), 302

    # Assign id if not provided
    if posted_id is None:
        posted_id = max([pic.get('id', 0) for pic in data], default=0) + 1
        picture['id'] = posted_id

    data.append(picture)
    with open(json_url, "w") as f:
        json.dump(data, f)

    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.get_json()
    for idx, pic in enumerate(data):
        if pic.get('id') == id:
            picture['id'] = id  # Ensure id stays the same
            data[idx] = picture
            with open(json_url, "w") as f:
                json.dump(data, f)
            return jsonify(picture), 200
    abort(404)

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for idx, pic in enumerate(data):
        if pic.get('id') == id:
            del data[idx]
            with open(json_url, "w") as f:
                json.dump(data, f)
            return "", 204
    abort(404)

