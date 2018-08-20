import parser

prefix = lambda x, y: x + '.' + y
clause = lambda x, y: x + '=' + y

class Key(object):
    """A set of columns that belong to a table"""

    def __init__(self, table, cols):
        self.cols = [prefix(table, x) for x in cols]
        self.table = table

    def __str__(self):
        return ','.join(self.cols)

    def qmarks(self):
        return ','.join(['?' for x in self.cols])

class Primary(Key):
    """A set of columns that define the primary key of a table"""

    def __init__(self, table, cols):
        super().__init__(table, cols)

    def __str__(self):
        return ' and '.join([clause(x, '?') for x in self.cols])

class Foreign(Key):
    """A set of columns that reference the primary key of another table"""

    def __init__(self, table, cols, ref, ref_cols):
        super().__init__(table, cols)
        self.ref = ref
        self.ref_cols = [prefix(ref, x) for x in ref_cols]

    def __str__(self):
        return ' and '.join([clause(x, y) for x,y in zip(self.cols, self.ref_cols)])

class Table:
    """An object containing a table definition"""

    def __init__(self, name):
        data = parser.analyze(name)
        self.name = name
        self.cols = Key(name, data['cols'])

        if len(data['primary']) > 0:
            self.primary = Primary(name, data['primary'][0])
        else:
            self.primary = None

        self.foreign = [Foreign(name, x['cols'], x['ref'], x['ref_cols']) for x in data['foreign']]
        self.refs = [x['ref'] for x in data['foreign']]

    def has_pk(self):
        return self.primary != None

    def get_pk(self):
        if self.has_pk():
            return str(self.primary)
        else:
            return None

    def has_fk(self):
        return len(self.foreign) > 0

    def get_fk(self, table):
        fk = [str(x) for x in self.foreign if x.ref == table]

        if len(fk) > 0:
            return fk[0]
        else:
            return None

    def has_ref(self, table):
        return table in self.refs
