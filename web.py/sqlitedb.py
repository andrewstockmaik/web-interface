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
def getItemsOnSearch(itemID='', userID='', minPrice='', maxPrice='', status='', desc = '', category = ''):
    _query = 'SELECT * FROM Items, CurrentTime'
    no_params = (itemID == '' and userID == '' and minPrice == '' and maxPrice == '' and desc == '' and category == '')

    if not no_params:
        _query += ' WHERE '
        putAnd = False;

        if (itemID != ''):
            _query += 'ItemID = ' + itemID
            putAnd = True

        if (userID != ''):
            if putAnd:
                _query += ' AND '
            _query += 'Seller_UserID = ' + "'" + userID + "'"
            putAnd = True

        if (minPrice != ''):
            if putAnd:
                _query += ' AND '
            _query += 'Currently >= ' + minPrice
            putAnd = True

        if (maxPrice != ''):
            if putAnd:
                _query += ' AND '
            _query += 'Currently <= ' + maxPrice
            putAnd = True

        if (desc != ''):
            if putAnd:
                _query += ' AND '
            _query += 'Description LIKE \'%' + desc + '%\''
            putAnd = True;

        if (category != ''):
            if putAnd:
                _query += ' AND '
            _query += '(SELECT COUNT(*) FROM Categories WHERE ItemID = Items.ItemID AND Category LIKE \'%' + category + '%\') > 0'
            putAnd = True;

    if (status != 'all'):
        if not no_params:
            _query += ' AND '
        else:
            _query += ' WHERE '

        if status == 'open':
            _query += '(select Time from CurrentTime) between Started and Ends AND (Buy_Price IS NULL OR Currently < Buy_Price)'
        elif status == 'notStarted':
            _query += 'Started > (select Time from CurrentTime)'
        elif status == 'close':
            _query += '(Ends < (select Time from CurrentTime) OR (Buy_Price NOT NULL AND Currently >= Buy_Price))'

    _query += " ORDER BY Number_of_Bids DESC"
    result = query(_query)
    print _query  # debug
    return result