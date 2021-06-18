#!/usr/bin/env python
# coding: utf-8

# In[3]:


#import libraries
import random
import sqlite3
from sqlite3 import Error

#define bestseller list to randomly generate transactions as starting point
bestsellerslist = ['Windshield Sun Shade','Car Vacuum','Car Trash Can','Wiper Blade','Window Shade','Headrest Hanger','Windshield Sun Shade plus Steering Wheel Sun Shade','Car Seat Covers','2-Piece Sun Shade','Microfiber Cleaning Cloth','Garbage Guard','Gel Seat Cushion','Trunk Organizers and Storage','Rubber Floor Mats','RV Sewer Hose','Office Chair Seat Cushion','Cabin Filter with Activated Carbon','LED Car Strip Lights','Cleaning Gel','RV Toilet Treatment','Cleaning Putty','Bumper Retainer Clips','Bike Phone Holder','10-Foot RV Sewer Hose Extension Kit','Car Wax Polish Spray','Interior Cleaner','Diamond Steering Wheel Cover','Portable Car Vacuum','180 Battery Organizer','Heavy Duty Threadlocker']

#generate 20 transactions
def generate_transactions(inputlist):
    index = 0
    transactions = []
    while index < 20:
        
        #generate random number of items in each shopping transaction
        transnum = random.randrange(1,20,1)

        #generate transactions using the transnum
        transaction = random.sample(inputlist,transnum)

        #sort alphabetically and append to transactions list
        transaction.sort()
        transactions.append(transaction)

        index +=1
    
    return transactions

#create database(s) and relevant tables

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def create_table(conn,name):
    """ create table from the create_table_statement"""
    try:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS %s (item_id text PRIMARY KEY)""" %(name))
        print('Table created')
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
    

def populate_table(conn,tablename,itemname):
    """populate table from populate_statement"""
    try:
        c = conn.cursor()
        c.execute("""INSERT INTO %s (item_id) VALUES (?)""" %(tablename),[itemname])
        print('Table populated')
        conn.commit()
        conn.close()
    except Error as e:
        print(e)


def query(conn,statement):
    try:
        c = conn.cursor()
        c.execute(statement)
        conn.commit()
        row = c.fetchall()
        print(row)
        conn.close()
    except Error as e:
        print(e)
        
def main():
    database = r"C:\Users\Nick\CS634_Data_Mining\auto_best_sellers_1.db"
    
    index = 0
    #create the 20 transaction tables
    for index in range(len(transactions)):
        #create database connection
        conn = create_connection(database)
        if conn is not None:
            table_name = 'transaction_'+str(index)
            create_table(conn,table_name)
            #populate each table with the items in each respective transaction
            for item in transactions[index]:
                item_name = item
                conn = create_connection(database)
                populate_table(conn,table_name,item_name)
        else:
            print("Cannot connect to database")

## Initialize the algorithm

def generateGroups(input_set,size):
    input_set = list(input_set)
    if size == 0:
        return [[]]
    new_set = []
    for index in range(0,len(input_set)):
        item = input_set[index]
        remaining = input_set[index + 1:]
        for j in generateGroups(remaining,size-1):
            new_set.append([item]+list(j))
    return new_set

def getItems(conn,transnum):
    try:
        items_list = []
        c = conn.cursor()
        #query the data and result will be in lexographical order
        c.execute("SELECT item_id FROM %s ORDER BY item_id ASC"%('transaction_'+str(transnum)))
        transaction = c.fetchall()
        for item in transaction:
            items_list.append(item[0])
        return items_list
        conn.close()
    except Error as e:
        print(e)

def getTransactions(conn,translength):
        transactions = []
        for i in range(translength):
            transaction = getItems(conn,i)
            transactions.append(transaction)
        return transactions

def scanTransactions(itemset,transactions):
    count = 0
    for i in range(len(transactions)):
        if set(itemset).issubset(transactions[i]):
            count +=1
    return count   

def getUnions(set1,n):
    sets = []
    for item in set1:
        if type(item) == type(''):
            item = [item]
            for i in set1:
                if type(i) == type(''):
                    i = [i]
                    if item != i:
                        u = set(item).union(set(i))
                        if u not in sets and len(u) == n:
                            sets.append(u)
        else:
            itemset = list(item)
            #print(set(itemset))
            for j in set1:
                if type(j) != type((1,2)):
                    u = set(itemset).union({j})
                    if u not in sets and len(u) == n:
                        sets.append(u)
                else:
                    itemset2 = set(list(j))
                    u = itemset2.union(itemset)
                    if u not in sets and len(u) == n:
                        sets.append(u)     
    return sets


import time
#conn = create_connection(r"C:\Users\Nick\CS634_Data_Mining\auto_best_sellers_5.db")
#transactionsList = getTransactions(conn,20)
#print(transactionsList)

#Apriori algorithm 
#start_time = time.time()
#results = apriori(transactionsList,0.4)
#print("Apriori time: %s seconds " %(time.time() - start_time))
#print('#' * 75)
#generateAssociationRules(results,0.4,0.8,transactionsList)                       
                            

#brute force algorithm
#start_time = time.time()
#brute_result = bruteForce(transactionsList,.4)
#print('#' * 75)
#print("Brute force time: %s seconds " %(time.time() - start_time))
#generateAssociationRulesBrute(brute_result,.4,.8,transactionsList)



# In[12]:


#create database(s) and relevant tables

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def create_table(conn,name):
    """ create table from the create_table_statement"""
    try:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS %s (item_id text PRIMARY KEY)""" %(name))
        print('Table created')
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
    

def populate_table(conn,tablename,itemname):
    """populate table from populate_statement"""
    try:
        c = conn.cursor()
        c.execute("""INSERT INTO %s (item_id) VALUES (?)""" %(tablename),[itemname])
        print('Table populated')
        conn.commit()
        conn.close()
    except Error as e:
        print(e)


def query(conn,statement):
    try:
        c = conn.cursor()
        c.execute(statement)
        conn.commit()
        row = c.fetchall()
        print(row)
        conn.close()
    except Error as e:
        print(e)
            
if __name__ == '__main__':
    for i in range(1,6):
        print('\n','#'*25,'Database {}'.format(i),'#'*75,'\n')
        for j in range(1,20):
            print("\nTransaction {}:".format(j),'\n')
            statement = "SELECT * FROM transaction_{} ORDER BY item_id ASC".format(j)
            query(create_connection(r"C:\Users\Nick\CS634_Data_Mining\auto_best_sellers_{}.db".format(i)),statement)


# In[ ]:




