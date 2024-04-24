from domain.trades_opportunity_scanner import TradesOpportunityScanner


class Alerts:

    @staticmethod
    def print_text(message):
        print(f"Alert: {message}")

    @staticmethod
    def run_alerts():
        print("running alerts:")
        # TradesOpportunityScanner.scan_most_trades()



