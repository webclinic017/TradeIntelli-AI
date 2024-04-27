from domain.models.configuration import SessionLocal, Configuration
from domain.trades_opportunity_scanner import TradesOpportunityScanner


class Alerts:

    @staticmethod
    def print_text(message):
        print(f"Alert: {message}")

    @staticmethod
    def run_alerts():
        print("running alerts:")
        db = SessionLocal()
        config = db.query(Configuration).filter(Configuration.id == 1).first()
        if config:
            print(f"run_check: {config.run_check}")
            if config.run_check:
                TradesOpportunityScanner.scan_most_trades()
        db.close()




