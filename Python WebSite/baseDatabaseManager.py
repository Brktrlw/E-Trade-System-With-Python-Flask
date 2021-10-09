from passlib.hash import sha256_crypt

class BaseDatabaseManager():
    databaseType=None

    @staticmethod
    def increaseProductAmountFromCart(customerId, productId):
        BaseDatabaseManager.databaseType.increaseProductAmountFromCart(customerId, productId)

    @staticmethod
    def getOrderItemsByOrderId(orderId):
        orderItemDetails=BaseDatabaseManager.databaseType.getOrderItemsByOrderId(orderId)
        return orderItemDetails
    @staticmethod
    def getOrderByOrderId(orderId):
        orderDetails=BaseDatabaseManager.databaseType.getOrderByOrderId(orderId)
        return orderDetails

    @staticmethod
    def getBasket(customerId:int):  # Müşteri ID'sine göre sepetteki ürünleri "/Sepetim" sayfasında listelediğimiz method
        result=BaseDatabaseManager.databaseType.getBasket(customerId)
        return result

    @staticmethod
    def cleanCartAfterOrder(customerId:int):
        BaseDatabaseManager.databaseType.cleanCartAfterOrder(customerId)

    @staticmethod
    def getOrderItemsByOrderId(orderId):
        orderItemList=BaseDatabaseManager.databaseType.getOrderItemsByOrderId(orderId)
        return orderItemList

    @staticmethod
    def addOrderList(maxorderId,productId,productAmount):
        BaseDatabaseManager.databaseType.addOrderList(maxorderId,productId,productAmount)

    @staticmethod
    def getMaxOrderId(customerId):
        maxOrderId=BaseDatabaseManager.databaseType.getMaxOrderId(customerId)
        return maxOrderId

    @staticmethod
    def getProductDetails(productId):
        productDetail=BaseDatabaseManager.databaseType.getProductDetails(productId)
        return productDetail

    @staticmethod
    def getOrdersByCustomerId(customerId):
        orders=BaseDatabaseManager.databaseType.getOrdersByCustomerId(customerId)
        return orders

    @staticmethod
    def getProductsWithSearchKeyword(keyword):
        products=BaseDatabaseManager.databaseType.getProductsWithSearchKeyword(keyword)
        return products

    @staticmethod
    def addOrder(customerId:int):
        BaseDatabaseManager.databaseType.addOrder(customerId)

    @staticmethod
    def sumTotalPrice(customerId:int): # Sepetteki ürünlerinin toplam fiyatını müşteri ID'sine göre toplayıp return ettiren method
        totalPrice=BaseDatabaseManager.databaseType.sumTotalPrice(customerId)
        return totalPrice

    @staticmethod
    def getProductsWithCatId(catId): # Kategori ID ile ürünleri veritabanından çekip return ettirdiğimiz method
        productsList=BaseDatabaseManager.databaseType.getProductsWithCatId(catId)
        return productsList

    @staticmethod
    def getAllProducts():  # Veritabanından Tüm Ürünleri çekip return ettirdiğimiz method
        productList=BaseDatabaseManager.databaseType.getAllProducts()
        return productList

    @staticmethod
    def isLoginCustomer(customerUserName,customerPassword): # Müşteri giriş yaparken parolası ve kullanıcı adının doğru olup olmadığına bool değer döndüren fonksiyon
        customerData=BaseDatabaseManager.databaseType.isLoginCustomer(customerUserName,customerPassword)
        return customerData

    @staticmethod
    def isCustomerUserName(customerUserName): # Kullanıcı kayıt olurken daha önce aynı kullanıcı adını alan biri var mı diye kontrol eder.
        isAnyCustomer=BaseDatabaseManager.databaseType.isCustomerUserName(customerUserName)
        return isAnyCustomer

    @staticmethod
    def isCustomerMail(customerMail): # Kullanıcı kayıt olurken veritabanında aynı mail adresinin olup olmadığını kontrol eden method
        isCustomerMail = BaseDatabaseManager.databaseType.isCustomerMail(customerMail)
        return isCustomerMail

    @staticmethod
    def delFavoriteProduct(customerId,productId):
        BaseDatabaseManager.databaseType.delFavoriteProduct(customerId,productId)

    @staticmethod
    def getSellerDetails(sellerUserName):
        sellerDetails=BaseDatabaseManager.databaseType.getSellerDetails(sellerUserName)
        return sellerDetails

    @staticmethod
    def findCustomerIdFromCustomerUserName(customerUserName):
        customerId = BaseDatabaseManager.databaseType.findCustomerIdFromCustomerUserName(customerUserName)
        return customerId

    @staticmethod
    def deleteProductFromBasket(productId,customerId):
        BaseDatabaseManager.databaseType.deleteProductFromBasket(productId,customerId)

    @staticmethod
    def addProductToCart(productId,customerId):
        BaseDatabaseManager.databaseType.addProductToCart(productId,customerId)

    @staticmethod
    def updateProductFromBasket(customerId,productId,proccess):
        BaseDatabaseManager.databaseType.updateProductFromBasket(customerId,productId,proccess)

    # ----------------------------------------------------------------------------------------------------------------------------------#
    #-------------------------------------------------- MÜŞTERİ İLE İLGİLİ İŞLEMLER ----------------------------------------------------#
    # ----------------------------------------------------------------------------------------------------------------------------------#


    @staticmethod
    def delCustomer():
        pass

    @staticmethod
    def updateCustomer():
        pass

    @staticmethod
    def addCustomer(customerName, customerUserName, customerMail,customerPassword):  # Veritabanına müşteri eklediğimiz method
        BaseDatabaseManager.databaseType.addCustomer(customerName, customerUserName, customerMail,sha256_crypt.encrypt(customerPassword))










