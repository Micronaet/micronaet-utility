#!/usr/bin/env python
# -*- encoding: utf-8 -*-
country = False

def get_product_from_code(sock, dbname, uid, pwd, code, data):
    ''' Find (or create) code passed for products
        sock: socket linked to openerp instance
        dbname: database name
        uid: user id
        pwd: password 
        code: product code to search
        data: data to use for create element if not present
    '''
    try:
        product_id = sock.execute(dbname, uid, pwd, "product.product", 'search', [
            ('default_code', '=', code)])
        if product_id:
            return product_id[0]
        else: 
            return sock.execute(dbname, uid, pwd, "product.product", 
                "create", data)
                    
    except:
        return False
        
def get_partner_from_code(sock, dbname, uid, pwd, code, data):
    ''' Find (or create) code passed for partner
        sock: socket linked to openerp instance
        dbname: database name
        uid: user id
        pwd: password 
        code: product code to search
        data: data to use for create element if not present
    '''
    try:
        partner_id = sock.execute(dbname, uid, pwd, "res.partner", 'search', [
            ('ref', '=', code)])
        if partner_id:
            return partner_id[0]
        else: 
            return sock.execute(dbname, uid, pwd, "res.partner", 
                "create", data)
    except:
        return False

""""def load_country(sock, dbname, uid, pwd):
    ''' Load once country list
    '''
    global country
    country_ids = sock.execute(dbname, uid, pwd, "res.country", 'search', [])
    
    for c in sock.execute(dbname, uid, pwd, "res.country", 'read', country_ids, ('id', 'code')):
        country[c[1]] = c[0]
        
def get_country_from_code(sock, dbname, uid, pwd, code):
    ''' Find country code
    '''
    global country
    if not country:
        load_country       
    
    try:
        return country.get(code, False)
    except:
        pass
    return False
"""
