from Oracle    import Oracle
from Util import decorateSQL

class Table(Oracle):
    """ This class is a base class for abstractions of Oracle tables.

    When you inherit from this class, all methods starting with 'query' will be transformed in queries that execute the query string returned by the original method and return a cx_Oracle iterable cursor for the result. All methods starting with 'get' will be transformed in queries that fetch exactly one result based on the query string returned by it. 

    All methods decorated with @dontDecorate won't be altered.

    Also, formatting patterns like {blabla} will be substituted by values of 'blabla' fields contained in either: 
        1) the dictionary returned by the methods Table._sqlPatterns() or Table._tableAlias(),
        2) the keyword arguments of the method,
        3) {thisTable} is always substituted by {schema}.{table} getting this values from the dictionary returned by Table._names()
    """
    __metaclass__ = decorateSQL()

    def __init__(self):
        Oracle.__init__(self)
        names = self._names()
        self.tableAlias  = {'thisTable': '{schema}.{table}'.format(**names)}
        self.tableAlias.update(self._tableAlias())
        self.sqlPatterns = self._sqlPatterns()

    def _names(self):
        return {'schema': 'schemaName',
                'table': 'tableName'}

    def _sqlPatterns(self):
        return {}

    def _tableAlias(self):
        return {}

    def queryAll(self):
        return """
        select * from {thisTable}
        """


class Comunidade(Table):
    def _names(self):
        return {'schema': 'meu_apnt_v6', 'table': 'tbl_comunidade'}

    def getName(self, lbsid = ''):
        return """
        select titulo from {thisTable} where lbs_id = '{lbsid}'
        """
