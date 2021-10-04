from passlib.hash import sha256_crypt
from baseDatabaseManager import BaseDatabaseManager

class CustomerManager():

    @staticmethod
    def addCustomer(customerName,customerUserName,customerMail,customerPassword):
        BaseDatabaseManager.databaseType.addCustomer(customerName,customerUserName,customerMail,sha256_crypt.encrypt(customerPassword))

    @staticmethod
    def updateCustomer(customerName,customerUserName,customerMail,customerPassword): # Veritabanından müşteri güncellediğimiz method
        BaseDatabaseManager.databaseType.updateCustomer(customerName,customerUserName,customerMail,customerPassword)

    @staticmethod
    def getCustomerData(customerId):
        customerData=BaseDatabaseManager.databaseType.getCustomerData(customerId)
        return customerData



















