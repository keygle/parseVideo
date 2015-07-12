# s1.py, last_update 2015-06-29 21:01 GMT+0800 CST

def get_s1():
    a = [
        [105, 113, 105, 121, 105], 
        [113, 105, 121, 105], 
    ]
    
    o = []
    for j in a:
        u = ''
        for i in j:
            u += chr(i)
        o += [u]
    
    return o

# end s1.py


