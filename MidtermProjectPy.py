#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

def apriori(set_list,min_support):
    #initialize
    discarded = {}
    C = {}
    L = {}
    stop = False
    n = 1
    while stop == False:
        if n <= 1:
            for transaction in range(len(set_list)):
                for item in set_list[transaction]:
                    #prevent duplicate scans of same subset
                    if item not in C:
                        #prevent scans of already discarded items and previously non-frequent sets
                        if item not in discarded:
                            sup_count = scanTransactions({item},set_list)
                            C[item] = sup_count

            #print first scan results
            print('\nIteration {}'.format(n))
            print('C1 candidate set: \n')
            
            for i in C:
                print(i,':',C[i])
            #create L with items that meet minimum support requirement
            for item in C:
                sup_calc = C[item] / len(set_list)
                if item not in discarded:
                    if sup_calc >= min_support:
                        L[item] = C[item]
                    else:
                        discarded[item] = sup_calc
                    
            print('\nL1 set: \n')
            for i in L:
                print(i,':',L[i])
            print('#'*75)
            
            L_n = L #helps to generate sets for second iteration 
            n += 1
            if L is None:
                stop = True
                break
        elif n > 1:
            C_n = {}
            #union of the sets
            sets = []
            L_n = list(L_n)
            sets = getUnions(L_n,n)
            
            #save last iteration's results to a variable
            L_n_minus_1 = L_n
            
            #reinitialize L_n for the following iteration
            L_n = {}
            
            for i in range(len(sets)):
                support_count = scanTransactions(sets[i],set_list)
                C_n[tuple(sets[i])] = support_count
            if C_n == {}:
                stop = True
                break
            
            #print candidate set
            print('\nIteration {}\n'.format(n))
            print('C{} candidate set: \n'.format(n))
            for i in C_n:
                print(i,':',C_n[i])
            
            #calculate supports of each item in candidate set and prune
            for item in C_n:
                #if itemset is frequent, then subsets must also be frequent (and not in discarded)
                if item not in discarded:
                    sup_calc = C_n[item] / len(set_list)
                    if sup_calc >= min_support:
                        L_n[item] = C_n[item]
                    else:
                        discarded[item] = sup_calc
             
            #print passing set
            print('\nL{} set: \n'.format(n))
            for i in L_n:
                print(i,':',L_n[i])
            print('#'*75)
            
            if L_n == {} or L_n is None:
                stop = True
                return L_n_minus_1
                break
            n += 1
    return L_n_minus_1                    


##brute force method
def bruteForce(set_list,min_support):
    n = 1
    C = {}
    L = {}
    stop = False
    while stop == False:
        if n <= 1:
            for transaction in range(len(set_list)):
                for item in set_list[transaction]:
                    #prevent duplicate scans of same subset
                    if type(item) != type(['type']):
                        sup_count = scanTransactions({item},set_list)
                        C[item] = sup_count
                    else:
                        sup_count = scanTransactions(item,set_list)
                        C[item] = sup_count

            #print first results
            print('#' * 50)
            print('\nIteration {} Set:\n'.format(n))

            for i in C:
                print(i,':',C[i])
            C_n = C
            n += 1
        else:
            
            #union of the sets
            sets = []
            C_n = list(C_n)
            sets = getUnions(C_n,n)
            print(sets)
            #save last iteration's results to a variable
            C_n_minus_1 = C_n
            
            #reinitialize L_n for the following iteration
            C_n = {}
            
            for i in range(len(sets)):
                support_count = scanTransactions(sets[i],set_list)
                C_n[tuple(sets[i])] = support_count
            
            #print set
            #print('#' * 50)
            #print('\nIteration {}'.format(n))
            #print('C{} candidate set: \n'.format(n))
            
            #list that will hold a value if the minimum support is reached
            #if no sets meet the minimum support, the loop will break
            passing_supports = {}
            for i in C_n:
                print(i,':',C_n[i])
                if C_n[i] / len(set_list) >= min_support:
                    passing_supports[i] = C_n[i]
            
            if passing_supports == {} or passing_supports is None:
                stop = True
                return C_n_minus_1
                print('#'*75)
                break
            
            if C_n == {} or C_n is None:
                stop = True
                return C_n_minus_1
                print('#'*75)
                break
            n += 1    
            
            
def permutation(input_list):
    # If list is empty then there are no permutations
    if len(input_list) == 0:
        return []
    
    # If there is only one element, only perm possible
    if len(input_list) == 1:
        return [input_list]
    l = [] # empty list that will store current permutation
    for i in range(len(input_list)):
       m = input_list[i]
       # Extract input_list[i] or m from the list
       # remaining list
       remaining = input_list[:i] + input_list[i+1:]
 
       # Generating all permutations where m is first
       for p in permutation(remaining):
           l.append([m] + p)
    return l
        

def generateRules(input_set,min_support,min_confidence,transactions):
    perms = permutation(input_set)
    rules = []
    for i in perms:
        sup_i = scanTransactions(i,transactions) / len(transactions)
        if sup_i >= min_support:
            for j in range(1,len(i)+1):
                rule = []
                left_side = i[:j]
                if len(left_side) != len(i):
                    #prevent duplicates
                    left = left_side
                    right = set(i) - set(left_side)
                    both = i
                    counts_both = scanTransactions(both,transactions)
                    counts_left = scanTransactions(left,transactions)
                    counts_right = scanTransactions(list(right),transactions)
                    sup_both = counts_both / len(transactions)
                    sup_left = counts_left / len(transactions)
                    sup_right = counts_right / len(transactions)
                    conf = sup_both / sup_left
                    rule = [set(left),right,conf]
                    if sup_left >= min_support:
                        if rule not in rules:
                            if (sup_left != 0) and (sup_right >= min_support):
                                if conf >= min_confidence:
                                    rules.append(rule)
    #remove duplicates
    for item in rules:
        #print(type(rules[item][0]))
        for item2 in rules:
            #print(item2[0])
            if item[0] == item2[0] and item != item2:
                rules.remove(item2)
    #print rules
    for rule in rules:
        print(rule[0],'->',rule[1],'confidence: ',rule[2])

def printRules(result_list,min_supp,min_conf,transactions):
    print('#'*75)
    print("\nAssociation Rules that meet minimum confidence: \n")
    for i in result_list:
        generateRules(list(i),min_supp,min_conf,transactions)                           




#main program
if __name__ == '__main__':
    stop_program = False
    while stop_program == False:
        try:
            db_choice = str(input("Please enter an integer 1-5 to indicate choice of database. Enter 0 if you wish to exit: "))
            if db_choice == str(0):
                stop_program = True
                break
            else:
                import time
                conn = create_connection(r"C:\Users\Nick\CS634_Data_Mining\auto_best_sellers_{}.db".format(db_choice))
                support_input = float(input("Please enter a minimum support (0.0-1.0): "))
                conf_input = float(input("Please enter a minimum confidence (0.0-1.0): "))
                #transactionsList = getTransactions(conn,20)
                
                #Apriori algorithm 
                start_time = time.time()
                results = apriori(getTransactions(conn,20),support_input)
                print("Apriori time: %s seconds " %(time.time() - start_time))
                print('#' * 75)
                printRules(results,support_input,conf_input,getTransactions(conn,20))
                
                #brute force algorithm
                start_time = time.time()
                brute_result = bruteForce(getTransactions(conn,20),support_input)
                print('#' * 75)
                print("Brute force time: %s seconds " %(time.time() - start_time))
                print('#' * 75)
                printRules(brute_result,support_input,conf_input,getTransactions(conn,20))

                stop_program = True
                break
        except:
            print("Not a valid choice")



# In[ ]:




