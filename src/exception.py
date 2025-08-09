import sys
def error_message_detail(error,error_detail:sys):
    """
    This function takes an error and its details, formats them into a string,
    and returns the formatted error message.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occurred in script: [{file_name}] at line number: [{exc_tb.tb_lineno}] with message: [{str(error)}]"
    return error_message

class CustomException(Exception):
    """
    Custom exception class that inherits from the built-in Exception class.
    It formats the error message using the error_message_detail function.
    """
    def __init__(self, error, error_detail:sys):
        super().__init__(error)
        self.error_message = error_message_detail(error, error_detail)
    
    def __str__(self):
        return self.error_message
    
    # this is for testing purposes 
# if __name__ == "__main__":
#     try:
#         raise ValueError("An example error")
#     except Exception as e:
#         exc = CustomException(e, sys)
#         print(exc)   