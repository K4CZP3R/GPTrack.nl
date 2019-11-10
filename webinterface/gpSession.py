class gpSession(object):
    def __init__(self, session_list):
        self.logged_in = session_list.get("logged_in", None)
        self.user = session_list.get("user", None)
        self.admin = session_list.get("admin", None)
        self.admin_username = session_list.get("admin_username", None)
        self.admin_password = session_list.get("admin_password", None)
    def update_ses(self, session_list):
        session_list["logged_in"] = self.logged_in
        session_list["user"] = self.user
        session_list["admin"] = self.admin
        session_list["admin_username"] = self.admin_username
        session_list["admin_password"] = self.admin_password
    
    def login_user(self, user_dict):
        self.user = user_dict
        self.logged_in = True
        
    def logout_user(self):
        self.user = None
        self.logged_in = None
    
    def login_admin(self, admin_email, admin_password):
        self.admin_username = admin_email
        self.admin_password = admin_password
        self.admin = True
    
    def logout_admin(self):
        self.admin_username = None
        self.admin_password = None
        self.admin = None
