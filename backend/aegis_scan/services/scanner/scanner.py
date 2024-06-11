"""
Using ZAP SDK to perform initally scanning
"""
import time

from aegis_scan.config import Config
from aegis_scan import db
from aegis_scan.models.models import Scan
from zapv2 import ZAPv2



class Scanner:
    """
    Class containing all initial scanning functions
    """
    def __init__(self) -> None:
        self.api_key = Config.ZAP_API_KEY

    def spider_scan(self, zap: ZAPv2, target: str):
        """
        Function to use Spider Module against the target
        """
        scan_id = zap.spider.scan(target)
        
        return scan_id
    
    def active_scan(self, zap: ZAPv2, target: str):
        """
        Function to use Active Scan Module against the target
        """
        scan_id = zap.ascan.scan(target)

        return scan_id

    def passive_scan(self, zap: ZAPv2):
        """
        Function to use Passive Scan Module against the target
        """
        while int(zap.pscan.records_to_scan) > 0:
            print('Passive Scan:', zap.pscan.records_to_scan)
            time.sleep(2)

        alerts = zap.core.alerts()

        return alerts
    
    def get_spider_status(self, scan_id: str, scan):
        """
        Get Spider Scan Progress
        """
        zap = ZAPv2(apikey=self.api_key)
        status = int(zap.spider.status(scanid=scan_id))

        if status == 'does_not_exist':
            db.session.delete(scan)
            db.session.commit()
        else:
            if status == 100:
                scan.status = "Spider Completed"
                db.session.commit()
            else:
                scan.status = "Spider In-Progress"
                db.session.commit()

        return scan.status
    
    def get_spider_results(self, zap: ZAPv2, scan_id: str):
        """
        Get Spider Scan Resulst
        """
        results = zap.spider.results(scanid=scan_id)

        return results

    def init_scanner(self, target: str, user_id: str):
        """
        Initialize Scanner Service
        """
        zap = ZAPv2(apikey=self.api_key)
        
        last_scan_id = db.session.query(Scan).count() + 1
        scan_id = f"SCAN{last_scan_id:04d}"

        scan = Scan(scan_id=scan_id, url=target, scan_type="Web", status="Running", user_id=user_id)
        db.session.add(scan)
        db.session.commit()

        spider_scan_id = self.spider_scan(zap=zap, target=target)

        scan.spider_scan_id = spider_scan_id
        db.session.commit()
