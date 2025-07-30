# -*- coding: utf-8 -*-
"""Plone support for the Propertyshelf MLS."""

from plone import api


PLONE_4 = '4' <= api.env.plone_version() < '5'
