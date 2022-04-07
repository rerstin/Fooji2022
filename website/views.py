from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json
from .auth import populate_database
views = Blueprint('views', __name__)



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    populate_database()
    # if request.method == 'POST':
    #     note = request.form.get('note')
        
    #     if len(note) < 1:
    #         flash('Note is too short!', category='error')
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})


@views.route('/orders_you_created', methods=['GET'])
def orders_you_created():
    return render_template("orders_you_created.html", user=current_user)

@views.route('/orders_you_joined', methods=['GET'])
def orders_you_joined():
    return render_template("orders_you_joined.html", user=current_user)
