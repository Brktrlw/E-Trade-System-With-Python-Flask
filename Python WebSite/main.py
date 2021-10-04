from SQLiteManager import SQLiteDataBaseManager
from baseDatabaseManager import BaseDatabaseManager
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL

from commentManager import CommentManager
from register import RegisterForm,LoginForm
from customerManager import CustomerManager
from MYSQLManager import MysqlManager
from productManager import ProductManager
from functools import wraps

app=Flask(__name__)
app.secret_key = 'super secret key'
#app.config["MYSQL_HOST"]="localhost"
#app.config["MYSQL_USER"]="root"
#app.config["MYSQL_PASSWORD"]=""
#app.config["MYSQL_DB"]="sicekmepetidb"
#app.config["MYSQL_CURSORCLASS"]="DictCursor"
#mysql=MySQL(app)


BaseDatabaseManager.databaseType=SQLiteDataBaseManager # Veritabanından gerekli sorgu işlemleri için kullandığımız veritabanının türünü yazıyoruz


# Kullanıcı giriş decaratörü
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Lütfen giriş yapınız")
            return redirect(url_for("getResponseHomePageIndex"))
    return decorated_function



@app.route("/") # Ana sayfa açılırken dönen response
def getResponseHomePageIndex():
    return render_template("index.html")

@app.route("/Sepetim") # Sepetim Sayfası açılırken dönen response
@login_required
def getResponseImagesIndex():
    customerId = BaseDatabaseManager.findCustomerIdFromCustomerUserName(session["username"])
    basketIsEmpty=BaseDatabaseManager.getBasket(customerId[0])
    try:
        sepettekiUrunler=basketIsEmpty.copy()
        uzunluk = len(sepettekiUrunler)
        totalPrice = BaseDatabaseManager.sumTotalPrice(customerId[0])
        return render_template("sepetim.html", sepettekiUrunler=sepettekiUrunler, uzunluk=uzunluk,totalPrice=totalPrice)
    except Exception as e:
        sepettekiUrunler=False
        return render_template("sepetim.html",sepettekiUrunler=sepettekiUrunler)

@app.route("/Products/<string:categorieName>") # Kategorileri Seçerken çalışan Method
def getProductListWithCategorie(categorieName:str):
    catId=None
    if categorieName=="Erkek-Giyim":
        catId=3
    elif categorieName=="Kadin-Giyim":
        catId=5
    elif categorieName=="Kirtasiye":
        catId=4
    elif categorieName=="Telefon":
        catId=1
    elif categorieName=="Bilgisayar":
        catId=2
    else:
        flash("Böyle Bir Sayfa Bulunamadı !")
        return redirect(url_for("getResponseHomePageIndex"))
    productsList=ProductManager.getProductsWithCatId(catId)
    lenOfList=len(productsList)   
    return render_template("products.html",productsList=productsList,lenOfList=lenOfList,catId=catId)

@app.route("/Product/<string:productId>")
def getProductDetailsPage(productId):
    productDetails=ProductManager.getProductDetails(productId)
    comments=CommentManager.getCommentsByProductId(productId)
    return render_template("productDetails.html",productDetails=productDetails,comments=comments,uzunluk=len(comments))

@app.route("/increaseLike",methods=["POST"])
@login_required
def increaseLikeByCommentId():
    customerId = BaseDatabaseManager.findCustomerIdFromCustomerUserName(session["username"])
    commentId= request.form.get('comment_id')

    isLike=CommentManager.isLikeComment(customerId[0],commentId)
    if isLike==[]:
        CommentManager.increaseCommentLikeByCommentId(commentId,customerId[0])
    else:
        CommentManager.reduceCommentLikeByCommentId(commentId,customerId[0])
    return redirect(request.referrer)


@app.route("/increaseDislikeByCommentId",methods=["POST"])
@login_required
def increaseDislikeByCommentId():
    customerId = BaseDatabaseManager.findCustomerIdFromCustomerUserName(session["username"])
    commentId = request.form.get('comment_id')
    isdislike = CommentManager.isdislikeComment(customerId[0], commentId)
    if isdislike == []:
        CommentManager.increaseCommentDisLikeByCommentId(commentId, customerId[0])
    else:
        CommentManager.reduceCommentdisLikeByCommentId(commentId, customerId[0])
    return redirect(request.referrer)

@app.route("/Product/")
def redirectProduct():
    return redirect(url_for("getAllProducts"))

@app.route("/Products/") # Tüm ürünlerin listelendiği sayfayı açar
def getAllProducts():
    catId=None
    productsList=ProductManager.getAllProducts()
    lenOfList=len(productsList)
    return render_template("products.html",productsList=productsList,lenOfList=lenOfList,catId=catId)

@app.route("/Login",methods=['POST','GET']) # Login sayfasını açar
def getLoginPageIndex():
    girisFormu=LoginForm(request.form)
    isTrue=None
    if request.method=="POST" and girisFormu.validate():
        inputCustomerUserName=girisFormu.customerUserName.data
        inputCustomerPassword=girisFormu.customerPassword.data
        isLogin=BaseDatabaseManager.isLoginCustomer(inputCustomerUserName,inputCustomerPassword)
        if isLogin==False:
            isTrue=False
            return render_template("login.html",form=girisFormu,isTrue=isTrue)
        else:
            isTrue=True
            session["logged_in"]=True
            session["username"]=inputCustomerUserName
            return redirect(url_for("getResponseHomePageIndex"))
    else:
        return render_template("login.html",form=girisFormu)

@app.route("/deleteFavorite",methods=["POST"])
def deleteFavoriteProduct():
    try:
        customerId = BaseDatabaseManager.findCustomerIdFromCustomerUserName(session["username"])
    except:
        flash("Lütfen giriş yapınız")
        return render_template("index.html")
    productId = request.form.get('product_id')
    customerId = customerId[0]
    BaseDatabaseManager.delFavoriteProduct(customerId,productId)
    flash("Ürün başarıyla favorilerden kaldırılmıştır","success")
    return redirect(request.referrer)

@app.route("/<string:deger>")
def get404Page(deger):
    flash("Sayfa bulunamadı.")
    return redirect(url_for("getResponseHomePageIndex"))

@app.route("/Favorilerim")
@login_required
def getFavorite():
    customerId = BaseDatabaseManager.findCustomerIdFromCustomerUserName(session["username"])
    favoriteProducts=ProductManager.getFavoriteProducts(customerId[0])
    lenFavoriteProducts=len(favoriteProducts)
    return render_template("favorities.html",favoriteProducts=favoriteProducts,lenFavoriteProducts=lenFavoriteProducts)

@app.route("/logout") # Çıkış yaptığımız method
def logoutFunc():
    session.clear()
    return redirect(url_for("getResponseHomePageIndex"))

@app.route("/Register",methods=["GET","POST"]) # Kayıt olurken dönen response
def getRegisterPageIndex():
    kayitFormu=RegisterForm(request.form)
    if request.method=="POST" and kayitFormu.validate():
        inputCustomerName=kayitFormu.customerName.data
        inputCustomerUserName=kayitFormu.customerUserName.data
        inputCustomerMail=kayitFormu.customerMail.data
        inputCustomerPassword=kayitFormu.customerPassword.data

        isCustomerUserName=BaseDatabaseManager.isCustomerUserName(inputCustomerUserName)
        isAnyCustomerMail=BaseDatabaseManager.isCustomerMail(inputCustomerMail)
        if isCustomerUserName==False and isAnyCustomerMail==False: # Müşteriyi veritabanına kaydettiğimiz blok
                CustomerManager.addCustomer(inputCustomerName,inputCustomerUserName,inputCustomerMail,inputCustomerPassword)
                return redirect(url_for("getLoginPageIndex"))
        elif isAnyCustomerMail==True and isCustomerUserName==False:
            return render_template("register.html",form=kayitFormu,isCustomerUserName=isCustomerUserName,isAnyCustomerMail=isAnyCustomerMail)
        elif isAnyCustomerMail==False and isCustomerUserName==True:
            return render_template("register.html",form=kayitFormu,isCustomerUserName=isCustomerUserName,isAnyCustomerMail=isAnyCustomerMail)
        else:
            return render_template("register.html", form=kayitFormu, isCustomerUserName=isCustomerUserName,isAnyCustomerMail=isAnyCustomerMail)
    else:
        return render_template("register.html",form=kayitFormu)

@app.route('/add', methods=['POST'])
@login_required
def addProductToCart():
    product_id = request.form.get('product_id')
    customerId = BaseDatabaseManager.findCustomerIdFromCustomerUserName(session["username"])
    ProductManager.addProductToCart(product_id,customerId[0])
    flash("Ürün başarıyla sepetinize eklenmiştir")
    return redirect(request.referrer)

# sepetten ürünün adetini arttırdığımız method
@app.route("/increaseAmount",methods=['POST'])
def increaseProductAmount():
    customerId = BaseDatabaseManager.findCustomerIdFromCustomerUserName(session["username"])
    product_id=request.form.get('product_id')
    customerId=customerId[0]
    ProductManager.updateProductFromBasket(customerId,product_id,True)
    flash("Sepetiniz güncellenmiştir.")
    return redirect(request.referrer)

@app.route("/reduceAmount",methods=["POST"])
def reduceProductAmount():
    customerId = BaseDatabaseManager.findCustomerIdFromCustomerUserName(session["username"])
    product_id = request.form.get('product_id')
    customerId = customerId[0]
    BaseDatabaseManager.updateProductFromBasket(customerId,product_id,False)
    flash("Sepetiniz güncellenmiştir.")
    return redirect(request.referrer)

@app.route("/deleteProduct",methods=['POST'])
def deleteProductFromBasket():
    customerId = BaseDatabaseManager.findCustomerIdFromCustomerUserName(session["username"])
    product_id = request.form.get('product_id')
    customerId = customerId[0]
    ProductManager.deleteProductFromBasket(product_id,customerId)
    flash("Ürün başarıyla sepetinizden kaldırılmıştır.")
    return redirect(request.referrer)

@app.route("/addFavorite",methods=["POST"])
@login_required
def addFavoriteToFavorites():
    customerId = BaseDatabaseManager.findCustomerIdFromCustomerUserName(session["username"])
    product_id = request.form.get('product_id')
    customerId = customerId[0]
    isFavorite=ProductManager.addFavoriteToFavorites(product_id,customerId)
    if isFavorite==False:
        flash("Ürün zaten favorilerinizdedir")
        return redirect(request.referrer)
    else:
        flash("Ürün başarıyla favorilere eklenmiştir.")
        return redirect(request.referrer)

@app.route("/seller/<string:sellerUserName>")
def getSellerPage(sellerUserName):
    sellerDetails=BaseDatabaseManager.getSellerDetails(sellerUserName)
    if sellerDetails==None:
        flash("Böyle bir mağaza bulunmamaktadır!")
        return redirect(url_for("getResponseHomePageIndex"))
    else:
        return render_template("sellerDetails.html",sellerDetails=sellerDetails)

@app.route("/Payment")
@login_required
def getPaymentPage():
    customerId = BaseDatabaseManager.findCustomerIdFromCustomerUserName(session["username"])
    basket=BaseDatabaseManager.getBasket(customerId[0])
    if basket==False or basket==None:
        flash("Sepetinizde ürün bulunmamaktadır")
        return redirect(url_for("getResponseImagesIndex"))
    cartProducts=BaseDatabaseManager.getBasket(customerId[0])
    lenCart=len(cartProducts)
    totalPrice=BaseDatabaseManager.sumTotalPrice(customerId[0])
    return render_template("payment.html",cartProducts=cartProducts,lenCart=lenCart,totalPrice=totalPrice)

@app.route("/Profil")
@login_required
def getProfilePage():
    customerId = BaseDatabaseManager.findCustomerIdFromCustomerUserName(session["username"])
    customerData=CustomerManager.getCustomerData(customerId[0])
    return render_template("profilim.html",username=session["username"],customerData=customerData)

@app.route("/Order",methods=["GET","POST"])
@login_required
def setOrder():
    if request.method=="GET":
        return redirect(url_for("getResponseHomePageIndex"))
    customerId = BaseDatabaseManager.findCustomerIdFromCustomerUserName(session["username"])
    basket=BaseDatabaseManager.getBasket(customerId[0])
    BaseDatabaseManager.addOrder(customerId[0])
    BaseDatabaseManager.cleanCartAfterOrder(customerId[0])
    maxOrderId=BaseDatabaseManager.getMaxOrderId(customerId[0])
    maxOrderId=maxOrderId[0]
    for i in range(0,len(basket)):
       BaseDatabaseManager.addOrderList(maxOrderId,basket[i][6],basket[i][2])
    return "işlem başarılı"

@app.route("/Search",methods=["GET","POST"])
def searchProductByName():
    if request.method=="GET":
        return redirect(url_for("getResponseHomePageIndex"))
    else:
        searchkeyword=request.form.get("searchkeyword")
        products=BaseDatabaseManager.getProductsWithSearchKeyword(searchkeyword)
        if products==[] or products==None:
            flash("Maalesef hiçbir ürün bulunamadı")
            return redirect(url_for("getResponseHomePageIndex"))
        else:
            lenOfList=len(products)
            return render_template("products.html",productsList=products,lenOfList=lenOfList)

        return searchkeyword

@app.route("/Siparislerim")
@login_required
def getSiparislerimPage():
    customerId = BaseDatabaseManager.findCustomerIdFromCustomerUserName(session["username"])
    orders=BaseDatabaseManager.getOrdersByCustomerId(customerId[0])
    orderItemList=list()
    for order in orders:
        orderItemList.append(BaseDatabaseManager.getOrderItemsByOrderId(order[0]))
    toplam=list()
    for i in orderItemList:
        toplam.append(len(i))
    return render_template("siparislerim.html",orders=orders,uzunluk=len(orders),toplam=toplam,orderItemList=orderItemList)

@app.route("/Siparislerim/<string:id>")
@login_required
def getOrderDetailsPage(id):
    return render_template("orderdetails.html",username=session["username"])


@app.route("/addComment",methods=["POST"])
def addCommentByProductId():
    customerId = BaseDatabaseManager.findCustomerIdFromCustomerUserName(session["username"])
    product_id = request.form.get('product_id')
    text_message= request.form.get("text_message")
    if text_message=="" or text_message==None or len(text_message)<5:
        flash("Lütfen yorumunuzu gözden geçiriniz")
        return redirect(request.referrer)
    CommentManager.addCommentByProductIdAndCustomerId(product_id,customerId[0],text_message)
    return redirect(request.referrer)


if __name__=="__main__":
    app.run(debug=True)
































