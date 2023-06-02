from mrjob.job import MRJob
from mrjob.step import MRStep
class DayMoreviews(MRJob):


    def mapper(self, _, line):
        # Divide cada línea en campos separados por coma
        for w in line.split():
            filing = w.split(',')
            user= filing[0]
            movie= filing[1] 
            rating= filing[2]
            genre= filing[3]
            date= filing[4]
            yield date, 1

    def reducer(self, key, values):
        views = sum(values)
        yield None, (views, key)

    def find_max_views(self, _, views_and_dates):
        max_views = 0
        max_date = None
        for view_date in views_and_dates:
            views, date = view_date
            if views > max_views:
                max_views = views
                max_date = date
        yield max_date, max_views

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.find_max_views)
        ]

if __name__ == '__main__':
    DayMoreviews.run()
