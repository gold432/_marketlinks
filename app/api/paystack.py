import os
from flask import request, jsonify, current_app
from flask_cors import cross_origin
from app import db
from app.api import bp
basedir = os.path.abspath(os.path.dirname(__file__))
from app.api.errors import response, bad_request
from app.models import User, Card, LPlan
from app.api.auth import token_auth
from pypaystack import Transaction, Customer
import json

@bp.before_request
def log_request():
    current_app.logger.debug('Request: %s', request)

@bp.route('paystack/initialize', methods=['POST'])
def initialize():
    q = request.get_json()
    email = q['email']
    amount = q['amount']
    metadata = q['metadata']
    t = Transaction()
    url = t.initialize(email=email, amount=amount, metadata=metadata)
    if not url:
        return response(500, 'Could not initialize the transaction')
    return jsonify({'url':url})

@bp.route('paystack/p_test', methods=['POST'])
def p_test():
    a = request.get_json()
    iSay = a['iSay']
    return jsonify({'you_said': iSay})

@bp.route('paystack/listen', methods=['POST'])
def listen():
    a = request.get_json()
    if a['event'] == 'subscription_create':
        data = a['data']
        metadata = data['customer']['metadata']
        year = metadata['year']
        module = metadata['module']
        email = metadata['email']
        password = metadata['password']
        user = User(email=email, password=password)
        user.subscribe(year, module)
        user.confirmed=true
        db.session.commit()

@bp.route('paystack/init', methods=['POST'])
def init():
    a = request.get_json()
    email = a['email'] 
    t=Transaction()
    p = a['l_plan']
    l_plan = LPlan.query.get(p)
    amount = l_plan.amount
    user=User.query.filter_by(email=email).first()
    if user:
        return bad_request('User already registered')
    r = t.initialize(email=email, amount=amount)
    if not r:
        return bad_request("something's wrong")
    
    auth_url = r[3]['authorization_url']
    return jsonify({'url': auth_url})

@bp.route('paystack/card', methods=['POST'])
def card():
    a = request.get_json()
    reference = a['reference']
    r = Transaction().verify(reference)
    if r:
        if r[3]['status'] == 'success':
            if a['plan']:
                plan = LPlan.query.filter_by(name=a['plan']).first()
            c = r[3]['customer']
            email = c['email']
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(email=c['email'], \
                        first_name=c['first_name'], last_name=c['last_name'])
                password = a['password']
                user.set_password(password)
                user.confirmed = True
                db.session.add(user)
            if plan:
                user.subscribe(plan)
            user.customer_code = c['customer_code']
            card_auth = r[3]['authorization']['authorization_code']
            card = Card.query.filter_by(authorization_code = card_auth).first()
            if not card:
                card = Card()
                card.authorization_code = card_auth
            db.session.add(card)
            db.session.commit()
            x = user.to_dict()
        else:
            return {'status': 'failed'}
    else:
        return response("Sorry, we've got an error, it's personal")
    return jsonify(x)

@bp.route('/paystack/get_customer/<email>', methods=['GET'])
def get_customer(email):
    customer = Customer()
    user = User.query.filter_by(email=email).first()
    response = customer.getone(user.ps_id)
    return jsonify(response)

@bp.route('/paystack/verify_transaction/<ref>', methods=['GET'])
def verify_transaction(ref):
    transaction = Transaction()
    response = transaction.verify(ref)
    return response

@bp.route('/paystack/charge_user', methods=['POST'])
def charge_user():
    data = request.get_json()
    l_plan = data['l_plan']
    user = data['user']
    l_plan = LPlan.query.get(l_plan)
    user = User.query.get(user)
    transaction = Transaction()
    response = transaction.charge(user.email, user.customer_code, l_plan.amount)
    if response[3]['status'] == 'failed':
        return {'status': 'failed'}
    user.l_plans.append(l_plan)
    return {'status': 'success'}

