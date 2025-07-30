# -*- coding: utf-8 -*-
"""Migration steps for plone.mls.listing."""

from plone import api
from plone.mls.core.interfaces import IMLSSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


PROFILE_ID = 'profile-plone.mls.core:default'


def migrate_to_1001(context):
    """Migrate from 1000 to 1001.

    * Activate portal actions.
    * Register JS resources.
    """
    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'actions')
    setup.runImportStepFromProfile(PROFILE_ID, 'jsregistry')


def migrate_to_1002(context):
    """Migrate from 1001 to 1002.

    * Add new registry settings for MLS.
    """
    registry = getUtility(IRegistry)
    registry.registerInterface(IMLSSettings)
