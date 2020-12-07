import requests
from tkinter import *
import sys
from pymongo import MongoClient
import math
import numpy
from collections import Counter, defaultdict
from food_functions import change_none_values_postcode
from mongo import Mongo
authorities_url = 'http://ratings.food.gov.uk/authorities/json'
url = 'http://ratings.food.gov.uk/search-address/en-GB/birmingham/1/5000/json'
class FoodRater:
    def __init__(self):
        self.cursor = Mongo()
        self.auth_codes = self.get_authority_codes(authorities_url)

    def get_response(self, url):
        response = requests.get(url)
        assert response.status_code == 200
        return response.json()
    
    def return_response(self, url):
        response = requests.get(url)
        assert response.status_code == 200
        return response
    
    def get_authority_codes(self, url):
        """Return the authority codes for each authority in the uk. Then we can get started!"""
        data = self.get_response(url)
        auth_codes = [{x['Name']: x['LocalAuthorityIdCode']} for x in data['ArrayOfWebLocalAuthorityAPI']['WebLocalAuthorityAPI']]
        return auth_codes[5:]   # remove the first five, which are not authority codes


    def get_num_items(self, url):
        """Returns the number of locations to be analysed."""
        response = self.get_response(url)               
        try:
            headers = response['FHRSEstablishment']['Header']
            items = headers['ItemCount']
            return int(items)
        except KeyError:
            print('There is no Header.')

    def get_page_count(self, items):
        """Returns the number of pages needed to obtain all the locations from the api"""
        items = items
        pages_needed = items / 5000
        pages = int(math.ceil(pages_needed))
        return pages
    
    def url_creator(self, code):
        url = f'http://ratings.food.gov.uk/enhanced-search/en-GB/^/^/ALPHA/0/{code}/1/30/json'
        return url

    def url_generator(self, code, pages):
        while pages > 0:
            data = yield self.get_response(f'http://ratings.food.gov.uk/enhanced-search/en-GB/^/^/ALPHA/0/{code}/{pages}/5000/json')              
            pages -= 1

    def get_restaurants(self,response):
        data = response['FHRSEstablishment']['EstablishmentCollection']['EstablishmentDetail']
        return data



    def make_objects(self, data):
        cleaned_data = []
        # print(data[0])
        if len(data) > 1:
            for x in data:
                for i in x:
                    cleaned_restaurant = {
                        'BusinessId': i['LocalAuthorityBusinessID'],  # build the model for the data, extracting the parts we want to use
                        'BusinessName': i['BusinessName'],
                        'BusinessType': i['BusinessType'],
                        'Rating': i['RatingValue'],
                        'Score': i['Scores'],
                        'Geocode': i['Geocode'],
                        'Postcode': i['PostCode']
                    }
                    cleaned_data.append(cleaned_restaurant)
        else:
            for i in data[0]:
                cleaned_restaurant = {
                    'BusinessId': i['LocalAuthorityBusinessID'],  # build the model for the data, extracting the parts we want to use
                    'BusinessName': i['BusinessName'],
                    'BusinessType': i['BusinessType'],
                    'Rating': i['RatingValue'],
                    'Score': i['Scores'],
                    'Geocode': i['Geocode'],
                    'Postcode': i['PostCode']
                }
                cleaned_data.append(cleaned_restaurant)

        cleaned_data = change_none_values_postcode(cleaned_data)
        print(len(cleaned_data))
        return cleaned_data
    

    def match_ratings_ps(self, data):
       
        dct = defaultdict(list)

        for i in data:
            
            if i['Rating'] == 'AwaitingInspection':
                    continue
            if i['Rating'] == 'Awaiting Inspection':
                    continue
            elif i['Rating'] == 'Exempt':
                    continue
            elif i['Rating'] == 'Pass':
                    i['Rating'] = 5
                    data.append(i['Rating'])
            else:
                dct[i['Postcode'][:4]].append(int(i['Rating']))
                continue
            
        return dct

    def display_data(self, data):
        new = Tk()
        new.title("Cities")
        new.geometry("500x500")
        frame = Frame(new)
        frame.pack(fill=BOTH, expand=TRUE)
        label = Label(frame, text='Here are the average ratings for each postcode in the city!')
        label.pack()
        t = Text(frame, height=35, width=50)
        t.pack()
        t.delete(1.0, END)
        for key, value in data.items():
            t.insert(END, f'Postcode: {key} : Average Rating: {numpy.mean(value)}')
            t.insert(END, '\n')

  
    
    def show_cities(self):
        def get_selection():
            selection = mylist.curselection()
            t = [x for x in self.auth_codes[selection[0]]]
            code = self.auth_codes[selection[0]][t[0]]
            url = self.url_creator(code)
            items = self.get_num_items(url)
            print(items)
            page_count = self.get_page_count(items)
            data1 = []
            for i in self.url_generator(code, page_count):
                data1.append(i)
            main_data = [self.get_restaurants(x) for x in data1]
            data = self.make_objects(main_data)
            final_data = self.match_ratings_ps(data)
            self.display_data(final_data)
            print('Matched the ratings and the postcodes')
        cities = self.auth_codes
        new = Tk()
        new.title("Cities")
        new.geometry("500x500")
        frame = Frame(new)
        frame.pack(fill=BOTH, expand=TRUE)
        label = Label(frame, text='Here are the cities and their respective authority codes.')
        label.pack()
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        mylist = Listbox(frame, yscrollcommand = scrollbar.set )
        for line in cities:
            for city, code in line.items():
                mylist.insert(END, f"{city}: {code}")

        mylist.pack(side = LEFT, fill=BOTH, expand=TRUE, padx=5, pady=5)
        scrollbar.config( command = mylist.yview )
        bottomframe = Frame(new)
        bottomframe.pack( side = BOTTOM )
        button = Button(bottomframe, text='Select a city to get started', command=get_selection)
        button.pack(side=BOTTOM)
        
    def show_restaurants(self):
        def get_selection():
            selection = mylist.curselection()
            t = [x for x in self.auth_codes[selection[0]]]
            code = self.auth_codes[selection[0]][t[0]]
            url = self.url_creator(code)
            items = self.get_num_items(url)
            print(items)
            page_count = self.get_page_count(items)
            data1 = []
            for i in self.url_generator(code, page_count):
                data1.append(i)
            main_data = [self.get_restaurants(x) for x in data1]
            data = self.make_objects(main_data)
            self.display_restaurant_data(data)
        cities = self.auth_codes
        new = Tk()
        new.title("Cities")
        new.geometry("500x500")
        frame = Frame(new)
        frame.pack(fill=BOTH, expand=TRUE)
        label = Label(frame, text='Here are the cities and their respective authority codes.')
        label.pack()
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        mylist = Listbox(frame, yscrollcommand = scrollbar.set )
        for line in cities:
            for city, code in line.items():
                mylist.insert(END, f"{city}: {code}")

        mylist.pack(side = LEFT, fill=BOTH, expand=TRUE, padx=5, pady=5)
        scrollbar.config( command = mylist.yview )
        bottomframe = Frame(new)
        bottomframe.pack( side = BOTTOM )
        button = Button(bottomframe, text='Select a city to get started', command=get_selection)
        button.pack(side=BOTTOM)
    def display_restaurant_data(self, data):
        new = Tk()
        new.title("Cities")
        new.geometry("800x500")
        frame = Frame(new)
        frame.pack(fill=BOTH, expand=TRUE)
        label = Label(frame, text='Here are the ratings for each restaurant/cafe in the city!')
        label.pack()
        t = Text(frame, height=35, width=50)
        t.pack(fill=BOTH, expand=TRUE)
        t.delete(1.0, END)
        for city in data:
            t.insert(END, f'{city["BusinessName"]}: {city["Rating"]}')
            # t.insert(END, city['Postcode'])
            t.insert(END, '\n')
        

    def get_total_ratings(self, data, postcode): 
        def get_rating():
            rating = int(input('Please enter rating: '))
            return rating
        rating = get_rating()
        data1 = get_ratings_pc(data, postcode)
        c = Counter(data1)
        return c[rating]

    # b12 = get_total_ratings(cleaned_data, 'B12')
    # print(b12)
    def run_app(self):      
        window = Tk()
        window.title("My App")
        label = Label(text='Welcome to the food rating app. ')
        label.grid(row=0, column=0)
        button_1 = Button(text='See ratings by city and postcode', command= self.show_cities, padx=40)
        button_2 = Button(text='Display restaurants and their ratings', command=self.show_restaurants, padx=40)
        button_3 = Button(text="Make new drink", padx=40)
        button_1.grid(row=1, column =0)
        button_2.grid(row=2, column=0)
        button_3.grid(row=3, column=0)
        t = Text(window, height=15, width=50)
        t.grid(row=4, column=0)
        window.mainloop()





if __name__ == '__main__':
    app = FoodRater()
    app.run_app()


    


