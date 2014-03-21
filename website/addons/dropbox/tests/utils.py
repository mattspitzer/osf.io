# -*- coding: utf-8 -*-
import mock
from contextlib import contextmanager

from webtest_plus import TestApp

import website
from website.addons.base.testing import AddonTestCase

app = website.app.init_app(
    routes=True, set_backends=False, settings_module='website.settings'
)

class DropboxAddonTestCase(AddonTestCase):
    ADDON_SHORT_NAME = 'dropbox'

    def create_app(self):
        return TestApp(app)

    def set_user_settings(self, settings):
        settings.access_token = '12345abc'
        settings.dropbox_id = 'mydropboxid'

    def set_node_settings(self, settings):
        settings.folder = 'foo'



mock_responses = {
    'put_file': {
        'bytes': 77,
        'icon': 'page_white_text',
        'is_dir': False,
        'mime_type': 'text/plain',
        'modified': 'Wed, 20 Jul 2011 22:04:50 +0000',
        'path': '/magnum-opus.txt',
        'rev': '362e2029684fe',
        'revision': 221922,
        'root': 'dropbox',
        'size': '77 bytes',
        'thumb_exists': False
    },
    'metadata_list': {
        "size": "0 bytes",
        "hash": "37eb1ba1849d4b0fb0b28caf7ef3af52",
        "bytes": 0,
        "thumb_exists": False,
        "rev": "714f029684fe",
        "modified": "Wed, 27 Apr 2011 22:18:51 +0000",
        "path": "/Public",
        "is_dir": True,
        "icon": "folder_public",
        "root": "dropbox",
        "contents": [
            {
                "size": "0 bytes",
                "rev": "35c1f029684fe",
                "thumb_exists": False,
                "bytes": 0,
                "modified": "Mon, 18 Jul 2011 20:13:43 +0000",
                "client_mtime": "Wed, 20 Apr 2011 16:20:19 +0000",
                "path": "/Public/latest.txt",
                "is_dir": False,
                "icon": "page_white_text",
                "root": "dropbox",
                "mime_type": "text/plain",
                "revision": 220191
            }
        ],
        "revision": 29007
    }
}

class MockDropbox(object):

    def put_file(full_path, file_obj, overwrite=False, parent_rev=None):
        return mock_responses['put_file']

    def metadata(path, list=True, file_limit=25000, hash=None, rev=None,
        include_deleted=False):
        if list:
            return mock_responses['metadata_list']
        else:
            # TODO(sloria): return non-list response
            return mock_responses['metadata_list']

    def get_file_and_metadata(*args, **kwargs):
        pass


@contextmanager
def patch_client(target):
    """Patches a function that returns a DropboxClient, returning an instance
    of MockDropbox instead.

    Usage: ::

        with patch_client('website.addons.dropbox.view.config.get_client') as client:
            # test view that uses the dropbox client.
    """
    with mock.patch(target) as client_getter:
        client = MockDropbox()
        client_getter.return_value = client
        yield client
