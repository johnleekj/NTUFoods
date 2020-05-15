# database containing store details.

#stores open everyday / close on 1900
#cantonese roast duck store: breakfast menu (till 1630)
#chicken rice store: alternate menus (odd and even days)
#handmade noodle store
#indian cuisine store

#stores open from Mon to Thur / close on 2100
#mini wok store
#soup delight store
#western food store
#yong tau foo store

import tkinter as tk
import pickle

class stalls:
    
    def __init__(self):
        
        self.pickle_in = open("stallandmenus.pickle","rb")       
        self.database = pickle.load(self.pickle_in)
 
    def fooditems(self, root, database, storename, menu, menulist): #food and it's price
        for x in database[storename][menu]:
            menulist.append(str(x))
    
    def foodprices(self, root, database, storename, menu, menulist):
        for x in database[storename][menu]:
            menulist.append(str(database[storename][menu][x]))
    
    def printtxt(self):
        pickle_in = open("stallandmenus.pickle","rb")
        menuandstallsdict = pickle.load(pickle_in)
        print(menuandstallsdict)



          
                      
        