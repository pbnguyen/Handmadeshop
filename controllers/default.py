def index():
   
   products = db(db.sanpham).select() 
   reviews = db(db.danhgia).select()             
   return locals()
      
def detail():   
   rvs = db(db.revs.ALL).select()
   return locals()
      
def user():
    return dict(form=auth())

def download():
    return response.download(request,db)

@auth.requires_login()
def cart():
    if not session.cart:
       session.flash = 'Add something to shopping cart'
       redirect(URL('index'))      
    return dict(cart=session.cart)

@auth.requires_login()
def review():
    form = SQLFORM(db.danhgia)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
       
    return dict(form=form)

@auth.requires_login()
def buy():
    total = sum(db.sanpham(id).price*qty for id,qty in session.cart.items())   
    form = SQLFORM(db.customer)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('purchase'))
    elif form.errors:
        response.flash = 'form has errors'
        response.flash = 'please fill out the form'
       
    return dict(cart=session.cart, total=total, form=form) 

@auth.requires_login()
def purchase():
    return locals()
@auth.requires_login()

def creditcard():
    if not session.cart:
       session.flash = 'Add something to shopping cart'
       redirect(URL('index'))
    import uuid
    from gluon.contrib.AuthorizeNet import process
    invoice = str(uuid.uuid4())
    total = sum(db.sanpham(id).price*qty for id,qty in session.cart.items())
    form = SQLFORM.factory(
               Field('creditcard',
	             requires=IS_NOT_EMPTY()),
               Field('expiration',default='',
                      requires=IS_MATCH('\d{2}/\d{4}')),
               Field('cvv',default='',requires=IS_MATCH('\d{3}')))
    if form.accepts(request,session):
        if process(form.vars.creditcard,form.vars.expiration,
                   total,form.vars.cvv,0.0,invoice,testmode=True):        
            session.cart.clear()
            session.flash = 'Thank you for your order'
        else:
            response.flash = "payment rejected (please contact us)"
    return dict(cart=session.cart,form=form,total=total)
@auth.requires_login()
def invoice():
    return dict(invoice=request.args(0))

@auth.requires_signature()
def cart_callback():
    id = int(request.vars.id)
    if request.vars.action == 'add':
        session.cart[id]=session.cart.get(id,0)+1
    if request.vars.action == 'sub':
        session.cart[id]=max(0,session.cart.get(id,0)-1)
    return str(session.cart[id])

@auth.requires_login()
def myorders():
    orders = db(db.sale.buyer==auth.user.id).select(orderby=~db.sale.created_on)
    return dict(orders=orders)

def about():
   return locals()
