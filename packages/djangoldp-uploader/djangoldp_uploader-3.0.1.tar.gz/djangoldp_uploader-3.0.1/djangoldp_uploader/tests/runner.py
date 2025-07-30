import sys
import yaml

import django
from django.conf import settings as django_settings
from djangoldp.conf.ldpsettings import LDPSettings

# create a test configuration
config = {
    # add the packages to the reference list
    'ldppackages': ['djangoldp_uploader'],

    'MEDIA_URL': '/media/',
    'MEDIA_ROOT': 'media',

    # required values for server
    'server': {
        'MEDIA_URL': '/media/',
        'MEDIA_ROOT': 'media',
    }
}

ldpsettings = LDPSettings(config)
django_settings.configure(ldpsettings)

django.setup()
from django.test.runner import DiscoverRunner

test_runner = DiscoverRunner(verbosity=1)

failures = test_runner.run_tests([
    'djangoldp_uploader.tests.tests_upload',
])
if failures:
    sys.exit(failures)
