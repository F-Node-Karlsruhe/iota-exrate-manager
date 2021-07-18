from iota_exrate_manager import ExRateManager
import time

em = ExRateManager()

time.sleep(5)

ipf = em.iota_to_fiat(1000000)

print(ipf)

time.sleep(20)

print(em.fiat_to_iota(ipf))
