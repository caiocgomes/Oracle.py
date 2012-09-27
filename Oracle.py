import cx_Oracle
from credentials import user, pwd, host, service

class Oracle(object):
    def __init__(self, user=user, passwd=pwd, host=host, service=service):
        args = {'user':user, 'passwd': passwd, 'host': host, 'service': service}
        connstring = '{user}/{passwd}@{host}/{service}'.format(**args)
        self.con    = cx_Oracle.connect(connstring)

    def query(self, querystring):
        cursor = cx_Oracle.Cursor(self.con)
        cursor.execute(querystring)
        return cursor

    def fetchOne(self, querystring):
        cursor = self.query(querystring)
        return cursor.fetchone()

    def callProcedure(self, procname, *args):
        cursor = cx_Oracle.Cursor(self.con)
        cursor.callproc(procname, args)


