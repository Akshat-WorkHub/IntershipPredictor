import sys
from src.logger.log import logging
logging.getLogger('exception.py')

class CustomException(Exception):
    def __init__(self,error,error_details: sys):
        super().__init__(str(error))

        self.error_msg = self.get_error_details(error,error_details)
        logging.error(self.error_msg)

    def get_error_details(self,error,error_details: sys):
        _,_,tbl_err = error_details.exc_info()

        filename = tbl_err.tb_frame.f_code.co_filename
        lineno = tbl_err.tb_lineno

        error_msg = f"""
-----------------------------------------
Error Occured At File : {filename}
Error Occured At Line-No. : {lineno}
Reason : {str(error)}
"""
        return error_msg
    
    def __str__(self):
        return self.error_msg
    

if __name__ == "__main__":
    try:
        a = int(input("Enter the Number : "))
        a = 10/a

        print(a)
    except Exception as e:
        raise CustomException(e,sys)