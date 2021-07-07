import os

APP_NAME = 'Shortly'
APP_CREATOR = "Rastaarc(Rastaxarm - 08141161177)"
API_ROUTE = '/graphql-api/'
APP_DESCRIPTION = f"{APP_NAME} is a webapp created for both freemium and premium users to short their links"
URL_PREFIX = os.environ.get("URL_PREFIX")
USER_TYPES = {
    "USER": 1,
    "PUSER": 2,
    "ADMIN": 3,
}
EXPIRY_TYPES = {
    "MONTHLY": "Monthly",
    "YEARLY": "Yearly",
}
ERROR_CODES = {
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "INTERNAL_ERROR": 500,
    "BAD_GATEWAY": 502,
    "SERVICE_UNAVAILABLE": 503,
    "GATEWAY_TIMEOUT": 504,
}
ITEMS_PER_PAGE = 10

MESSAGES = {
    "NO_ACCESS": "Sorry, you don't have access to this operation(s)",
    "FETCH_USERS_ERROR": "An error occurred while fetching the users data",
    "FETCH_LINK_FAILED": "An error occurred while fetching the links",
    "_LINK_CREATED_SUC": "Your link has been created successfully",
    "_LINK_CREATED_ERR": "Failed to create your link, please try again later",
    "NEW_ACCOUNT_SUCCESS": "New Account created successfully",
    "NO_VALID_CREDENTIALS": "No credentials supplied, Please try again",
    "INVALID_CREDENTIALS": "Sorry! Invalid credentials supplied, Please try again",
    "INVALID_LINK_KEYWORD": "Sorry! Invalid Link Keyword supplied, Minimum of 3 and Maximum of 30",
    "INVALID_LINK_": "Sorry! Invalid Link supplied",
    "NEW_ACCOUNT_SUCCESSFUL": "Account created successfully",
    "UNKNOWN_ERROR": "Unknown Error occurred, please try again or contact the administrator",
    "INVALID_USERNAME": "Invalid Username supplied. Please choose another one",
    "INVALID_EMAIL": "Invalid Email supplied. Please choose another one",
    "INVALID_PASSWORD": "Please create a valid password with minimum of 5 characters",
    "LOGIN_SUC": "Account Logged-in successfully",
    "LOGIN_ERR": "Sorry, Your username/email or password is incorrect",
    "NO_USER": "Sorry, We can't find the user with the detail(s) supplied",
    "USER_EXIST": "Sorry! This Username has been registered. Choose another one for your account",
    "EMAIL_EXIST": "Sorry! This Email has been registered. Choose another one for your account",
    "ONLY_ADMIN": "Only Admin is required to access this API route",
    "INVALID_DATA": "Sorry! Invalid data supplied, Please try again",
    "ADDED_SUCC": "New record added successfully",
    "EMAIL_SUCC": "Email sent successfully. We sent a recovery link to your email address, check mailbox/spam box",
    "EMAIL_ERROR": "Error occurred while sending your mail, please try again or contact the administrator",
    "ADDED_ERROR": "Error occurred while inserting the new data, please try again or contact the administrator",
    "UPDATED_SUCC": "Record updated successfully",
    "PROFILE_SUCC": "Profile updated successfully",
    "DELETE_SUCC": "Record deleted successfully",
    "DELETE_ERR": "Operation not successful, Failed to delete Record",
    "UPDATE_SUCC": "Record updated successfully",
    "UPDATE_ERR": "Operation not successful, Failed to update Record",
    "NO_RECORD_TO_DELETE": "Operation not successful, No Record to delete",
    "NO_RECORD_TO_UPDATE": "Operation not successful, No Record to update",
    "REQUEST_JSON_MISSING": "The Required Request Json Missing",
    "INVALID_RECOVERY_KEY": "Sorry! Invalid/expired key supplied, Please provide a valid key generated for this account",
    "PASS_UPDATE_SUCC": "Congrat! your password has been updated successfully",
    "PASS_UPDATE_ERROR": "Sorry! failed to update your password. Please try again later",
}
SERIALIZER_LOADS_MAX_AGE = 60*60*72  # 72 HOURS
