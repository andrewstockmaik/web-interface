import web

db = web.database(dbn='sqlite',
        db='AuctionBase.db'
    )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except Exception as e:
#     t.rollback()
#     print str(e)
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    # select [column] from [table]
    query_string = 'select Time from CurrentTime'
    results = query(query_string)
    # results returns as array, need Time from first (only) entry
    return results[0].Time

# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemById(item_id):
    query_string = 'select * from Items where item_ID = $itemID'
    try:
        result = query(query_string, { 'itemID': item_id })
        return result[0]
    except IndexError:
        return None

def getUserById(user_id):
    query_string = 'select * from Users where UserID = $userID'
    try:
        result = query(query_string, { 'userID': user_id })
        return result[0]
    except IndexError:
        return None

def getStatusByItemId(item_id):
    query_string = 'select * from Items where item_ID = $itemID'
    try:
        result = query(query_string, { 'itemID': item_id })
        return result[0]
    except IndexError:
        return None

def getCategoriesByItemId(item_id):
    query_string = 'select Category from Categories where ItemID = $itemID'
    return query(query_string, { 'itemID': item_id })

def getBidsByItemId(item_id):
    query_string = 'select * from Bids where ItemID = $itemID order by Amount DESC, Time DESC'
    return query(query_string, { 'itemID': item_id })

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time
