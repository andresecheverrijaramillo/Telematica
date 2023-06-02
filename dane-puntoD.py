from mrjob.job import MRJob

class MinMaxStockPrice(MRJob):
    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            yield filing[0],(float(filing[1]), filing[2])
    
    def reducer(self, key, values):
        prices = list(values)
        min_price = min(prices)
        max_price = max(prices)
        yield key, (min_price[1],max_price[1])

if __name__ == '__main__':
    MinMaxStockPrice.run()