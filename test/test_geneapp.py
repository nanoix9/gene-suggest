#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app as _app, db as _db, Gene
import pytest

@pytest.yield_fixture(scope='session')
def app(request):
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    _app.config['TESTING'] = True

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()

@pytest.yield_fixture(scope='session')
def db(app, request):
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()

@pytest.yield_fixture(scope='function')
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()

@pytest.fixture(scope='session')
def client(app):
    client = app.test_client()
    return client

def _add_data(session, data):
    for species, display_label in data:
        session.add(Gene(species=species, display_label=display_label))
    session.commit()

def test_gene_suggest(client, session):
    _add_data(session, [
        ('homo_sapiens', 'A2M-AS1'),
        ('homo_sapiens', 'A2ML1'),
        ('homo_sapiens', 'A2ML1-AS1'),
        ('homo_sapiens', 'A3GALT2'),
        ('mus_caroli', 'Ighe'),
        ('mus_caroli', 'Ighg2b'),
        ('mus_caroli', 'Ighg1')
        ])

    res = client.get('/gene_suggest?species=homo_sapiens&query=a2&limit=2')
    assert res.status_code == 200
    assert len(res.json) == 2
    assert res.json[0] == 'A2M-AS1'
    assert res.json[1] == 'A2ML1'

    res = client.get('/gene_suggest?species=mus_caroli&query=ighg&limit=2')
    assert res.status_code == 200
    assert len(res.json) == 2
    assert res.json[0] == 'Ighg1'
    assert res.json[1] == 'Ighg2b'

def test_gene_suggest_no_enough_suggest(client, session):
    _add_data(session, [
        ('homo_sapiens', 'A2M-AS1'),
        ('homo_sapiens', 'A2ML1'),
        ('homo_sapiens', 'A2ML1-AS1'),
        ('homo_sapiens', 'A3GALT2')
        ])

    res = client.get('/gene_suggest?species=homo_sapiens&query=a2&limit=10')
    assert res.status_code == 200
    assert len(res.json) == 3
    assert res.json[0] == 'A2M-AS1'
    assert res.json[1] == 'A2ML1'
    assert res.json[2] == 'A2ML1-AS1'

def test_gene_suggest_no_match(client, session):
    _add_data(session, [
        ('homo_sapiens', 'A2M-AS1'),
        ('homo_sapiens', 'A2ML1'),
        ('homo_sapiens', 'A2ML1-AS1'),
        ('homo_sapiens', 'A3GALT2')
        ])

    res = client.get('/gene_suggest?species=homo_sapiens&query=b&limit=10')
    assert res.status_code == 200
    assert len(res.json) == 0

def test_gene_suggest_no_exist_species(client, session):
    _add_data(session, [ ('homo_sapiens', 'A2M-AS1') ])

    res = client.get('/gene_suggest?species=mus_caroli&query=a2&limit=10')
    assert res.status_code == 200
    assert len(res.json) == 0

def test_gene_suggest_empty_query(client, session):
    res = client.get('/gene_suggest?species=homo_sapiens&query=&limit=10')
    assert res.status_code == 400
    assert 'query should not be empty' in res.data.decode('utf8')

