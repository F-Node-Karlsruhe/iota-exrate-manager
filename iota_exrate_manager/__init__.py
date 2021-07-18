from .apis import cmc
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

        print('refreshing')
        
        if 'coinmarketcap' in self._apis:

            cmc_exrates = apis.cmc(self._currencies, self._cmc_api_key)

            if cmc_exrates:

                self.__update_exrates(cmc_exrates)

                return

        # use coingecko as default   
        cg_exrates = apis.coingecko(self._currencies)

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

        if self._last_updated:

            return datetime.utcnow() < self._last_updated + timedelta(minutes=self._delay_threshold)

        return False


    def iota_to_fiat(self, amount, currency=None, decimal_digits=2):

        if currency is None:

            currency = self._currencies[0]

        if not self.up_to_date():

            warnings.warn('Exchange rates are not up to date. Last updated %s' % self._last_updated)

        return round(self._ex_rates[currency] * amount / 1_000_000, decimal_digits)


    def fiat_to_iota(self, amount, currency=None):

        if currency is None:

            currency = self._currencies[0]

        if not self.up_to_date():

            warnings.warn('Exchange rates are not up to date. Last updated %s' % self._last_updated)

        return int(amount / self._ex_rates[currency] * 1_000_000)

