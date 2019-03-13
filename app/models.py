#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .geneapp import db

GENE_TABLE_NAME = 'gene_autocomplete'

class Gene(db.Model):

    __tablename__ = GENE_TABLE_NAME

    species = db.Column(db.String, primary_key=True)
    display_label = db.Column(db.String, primary_key=True)

