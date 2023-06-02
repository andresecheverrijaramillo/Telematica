from mrjob.job import MRJob
class AverageSalaryPerSececon(MRJob):

    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            sececon = filing[1]
            salary = float(filing[2])
            yield sececon, salary

    def reducer(self, key, values):
        total_salary = 0
        count = 0

        for salary in values:
            total_salary += salary
            count += 1

        average_salary = total_salary / count

        yield key, average_salary

class AverageSalaryPerEmployee(MRJob):

    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            idemp = filing[0]
            salary = float(filing[2])
            yield idemp, salary

    def reducer(self, key, values):
        total_salaries = 0
        count = 0

        for salary in values:
            total_salaries += salary
            count += 1

        yield key, total_salaries / count

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
    AverageSalaryPerSececon.run()
    AverageSalaryPerEmployee.run()
    SececonsByEmployee.run()