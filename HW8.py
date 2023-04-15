# Your name: Claudia VanValkenburg
# Your student id: 07533756
# Your email: vanvalce@umich.edu

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''SELECT restaurants.name, categories.category, buildings.building, restaurants.rating '''
            '''FROM restaurants '''
            '''JOIN categories ON restaurants.category_id = categories.id '''
            '''JOIN buildings ON restaurants.building_id = buildings.id;''')
    lines = cur.fetchall()
    rest_data = {}
    for name, category, building, rating in lines:
        rest_data[name] = {'category': category, 'building':building, 'rating': rating}
    cur.close()
    conn.close()
    return rest_data

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''
        SELECT categories.category, COUNT(restaurants.id) AS count FROM categories
        JOIN restaurants ON categories.id = restaurants.category_id
        GROUP BY categories.category ORDER BY count ''')
    categories = cur.fetchall()
    cat_dict = dict(categories)
    conn.close()
    fig, ax = plt.subplots(figsize=(12,6))
    fig.subplots_adjust(wspace=.6, left = .4)
    ax.barh(list(cat_dict.keys()), list(cat_dict.values()))
    ax.set_xlabel("Number of Restaurants")
    ax.set_ylabel("Restaurant Categories")
    ax.set_xlim([0,5])
    ax.set_title("Types of Restaurant on South University Ave")
    plt.show()
    return cat_dict

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(
        '''SELECT restaurants.name FROM restaurants 
        JOIN buildings ON restaurants.building_id = buildings.id
        WHERE buildings.building = ?
        ORDER BY restaurants.rating DESC''', (building_num,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    names = [row[0]for row in results]
    return names

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''SELECT categories.category, AVG(restaurants.rating) as avg_rating
                FROM categories
                JOIN restaurants ON categories.id = restaurants.category_id
                GROUP BY categories.category ORDER BY AVG (restaurants.rating) DESC''')
    cat_results = cur.fetchall()
    cur.execute('''SELECT categories.category, AVG(restaurants.rating) as avg_rating
                FROM categories
                JOIN restaurants ON categories.id = restaurants.category_id
                GROUP BY categories.category ORDER BY AVG (restaurants.rating) DESC''')
    high_cat = cur.fetchone()
    categories = [row[0] for row in cat_results]
    cat_avgs = [row[1] for row in cat_results]
    cur.execute('''SELECT buildings.building, AVG(restaurants.rating) as avg_rating 
                FROM buildings
                JOIN restaurants ON buildings.id = restaurants.building_id
                GROUP BY buildings.building ORDER BY AVG (restaurants.rating) DESC''')
    build_results = cur.fetchall()
    cur.execute('''SELECT buildings.building, AVG(restaurants.rating) as avg_rating 
                FROM buildings
                JOIN restaurants ON buildings.id = restaurants.building_id
                GROUP BY buildings.building ORDER BY AVG (restaurants.rating) DESC''')
    high_build = cur.fetchone()
    buildings = [row[0] for row in build_results]
    build_avgs = [row[1] for row in build_results]
    fig, (ax1, ax2) = plt.subplots(2,1, figsize=(10,8))
    fig.subplots_adjust(wspace=.1, hspace = .5, left=.3)
    ax1.set_title("Average Restaurant Ratings by Category")
    ax1.set_xlabel("Ratings")
    ax1.set_ylabel("Categories")
    cat_y_pos = range(len(categories))
    ax1.set_xlim([0,5])
    ax1.barh(cat_y_pos, cat_avgs[::-1], align = 'center')
    ax1.set_yticks(cat_y_pos)
    ax1.set_yticklabels(categories)

    
    ax2.set_title("Average Restaurant Ratings by Building")
    ax2.set_xlabel("Ratings")
    ax2.set_ylabel("Buildings")
    build_y_pos = range(len(buildings))
    ax2.set_xlim([0,5])
    ax2.set_ylim([-1,len(buildings)])
    ax2.barh(build_y_pos, build_avgs[::-1], align = 'center')
    ax2.set_yticks(build_y_pos)
    ax2.set_yticklabels(buildings)

    plt.subplots_adjust(wspace = .6)

    cur.close()
    conn.close()
    return [(high_cat[0], high_cat[1]), (high_build[0], high_build[1])]

#Try calling your functions here
def main():
    db = "South_U_Restaurants.db"

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
