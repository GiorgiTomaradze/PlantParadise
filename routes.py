from flask import render_template,redirect
from extensions import app,db
from forms import AddProduct,AddBlog,SignUp,LogIn
import os
from models import Product,Blog,User,Category
from flask_login import login_user,logout_user,login_required,current_user



@app.route("/")
def home():
    role = "user"
    return render_template("index.html", products=Product.query.all(), role=role, active_page='home')

@app.route("/about")
def about():
    return render_template("about.html", products=Product.query.all(), active_page='about')

@app.route("/products/<int:category_id>")
@app.route("/products")
def products(category_id =None):
    if category_id:
        products = Category.query.get(category_id).products
    else:
        products=Product.query.all()
    return render_template("products.html",products=products, active_page='products')

@app.route("/blogs")
def blogs():
    return render_template("blogs.html", blogs=Blog.query.all(),active_page='blogs')

@app.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html", id=product_id)

    return render_template("product.html", product=product, products=Product.query.all(),)


@app.route("/blog/<int:blog_id>")
def blog(blog_id):
    blog = Blog.query.get(blog_id)
    if not blog:
        return render_template("404.html", id=blog_id)

    return render_template("blog.html", blog=blog, blogs=Blog.query.all(),)



@app.route("/add_product", methods=['POST','GET'])
@login_required
def add_product():
    if current_user.role != 'admin':  
        return redirect("/")
    form = AddProduct()
    if form.validate_on_submit():
        # image = form.image.data
        # file_path = os.path.join( "static" ,"images", image.filename)
        new_products = Product(name = form.name.data,
                               text = form.text.data,
                               price = form.price.data, 
                               image_url = form.image_url.data,
                               category_id = form.category_id.data
                               ) 

        db.session.add(new_products)
        db.session.commit()
        return redirect("/")
        # image.save((os.path.join(app.root_path, file_path )))
    else:
        print(form.errors)                
    return render_template("add_product.html", form=form)

@app.route("/add_blog", methods=['POST','GET'])
@login_required
def add_blog():
    form = AddBlog()
    if form.validate_on_submit():
        # image = form.image.data
        # file_path = os.path.join( "static" ,"images", image.filename)
        new_blog = Blog(name = form.name.data, text = form.text.data, image_url = form.image_url.data) 

        db.session.add(new_blog)
        db.session.commit()
        return redirect("/blogs")
        # image.save((os.path.join(app.root_path, file_path )))
    else:
        print(form.errors)                
    return render_template("add_blog.html", form=form)


@app.route("/edit_product/<int:product_id>", methods=['POST','GET'])
def edit_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html")
    
    form = AddProduct(name=product.name, text=product.text, image_url=product.image_url, price=product.price)

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.text = form.text.data
        product.image_url = form.image_url.data

        db.session.commit()
        return redirect("/")

    return render_template("edit_product.html",form=form)

@app.route("/delete_product/<int:product_id>", methods=['GET','DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html")
    
    db.session.delete(product)
    db.session.commit()
    return redirect("/")


@app.route("/edit_blog/<int:blog_id>", methods=['POST','GET'])
def edit_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if not blog:
        return render_template("404.html")
    
    form = AddBlog(name=blog.name, text=blog.text, image_url=blog.image_url)

    if form.validate_on_submit():
        blog.name = form.name.data
        blog.text = form.text.data
        blog.image_url = form.image_url.data

        db.session.commit()
        return redirect("/")

    return render_template("edit_blog.html",form=form)


@app.route("/delete_blog/<int:blog_id>", methods=['GET','DELETE'])
def delete_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if not blog:
        return render_template("404.html")
    
    db.session.delete(blog)
    db.session.commit()
    return redirect("/blogs")

@app.route("/singup", methods = ['POST','GET'])
def singup():
    form = SignUp()
    
    if form.validate_on_submit():
        new_user = User(username = form.username.data,
                        email = form.email.data,
                        password = form.password.data
                        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect("/")
    
    return render_template("singup.html", form=form)

@app.route("/login",methods= ['POST','GET'])
def login():
    form = LogIn()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect ("/")   
    return render_template("login.html", form=form)

    
@app.route("/logout",methods= ['POST','GET'])
def logout():
        print(current_user.password)
        logout_user()
        return redirect("/")

@app.route("/search/<string:product_name>")
def search(product_name):
    products = Product.query.filter(Product.name.ilike(f"%{product_name}%")).all()
    return render_template("products.html", products=products)