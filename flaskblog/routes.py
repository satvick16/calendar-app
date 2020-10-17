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
    events = Event.query.order_by(Event.date.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', events=events)


@app.route("/new-event", methods=['GET', 'POST'])
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data, date=form.date.data, 
            start_time=form.start_time.data, end_time=form.end_time.data, 
            repeat=form.repeat.data)
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
        event.date = form.date.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.repeat = form.repeat.data
        db.session.commit()
        flash('Your event has been updated!', 'success')
        return redirect(url_for('event', event_id=event.id))
    elif request.method == 'GET':
        form.title.data = event.title
        form.date.data = event.date
        form.start_time.data = event.start_time
        form.end_time.data = event.end_time
        form.repeat.data = event.repeat
    return render_template('new_event.html', title='Update Event',
                           form=form, legend='Update Event')


@app.route("/event/<int:event_id>/delete", methods=['POST'])
def delete_post(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Your event has been deleted!', 'success')
    return redirect(url_for('home'))
