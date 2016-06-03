def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))

def register():
    id_user= db.auth_user.insert(
        username=request.vars['username'],
        password=db.auth_user.password.validate(request.vars['password'])[0],
        first_name=request.vars['first_name'],
        last_name=request.vars['last_name'],
        email = request.vars['email'])
    return
    


@service.jsonrpc
def systemListMethods():
    return ['add','sub','check_in','restaurant_menu','reserve_table','order_item']

@service.jsonrpc
def add(a,b):
    return a+b
@service.jsonrpc
def sub(a,b):
    return a-b

@service.jsonrpc
def restaurants_area(latitude=0, longitude=0, num=10):
	
	count = db(db.restaurant).count()
	
	session.num = session.num or num
	session.count = (session.count or 0) + 1
	session.range_start = session.range_start or 0
	session.range_end = session.range_end or count
	
	session.latitude = session.latitude or latitude
	session.longitude = session.longitude or longitude
	
	point = lambda lat,lon: Point(str(lat) + '; ' + str(lon))
	p = point(session.latitude, session.longitude)
	d = distance.distance
	
	restaurants = db(db.restaurant).select()	
	restaurants = restaurants.sort(lambda row: d(p,point(row.latitude, row.longitude)).km)
	
	session.range_start = session.range_start if count < (int(session.count)-1)*int(session.num) else (int(session.count)-1)*int(session.num)
	session.range_end = session.range_end if count < int(session.count)*int(session.num) else int(session.count)*int(session.num)
	
	return restaurants[session.range_start:session.range_end]

@service.jsonrpc
def check_in(restaurant_id):
    session.restaurant_id = db.restaurant(restaurant_id).id
    return dict(restaurant_id=session.restaurant_id)

@service.jsonrpc
def item_image(image_id):
    return dict(url=db.restaurant_images(image_id))
    
@service.jsonrpc
def restaurant_menu():
    menu = db.restaurant(session.restaurant_id).menu
    menuitems = db(db.item.id.belongs(menu.menuitems)).select(db.item.ALL)
    return menuitems

@service.jsonrpc
def reserve_table(capacity):
    restaurant = db.restaurant(session.restaurant_id)
    session.table_id = db.restaurant_table.insert(
        user_id = auth.user,
        restaurant=restaurant,
        capacity=capacity,
        booked_on=datetime.datetime.now())
    return dict(table_id=session.table_id)

@service.jsonrpc
def order_item(item_id,quantity=1,refill=False):
    restaurant_table = db.restaurant_table(session.table_id)
    restaurant_order = db.restaurant_order.insert(
        user_id = auth.user,
        item=item_id,
        quantity=quantity,
        restaurant_table=restaurant_table,
        ordered_on=datetime.datetime.now())
    return dict(order_id=restaurant_order)

@service.jsonrpc
def count():
    session.counter = (session.counter or 0) + 1
    return dict(counter=session.counter, now=request.now)
