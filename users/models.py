# users.models
# Contains additional User profile data but no authentication
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Jan 15 16:50:01 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Contains additional User profile data but no authentication
"""

##########################################################################
## Imports
##########################################################################


from django.db import models
from minent.utils import nullable
from urllib.parse import urlencode
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

##########################################################################
## UserProfile model
##########################################################################


class Profile(models.Model):

    user         = models.OneToOneField(User, editable=False)
    email_hash   = models.CharField(max_length=32, editable=False)
    biography    = models.CharField(max_length=255, **nullable)
    organization = models.CharField(max_length=255, **nullable)
    location     = models.CharField(max_length=255, **nullable)

    def get_gravatar_url(self, size=200, default="mm"):
        """
        Computes the gravatar url from an email address
        """
        params = urlencode({'d': default, 's': str(size)})
        grvurl = "http://www.gravatar.com/avatar/%s?%s" % (self.email_hash,
                                                           params)
        return grvurl

    @property
    def gravatar(self):
        return self.get_gravatar_url()

    @property
    def gravatar_icon(self):
        return self.get_gravatar_url(size=24)

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def full_email(self):
        email = "%s <%s>" % (self.full_name, self.user.email)
        return email.strip()

    def get_api_detail_url(self):
        """
        Returns the API detail endpoint for the object
        """
        return reverse('api:user-detail', args=(self.pk,))

    def __unicode__(self):
        return self.full_email