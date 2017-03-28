import logging
import requests
import bs4  # we use bs4 to parse the HTML page

from minemeld.ft.basepoller import BasePollerFT

LOG = logging.getLogger(__name__)


class Miner(BasePollerFT):
    def configure(self):
        super(Miner, self).configure()

        self.polling_timeout = self.config.get('polling_timeout', 3600)
        self.verify_cert = self.config.get('verify_cert', False)

        self.url = 'https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt'

    def _build_iterator(self, item):
        # builds the request and retrieves the page
        rkwargs = dict(
            stream=False,
            verify=self.verify_cert,
            timeout=self.polling_timeout
        )

        r = requests.get(
            self.url,
            **rkwargs
        )

        try:
            r.raise_for_status()
        except:
            LOG.debug('%s - exception in request: %s %s',
                      self.name, r.status_code, r.content)
            raise

        # parse the page
        con = r.text.decode('utf-8')
        lines = con.split("\n")
        result = []
        for s in lines:
            if s.startswith("#") == False:
                result.append(s)

        return result

    def _process_item(self, item):
        arr = item.split("\t")
        if len(arr) < 1:
            LOG.error('%s - no data-context-item-id attribute', self.name)
            return []

        indicator = arr[0]
        value = {
            'type': 'IPv4',
            'confidence': 50
        }

        return [[indicator, value]]
