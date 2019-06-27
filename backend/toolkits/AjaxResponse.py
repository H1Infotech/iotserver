from django.http import JsonResponse

class AjaxResponse(object):
    
    def __init__(self):

        self.error = ""
        self.data = ""
        self.message = ""
    
    def successMessage(self, data=None , message = "success",headOrign="*"):
        self.message = message
        if data == None:
            data = ""
        jsondata = {"error":str(self.error),
                    "message":self.message,
                    "data":data}
        response = JsonResponse(jsondata)
        #print(jsondata)
        response["Access-Control-Allow-Origin"] = headOrign 
        response["Access-Control-Allow-Methods"] = "GET,POST" 
        response["Access-Control-Max-Age"] = "1000" 
        response["Access-Control-Allow-Headers"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"

        return response
    
    def errorMessage(self, data=None ,error="",  message = "false",headOrign="*"):
        self.error = error
        self.message = message
        if data == None:
            data = ""
        jsondata = {"error":str(self.error),
                    "message":self.message,
                    "data":data}
        print(jsondata)
        response = JsonResponse(jsondata)
        response["Access-Control-Allow-Origin"] = headOrign 
        response["Access-Control-Allow-Methods"] = "GET,POST" 
        response["Access-Control-Max-Age"] = "1000" 
        response["Access-Control-Allow-Headers"] = "*"  
        response["Access-Control-Allow-Credentials"] = "true"
        return response