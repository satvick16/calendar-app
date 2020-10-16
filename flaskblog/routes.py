import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db
from flaskblog.forms import *
from flaskblog.models import *


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', events=events)


@app.route("/new-event", methods=['GET', 'POST'])
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data, content=form.content.data)
        db.session.add(event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_event.html', title='New Event',
                           form=form, legend='New Event')


@app.route("/event/<int:event_id>")
def event(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event.html', title=event.title, event=event)


@app.route("/event/<int:event_id>/update", methods=['GET', 'POST'])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm()
    if form.validate_on_submit():
        event.title = form.title.data
        event.content = form.content.data
        db.session.commit()
        flash('Your event has been updated!', 'success')
        return redirect(url_for('event', post_id=event.id))
    elif request.method == 'GET':
        form.title.data = event.title
        form.content.data = event.content
    return render_template('new_event.html', title='Update Event',
                           form=form, legend='Update Event')


@app.route("/event/<int:event_id>/delete", methods=['POST'])
def delete_post(event_id):
    event = Event.query.get_or_404(post_id)
    db.session.delete(event)
    db.session.commit()
    flash('Your event has been deleted!', 'success')
    return redirect(url_for('home'))
