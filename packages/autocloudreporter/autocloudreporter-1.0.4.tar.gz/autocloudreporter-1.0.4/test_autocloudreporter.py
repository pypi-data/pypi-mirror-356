# Copyright (C) Red Hat Inc.
#
# autocloudreporter is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author:   Adam Williamson <awilliam@redhat.com>

# these are all kinda inappropriate for pytest patterns
# pylint: disable=old-style-class, no-init, protected-access, no-self-use, unused-argument

"""Tests for autocloudreporter."""

from __future__ import unicode_literals
from __future__ import print_function

# external imports
import fedfind.release
from fedora_messaging.api import Message
import mock

# 'internal' imports
import autocloudreporter

# fedfind metadata dict used to avoid a round trip to get the real one.
METADATA01 = {
    "composeinfo": {
        "header": {
            "type": "productmd.composeinfo",
            "version": "1.2"
        },
        "payload": {
            "compose": {
                "date": "20170206",
                "id": "Fedora-Atomic-25-20170206.0",
                "respin": 0,
                "type": "production"
            },
            "release": {
                "internal": False,
                "name": "Fedora",
                "short": "Fedora",
                "type": "ga",
                "version": "25"
            },
        },
    },
}

# fedfind image dict we use to avoid a round trip to get the real one.
FFIMG01 = {
    "variant": "CloudImages",
    "arch": "x86_64",
    "bootable": False,
    "checksums": {
        "sha256": "1ba75850449f94b128c0fca4fed158611106ae836f06a2d5662c0ab435440d7c"
    },
    "disc_count": 1,
    "disc_number": 1,
    "format": "vagrant-virtualbox.box",
    "implant_md5": None,
    "mtime": 1486362835,
    "path": "CloudImages/x86_64/images/Fedora-Atomic-Vagrant-25-20170206.0.x86_64.vagrant-virtualbox.box",
    "size": 642150400,
    "subvariant": "Atomic",
    "type": "vagrant-virtualbox",
    "volume_id": None
}

# constant mocking of the compose and image used for testing
imgpatcher = mock.patch.object(fedfind.release.AtomicNightly, 'all_images', [FFIMG01])
imgpatcher.start()
mdpatcher = mock.patch.object(fedfind.release.AtomicNightly, 'metadata', METADATA01)
mdpatcher.start()

# initialize two test consumers with different configs
PRODCONF = {
    'consumer_config': {
        'autocloud_url': "https://apps.fedoraproject.org/autocloud",
        'resultsdb_url': "http://resultsdb01.qa.fedoraproject.org/resultsdb_api/api/v2.0/",
    }
}
STGCONF = {
    'consumer_config': {
        'autocloud_url': "https://apps.stg.fedoraproject.org/autocloud",
        'resultsdb_url': "http://resultsdb-stg01.qa.fedoraproject.org/resultsdb_api/api/v2.0/",
    }
}

with mock.patch.dict('fedora_messaging.config.conf', PRODCONF):
    CONSUMER = autocloudreporter.AutocloudReporter()
with mock.patch.dict('fedora_messaging.config.conf', STGCONF):
    STGCONSUMER = autocloudreporter.AutocloudReporter()

@mock.patch('resultsdb_api.ResultsDBapi.create_result', return_value=True, autospec=True)
def test_success(fake_create):
    """Test we get a properly submitted result for a passed test."""
    msg = Message(
        topic="org.fedoraproject.prod.autocloud.image.success",
        body={
            "compose_id": "Fedora-Atomic-25-20170206.0",
            "compose_url": "http://kojipkgs.fedoraproject.org/compose/twoweek/Fedora-Atomic-25-20170206.0/compose/CloudImages/x86_64/images/Fedora-Atomic-Vagrant-25-20170206.0.x86_64.vagrant-virtualbox.box",
            "family": "Atomic",
            "image_name": "Fedora-Atomic-Vagrant-25-20170206.0",
            "job_id": 2023,
            "release": "25",
            "status": "success",
            "type": "vagrant-virtualbox"
        },
    )
    CONSUMER(msg)
    assert fake_create.call_count == 1
    assert fake_create.call_args[1]['outcome'] == 'PASSED'
    assert fake_create.call_args[1]['ref_url'] == 'https://apps.fedoraproject.org/autocloud/jobs/2023/output'
    assert fake_create.call_args[1]['source'] == 'autocloud'
    assert fake_create.call_args[1]['testcase']['ref_url'] == 'https://github.com/kushaldas/autocloud/'
    assert fake_create.call_args[1]['item'] == 'Fedora-Atomic-Vagrant-25-20170206.0.x86_64.vagrant-virtualbox.box'

    fake_create.reset_mock()
    msg.topic = msg.topic.replace('.prod.', '.stg.')

    STGCONSUMER(msg)
    assert fake_create.call_count == 1
    assert fake_create.call_args[1]['outcome'] == 'PASSED'
    assert fake_create.call_args[1]['ref_url'] == 'https://apps.stg.fedoraproject.org/autocloud/jobs/2023/output'
    assert fake_create.call_args[1]['source'] == 'autocloud'
    assert fake_create.call_args[1]['testcase']['ref_url'] == 'https://github.com/kushaldas/autocloud/'
    assert fake_create.call_args[1]['item'] == 'Fedora-Atomic-Vagrant-25-20170206.0.x86_64.vagrant-virtualbox.box'

@mock.patch('resultsdb_api.ResultsDBapi.create_result', return_value=True, autospec=True)
def test_failed(fake_create):
    """Test we get a properly submitted result for a failed test."""
    msg = Message(
        topic="org.fedoraproject.prod.autocloud.image.failed",
        body={
            "compose_id": "Fedora-Atomic-25-20170206.0",
            "compose_url": "http://kojipkgs.fedoraproject.org/compose/twoweek/Fedora-Atomic-25-20170206.0/compose/CloudImages/x86_64/images/Fedora-Atomic-Vagrant-25-20170206.0.x86_64.vagrant-virtualbox.box",
            "family": "Atomic",
            "image_name": "Fedora-Atomic-Vagrant-25-20170206.0",
            "job_id": 2023,
            "release": "25",
            "status": "failed",
            "type": "vagrant-virtualbox"
        },
    )
    CONSUMER(msg)
    assert fake_create.call_count == 1
    assert fake_create.call_args[1]['outcome'] == 'FAILED'

    fake_create.reset_mock()
    msg.topic = msg.topic.replace('.prod.', '.stg.')

    STGCONSUMER(msg)
    assert fake_create.call_count == 1
    assert fake_create.call_args[1]['outcome'] == 'FAILED'

@mock.patch('resultsdb_api.ResultsDBapi.create_result', return_value=True, autospec=True)
def test_other(fake_create):
    """Test we get a properly submitted result for some unexpected
    value. In fact if Autocloud adds more statuses we'll probably wind
    up with more fedmsg topics, but oh well.
    """
    msg = Message(
        topic="org.fedoraproject.prod.autocloud.image.failed",
        body={
            "compose_id": "Fedora-Atomic-25-20170206.0",
            "compose_url": "http://kojipkgs.fedoraproject.org/compose/twoweek/Fedora-Atomic-25-20170206.0/compose/CloudImages/x86_64/images/Fedora-Atomic-Vagrant-25-20170206.0.x86_64.vagrant-virtualbox.box",
            "family": "Atomic",
            "image_name": "Fedora-Atomic-Vagrant-25-20170206.0",
            "job_id": 2023,
            "release": "25",
            "status": "somethingelse",
            "type": "vagrant-virtualbox"
        },
    )
    CONSUMER(msg)
    assert fake_create.call_count == 1
    assert fake_create.call_args[1]['outcome'] == 'NEEDS_INSPECTION'

    fake_create.reset_mock()
    msg.topic = msg.topic.replace('.prod.', '.stg.')

    STGCONSUMER(msg)
    assert fake_create.call_count == 1
    assert fake_create.call_args[1]['outcome'] == 'NEEDS_INSPECTION'

# vim: set textwidth=100 ts=8 et sw=4:
