from mrjob.job import MRJob
class MovieRatingStatistics(MRJob):


    def mapper(self, _, line):
        # Divide cada línea en campos separados por coma
        for w in line.split():
            filing = w.split(',')
            user= filing[0] 
            rating= filing[2]
            yield user, float(rating)

    def reducer(self, key, values):
        total_rating= 0
        count = 0

        for rating in values:
            total_rating += rating
            count += 1

        average_rating = total_rating / count

        yield key, (average_rating,count)
if __name__ == '__main__':
    MovieRatingStatistics.run()
