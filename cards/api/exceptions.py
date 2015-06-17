from rest_framework.exceptions import APIException

class BadRequestException(APIException):
    status_code = 409
    default_detail = "You are trying to draw more cards than the deck contains"
