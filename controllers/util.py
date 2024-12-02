from flask import jsonify

def construir_rpta_json(data, error_message = None, cod_error=200):
    '''Estandariza el JSON de respuesta a enviar a través de la API'''
    if cod_error == 200:
        rpta = {
            'status': 'success'
            ,'data' : data
        }
    else:
        rpta = {
            'status': 'error'
            ,'error_message' : error_message
        }
    
    return jsonify(rpta), cod_error