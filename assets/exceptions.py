# this python file contains custom created exceptions
# my first time using this class
# it is a good practice to use this class when building large projects, so now I'm just trying it out

class InfoDisplayException(Exception):

    def __str__(self):
        return f"InfoDisplayException: Info has been displayed by user."

class DataNotFoundError(Exception):

    def __init__(self, message="o requested data found in file"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"DataNotFoundErorr: {self.message}"