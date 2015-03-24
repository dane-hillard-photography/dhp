from django.conf import settings


def template_visible_settings(request):
    added_settings = {}
    for setting in getattr(settings, 'TEMPLATE_VISIBLE_SETTINGS', ()):
        if hasattr(settings, setting):
            added_settings[setting] = getattr(settings, setting, '')
    return added_settings
