from mrjob.job import MRJob
from mrjob.step import MRStep

class DayLowestRating(MRJob):
    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            user = filing[0]
            movie = filing[1] 
            rating = filing[2]
            genre = filing[3]
            date = filing[4]
            yield date, float(rating)

    def reducer(self, key, values):
        total_rating = 0
        count = 0

        for rating in values:
            total_rating += rating
            count += 1

        average_rating = total_rating / count

        yield None, (average_rating, key)  # Yield average rating and date

    def find_lowest_average_rating(self, _, values):
        min_average_rating = float('inf')
        min_date = None

        for average_rating, date in values:
            if average_rating < min_average_rating:
                min_average_rating = average_rating
                min_date = date

        yield min_date, min_average_rating

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.find_lowest_average_rating)
        ]

if __name__ == '__main__':
    DayLowestRating.run()
