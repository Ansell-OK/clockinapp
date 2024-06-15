import pyrebase
from db.config import firebaseConfig as keys 
from flet.security import encrypt, decrypt 


secret_key = 'dokintaadmin'

class PyrebaseWrapper:
    """
    Wraps Pyrebase with flet authentication flow and abstarxts crud from app
    """

    def __init__(self, page):
        self.page = page
        self.firebase = pyrebase.initialize_app(keys)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        self.storage = self.firebase.storage()
        self.idToken = None
        self.uuid = None
        self.check_token()

        self.streams = []
    
    def save_tokens(self, token, uuid, page):
        encrypted_token = encrypt(token, secret_key)
        page.client_storage.set("firebase_token", encrypted_token)
        page.client_storage.set("firebase_id", uuid)
        self.idToken = token
        self.uuid=uuid
    
    def erase_token(self):
        self.page.client_storage.remove("firebase_token")
        self.page.client_storage.remove("firebase_id")

    def register_user(self, name,  email, phone, password):
        self.auth.create_user_with_email_and_password(email, password)
        self.sign_in(email, password)
        data = {"name": name, 'email': email, 'phone': phone, 'is_online': False}
        self.db.child("users").child(self.uuid).update(data = data, token=self.idToken)
    
    def sign_in(self, email, password):
        user = self.auth.sign_in_with_email_and_password(email, password)
        self.db.child("users").child(user['localId']).update({"is_online": True})
        if user:
            token = user["idToken"]
            uuid = user["localId"]
            self.save_tokens(token, uuid, self.page)


    def sign_out(self):
        self.db.child('users').child(self.uuid).update({'is_online': False})
        self.erase_token()

    def check_token(self):
        ### Prevents the user from having to sign in all the time
        encrypted_token = self.page.client_storage.get("firebase_token")
        uuid = self.page.client_storage.get("firebase_id")
        if encrypted_token:
            decrypted_token = decrypt(encrypted_token, secret_key)
            self.idToken = decrypted_token
            self.uuid = uuid
            try:
                self.auth.get_account_info(self.idToken)
                return "Success"
            except:
                return None
        return None

    def add_class(self, course, location, date, time, duration, level):
        if self.uuid == None:
            self.uuid = self.auth.get_account_info(self.idToken)["users"][0]["localId"]
        data = {'course': course, 'location': location, 'date': date, "time": time, "duration": duration, 'level': level, 'clocked_in': False, 'clocked_out': False}
        self.db.child("users").child(self.uuid).child("classes").push(data, self.idToken)
    
    def edit_class(self,  course, location, date, time, duration, level):
        if self.uuid == None:
            self.uuid = self.auth.get_account_info(self.idToken)["users"][0]["localId"]
        data = {'course': course, 'location': location, 'date': date, "time": time, "duration": duration, 'level': level}
        self.db.child("users").child(self.uuid).update("classes").push(data, self.idToken)
    
    def clock_in(self):
        if self.uuid == None:
            self.uuid = self.auth.get_account_info(self.idToken)["users"][0]["localId"]
        self.db.child("users").child(self.uuid).update({"clocked_in": True})
    
    def clock_out(self):
        if self.uuid == None:
            self.uuid = self.auth.get_account_info(self.idToken)["users"][0]["localId"]
        self.db.child("users").child(self.uuid).update({"clocked_out": True})


    def get_classes(self):
        return self.db.child("users").child(self.uuid).get(token=self.idToken).val()
    
    def stream_data_conversation_main(self, stream_handler):
        stream = self.db.child("users").child(self.uuid).child("classes").stream(stream_handler=stream_handler, token=self.idToken)
        self.streams.append(stream)
    
    def kill_all_streams(self):
        for stream in self.streams:
            try:
                stream.close()
            except:
                print("no streams")