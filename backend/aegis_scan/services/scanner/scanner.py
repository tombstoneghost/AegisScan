"""
Using ZAP SDK to perform initally scanning
"""
import json
import time

import requests

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
        self.completed_active_scan = []
        self.passive_scan_status = "Running"

    def spider_scan(self, zap: ZAPv2, target: str):
        """
        Function to use Spider Module against the target
        """
        # zap.spider.set_option_max_depth(5)
        scan_id = zap.ajaxSpider.scan(target)
        
        return scan_id
    
    def active_scan(self, zap: ZAPv2, target: str):
        """
        Function to use Active Scan Module against the target
        """
        spider_scan_id = self.spider_scan(zap=zap, target=target)
        while int(zap.ajaxSpider.status()) < 100:
            pass

        print("AScan", target)
        scan_id = zap.ascan.scan(target)
        print("ScanID", scan_id)

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
    
    def get_spider_status(self, scan_id: str, scan, zap: ZAPv2):
        """
        Get Spider Scan Progress
        """
        status = zap.ajaxSpider.status

        if status == 'does_not_exist':
            status = "Failed"
            scan.status = status
            db.session.commit()
        else:
            if status == "stopped":
                result = self.get_spider_results(zap=zap)
                result = json.dumps(result)

                scan.result = result
                scan.status = "Spider Completed"
                db.session.commit()
            else:
                scan.status = "Spider In-Progress"
                db.session.commit()

        return scan.status, status

    def get_active_status(self, scan_id: str, zap: ZAPv2, scan):
        """
        Get Active Scan Progress
        """
        status = zap.ascan.status(scanid=scan_id)

        if status == 'does_not_exist':
            status = "Failed"
            scan.status = status
            db.session.commit()
            return 0

        return int(status)

    def clear_passive_queue(self):
        """
        Clear Passive Scan Queue
        """
        try:
            res = requests.get('http://127.0.0.1:8080/JSON/pscan/action/clearQueue/', headers={
                'Accept': 'application/json'
            }, timeout=30)

            print(res.json())
        except Exception as e:
            print("[!] Unable to clear passive queue")
            print(e)

    def run_passive_scan(self, zap: ZAPv2, target: str):
        """
        Initiate Passive Scan
        """
        self.clear_passive_queue()

        self.passive_scan_status = "Passive In-Progress"

        self.spider_scan(zap=zap, target=target)

        alerts = self.passive_scan(zap=zap)

        self.passive_scan_status = "Passive Completed"

        return json.dumps(alerts)

    def run_active_scan(self, zap: ZAPv2, targets: list, scan):
        """
        Initiate Active Scan on all the targets found from spider.
        """
        active_scan_ids = []

        print("Targets", targets)

        for t in targets:
            print("t", t)
            scan_id = self.active_scan(zap=zap, target=t)
            active_scan_ids.append(scan_id)

        active_scan_ids = ",".join(active_scan_ids)

        scan.active_scan_id = active_scan_ids

    
    def get_scan_status(self, scan_id: str, scan):
        """
        Check complete scan status
        """
        zap = ZAPv2(apikey=self.api_key)
 
        # Get current status
        status = scan.status
        progress = 0

        # Get scan type
        scan_type = scan.scan_type

        if scan_type == 'spider':
            if "Running" in status:
                # Check for Spider Scan Status
                status, progress = self.get_spider_status(scan_id=scan_id, scan=scan, zap=zap)

            if 'Spider In-Progress' in status:
                # Check for Spider Scan Status
                status, progress = self.get_spider_status(scan_id=scan_id, scan=scan, zap=zap)

            if "Spider Completed" in status:
                spider_results = self.get_spider_results(zap=zap)

                spider_results = json.dumps(spider_results)

                scan.spider_result = spider_results
        
        if scan_type == 'active':
            if "Running Active Scan" in status:
                active_scan_ids = str(scan.active_scan_id)
                active_scan_ids = active_scan_ids.split(",")

                for sid in active_scan_ids:
                    scan_status = self.get_active_status(scan_id=sid, zap=zap, scan=scan)
                    progress = scan_status
                    print("Scan Status: ", sid, scan_status)
                    if scan_status == 100:
                        self.completed_active_scan.append(scan_id)
                        active_result = self.get_active_results(zap=zap, scan_id=sid)
                        if scan.result is not None:
                            scan.result = scan.result + "$#$" + json.dumps(active_result)
                        else:
                            scan.result = json.dumps(active_result)
                        db.session.commit()

                if len(self.completed_active_scan) == len(active_scan_ids):
                    status = "Active Scan Completed"
                    scan.status = status
                    db.session.commit()

            if "Active Scan Completed" in status:
                return status, progress
            
        if scan_type == 'passive':
            status = self.passive_scan_status
            scan.status = status
            if "Completed" not in status:
                progress = 50
            else:
                progress = 100
            db.session.commit()
        
        return status, progress
          
    def get_spider_results(self, zap: ZAPv2):
        """
        Get Spider Scan Results
        """
        results = zap.ajaxSpider.results()

        return results
    
    def get_active_results(self, zap: ZAPv2, scan_id: str):
        """
        Get Active Scan Result for a scan_id
        """
        alerts = zap.core.alerts()

        return alerts

    def init_scanner(self, target: str, user_id: str, scan_type: str):
        """
        Initialize Scanner Service
        """
        zap = ZAPv2(apikey=self.api_key)
        
        last_scan = db.session.query(Scan).order_by(Scan.id.desc()).first()
        last_scan_id = int(str(getattr(last_scan, "scan_id")).split("SCAN")[1]) + 1

        scan_id = f"SCAN{last_scan_id:04d}"

        scan = Scan(scan_id=scan_id, url=target, scan_type=scan_type, target_type="Web", status="Running", user_id=user_id)
        db.session.add(scan)
        db.session.commit()

        if scan_type == "spider":
            spider_scan_id = self.spider_scan(zap=zap, target=target)
            scan.spider_scan_id = spider_scan_id
            db.session.commit()
        
        if scan_type == 'active':
            print("Target", target)
            self.run_active_scan(scan=scan, targets=[target], zap=zap)

            status = "Running Active Scan"
            scan.status = status
            db.session.commit()

        if scan_type == 'passive':
            alerts = self.run_passive_scan(zap=zap, target=target)
            scan.result = alerts
            scan.status = "Passive Completed"
            db.session.commit()
