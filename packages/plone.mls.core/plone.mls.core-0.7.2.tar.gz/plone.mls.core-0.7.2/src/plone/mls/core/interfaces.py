# -*- coding: utf-8 -*-
"""Interface definitions."""

from plone.mls.core.i18n import _
from zope import schema
from zope.interface import Interface


class IMLSSettings(Interface):
    """Global Propertyshelf MLS settings.

    This describes records stored in the configuration registry and obtainable
    via plone.registry.
    """

    mls_site = schema.TextLine(
        default=u'',
        description=_(
            u'This is the URL of the MLS you want to connect to, e.g. '
            u'https://demomls.com.',
        ),
        required=True,
        title=_(u'MLS URL'),
    )

    mls_key = schema.TextLine(
        default=u'',
        description=_(u'This is your personal access token for the MLS.'),
        required=True,
        title=_(u'MLS API Key'),
    )

    agency_id = schema.TextLine(
        default=u'',
        description=_(
            u'This is the ID/short name of your agency/organization.',
        ),
        required=True,
        title=_(u'Agency ID'),
    )

    override_from_email = schema.TextLine(
        required=False,
        title=_(u'Override From Email Address'),
        description=_(
            u'If entered, this email address will be used as the from email '
            u'address for all listing inquiries from this embedding (e.g. using noreply@yourdomain.com). '
            u'If left blank, it will default to use the same domain that is used for '
            u'the ESMTP username in the Plone email settings, using a default '
            u'address of leads@smtpdomain.com.',
        ),
    )

    check_valid_listing = schema.Bool(
        default=False,
        required=False,
        title=_(u'Additional Check For Valid Listing'),
        description=_(
            u'If enabled, the listing collections and searches will first check whether this '
            u'listing is valid based on the configuration of that collection before showing '
            u'the detail page for that listing. '
            u'Note: This will decrease the performance and should only be used temporarily in very '
            u'specific cases when changes to the listing collections need to be reflected immediately '
            u'in order to remove indexed pages from search engines.',
        ),
    )


class IPossibleLocalMLSSettings(Interface):
    """Marker interface for possible local MLS settings."""


class ILocalMLSSettings(Interface):
    """Marker interface for activated local MLS settings."""
