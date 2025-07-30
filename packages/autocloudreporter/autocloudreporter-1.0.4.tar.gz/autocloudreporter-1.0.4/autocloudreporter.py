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

"""fedora-messaging consumer to report Autocloud results to ResultsDB."""

import logging

import fedora_messaging.exceptions
import fedora_messaging.config
from resultsdb_api import ResultsDBapi, ResultsDBapiException
from resultsdb_conventions.fedora import FedoraImageResult

__version__ = "1.0.4"


class AutocloudReporter(object):
    """A fedmsg consumer that consumes Autocloud test results and
    produces ResultsDB results. Listens for production Autocloud
    fedmsgs and reports to the production ResultsDB.
    """
    def __init__(self):
        self.autocloud_url = fedora_messaging.config.conf["consumer_config"]["autocloud_url"]
        self.resultsdb_url = fedora_messaging.config.conf["consumer_config"]["resultsdb_url"]
        self.logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, message):
        """Consume incoming message."""
        rdb_instance = ResultsDBapi(self.resultsdb_url)
        try:
            job_id = message.body['job_id']
            cid = message.body['compose_id']
            # bit lazy, assumes no queries
            filename = message.body['compose_url'].split('/')[-1]
            outcome = {'success': "PASSED", 'failed': "FAILED"}.get(
                message.body['status'], 'NEEDS_INSPECTION')
        except KeyError:
            self.logger.error("Essential information missing from message %s!",
                              message.id)
            return

        self.logger.info("Reporting for %s job %s...", cid, job_id)
        try:
            res = FedoraImageResult(
                cid=cid,
                filename=filename,
                outcome=outcome,
                tc_name='compose.cloud.all',
                ref_url="{0}/jobs/{1}/output".format(self.autocloud_url, job_id),
                tc_url='https://github.com/kushaldas/autocloud/',
                note='',
                source='autocloud'
            )
            res.report(rdb_instance)
        except ValueError as err:
            if "Can't find image" in str(err):
                # happens if we're reporting a stale result for some
                # reason
                self.logger.error("Can't construct result! Compose probably garbage collected")
                raise fedora_messaging.exceptions.Drop
            else:
                raise
        # note: the above raises an exception if any error occurs,
        # if it does not raise, we can assume reporting worked
        self.logger.info("Reporting for %s job %s complete", cid, job_id)

# vim: set textwidth=100 ts=8 et sw=4:
