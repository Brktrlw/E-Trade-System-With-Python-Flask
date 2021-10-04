from typing import overload
from errorLogger import BaseErrorLogger
from datetime import datetime
class FileErrorLogger(BaseErrorLogger):
    @staticmethod
    def FileLogger(errors):
        errorTime=datetime.now()
        with open("errors.txt","a") as file:
            file.write(str(errors)+ " "+str(errorTime)+"\n")



















