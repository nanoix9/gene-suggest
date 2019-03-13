#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

LIMIT_LOWER = 1
LIMIT_UPPER = 100
DB_URI = 'mysql://anonymous@ensembldb.ensembl.org/ensembl_website_90'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from .models import Gene

@app.route('/gene_suggest', methods=['GET'])
def index():
    species = request.args.get('species')
    query = request.args.get('query')
    limit_str = request.args.get('limit')

    if species is None or len(species) == 0:
        return abort(400, 'species should not be empty')
    if query is None or len(query) == 0:
        return abort(400, 'query should not be empty')

    limit_err_msg = 'limit must be an integer between {} and {}' \
            .format(LIMIT_LOWER, LIMIT_UPPER)
    try:
        limit = int(limit_str)
    except:
        return abort(400, limit_err_msg)

    if limit < LIMIT_LOWER or limit > LIMIT_UPPER:
        return abort(400, limit_err_msg)

    try:
        suggests = query_gene_suggest(query, species, limit)
        return jsonify(suggests)
    except:
        return abort(400, 'fail to get gene suggestion')

def query_gene_suggest(query, species, limit):
    res = db.session.query(Gene).first()

    stmt = db.session.query(Gene.display_label) \
            .distinct() \
            .filter( \
                and_( \
                    Gene.species == species, \
                    Gene.display_label.ilike(query + '%'))) \
            .order_by(Gene.display_label) \
            .limit(limit)
    result = stmt.all()
    return [g.display_label for g in result]

