from baseDatabaseManager import BaseDatabaseManager

class ProductManager():

    @staticmethod
    def deleteProductFromBasket(productId, customerId):
        BaseDatabaseManager.databaseType.deleteProductFromBasket(productId, customerId)

    @staticmethod
    def getProductDetails(productId):
        productDetails=BaseDatabaseManager.databaseType.getProductDetails(productId)
        return productDetails

    @staticmethod
    def getFavoriteProducts(customerId):
        favoriteProducts=BaseDatabaseManager.databaseType.getFavoriteProducts(customerId)
        return favoriteProducts

    @staticmethod
    def addProductToCart(productId, customerId):
        BaseDatabaseManager.databaseType.addProductToCart(productId, customerId)

    @staticmethod
    def addFavoriteToFavorites(productId, customerId):
        isFavorite=BaseDatabaseManager.databaseType.addFavoriteToFavorites(productId, customerId)
        return isFavorite

    @staticmethod
    def getAllProducts():
        productsList=BaseDatabaseManager.databaseType.getAllProducts()
        return productsList

    @staticmethod
    def getProductsWithCatId(catId):
        productsList=BaseDatabaseManager.databaseType.getProductsWithCatId(catId)
        return productsList

    @staticmethod
    def updateProductFromBasket(customerId, productId, proccess):
        BaseDatabaseManager.databaseType.updateProductFromBasket(customerId, productId, proccess)

    @staticmethod
    def deleteProductFromBasket(productId, customerId):
        BaseDatabaseManager.databaseType.deleteProductFromBasket(productId, customerId)

    @staticmethod
    def getBasket(customerId):
        dataOfBasket=BaseDatabaseManager.databaseType.getBasket(customerId)
        return dataOfBasket

















