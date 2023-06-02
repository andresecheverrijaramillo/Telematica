from mrjob.job import MRJob

class LowestAndHighestByGenre(MRJob):
    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            user = filing[0]
            movie = filing[1] 
            rating = filing[2]
            genre = filing[3]
            date = filing[4]
            yield genre, (float(rating), movie)

    def reducer(self, key, values):
        ratings = list(values)
        min_rating = min(ratings)
        max_rating = max(ratings)
        yield key, (min_rating[1],max_rating[1])

if __name__ == '__main__':
    LowestAndHighestByGenre.run()
