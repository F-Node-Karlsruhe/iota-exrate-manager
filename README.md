# iota-exrate-manager
Python package that keeps track of iota exchange rates via various APIs and converts prices.

## Install
```
pip install iota-exrate-manager
```

## Usage
```python
from iota_exrate_manager import ExRateManager
import time

# default currency is usd and the default refresh period is 60 seconds
em = ExRateManager()

# give time to fetch
time.sleep(5)

# convert iota to fiat (default first currency in currencies -> usd if not specified)
ipf = em.iota_to_fiat(1_000_000)

# convert fiat to iota
em.fiat_to_iota(ipf))
```
