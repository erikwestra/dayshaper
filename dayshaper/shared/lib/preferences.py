""" dayshaper.shared.lib.preferences

    This module provides low-level access to system preference settings.
"""
from dayshaper.shared.models import *

#############################################################################

def get(setting, default=None):
    """ Retrieve the value of the given preference setting as a string.

        If there is no setting with that name, we return the given default
        value.
    """
    try:
        pref = PreferenceSetting.objects.get(name=setting)
    except PreferenceSetting.DoesNotExist:
        return default # No such setting.
    return pref.value

#############################################################################

def set(setting, value):
    """ Set the value of the given preference setting to the given string.
    """
    pref,created = \
            PreferenceSetting.objects.get_or_create(name=setting,
                                                    defaults={'value' : value})
    if not created:
        pref.value = value
        pref.save()

#############################################################################

def get_int(setting, default=None):
    """ Retrieve the given preference setting, as an integer value.

        If there is no setting with that name, we return the given default
        value.
    """
    value = get(setting)
    if value == None: 
        return default
    else:
        return int(value)

#############################################################################

def set_int(setting, value):
    """ Set the given preference setting to the given integer value.
    """
    set(setting, str(value))

