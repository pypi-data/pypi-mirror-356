# -*- coding: utf-8 -*-
"""Interface definitions."""

# zope imports
from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class IListingSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer."""


class IListingDetails(Interface):
    """Marker interface for ListingDetails view."""


class IBaseListingItems(Interface):
    """Marker interface for all listing 'collection' items."""


class IPossibleListingCollection(Interface):
    """Marker interface for possible ListingCollection viewlet."""


class IListingCollection(IBaseListingItems):
    """Marker interface for ListingCollection viewlet."""


class IPossibleListingSearch(Interface):
    """Marker interface for possible ListingSearch viewlet."""


class IListingSearch(IBaseListingItems):
    """Marker interface for ListingSearch viewlet."""


class IPossibleRecentListings(Interface):
    """Marker interface for possible RecentListings viewlet."""


class IRecentListings(IBaseListingItems):
    """Marker interface for RecentListings viewlet."""
