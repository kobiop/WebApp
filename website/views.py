from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
#from . import db
import json
from website.database import offLineSerach,load_apartments_from_db,load_apartment_from_db,add_new_listings_to_db,add_user_preferences_to_db, user_filter

views= Blueprint('views',__name__)

# Your Flask route function
@views.route('/listing/', defaults={'page_number': 1})
@views.route('/listing/<int:page_number>')
def features(page_number):
    listing = load_apartments_from_db(page_number)
    return render_template("listing.html", listings=listing, page_number=page_number, total_pages=5, user=current_user)


# @views.route('/listing')
# def features():
#     list_job = load_apartments_from_db()
#     return render_template("listing.html",listings=list_job ,user=current_user)


@views.route('/offLineSearch', methods=['GET', 'POST'])
def show_listing():
    if request.method == 'POST': 
        data = request.form
        add_user_preferences_to_db(data)
        offLineSerach()
        render_template('offlineSearch.html')

    return render_template('offlineSearch.html') 

@views.route('/add_listing',methods=['POST','GET'])
def add_listing():
    return render_template("new_list_form.html", user=current_user) 

@views.route('/preferences/apply',methods=['POST','GET'])
def fillter():
     if request.method == 'POST': 
        data = request.form #Gets the note from the HTML
        listing=user_filter(data)
        total_pages= int(len(listing)/12)+1

        return render_template("listing.html", listings=listing, page_number=1, total_pages=total_pages, user=current_user)

@views.route('/preferences',methods=['POST','GET'])
def preferences():
    # if request.method == 'POST': 
    #     # data = request.form #Gets the note from the HTML
    #     # listing=user_filter(data)
    #     return redirect(url_for('views.features',page_number=1))
    
    return render_template("preferences.html", user=current_user) 




@views.route('/add_listing/apply',methods=['POST'])
def add_new_listing_to_db():
    data=request.form
    add_new_listings_to_db(data)
    return render_template("listing_submitted.html", user=current_user) 

@views.route('/',methods=['POST','GET'])
def home():
    # if request.method == 'POST': 
    #     note = request.form.get('note')#Gets the note from the HTML 

    #     if len(note) < 1:
    #         flash('Note is too short!', category='error') 
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
    #         db.session.add(new_note) #adding the note to the database 
    #         db.session.commit()
    #         flash('Note added!', category='success')

    return render_template("home.html", user=current_user) 


# @views.route('/delete-note', methods=['POST'])
# def delete_note():  
#     note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})