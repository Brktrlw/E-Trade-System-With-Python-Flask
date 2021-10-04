from baseDatabaseManager import BaseDatabaseManager

class CommentManager():
    @staticmethod
    def increaseProductAmountFromCart(customerId, productId):
        BaseDatabaseManager.databaseType.increaseProductAmountFromCart(customerId, productId)

    @staticmethod
    def isLikeComment(customerId, commentId):
        isLike = BaseDatabaseManager.databaseType.isLikeComment(customerId, commentId)
        return isLike

    @staticmethod
    def isdislikeComment(customerId, commentId):
        isdislike = BaseDatabaseManager.databaseType.isdislikeComment(customerId, commentId)
        return isdislike

    @staticmethod
    def increaseCommentDisLikeByCommentId(customerId, commentId):
        BaseDatabaseManager.databaseType.increaseCommentDisLikeByCommentId(customerId, commentId)

    @staticmethod
    def reduceCommentLikeByCommentId(commentId, customerId):
        BaseDatabaseManager.databaseType.reduceCommentLikeByCommentId(commentId, customerId)

    @staticmethod
    def reduceCommentdisLikeByCommentId(commentId, customerId):
        BaseDatabaseManager.databaseType.reduceCommentdisLikeByCommentId(commentId, customerId)

    @staticmethod
    def increaseCommentLikeByCommentId(commentId, customerId):
        BaseDatabaseManager.databaseType.increaseCommentLikeByCommentId(commentId, customerId)

    @staticmethod
    def getCommentsByProductId(productId):
        comments = BaseDatabaseManager.databaseType.getCommentsByProductId(productId)
        return comments

    @staticmethod
    def addCommentByProductIdAndCustomerId(productId,customerId,commentText):
        BaseDatabaseManager.databaseType.addCommentByProductIdAndCustomerId(productId,customerId,commentText)