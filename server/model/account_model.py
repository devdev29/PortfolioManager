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
        self.__account_no = account_no
    
    @account_type.setter
    def set_account_type(self, account_type: int):
        self.__account_type = account_type
    
    def to_list(self):
        return [
            self.__account_no,
            self.bank_name,
            self.__account_type,
            self.amount
        ]
