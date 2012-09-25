from Oracle    import Oracle
from sqlDecorators import decorateSQL

class Table(Oracle):
    __metaclass__ = decorateSQL()

    def __init__(self, schema = 'MEU_APNT_V6', table = 'TBL_COMUNIDADE'):
        self.tableAlias  = {'thisTable': '{schema}.{table}'.format(**locals())}
        self.tableAlias.update(self._tableAlias())
        self.sqlPatterns = self._sqlPatterns()

    def _sqlPatterns(self):
        return {}

    def _tableAlias(self):
        return {}

    def queryAll(self):
        return """
        select * from {thisTable}
        """
