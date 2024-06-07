"""
Using ZAP SDK to perform initally scanning
"""
import time
import pprint

from aegis_scan.config import Config
from zapv2 import ZAPv2



class Scanner:
    """
    Class containing all initial scanning functions
    """
    def __init__(self) -> None:
        self.api_key = Config.ZAP_API_KEY

    def spider(self, zap: ZAPv2, target: str):
        """
        Function to use Spider Module against the target
        """
        scan_id = zap.spider.scan(target)
        while int(zap.spider.status(scanid=scan_id)) < 100:
            progress = zap.spider.status(scan_id)
            print(f"Spider Progress: {progress}")
            time.sleep(1)

        print("Scan Results")
        results = zap.spider.results(scanid=scan_id)

        return results

    def passive(self, zap: ZAPv2):
        """
        Function to use Passive Scan Module against the target
        """
        while int(zap.pscan.records_to_scan) > 0:
            print('Passive Scan:', zap.pscan.records_to_scan)
            time.sleep(2)

        hosts = ', '.join(zap.core.hosts)
        alerts = zap.core.alerts()

        print(f'Hosts: {hosts}')
        print('Alerts: ')
        pprint.pprint(alerts)

    def active(self, zap: ZAPv2, target: str):
        """
        Function to use Active Scan Module against the target
        """
        print(f"Running Active Scan on {target}")
        scan_id = zap.ascan.scan(target)

        while int(zap.ascan.status(scanid=scan_id)) < 100:
            progress = zap.ascan.status(scanid=scan_id)
            print(f'Scan Progress: {progress}')

            time.sleep(2)

        print('Alerts:')
        pprint.pprint(zap.core.alerts(baseurl=target))

    def init_scanner(self, target: str):
        """
        Initialize Scanner Service
        """
        zap = ZAPv2(apikey=self.api_key)

        targets_found = self.spider(zap=zap, target=target)
        # self.passive(zap=zap)
        
        for t in targets_found:
            self.active(zap=zap, target=t)


TARGET_URL = "https://public-firing-range.appspot.com/"
scanner = Scanner()
scanner.init_scanner(target=TARGET_URL)
