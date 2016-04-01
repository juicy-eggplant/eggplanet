_SEVERITY = {'Low': 0, 'Medium': 1, 'High': 2}
_M = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'June',
      '07': 'July', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}


class Catagory(object):
    def __init__(self):
        self.period = Period()
        self.vendor = {}

    def handler(self, date, severity, vendors):
        self.period.handler(date, severity)
        for v in vendors:
            self.vendor[v] = self.vendor.get(v, Company(v))
            for p in vendors[v]:
                self.vendor[v].handler(p, severity, date)

    def simple_data_pack_time(self):
        return self.period.general_summary()

    def simple_data_pack_company(self):
        return self.vendor

    def simple_data_pack_specific_company(self, c):
        assert c in self.vendor
        return self.vendor[c]

    def simple_data_pack_specific_product(self, c, p):
        assert c in self.vendor
        return self.vendor[c].specific_product_summary(p)

    def simple_data_pack_timeO_company(self, c):
        assert c in self.vendor
        return self.vendor[c].period.general_summary()

    def simple_data_pack_timeO_product(self, c, p):
        assert c in self.vendor
        return self.vendor[c].specific_product_time_summary(p)

    

class Period(object):
    def __init__(self, name=None):
        self.name = name
        self.total = 0
        self.year = {}
        self.general_month = {}  # month of all YEAR object in this Period object
        self.date = {}

    def __name__(self):
        return self.name

    def __iter__(self):
        return self.year.iterkeys()

    def handler(self, date, severity):
        year, mon, day = tuple(date.split('-'))

        self.total += 1

        s = _SEVERITY[severity]
        self.date[date] = self.date.get(date, [0, 0, 0])
        self.date[date][s] += 1

        m = _M[mon]
        self.general_month[m] = self.general_month.get(m, [0, 0, 0])
        self.general_month[m][s] += 1

        self.year[year] = self.year.get(year, Year(year, self.name))
        self.year[year].handler(mon, day, severity)

    def __str__(self):
        res = ''
        if self.name:
            res += '%s: \n'%self.name 
        for y in self.general_summary():
            res += str(y)
        return res

    def general_summary(self):
        'Total number of vulnerabilities of each year, number of vulnerabilities in each severity period,\
        Total number of vulnerabilities of each month, number of vulnerabilities in each severity period'
        for y in self.year:
            yield self.year[y]

    def year_summary(self, y):
        assert y in self.year
        return self.year[y]

    def general_month_summary(self, m):
        assert m in _M
        m = _M[m]
        return sum(self.general_month[m]), self.general_month[m]

    def daily_summary(self, d):
        assert d in self.date
        return sum(self.date[d]), self.date[d]


class Year(object):
    def __init__(self, year, name=None):
        self.name = name
        self.total = 0
        self.severity = [0, 0, 0]
        self.year = year
        self.month = {}

    def __name__(self):
        return self.name

    def __str__(self):
        title = "Year: %s --- Total: %d, Severity: \
[Low: %d, Medium: %d, High: %d]\n\n" % (self.year, self.total,
                                        self.severity[0],
                                        self.severity[1],
                                        self.severity[2])
        if self.name:
            title = "%s: \n"%self.name + title
        arr = sorted(self.month)
        body = ""
        for m in arr:
            body += "%s\n" % str(self.month[m])
        return title + body

    def handler(self, m, d, severity):
        self.total += 1
        s = _SEVERITY[severity]
        self.severity[s] += 1

        self.month[m] = self.month.get(m, Month(m, self.name))
        self.month[m].handler(d, severity)


class Month(object):
    def __init__(self, month, name=None):
        self.name = name
        self.total = 0
        self.month = month
        self.days = {}
        self.severity = [0, 0, 0]

    def __name__(self):
        return self.name

    def __str__(self):
        return "%s --- Total: %d, Severity: [Low: %d, Medium: %d, High: %d]" % (
            _M[self.month], self.total, self.severity[0],
            self.severity[1], self.severity[2])

    def handler(self, d, severity):
        s = _SEVERITY[severity]
        self.total += 1
        self.severity[s] += 1

        self.days[d] = self.days.get(d, Day(d, self.name))
        self.days[d].handler(severity)


class Day(object):
    def __init__(self, day, name=None):
        self.name = name
        self.total = 0
        self.day = day
        self.severity = [0, 0, 0]

    def __name__(self):
        return self.name

    def handler(self, severity):
        s = _SEVERITY[severity]
        self.total += 1
        self.severity[s] += 1


class Company(object):
    def __init__(self, name):
        self.vendor = name
        self.prod = {}
        self.total = 0
        self.severity = [0, 0, 0]
        self.period = Period(self.vendor.capitalize())

    def handler(self, p, severity, date):
        s = _SEVERITY[severity]
        self.total += 1
        self.severity[s] += 1
        self.period.handler(date, severity)

        self.prod[p] = self.prod.get(p, Product(p, self.__name__()))
        self.prod[p].handler(date, severity)

    def __name__(self):
        return self.vendor.capitalize()

    def __len__(self):
        return len(self.prod)

    def __iter__(self):
        return self.prod.iterkeys()

    def __str__(self):
        res = 'Company Name: %s,\n\
Number of vulnerabilities: %d,\n\
Severity [Low: %d, Medium: %d, High: %d],\n\
Number of products: %d,\n\
    PRODUCTS:\n' % (self.__name__().capitalize(),
                    self.total, self.severity[0],
                    self.severity[1],
                    self.severity[2], len(self))
        for p in self.prod:
            res += '             %s;\n' % (self.prod[p])
        return res

    def general_summary(self):
        '''
        Number of vulnerabilities
        Number of vulnerabilities in each severity period
        Number of products
        '''
        return self.total, self.severity, len(self), self.prod

    def time_oriented_summary(self):
        return self.period

    def specific_product_summary(self, p):
        '''Name of Product,
           Total number of vulnerabilities,
           Number of vulnerabilities in each severity period,
           '''
        assert p in self.prod
        return self.prod[p].general_summary()

    def specific_product_time_summary(self, p):
        assert p in self.prod
        return self.prod[p].time_oriented_summary()


class Product(object):
    def __init__(self, prod, vendor):
        self.prod = prod
        self.fullname = "%s's %s"%(vendor, prod.capitalize())
        self.total = 0
        self.severity = [0, 0, 0]
        self.period = Period(self.fullname)

    def __name__(self):
        return self.prod.capitalize()

    def __str__(self):
        return '%s, \
Total number of vulnerabilities: %d, \
Severity [Low: %d, Medium: %d, High: %d]' % (self.fullname,
                                             self.total,
                                             self.severity[0],
                                             self.severity[1],
                                             self.severity[2])

    def handler(self, date, severity):
        s = _SEVERITY[severity]
        self.total += 1
        self.severity[s] += 1
        self.period.handler(date, severity)

    def general_summary(self):
        '''Name of Product,
           Total number of vulnerabilities,
           Number of vulnerabilities in each severity period,
           '''
        return self.prod, self.total, self.severity

    def time_oriented_summary(self):
        return self.period.general_summary()
