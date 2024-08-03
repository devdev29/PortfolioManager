from dataclasses import dataclass

@dataclass
class Account:
    __account_no: str
    bank_name: str
    __account_type: str
    amount: float
    
    @property
    def account_no(self):
       return self.__account_no
   
    @property
    def account_type(self):
        return self.__account_type 
   
    @account_no.setter
    def set_account_no(self, account_no: str):
        if not len(account_no) != 15:
            return -1
        self.__account_no = account_no
        return 1
    
    @account_type.setter
    def set_account_type(self, account_type: int):
        if account_type > 2 and account_type < 0:
            return -1
        self.__account_type = account_type
        return 1
