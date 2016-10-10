from functools import partial
def save_value(value, callback):
    print ("Saving {} to database!".format(value))
    save_result_to_db(result, callback)

def print_response(db_response):
    print ("Response from database: {}".format(db_response))

def save_result_to_db(result, callback):
    pass
    #return
    #print_response  #when the  data is ready
