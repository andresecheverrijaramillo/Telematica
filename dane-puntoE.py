from mrjob.job import MRJob
from datetime import datetime

class StockAnalysis(MRJob):

    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            company = filing[0]
            price = float(filing[1])
            date = datetime.strptime(filing[2].strip(), '%Y-%m-%d')
            date_str = date.strftime('%Y-%m-%d')
            yield company, (date_str, price)

    def reducer(self, company, values):
        sorted_values = sorted(values, key=lambda x: x[0])
        previous_price = None
        has_increased = True

        for date, price in sorted_values:
            if previous_price is not None and price < previous_price:
                has_increased = False
                break

            previous_price = price

        if has_increased:
            yield company, 'Always increased or stable'

if __name__ == '__main__':
    StockAnalysis.run()