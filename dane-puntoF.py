from mrjob.job import MRJob
from mrjob.step import MRStep
class DiaNegro(MRJob):

    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            yield filing[0], (float(filing[1]), filing[2])

    def reducer(self, key, values):
        prices = list(values)
        min_price = min(prices, key=lambda x: x[0])
        yield min_price[1], 1

    def find_day_with_lowest_prices(self, key, values):
        count = sum(values)
        max_counter = 0
        max_day = None

        if count > max_counter:
            max_counter = count
            max_day = key

        yield None, (max_day, max_counter) 

    def find_max_day(self, _, pairs):
        max_day = None
        max_counter = 0

        for day, counter in pairs:
            if counter > max_counter:
                max_counter = counter
                max_day = day

        yield max_day, max_counter

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.find_day_with_lowest_prices),
            MRStep(reducer=self.find_max_day)
        ]

if __name__ == '__main__':
    DiaNegro.run()