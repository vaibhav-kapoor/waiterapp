# -*- coding: utf-8 -*-

db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])

def make_thumbnail(table, image_id, size=(150, 150)):
	import os
	from PIL import Image
	this_image = table(image_id)
	im = Image.open(os.path.join(request.folder), 'uploads',
		this_image.image)
	im.thumbnail(size, Image.ANTIALIAS)
	thumbnail = 'document.thumbnail.%s.png' % this_image.image.split('.')[2]
	im.save(os.path.join(request.folder, 'uploads', thumbnail), 'png')
	this_image.update_record(thumbnail=thumbnail)
	return

def resize_image(image, size, path):
    from PIL import Image
    import os.path
    try:
        img = Image.open('%sstatic/uploads/%s' % (request.folder, image))
        img.thumbnail(size, Image.NEAREST)
        root, ext = os.path.splitext(image)
        filename = '%s_%s%s' %(root, path, ext)
        img.save('%sstatic/uploads/%s' % (request.folder, filename))
    except Exception, e:
        return e
    else:
        return filename

def render_image(ids,row): 
	span = SPAN() 
	for id in ids: 
		img = db.restaurant_images(id)
		if img:
			span.append(A(img.filename,_href=URL('download',args=img.image))) 
	return span   

from gluon.tools import Auth,Crud, Service, prettydate
from gluon.contrib.login_methods.basic_auth import basic_auth
from gluon.tools import geocode
import datetime, os
crud, service = Crud(db), Service(), 
auth = Auth(db)
auth.define_tables(username=True)
auth.settings.allow_basic_login = True
auth.settings.hmac_key = 'sha512:a-pass-phrase'
auth.settings.password_min_length = 4
auth.settings.login_after_registration = True
auth.settings.create_user_groups = False
auth.settings.login_email_validate = False

auth.settings.login_methods = [basic_auth('http://127.0.0.1:8000')]


db.define_table('restaurant_images',
	Field('image', 
		'upload',
		uploadfolder=os.path.join(request.folder,'static'),
		uploadseparate=True
		),
	Field('uploaded_by', db.auth_user),
	format='%(id)s')

db.define_table('item',
	Field('name'),
	Field('description', 'text'),
	Field('category'),
	Field('price', 'double'),
	Field('images', 'list:reference restaurant_images'),
	format='%(name)s')

db.define_table('menu',
	Field('menuitems', 'list:reference item'),
	format='%(id)s')

db.define_table('restaurant_table',
	Field('user_id', 'reference auth_user'),
	Field('table_active', 'boolean', default=False),
	Field('restaurant', 'reference restaurant'),
	Field('capacity', 'integer'),
	Field('booked_on', 'datetime'))
	
db.define_table('restaurant_order',
	Field('user_id', 'reference auth_user'),
	Field('item', 'reference item'),
	Field('refill', 'boolean', default=False),
	Field('quantity', 'integer', default=1),
	Field('restaurant_table', 'reference restaurant_table'),
	Field('ordered_on', 'datetime'))

db.define_table('bill',
	Field('restaurant_table', 'reference restaurant_table'),
	Field('restaurant_order', 'list:reference order'),
	Field('billed_on', 'datetime'),
	Field('total_bill', 'double'))

db.define_table('restaurant',
	Field('name'),
	Field('address'),
	Field('latitude',
			compute=lambda r: geocode(r.address)[0]),
	Field('longitude', 
			compute=lambda r: geocode(r.address)[1]),
	Field('phone'),
	Field('url'),
	Field('menu', 'reference menu'),
	Field('images', 'list:reference restaurant_images'),
	format='%(latitude; longitude)s')

session.connect(request, response, db)
