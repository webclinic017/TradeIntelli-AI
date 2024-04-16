from domain.trades_opportunity_scanner import TradesOpportunityScanner


class Alerts:

    @staticmethod
    def print_text(message):
        print(f"Alert: {message}")

    @staticmethod
    def run_alerts():
        print("running alerts:")
        res = TradesOpportunityScanner.scan_most_trades()
        print(f"TradesOpportunityScanner output: {res}")



