import logging
import esdclasses
import UserDict
import loader_util
import query_util
import os
import csv

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

    alldata = loader_util.load_data_from_s3()

    result = query_util.find_matches_by_product_model(alldata, product, model)
    
    #msg = render_template('verify_input',
    #                      product=session.attributes['product'],
    #                      model=session.attributes['model'])

    session.attributes['answer'] = result.toSimpleString()

    msg = render_template('read_matches', result=session.attributes['answer'])

    return question(msg)



@ask.intent("ListProductsIntent")

def list_products():

    alldata = loader_util.load_data_from_s3()

    products_supported = query_util.get_list_of_products_string(alldata, ", ")
    session.attributes['product_supported'] = products_supported

    msg = render_template('list_products', product_names=products_supported)

    return question(msg)


@ask.intent("ListModelsByProductIntent", convert={'spoken_product': str})

def list_models_for_product(spoken_product):

    product = spoken_product;
    alldata = loader_util.load_data_from_s3()

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

    # read environment variables from local file in directory
    # this local file may be empty in command line instances where AWS
    # credentials will come from profile in ~/.aws/credentials.
    # In Pivotal Cloud Foundry, however, we'll have Jenkins populate this file
    # so that we can pass these secrets to the environment of the running
    # application
    with open('EnvironmentVariables.csv', mode='rU') as csvfile:  #mode U is deprecated in Python 3.6
	reader = csv.DictReader(csvfile, dialect='excel')
	i=0
	for row in reader:
                os.environ[row['VariableName']] = row['VariableValue']
                print("Set env variable " + row['VariableName'] + "="
                      + row['VariableValue'])
        csvfile.close()


    port = os.getenv("PORT",None)       # important for PCF
    if port == None:
        # We're probably running from command line
        app.run(debug=True)
    else:
        # If we're running in Cloud Foundry, we'll end up here
        print("Setting port to: " + port)
        #portint = '{0:d}'.format(port)
        portint = port
        # we start flask with host and port for PCF; non-PCF only requires debug
        app.run(debug=True, host='0.0.0.0',port=portint) 



