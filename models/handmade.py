db.define_table('sanpham',
   Field('spname'),
   Field('price','double'),
   Field('description','text'),
   Field('image','upload'),
   format='%(spname)s')
   
db.define_table('danhgia',  
   Field('rview','text'),
   Field('your_name'),
   Field('your_city'),
   Field('rating'),
   Field('tenpro','reference sanpham'),   
   format='%(rview)s')   

   

db.define_table('customer',
   Field('shipping_address'),
   Field('city'),
   Field('state'),
   Field('zip_code'),
   Field('country'),
   auth.signature),
   
session.cart = session.cart or {}
