from mrjob.job import MRJob

class SececonsByEmployee(MRJob):

    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            idemp = filing[0]
            sececon = filing[1]
            yield idemp, sececon

    def reducer(self, key, values):
        unique_sececons = set(values)
        yield key, len(unique_sececons)

if __name__ == '__main__':
    SececonsByEmployee.run()