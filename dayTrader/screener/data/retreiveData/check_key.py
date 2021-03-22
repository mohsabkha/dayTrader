####################################################################
#PURPOSE: used to ensure that a key in a dictionary exists
#ARGS: dictionary, key
#RETURNS: the dictionary key value
#NOTE: n/a
#TO-DO: n/a
####################################################################
def check_key(dict, key): 
    if key in dict: 
        return dict[key]
    else: 
        return 'NaN'