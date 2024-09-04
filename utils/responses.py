
def success_response(data,message,status_code=200,**kwargs):
    return {"data":data,
            "message":message,
            "meta":{"status_code":status_code,
                    **kwargs}}


def failure_response(message,status_code=400,**kwargs):
    return{"data":{},
           "error":message,
           "meta":{"status_code":status_code,
                   **kwargs}}