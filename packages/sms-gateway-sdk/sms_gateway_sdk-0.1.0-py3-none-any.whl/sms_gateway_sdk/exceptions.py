class SMSGatewayError(Exception):
    pass

class AuthenticationError(SMSGatewayError):
    pass

class APIRequestError(SMSGatewayError):
    pass
