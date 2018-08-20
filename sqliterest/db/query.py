from table import Table, clause

class Query(object):
    """An object that represents a query"""

    def __init__(self, tables):
        self.names = ','.join(tables)
        self.tables = [Table(x) for x in tables]
        self.size = len(tables)
        self.last = self.tables[-1]
        self.joins = self.get_foreign_keys()

        if self.last.has_pk():
            self.joins.append(self.last.get_pk())

        self.sql_where = ' and '.join(self.joins)

    def get_foreign_keys(self):
        # input: array of Table objects
        # given a specific order of tables, represented by the array argument
        # determines if in that order there are foreign keys to make the joins.
        # If there are, an array of foreign keys is returned
        # If not, the requested join can't be made, so an error will be raised.
        retval = []

        for i in range(0, self.size - 1):
            lookahead = self.tables[i + 1].name
            if self.tables[i].has_ref(lookahead):
                retval.append(self.tables[i].get_fk(lookahead))
            else:
                # TODO raise an error here
                print('fk error!')

        return retval

class Select(Query):
    """An object that represents a select query"""

    def __init__(self, tables):
        super().__init__(tables)

    def __str__(self):
        if len(self.joins) > 0:
            sql = 'select {} from {} where {}'
        else:
            sql = 'select {} from {}'

        return sql.format(self.last.cols, self.names, self.sql_where)

class Delete(Query):
    """An object that represents a delete query"""

    def __init__(self, tables):
        super().__init__(tables)

    def __str__(self):
        if len(self.joins) > 0:
            sql = 'delete from {} where {}'
        else:
            sql = 'delete from {}'

        return sql.format(self.names, self.sql_where)

class Insert(Query):
    """An object that represents an insert query"""

    def __init__(self, tables, values):
        super().__init__(tables)
        self.values = values

    def __str__(self):
        return 'insert into {} ({}) values ({})'.format(self.names, self.last.cols.qmarks(), ','.join(self.values))

class Update(Query):
    """An object that represents an update query"""

    def __init__(self, tables, cols, values):
        super().__init__(tables)
        # with the update statement you can update a subset of the columns in the table
        self.cols = cols
        self.values = values

    def __str__(self):
        if len(self.joins) > 0:
            sql = 'update {} set {} where {}'
        else:
            sql = 'update {} set {}'

        updates = [clause(x,y) for x,y in zip(self.cols, self.values)]

        return sql.format(self.names, ','.join(updates), self.last.get_pk())

print (Select (['b']))
print (Select (['a', 'b', 'c']))
print (Delete (['b']))
print (Delete (['a', 'b', 'c']))
print (Insert (['a'], ['v1','v2','v3','v4']))
print (Update (['a'], ['col3', 'col4'], ['v1', 'v2']))
print (Update (['b'], ['col3'], ['v1']))