import MySQLdb

class DBConnError(Exception):
    '''
    '''
    pass

class DomainDelError(Exception):
    '''
    '''
    pass


class DataBase(object):

    def __init__(self, host, user, passwd, dbname):
        '''
        '''
        self.boolToStr = {False: 'false', True: 'true'}

        try:
            self.connection = MySQLdb.connect(host, user, passwd, dbname)
            self.cursor = self.connection.cursor()
        
        except MySQLdb.OperationalError:
            raise DBConnError
            

    def __del__(self):
        '''
        '''
        self.connection.commit()
        self.connection.close()


    def isDomain(self, domain):
        '''
        '''
        sql = "SELECT * FROM `domain` WHERE `name` = '{}'".format(domain)
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def isAddress(self, address):
        '''
        '''
        sql = "SELECT * FROM `virtual_user` WHERE `address` = '{}'".format(address)
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def insertDomain(self, domain, relay=True):
        '''
        '''
        sql = ("INSERT INTO `domain`(name, relay) VALUES('{}', {})"
               "".format(domain, self.boolToStr[relay])
              )

        self.cursor.execute(sql)
        self.connection.commit()

    def deleteDomain(self, domain):
        '''
        '''
        try:
            sql = ("DELETE FROM `domain` WHERE name = '{}'".format(domain))
            self.cursor.execute(sql)
            self.connection.commit()
        except MySQLdb.IntegrityError:
            raise DomainDelError


    def insertUser(self, comment, address, hashedPassword, maildir, quota=0, active=True, imap=True, pop3=True):
        '''
        '''
        domain = address.split('@')[1]
        sql = "SELECT id FROM `domain` WHERE `name` = '{}'".format(domain)
        self.cursor.execute(sql)
        domain_id = self.cursor.fetchone()[0]
        sql = ("INSERT INTO `virtual_user`(domain_id, comment, address, pass, maildir, quota, active, allow_imap, allow_pop3) "
               "VALUES({}, '{}', '{}', '{}', '{}', {}, {}, {}, {})".format(domain_id, comment, address, hashedPassword, maildir, quota,
               self.boolToStr[active], self.boolToStr[imap], self.boolToStr[pop3]))
        self.cursor.execute(sql)
        self.connection.commit()


    def deleteUser(self, address):
        '''
        '''
        sql = ("DELETE FROM `virtual_user` WHERE address = '{}'".format(address))
        self.cursor.execute(sql)
        self.connection.commit()

    def modPassword(self, address, password):
        '''
        '''
        sql = ("UPDATE `virtual_user` SET pass='{}' where address='{}'".format(password,address))
        self.cursor.execute(sql)
        self.connection.commit()

    def modQuota(self, address, quota):
        '''
        '''
        sql = ("UPDATE `virtual_user` SET quota={} where address='{}'".format(quota,address))
        self.cursor.execute(sql)
        self.connection.commit()

    def getAlias(self, recipient):
        '''
        '''
        sql = ("SELECT destination FROM `virtual_alias_map` WHERE recipient = '{}'".format(recipient))
        if self.cursor.execute(sql):
            alias = self.cursor.fetchone()[0]
            return alias
        else:
            return False

    def getAliases(self):
        '''
        '''
        sql = ("SELECT recipient,destination FROM `virtual_alias_map`")
        self.cursor.execute(sql)
        aliases = self.cursor.fetchall()
        return aliases

        



