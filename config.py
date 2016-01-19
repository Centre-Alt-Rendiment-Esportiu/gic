"""
@dani.ruiz
"""
#SQLALCHEMY_DATABASE_URI = 'mysql://root:1234@localhost/gic'
SQLALCHEMY_DATABASE_URI = 'oracle://CAR_PCF_TEST:isocar@ora.isoco.car.loc:1521/PCAR'

#import cx_Oracle
#dsn_tns = cx_Oracle.makedsn('ora.isoco.car.loc', '1521', 'PCAR')
#SQLALCHEMY_DATABASE_URI = cx_Oracle.connect('CAR_PCF_TEST', 'isocar', dsn_tns)
