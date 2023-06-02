from mrjob.job import MRJob
from mrjob.step import MRStep
class DayLessviews(MRJob):

    def mapper(self, _, line):
        # Divide cada línea en campos separados por coma
        for w in line.split():
            filing = w.split(',')
            user = filing[0]
            movie = filing[1]
            rating = filing[2]
            genre = filing[3]
            date = filing[4]
            yield date, 1

    def reducer(self, key, values):
        views = sum(values)
        yield None, (views, key)

    def find_min_views(self, _, views_and_dates):
        min_views = float('inf')
        min_date = None
        for views, date in views_and_dates:
            if views < min_views:
                min_views = views
                min_date = date
        yield min_date, min_views

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.find_min_views)
        ]

if __name__ == '__main__':
    DayLessviews.run()