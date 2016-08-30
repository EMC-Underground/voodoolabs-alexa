import esdclasses


# esd is an EMCSupportDates object
# product is a product string
# model is a model string
def find_matches_by_product_model(esd, product, model):
    result_esd = esd.find_matches_by_product(product)
    result_esd = result_esd.find_matches_by_model(model)
    return result_esd


# esd is an EMCSupportDates object
# product is a product string
def find_matches_by_product(esd, product):
    result_esd = esd.find_matches_by_product(product)
    return result_esd


    
# esd is an EMCSupportDates object
# model is a model string
def find_matches_by_model(esd, model):
    result_esd = esd.find_matches_by_model(model)
    return result_esd


# esd is an EMCSupportDates object
# token_separator is a string to use to demarkate the tokens (e.g. "," or "\n")
# returns alexa-customized string of products that are represented in the data
def get_list_of_products_string(esd, token_separator):
    productsstring = ''
    pi = 0
    for p in esd.getproductslist():
        if pi == 0:
                productsstring = productsstring + p
        else:
                productsstring = productsstring + token_separator + p
        pi += 1
        
    return productsstring


# esd is an EMCSupportDates object
# returns a list [ ] of products that are represented in the data
def get_list_of_models_by_product(esd, product):
    result_esd = find_matches_by_product(esd, product)
    resultstring = result_esd.getmodelslist()
    return result_esd      

# esd is an EMCSupportDates object
# token_separator is a string to use to demarkate the tokens (e.g. "," or "\n")
# returns alexa-customized string of products that are represented in the data
def get_list_of_models_by_product_string(esd, product, token_separator):
    result_list = get_list_of_models_by_product(esd, product)
    modelsstring = ''
    mi = 0
    for m in result_list.getmodelslist():
        if mi == 0:
                modelsstring = modelsstring + m
        else:
                modelsstring = modelsstring + token_separator + m
        mi += 1

    return modelsstring
