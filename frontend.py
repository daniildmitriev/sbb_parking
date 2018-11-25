# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator

import numpy
from flask import session
from markupsafe import escape
from flask import request
from .api import LightTracker
import memcache
from flask import request
from werkzeug.contrib.cache import SimpleCache

from .forms import SignupForm, DashboardConfirmForm, DashboardReserveForm, DashboardLogoutForm
from .nav import nav


mc = SimpleCache()
frontend = Blueprint('frontend', __name__)
light_tracker = LightTracker()
mc.set("NUM_SPOTS", 1)
mc.set("RELOAD_COUNTER_INDEX", 5)
mc.set("RELOAD_COUNTER_RESERVE", 5)
mc.set("RELOAD_COUNTER_CONFIRM", 5)
# We're adding a navbar as well through flask-navbar. In our example, the
# navbar has an usual amount of Link-Elements, more commonly you will have a
# lot more View instances.


# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@frontend.route('/', methods=('GET', 'POST'))
def index():
    print(request.form)
    form = SignupForm()
    print("VALIDATING")
    # if mc.get("RELOAD_COUNTER_INDEX") > 0:
    #     mc.set("RELOAD_COUNTER_INDEX", mc.get("RELOAD_COUNTER_INDEX") - 1)
    #     return render_template('signup.html', form=form)

    if request.method == 'POST' and form.validate():
        session['username'] = form.name.data
        print("VALIDATEEEED!!!")
        # We don't have anything fancy in our application, so we are just
        # flashing a message when a user completes the form successfully.
        #
        # Note that the default flashed messages rendering allows HTML, so
        # we need to escape things if we input user values:
        flash('Hello, {}. You have successfully signed up'
              .format(escape(form.name.data)))

        # In a real application, you may wish to avoid this tedious redirect.
        print('right before redirection')
        return redirect(url_for('frontend.dashboard_reserve'))

    return render_template('signup.html', form=form)


@frontend.route('/dashboard_reserve', methods=('GET', 'POST'))
def dashboard_reserve():
    print('right after the redirect')
    form = DashboardReserveForm()
    NUM_SPOTS = mc.get("NUM_SPOTS")

    if mc.get("NUM_SPOTS") == 0:
        flash('No free spots available')
    else:
        flash('Number of spots available: ' + str(NUM_SPOTS))
    if request.method == 'POST' and 'username' in session and form.validate() and mc.get("NUM_SPOTS") > 0:

        # RESERVE BUTTON IS PRESSED
        light_tracker.reserve()
        NUM_SPOTS -= 1
        mc.set("NUM_SPOTS", NUM_SPOTS)
        print("VALIDATEEEED!!!")
        # We don't have anything fancy in our application, so we are just
        # flashing a message when a user completes the form successfully.
        #
        # Note that the default flashed messages rendering allows HTML, so
        # we need to escape things if we input user values:
        #if(CarDetection == False):
        flash('You have successfully reserved a parking spot')
        # In a real application, you may wish to avoid this tedious redirect.
        #else
        #flash('Sorry, no parking spaces available ;(')
        #Exit.
        return redirect(url_for('.dashboard_confirm'))


    return render_template('dashboard_reserve.html', form=form)


@frontend.route('/dashboard_confirm', methods=('GET', 'POST'))
def dashboard_confirm():
    if 'username' in session:
        form = DashboardConfirmForm()
        if mc.get("RELOAD_COUNTER_CONFIRM") == 1:
            mc.set("RELOAD_COUNTER_CONFIRM", 0)
            return render_template('dashboard_confirm.html', form=form)
        if request.method == 'POST' and  form.validate():
            light_tracker.confirm()
            print("VALIDATEEEED!!!")
            # We don't have anything fancy in our application, so we are just
            # flashing a message when a user completes the form successfully.
            #
            # Note that the default flashed messages rendering allows HTML, so
            # we need to escape things if we input user values:
            flash('You confirmed your parking')

            # In a real application, you may wish to avoid this tedious redirect.
            return redirect(url_for('.have_a_nice_trip'))

    return render_template('dashboard_confirm.html', form=form)

@frontend.route('/nice_trip', methods=('GET', 'POST'))
def have_a_nice_trip():
    form = DashboardLogoutForm()
    if form.validate():
        mc.set("NUM_SPOTS", mc.get("NUM_SPOTS") + 1)
        session.pop('username', None)
        return redirect(url_for('.index'))
    return render_template('have_a_nice_trip.html', form=form)



# # Shows a long signup form, demonstrating form rendering.
# @frontend.route('/', methods=('GET', 'POST'))
# def example_form():
#     form = SignupForm()
#     print("VALIDATING")
#     print(form.name)
#     print(form.errors)
#     print(form.validate())
#     if form.validate():
#         print("VALIDATEEEED!!!")
#         # We don't have anything fancy in our application, so we are just
#         # flashing a message when a user completes the form successfully.
#         #
#         # Note that the default flashed messages rendering allows HTML, so
#         # we need to escape things if we input user values:
#         flash('Hello, {}. You have successfully signed up'
#               .format(escape(form.name.data)))
#
#         # In a real application, you may wish to avoid this tedious redirect.
#         return redirect(url_for('.index'))
#
#     return render_template('signup.html', form=form)
