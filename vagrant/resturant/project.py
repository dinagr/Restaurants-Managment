from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

menuItems = session.query(MenuItem).all()
for item in menuItems:
    session.delete(item)
resturants = session.query(Restaurant).all()
for r in resturants:
    session.delete(r)
session.commit()

rest1 = Restaurant(name = "Great Resturant")
session.add(rest1)

menuItem11 = MenuItem(restaurant_id = 1, name = "Soup", price = "3$", description = "Onion soup")
session.add(menuItem11)

menuItem12 = MenuItem(restaurant_id = 1, name = "Chicken", price = "18$", description = "fried chicken")
session.add(menuItem12)

menuItem13 = MenuItem(restaurant_id = 1, name = "ice cream", price = "9$", description = "chocolate ice cream")
session.add(menuItem13)

rest2 = Restaurant(name = "Dina's Pizza place")
session.add(rest2)

menuItem21 = MenuItem(restaurant_id = 2, name = "Pizaa margarita", price = "12$", description = "tomato souce, mozzarela")
session.add(menuItem21)

menuItem22 = MenuItem(restaurant_id = 2, name = "Hawaian Pizza", price = "20$", description = "Pinapple, mozzarela")
session.add(menuItem22)

rest3 = Restaurant(name = "Chocolate House")
session.add(rest3)

menuItem31 = MenuItem(restaurant_id = 3, name = "Chocolate cake", price = "7$", description = "Chocolate, chocolate and chocolate")
session.add(menuItem31)

menuItem32 = MenuItem(restaurant_id = 3, name = "Crazy waffle", price = "11$", description = "strawbery, banana, pecan, weaped cream")
session.add(menuItem32)

menuItem33 = MenuItem(restaurant_id = 3, name = "Best milkshake", price = "9$", description = "Chocolate, strawbaey, mango")
session.add(menuItem33)

menuItem33 = MenuItem(restaurant_id = 3, name = "Coconut mountain", price = "25$", description = "Coconut desert")
session.add(menuItem33)

session.commit()

# show all resturants

@app.route('/')
@app.route('/restaurants/')
def restaurant():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurantmenu.html', restaurants=restaurants)

# Create a new restaurant

@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurantMenu():
    if request.method == 'POST':
        newRest = Restaurant(
            name=request.form['name'])
        session.add(newRest)
        session.commit()
        flash("A new resturnat was created successfully!")
        return restaurant()
    else:
        return render_template('newrestaurantmenu.html') 
    
# edit a restaurant

@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    rest = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        rest.name=request.form['name']
        session.commit()
        flash("The retaurant name was edited successfully!")
        return restaurant()
    else:
        return render_template('editrestaurantmenu.html', restaurant_id=restaurant_id, restaurant=rest)

# delete a restaurant

@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    rest = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(rest)
        session.commit()
        flash("The restaurant was deleted successfully!")
        return restaurant()
    else:
        return render_template('deleterestaurantmenu.html', restaurant_id=restaurant_id,  restaurant=rest)

# Show specific restaurant

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items = items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("A new menu item was created successfully!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id) 

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem=session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        #item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id)
        if (request.form['name'] <> ''):
            editedItem.name=request.form['name']
        if (request.form['description'] <> ''):
            editedItem.description=request.form['description']
        if (request.form['price'] <> ''):
            editedItem.price=request.form['price']
        session.commit()
        flash("The menu item was edited successfully!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id = menu_id, item=editedItem)

# Task 3: Create a route for deleteMenuItem function here 

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem=session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("The menu item was deleted successfully!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id = menu_id, item=deletedItem)

#Making an API endpoint (Get Requests)
    
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurant = session.query(Restaurant).all()
    return jsonify(MenuItems=[i.serialize for i in restaurant])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/', methods=['GET', 'POST'])
def menuItemJson(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
    return jsonify(MenuItems=[item.serialize])

if __name__ == '__main__':
    app.secret_key = 'super_scret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
