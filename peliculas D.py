from mrjob.job import MRJob
class UsersPerMovieAndReviews(MRJob):
    def mapper(self, _, line):
        # Divide cada línea en campos separados por coma
        for w in line.split():
            filing = w.split(',')
            user= filing[0]
            movie= filing[1] 
            rating= filing[2]
            genre= filing[3]
            date= filing[4]
            yield movie, float(rating)

    def reducer(self, key, values):
        total_rating= 0
        count = 0

        for rating in values:
            total_rating += rating
            count += 1

        average_rating = total_rating / count

        yield key, (average_rating,count)

if __name__ == '__main__':
    UsersPerMovieAndReviews.run()