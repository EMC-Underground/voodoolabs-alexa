import logging
import esdclasses
import UserDict
import loader_util
import query_util
import os

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

product = "unspecified"

model = "unspecified"


@ask.launch

def give_welcome():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("ProceedIntent")

def proceed():

    proceed_msg = render_template('get_product')

    return question(proceed_msg)


@ask.intent("GetProductIntent", convert={'spoken_product': str})

def product_answer(spoken_product):

    product = spoken_product;

    session.attributes['product'] = product
    
    msg = render_template('get_model', product=session.attributes['product'])

    return question(msg)


@ask.intent("GetModelIntent", convert={'spoken_model': str})

def model_answer(spoken_model):

    model = spoken_model;

    session.attributes['model'] = model
    
    msg = render_template('verify_input',
                          product=session.attributes['product'],
                          model=session.attributes['model'])

    return question(msg)


@ask.intent("GetProductModelIntent", convert={'spoken_product': str, 'spoken_model': str})

def product_model_answer(spoken_product, spoken_model):

    product = spoken_product;
    model = spoken_model;

    #if 'product' in convert_errors:
        # something happened and product may be garbage
        # value (e.g. "?") for later interrogation.
        #return question(render_template('repeat_product'))

    session.attributes['product'] = product
     
    #if 'model' in convert_errors:
        # something happened and model may be garbage
        # value (e.g. "?") for later interrogation.
        #return question(render_template('repeate_model'))

    session.attributes['model'] = model

    alldata = loader_util.load_data()

    result = query_util.find_matches_by_product_model(alldata, product, model)
    
    #print(alldata.toJSON(0))
    
    #msg = render_template('verify_input',
    #                      product=session.attributes['product'],
    #                      model=session.attributes['model'])

    session.attributes['answer'] = result.toSimpleString()

    msg = render_template('read_matches', result=session.attributes['answer'])

    return question(msg)



@ask.intent("ListProductsIntent")

def list_products():

    alldata = loader_util.load_data()

    products_supported = query_util.get_list_of_products_string(alldata, ", ")
    session.attributes['product_supported'] = products_supported

    msg = render_template('list_products', product_names=products_supported)

    return question(msg)


@ask.intent("ListModelsByProductIntent", convert={'spoken_product': str})

def list_models_for_product(spoken_product):

    product = spoken_product;
    alldata = loader_util.load_data()

    models_supported = query_util.get_list_of_models_by_product_string(alldata, product, ", ")

    session.attributes['models_supported_by_product'] = models_supported
    
    msg = render_template('list_models', product=product, model_names=models_supported)

    return question(msg)


@ask.intent("YesIntent")

def declare_right_answer():

    msg = render_template('right')

    return statement(msg)


@ask.intent("NoIntent")

def declare_wrong_answer():

    msg = render_template('wrong')

    return statement(msg)


@ask.intent("DefaultIntent")

def default_response():

    msg = render_template('default')

    return question(msg)


if __name__ == '__main__':

    port = int(os.getenv("PORT"))
    app.run(debug=True, host='0.0.0.0',port=port)



