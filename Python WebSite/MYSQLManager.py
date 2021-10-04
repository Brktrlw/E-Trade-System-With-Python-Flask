from fileErrorLogger import FileErrorLogger
from DatabaseLogger import DatabaseLoggers
from baseDatabaseManager import BaseDatabaseManager
import mysql.connector

class MysqlManager(BaseDatabaseManager):

    # Müşterinin kullanıcı adından müşteri Id'sini bulduğumuz method
    @staticmethod
    def findCustomerIdFromCustomerUserName(customerUserName):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="12345",database="sicekmepeti")
            cursor = connection.cursor()
            cursor.execute(f"SELECT CustomerId FROM Customers WHERE CustomerUserName='{customerUserName}'")
            customerId = cursor.fetchone()
            return customerId
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    # Müşterinin Id'si ile sepetindeki ürünleri veritabanından çektiğimiz method
    @staticmethod
    def getBasket(customerId: int):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="12345",database="sicekmepeti")
            cursor = connection.cursor()
            cursor.execute(f"SELECT ProductName,ProductPrice,Amount,ProductImageUrl,ProductSize,ProductDetails FROM Basket INNER JOIN Products ON Basket.ProductId=Products.ProductId where Basket.CustomerId={customerId}")
            dataOfBasket = cursor.fetchall()
            if dataOfBasket == []:
                return False
            else:
                return dataOfBasket
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    # Sepetteki ürünlerin toplam fiyatını döndürdüğümüz method
    @staticmethod
    def sumTotalPrice(customerId:int):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="12345",database="sicekmepeti")
            cursor=connection.cursor()
            cursor.execute(f"SELECT SUM(ProductPrice) FROM Basket INNER JOIN Products ON Basket.ProductId=Products.ProductId where CustomerId={customerId}")
            totalPrice=cursor.fetchone()
            return int(totalPrice[0])
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    # Kategori Id'si ile ilgili ürünleri döndürdüğümüz method
    @staticmethod
    def getProductsWithCatId(catId):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="12345",database="sicekmepeti")
            cursor=connection.cursor()
            cursor.execute(f"SELECT * FROM Products WHERE ProductCatId={catId}")
            productsList=cursor.fetchall()
            return productsList
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    #  Veritabanından Tüm Ürünleri çekip return ettirdiğimiz method
    @staticmethod
    def getAllProducts():
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="12345",database="sicekmepeti")
            cursor = connection.cursor()
            cursor.execute("SELECT ProductId,ProductName,ProductPrice,ProductImageUrl,ProductDetails,ProductSize,ProductCatId,ProductStar,ProductDescription,CategorieName,ProductBrand FROM Products INNER JOIN Categories ON Products.ProductCatId=Categories.Id")
            productList = cursor.fetchall()
            return productList
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    # ----------------------------------------------------------------------------------------------------------------------------------#
    # -------------------------------------------------- MÜŞTERİ İLE İLGİLİ İŞLEMLER ----------------------------------------------------#
    # ----------------------------------------------------------------------------------------------------------------------------------#

    # Veritabanına müşteri Eklediğimiz Method
    @staticmethod
    def addCustomer(customerName, customerUserName, customerMail, customerPassword):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="12345",database="sicekmepeti")
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO Customers (CustomerName,CustomerUserName,CustomerMail,CustomerPassword) VALUES ('{customerName}','{customerUserName}','{customerMail}','{customerPassword}')")
            connection.commit()
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    # Müşteri giriş yaparken parolası ve kullanıcı adının doğru olup olmadığına bool değer döndüren method
    @staticmethod
    def isLoginCustomer(customerUserName,customerPassword):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="12345",database="sicekmepeti")
            cursor = connection.cursor()
            cursor.execute(f"SELECT CustomerName FROM Customers WHERE CustomerUserName='{customerUserName}' and CustomerPassword='{customerPassword}'")
            customerData = cursor.fetchone()
            if customerData == None:
                return False
            else:
                return True
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    # Kullanıcı kayıt olurken daha önce aynı kullanıcı adını alan biri var mı diye kontrol eder.
    @staticmethod
    def isCustomerUserName(customerUserName):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="12345",database="sicekmepeti")
            cursor=connection.cursor()
            cursor.execute(f"SELECT CustomerName FROM CUSTOMERS where CustomerUserName='{customerUserName}'")
            isAnyCustomer=cursor.fetchone()
            if isAnyCustomer==None:
                return False
            else:
                return True
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    # Kayıt olurken aynı mail adresinde bir müşterinin olup olmadığını kontrol eden blok
    @staticmethod
    def isCustomerMail(customerMail):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="12345",database="sicekmepeti")
            cursor = connection.cursor()
            cursor.execute(F"SELECT * FROM CUSTOMERS WHERE CustomerMail='{customerMail}'")
            isCustomerMail = cursor.fetchone()
            if isCustomerMail == None:
                return False
            else:
                return True
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)






