import sqlite3
from fileErrorLogger import FileErrorLogger
from DatabaseLogger import DatabaseLoggers
from baseDatabaseManager import BaseDatabaseManager
from datetime import datetime
class SQLiteDataBaseManager(BaseDatabaseManager):

    @staticmethod
    def getSellerDetails(sellerUserName):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"SELECT * from Sellers where sellerUserName='{sellerUserName}'")
            sellerDetails = cursor.fetchone()
            return sellerDetails
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()
    @staticmethod
    def addCommentByProductIdAndCustomerId(productId,customerId,commentText):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()

            year = datetime.now().year
            month = datetime.now().month
            day = datetime.now().day
            hour = datetime.now().hour
            minute = datetime.now().minute

            date = str(day) + "/" + str(month) + "/" + str(year) + "-" + str(hour) + ":" + str(minute)
            cursor.execute(f"INSERT INTO ProductComment ('CustomerId','ProductId','Commenttext','commentdate','commentlike','commentdislike') "
                           f"VALUES ('{customerId}','{productId}','{commentText}','{date}','0','0')")
            connection.commit()
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()
    # Müşterinin kullanıcı adından müşteri Id'sini bulduğumuz method
    @staticmethod
    def findCustomerIdFromCustomerUserName(customerUserName):
        try:
            connection=sqlite3.connect("database.db")
            cursor=connection.cursor()
            cursor.execute(f"SELECT CustomerId FROM Customers WHERE CustomerUserName='{customerUserName}'")
            customerId=cursor.fetchone()
            return customerId
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    # Sepetteki ürünlerinin toplam fiyatını müşteri ID'sine göre toplayıp return ettiren method
    @staticmethod
    def sumTotalPrice(customerId:int):
        try:
            connection=sqlite3.connect("database.db")
            cursor=connection.cursor()
            cursor.execute(f"SELECT SUM(Products.ProductPrice*Amount) FROM BASKET INNER JOIN Products ON Products.ProductId=Basket.ProductId where CustomerId={customerId}")
            totalPrice=cursor.fetchone()
            return int(totalPrice[0])
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()
    @staticmethod
    def getCustomerData(customerId):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM CUSTOMERS where CustomerId='{customerId}'")
            customerData = cursor.fetchone()
            return customerData
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def cleanCartAfterOrder(customerId):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM Basket where CustomerId='{customerId}'")
            connection.commit()
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def addOrder(customerId):
        from datetime import datetime
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        hour = datetime.now().hour
        minute = datetime.now().minute
        date = str(day) + "/" + str(month) + "/" + str(year) + "-" + str(hour) + ":" + str(minute)
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO Orders ('CustomerId','OrderDate','OrderPrice') VALUES ('{customerId}','{date}','{BaseDatabaseManager.sumTotalPrice(customerId)}')")
            connection.commit()
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def addOrderList(maxorderId,productId,productAmount):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO Order_Items ('OrderId','ProductId','ProductAmount') VALUES ('{maxorderId}','{productId}','{productAmount}') ")
            connection.commit()
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def getMaxOrderId(customerId):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"SELECT MAX(OrderId) FROM Orders where CustomerId='{customerId}'")
            maxId=cursor.fetchone()
            return maxId
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()


    # Müşteri giriş yaparken parolası ve kullanıcı adının doğru olup olmadığına bool değer döndüren method
    @staticmethod
    def isLoginCustomer(customerUserName,customerPassword):
        try:
            connection = sqlite3.connect("database.db")
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

    @staticmethod
    def getProductsWithSearchKeyword(keyword):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM Products WHERE ProductName LIKE '%{keyword}%'")
            products = cursor.fetchall()
            if products == []:
                return None
            else:
                return products
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def getOrderItemsByOrderId(orderId):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"SELECT OrderId,ProductName,ProductAmount FROM Order_Items INNER JOIN Products ON Order_Items.ProductId=Products.ProductId where OrderId={orderId}")
            orderItemList = cursor.fetchall()
            return orderItemList
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def getOrdersByCustomerId(customerId):
        try:
            connection=sqlite3.connect("database.db")
            cursor=connection.cursor()
            cursor.execute(f"SELECT * FROM Orders where customerId='{customerId}' ORDER BY  OrderDate DESC")
            orders=cursor.fetchall()
            return orders
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def getOrderByOrderId(orderId):
        try:
            connection=sqlite3.connect("database.db")
            cursor=connection.cursor()
            cursor.execute(f"SELECT * FROM Orders where OrderId={orderId}")
            orderDetails=cursor.fetchall()
            return orderDetails
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def getOrderItemsByOrderId(orderId):
        try:
            connection=sqlite3.connect("database.db")
            cursor=connection.cursor()
            cursor.execute(f"SELECT ProductName,ProductAmount,ProductImageUrl,ProductPrice FROM Order_Items INNER JOIN Products ON Products.ProductId=Order_Items.ProductId where OrderId={orderId}")
            orderItemDetails=cursor.fetchall()
            return orderItemDetails
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()
    # Kullanıcı kayıt olurken daha önce aynı kullanıcı adını alan biri var mı diye kontrol eder.
    @staticmethod
    def isCustomerUserName(customerUserName):
        try:
            connection=sqlite3.connect("database.db")
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
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM CUSTOMERS WHERE CustomerMail='{customerMail}'")
            isCustomerMail = cursor.fetchone()
            if isCustomerMail == None:
                return False
            else:
                return True
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)

    @staticmethod
    def getFavoriteProducts(customerId):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"SELECT ProductName,ProductPrice,ProductImageUrl,ProductSize,ProductDetails,Products.ProductId,ProductDescription,Productstar,ProductCargoType FROM Favorites INNER JOIN Products ON Favorites.ProductId=Products.ProductId where Favorites.CustomerId={customerId}")
            favoriteProducts = cursor.fetchall()
            return favoriteProducts
        except Exception as e:
            print(e)
        finally:
            connection.close()

    # Favorilerden ürün silmeye yarayan method
    @staticmethod
    def delFavoriteProduct(customerId,productId):
        try:
            connection=sqlite3.connect("database.db")
            cursor=connection.cursor()
            cursor.execute(f"DELETE FROM Favorites where ProductId='{productId}' and CustomerId='{customerId}'")
            connection.commit()
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def getCommentsByProductId(productId):
        try:
            connection=sqlite3.connect("database.db")
            cursor=connection.cursor()
            cursor.execute(f"Select CommentId,CustomerUserName,CommentText,CommentDate,CommentLike,CommentDislike from ProductComment INNER JOIN Customers ON ProductComment.CustomerId=Customers.CustomerId where ProductId={productId} order by CommentDate desc")
            comments=cursor.fetchall()
            return comments;
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def reduceCommentLikeByCommentId(commentId,customerId):
        try:
            connection = sqlite3.connect("database.db")
            cursor=connection.cursor()
            cursor.execute(f"UPDATE ProductComment set CommentLike=(SELECT CommentLike FROM ProductComment where CommentId={commentId})-1 where CommentId={commentId}")
            connection.commit()
            cursor.execute(f"DELETE FROM Commentlikes where customerId={customerId} and commentId={commentId}")
            connection.commit()
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def reduceCommentdisLikeByCommentId(commentId,customerId):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"UPDATE ProductComment set CommentdisLike=(SELECT CommentdisLike FROM ProductComment where CommentId={commentId})-1 where CommentId={commentId}")
            connection.commit()
            cursor.execute(f"DELETE FROM Commentdislike where customerId={customerId} and commentId={commentId}")
            connection.commit()
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def isLikeComment(customerId,commentId):
        try:
            connection = sqlite3.connect("database.db")
            cursor=connection.cursor()
            cursor.execute(f"SELECT * FROM CommentLikes where customerId={customerId} and commentId='{commentId}'")
            isLike=cursor.fetchall()
            return isLike
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def isdislikeComment(customerId,commentId):
        try:
            connection = sqlite3.connect("database.db")
            cursor=connection.cursor()
            cursor.execute(f"SELECT * FROM CommentDisLike where customerId={customerId} and commentId='{commentId}'")
            isdislike=cursor.fetchall()
            return isdislike
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def increaseCommentLikeByCommentId(commentId,customerId):
        try:
            connection = sqlite3.connect("database.db")
            cursor=connection.cursor()
            cursor.execute(f"UPDATE ProductComment set CommentLike=(SELECT CommentLike FROM ProductComment where CommentId={commentId})+1 where CommentId={commentId}")
            connection.commit()
            cursor.execute(f"INSERT INTO CommentLikes ('CustomerId','CommentId') VALUES ('{customerId}','{commentId}')")
            connection.commit()
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def increaseCommentDisLikeByCommentId(commentId,customerId):
        try:
            connection = sqlite3.connect("database.db")
            cursor=connection.cursor()
            cursor.execute(f"UPDATE ProductComment set CommentdisLike=(SELECT CommentdisLike FROM ProductComment where CommentId={commentId})+1 where CommentId={commentId}")
            connection.commit()
            cursor.execute(f"INSERT INTO CommentdisLike ('CustomerId','CommentId') VALUES ('{customerId}','{commentId}')")
            connection.commit()
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def getProductDetails(productId):
        try:
            connection = sqlite3.connect("database.db")
            cursor=connection.cursor()
            cursor.execute(f"select ProductId,ProductName,ProductPrice,ProductImageUrl,ProductDetails,ProductSize,ProductStar,ProductDescription,ProductBrand,ProductCargoType,CategorieName,ProductCatId,Sellers.SellerUserName from products INNER JOIN Categories ON Categories.Id=Products.ProductCatId INNER JOIN Sellers ON pRODUCTS.ProductSellerId=Sellers.SellerId where ProductId={productId}")
            productDetails=cursor.fetchone()
            return productDetails
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    @staticmethod
    def addFavoriteToFavorites(productId, customerId):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM Favorites where ProductId='{productId}' and CustomerId='{customerId}'")
            isProductFavorite=cursor.fetchone()
            if isProductFavorite==None:
                cursor.execute(f"INSERT INTO Favorites ('ProductId','CustomerId') VALUES ('{productId}','{customerId}')")
                connection.commit()
            else:
                return False
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    # Sepete ürün eklerken çalışan method
    @staticmethod
    def addProductToCart(productId, customerId):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM Basket where CustomerId='{customerId}' and productId='{productId}'")
            basketData = cursor.fetchone()
            if basketData == None:
                cursor.execute(
                    f"INSERT INTO Basket ('CustomerId','ProductId','Amount') VALUES ('{customerId}','{productId}','1')")
                connection.commit()
            else:
                SQLiteDataBaseManager.updateProductFromBasket(customerId, productId, True)
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    #  Veritabanından Tüm Ürünleri çekip return ettirdiğimiz method
    @staticmethod
    def getAllProducts():
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute("SELECT ProductId,ProductName,ProductPrice,ProductImageUrl,ProductDetails,ProductSize,ProductCatId,ProductStar,ProductDescription,CategorieName,ProductBrand FROM Products INNER JOIN Categories ON Products.ProductCatId=Categories.Id")
            productList = cursor.fetchall()
            return productList
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    # Kategori Id'si ile ilgili ürünleri döndürdüğümüz method
    @staticmethod
    def getProductsWithCatId(catId):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM Products WHERE ProductCatId={catId}")
            productsList = cursor.fetchall()
            return productsList
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    # True ya da False ile sepetteki ürünün adetini arttırıp azalttığımız method
    @staticmethod
    def updateProductFromBasket(customerId, productId, proccess):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            if proccess == True:
                cursor.execute(
                    f"UPDATE Basket set Amount =(SELECT Amount FROM Basket where CustomerId={customerId} and ProductId={productId})+1 where customerId={customerId} and productId={productId}")
            elif proccess == False:
                cursor.execute(f"SELECT Amount FROM Basket WHERE CustomerId={customerId} and ProductId={productId}")
                productAmount = cursor.fetchone()
                if productAmount[0] == 1:
                    # Ürün azaltırken adet 1den küçük olduğu sırada ürün sepetten silinir.
                    SQLiteDataBaseManager.deleteProductFromBasket(productId, customerId)
                else:
                    cursor.execute(
                        f"UPDATE Basket set Amount =(SELECT Amount FROM Basket where CustomerId={customerId} and ProductId={productId})-1 where customerId={customerId} and productId={productId}")
            connection.commit()
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    # Sepetteki ürünü kaldırmaya yarayan method
    @staticmethod
    def deleteProductFromBasket(productId, customerId):
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM Basket WHERE ProductId={productId} and CustomerId='{customerId}'")
            connection.commit()
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()

    # Müşterinin Id'si ile sepetindeki ürünleri veritabanından çektiğimiz method
    @staticmethod
    def getBasket(customerId: int):  # Müşteri ID'sine göre sepetteki ürünleri "/Sepetim" sayfasında listelediğimiz method
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"SELECT ProductName,ProductPrice,Amount,ProductImageUrl,ProductSize,ProductDetails,Products.ProductId FROM Basket INNER JOIN Products ON Basket.ProductId=Products.ProductId where Basket.CustomerId={customerId}")
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

    @staticmethod
    def addCustomer(customerName, customerUserName, customerMail, customerPassword): # Veritabanına müşteri Eklediğimiz Method
        try:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO Customers ('CustomerName','CustomerUserName','CustomerMail','CustomerPassword') VALUES ('{customerName}','{customerUserName}','{customerMail}','{customerPassword}')")
            connection.commit()
        except Exception as e:
            DatabaseLoggers.databaseLogger(e)
            FileErrorLogger.FileLogger(e)
        finally:
            connection.close()


