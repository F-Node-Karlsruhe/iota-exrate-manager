"""
iota-exrate-manager
Python package that keeps track of iota prices via various APIs and converts prices.
"""

__version__ = "0.1.0"
__author__ = 'F-Node-Karlsruhe'

from .apis import coingecko, cmc
from datetime import datetime, timedelta
import sched
import time
import warnings
import threading

SUPPORTED_CURRENCIES = {'usd', 'eur', 'gbp', 'jpy', 'chf', 'cad'}

class ExRateManager:

    _ex_rates = {}

    _apis = {'coinmarketcap', 'coingecko'}

    _last_updated = None

    """Create a ExRateManager.
    :param refresh_rate: Refresh rate in seconds.
                         Default 60
    :param delay_threshold: After which time without a successful refresh a warning is emitted
                            in minutes.
                            Default 5
    :param currencies: List of currencies quotes for iota which are fetched.
                       Default ['usd']
    :param cmc_api_key: The coinmarketcap API key to fetch the cmc API.
                        Default None
    """

    def __init__(self,
                refresh_rate=60,
                delay_threshold=5,
                currencies=['usd'],
                cmc_api_key=None):

        for currency in currencies:

            if currency not in SUPPORTED_CURRENCIES:

                raise Exception('Currency %s not supported' % currency)

        self._currencies = currencies

        if cmc_api_key is None:

            self._apis.remove('coinmarketcap')

        else:

            self._cmc_api_key = cmc_api_key

        self._scheduler = sched.scheduler(time.time, time.sleep)

        self._refresh_rate = refresh_rate

        self._delay_threshold = delay_threshold

        # run refresh as a deamon thread
        thread = threading.Thread(target=self.__refresh)
        thread.daemon = True
        thread.start()



    def __refresh(self):
        
        if 'coinmarketcap' in self._apis:

            cmc_exrates = cmc(self._currencies, self._cmc_api_key)

            if cmc_exrates:

                self.__update_exrates(cmc_exrates)

                return

        # use coingecko as default   
        cg_exrates = coingecko(self._currencies)

        if cg_exrates:

            self.__update_exrates(cg_exrates)

            return

        # schedule new try even if both fail
        self._scheduler.enter(self._refresh_rate, 1, self.__refresh)

        self._scheduler.run()



    def __update_exrates(self, update):

        self._ex_rates.update(update)

        self._last_updated = datetime.utcnow()

        # schedule new refresh run
        self._scheduler.enter(self._refresh_rate, 1, self.__refresh)

        self._scheduler.run()



    def up_to_date(self):
        '''
        Returns true if the last update was not longer ago than the specified threshold
        '''

        if self._last_updated:

            return datetime.utcnow() < self._last_updated + timedelta(minutes=self._delay_threshold)

        return False


    def iota_to_fiat(self, amount, currency=None, decimal_digits=2):
        '''
        Converts an iota amount into the requested currency
        '''

        if currency is None:

            currency = self._currencies[0]

        if not self.up_to_date():

            warnings.warn('Exchange rates are not up to date. Last updated %s' % self._last_updated)

        return round(self._ex_rates[currency] * amount / 1_000_000, decimal_digits)


    def fiat_to_iota(self, amount, currency=None):
        '''
        Converts an amount of the specified currency into iota
        '''

        if currency is None:

            currency = self._currencies[0]

        if not self.up_to_date():

            warnings.warn('Exchange rates are not up to date. Last updated %s' % self._last_updated)

        return int(amount / self._ex_rates[currency] * 1_000_000)

