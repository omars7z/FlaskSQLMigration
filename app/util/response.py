from flask import jsonify

def suc_res(data, status=200): #change status code according to error
    return {"success": True, "data": data}, status

def error_res(data, status=404):
    return {"success": False, "data": data}, status

