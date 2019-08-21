# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.conf import settings
from django.contrib.gis.geos import Point

from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


from django.contrib.gis.db import models


class LocationQuerySet(models.QuerySet):
    """
    Custom queryset object which provides a bunch of useful methods for querying actions.
    """

    def near(self, point, distance=None, field='point__distance'):
        """
        Annotate queryset with distances for activities from some particular point. Can also perform filtering based on distance if `distance` argument is specified.

        :param point: Point to use as a center
        :param distance: Perform filtering on distance (optional)
        :param field: Field to use for distance calculation (optional)
        :return: Annotated (and possibly filtered) queryset
        """
        if distance is None:
            distance = settings.SPHAX_CONFIG['DISTANCE_MAX']
        queryset = self.filter(**{
            '{}_lte'.format(field): (point, D(km=distance))
        })
        return queryset

    def near_list(self, point, distance=None, field='point__distance'):
        """
        Annotate queryset with distances for activities from some particular point. Can also perform filtering based on distance if `distance` argument is specified.

        :param point: Point to use as a center
        :param distance: Perform filtering on distance (optional)
        :param field: Field to use for distance calculation (optional)
        :return: Annotated (and possibly filtered) queryset
        """
        if distance is None:
            distance = settings.SPHAX_CONFIG['DISTANCE_MIN']

        queryset = self.filter(**{
            '{}_lte'.format(field): (point, D(km=distance))
        })
        if queryset.count() < 10:
            while queryset.count() < 10:
                if distance >= settings.SPHAX_CONFIG['DISTANCE_MAX']:
                    break
                distance += settings.SPHAX_CONFIG['DISTANCE_STEP']
                queryset = self.filter(**{
                    '{}_lte'.format(field): (point, D(km=distance))
                })
        return queryset


class LocationManager(models.Manager):
    """
    Custom manager for activities.
    We use this to have some fields preselected automatically to speed up performance.
    """

    def get_queryset(self):
        return LocationQuerySet(self.model, using=self._db).prefetch_related(
            'city',
        )

    def distance_queryset(self, point):
        queryset = self.get_queryset().annotate(distance=Distance(
            'point', point)).near_list(point).order_by('-distance')
        return queryset


class Location(models.Model):
    city = models.CharField(
        _("City"), max_length=255, blank=True, null=True)
    postcode = models.CharField(
        _("Post code"), max_length=30, blank=True, null=True)
    street = models.CharField(
        _("Street"), max_length=255, blank=True, null=True)
    point = models.PointField(
        _('Latitude-Longitude point'), blank=True, null=True)
    timezone = models.CharField(
        _('Time zone'), default=settings.TIME_ZONE, max_length=100)

    objects = models.Manager()
    distances = LocationManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.point:
            self.set_location()
        return super(Location, self).save(*args, **kwargs)

    def set_location(self):
        """
            Set all locations to the object
        """
        from django.apps import apps
        if not self.point:
            if self.street and self.postcode:
                geolocator = GoogleV3(api_key=settings.GEOCODING_API_KEY)
                try:
                    adresse = "{0} {1} {2}".format(
                        self.street, self.postcode, self.city.name)
                except AttributeError:
                    adresse = "{} {}".format(self.street, self.postcode)
                try:
                    location = geolocator.geocode(adresse, timeout=10)
                except GeocoderTimedOut:
                    try:
                        location = geolocator.geocode(adresse, timeout=10)
                    except GeocoderTimedOut:
                        pass
                except GeocoderServiceError:
                    pass

                    self.point = Point(location.longitude, location.latitude)
                    if location.raw.get("address_components", None):
                        for add in location.raw["address_components"]:
                            if add["types"] == "streed_number":
                                self.street += add["long_name"]
                            if add["types"] == "route":
                                self.street += add["long_name"]
                            if add['types'] == "administrative_area_level_1":
                                self.city = add["long_name"]
            else:
                if self.city:
                    self.point = self.city.location
        return self.point
