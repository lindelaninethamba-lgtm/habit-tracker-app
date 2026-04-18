class User:
    """creates user class that defines the attributes of the habit user
    with a username,email address and database assigned user_id"""
    def __init__(self, username:str, email_address:str, is_active:bool = True, 
                 user_id:str = None):
        self.user_id = user_id
        self.username = username
        self.email_address = email_address
        self.is_active = is_active
        
    def __str__(self):
        """translates data into a comprehensive string summary of the user"""
        return (f"[{self.user_id}] {self.name} "
        f"(@{self.username}) - "
        f"Active: {self.is_active}")
    