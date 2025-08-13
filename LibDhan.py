from Dhan_Tradehull import Tradehull

str_Client_Code =   "1106451789"
str_Token_ID    =   "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzU1NjcwNDcxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNjQ1MTc4OSJ9.Sl1nEaXAZCfLZNVgcngYBXknrRsJf20LwcYyPPoK631A-q5C-JUTDyiZy-7Zx04nqcqOf0QJJLBPgok8R72vhw"

class Dhan:
    """ def __new__(cls):
        tsl     =   Tradehull(str_Client_Code,str_Token_ID)
        return tsl """
    

    def __init__(self):
        self._Connection = Tradehull(str_Client_Code,str_Token_ID)

    @property
    def DhanConnection(self):
        return self._Connection
    
