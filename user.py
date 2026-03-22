class User:
    def __init__(self, username:str, email_address:str, is_active:bool = True, 
                 user_id:str = None):
        self.user_id = user_id
        self.username = username
        self.email_address = email_address
        self.is_active = is_active
        
    def __str__(self):
        return (f"[{self.user_id}] {self.name} "
        f"(@{self.username}) - "
        f"Active: {self.is_active}")