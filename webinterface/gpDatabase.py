import pymongo
import app_config
import uuid
import gpEncryption
import time


class gpDatabase:
    def __init__(self):
        self.client = pymongo.MongoClient(app_config.MONGO_URL)
        self.database = self.client['gpTracker']

        self.users = self.database['users']
        self.reminders = self.database['reminders']
        self.gptrackers = self.database['gptrackers']
        self.gptrackers_data = self.database['gptrackers_data']

    def make_unified_user_gptrackers_list(self, users_list: list): #connect users+gptracker devices
        unified = list()
        for u in users_list:
            u_devices = self.get_gptrackers(u['uuid'])
            if u_devices[0] is not True:
                u_devices[1] = []
            unified.append({'user': u, 'devices':u_devices[1]})
        return unified
    def make_unified_gptracker_data(self, gptrackers_device: list): #connect gptracker+gptracker_data
        unified = list()
        for g in gptrackers_device:
            g_data = self.get_gptracker_data(g['uuid'])
            if g_data[0] is not True:
                g_data[1] = {"gps":None, "hr":None, "last_update":"0"}
            unified.append({'device':g, 'data':g_data[1]})
        return unified

    def get_gptracker_data(self, device_uuid):
        data_device_uuid = str(device_uuid)
        result = self.gptrackers_data.find_one({"uuid":data_device_uuid})
        if result is None:
            return [False, "There is no data for this GPTracker!"]

        return [True, result]


    def update_gptracker_data_gps(self, device_uuid, data):
        data_device_uuid = str(device_uuid)
        data_gps = str(data)

        res = self.gptrackers_data.find_one({'uuid': data_device_uuid})
        if res is None:
            self.gptrackers_data.insert_one(
                {
                    "uuid": data_device_uuid,
                    "gps": data_gps,
                    "last_update": int(time.time())
                }
            )
        else:
            data = {"uuid":data_device_uuid}
            data_update = {
                "$set": {"gps": data_gps, "last_update": int(time.time())}
            }
            self.gptrackers_data.update_one(data, data_update)
        return [True, "GPS Data updated"]
    def update_gptracker_data_hr(self, device_uuid, data):
        data_device_uuid = str(device_uuid)
        data_hr = str(data)

        res = self.gptrackers_data.find_one({'uuid': data_device_uuid})
        if res is None:
            self.gptrackers_data.insert_one(
                {
                    "uuid": data_device_uuid,
                    "hr": data_hr,
                    "last_update": int(time.time())
                }
            )
        else:
            data = {"uuid":data_device_uuid}
            data_update = {
                "$set": {"hr":data_hr, "last_update":int(time.time())}
            }
            self.gptrackers_data.update_one(data, data_update)
        
        return [True, "HR data updated"]
    def remove_gptrack(self, uuid):
        self.gptrackers.delete_one({"uuid": str(uuid)})
        self.gptrackers_data.delete_one({"uuid": str(uuid)})
        return [True, "Deleted!"]
    def update_gptracker(self, uuid, name, owner_uuid):
        self.gptrackers.update_one({"uuid":str(uuid)},
        {
            "$set":{
                "name": str(name),
                 "owner_uuid": str(owner_uuid)
            }
        })
        return [True, "Updated!"]
        
    def create_gptrack(self, uuid, name, owner_uuid=""):
        gptracker_uuid = str(uuid)
        gptracker_name = str(name)
        gptracker_owner_uuid = str(owner_uuid)

        res = self.gptrackers.find_one({'uuid':uuid})
        if res is not None:
            return [False, "This gptracker does already exist!"]
        
        gptracker = {
            "uuid": gptracker_uuid,
            "name": gptracker_name,
            "owner_uuid": gptracker_owner_uuid
        }

        self.gptrackers.insert_one(gptracker)
        return [True, "GP Tracker added!"]
    
    def register_gptracker(self, uuid, owner_uuid, name):
        gptracker_uuid = str(uuid)
        gptracker_owner_uuid = str(owner_uuid)
        gptracker_name = str(name)

        res_tracker = self.gptrackers.find_one({'uuid':uuid})
        if res_tracker is None:
            return [False, "This gptracker does not exist!"]
        
        if res_tracker['owner_uuid'] is not "":
            return [False, "This GPtracker is already assigned!"]
        
        res_user = self.get_user(uuid=gptracker_owner_uuid)
        if res_user[0] is False:
            return [False, "This user does not exist!"]

        
        
        gptracker = {"uuid": gptracker_uuid}
        gptracker_update = {
            "$set": {
                "owner_uuid": owner_uuid,
                "name": gptracker_name
                }
        }
        self.gptrackers.update_one(gptracker, gptracker_update)
        return [True, "GPTracker assigned to: {}".format(gptracker_owner_uuid)]
    def unregister_gptracker(self, uuid):
        gptracker_uuid = str(uuid)

        res_tracker = self.gptrackers.find_one({'uuid': uuid})
        if res_tracker is None:
            return [False, "This gptracker does not exist!"]
        
        gptracker = {"uuid":gptracker_uuid}
        gptracker_update = {
            "$set": {"owner_uuid": ""}
        }
        self.gptrackers.update_one(gptracker, gptracker_update)
        return [True, "GPTracker is unregistered!"]
    def get_gptracker(self, uuid):
        gptracker_uuid = str(uuid)
        result = self.gptrackers.find_one({"uuid":gptracker_uuid})
        if result is None:
            return [False, "This gptracker does not exist!"]

        return [True, result]
    def get_all_reminders(self):	
        result = self.reminders.find({})	
        reminders_list = list()	
        for r in result:	
            try:
                r.pop("_id")	
                r.pop("creator_uuid")	
                r.pop("device_uuids")	
                r.pop("uuid")	
            except:
                print("could not pop some values")
            reminders_list.append(r)	
        if len(reminders_list) is 0:
            return [False, "there are no reminders"]
        return [True, reminders_list]	
    def get_device_reminders(self, device_uuid):	
        device_uuid = str(device_uuid)	
        serach_dict = {'device_uuids': device_uuid}	
        result = self.reminders.find(serach_dict)	


        reminders_list = list()	
        for r in result:
            try:	
                r.pop("_id")	
                r.pop("creator_uuid")	
                r.pop("device_uuids")	
                r.pop("uuid")	
            except:
                print("could not pop some values")
            reminders_list.append(r)	
        if len(reminders_list) is 0:	
            return [False, "There are no reminders"]	
        return [True, reminders_list]
    def drop_all_dbs(self):
        self.client.drop_database(self.database)
    def admin_get_all_users(self):
        result = self.users.find({})
        users_list = list()
        for r in result:
            users_list.append(r)
        if len(users_list) is 0:
            return [False, "There are no users"]
        return [True, users_list]
    def admin_get_all_trackers(self):
        result = self.gptrackers.find({})
        gptrackers_list = list()
        for r in result:
            gptrackers_list.append(r)
        
        if len(gptrackers_list) is 0:
            return [False, "There are no trackers"]
        return [True, gptrackers_list]
    def get_gptrackers(self, owner_uuid):
        gptracker_owner_uuid = str(owner_uuid)
        search_dict = {'owner_uuid':gptracker_owner_uuid}
        result = self.gptrackers.find(search_dict)
        
        gptrackers_list = list()
        for r in result:
            gptrackers_list.append(r)
        
        if len(gptrackers_list) is 0:
            return [False, "There are no trackers assigned"]
        return [True, gptrackers_list]

    def get_reminders(self, uuid):
        search_dict = {'creator_uuid': str(uuid)}
        result = self.reminders.find(search_dict)
        
        reminders_list = list()
        for r in result:
            reminders_list.append(r)
        if len(reminders_list) is 0:
            return [False, "Threre are no reminders"]
        return [True,reminders_list]
    
    def create_reminder(self, content, time, creator_uuid, device_uuid):
        reminder_time = str(time)
        reminder_content = str(content)
        reminder_creator_uuid = str(creator_uuid)
        reminder_uuid = str(uuid.uuid4())
        
        reminder_device_uuids = device_uuid
        if "list" not in str(type(device_uuid)):
            reminder_device_uuids = [device_uuid]
        
    
        reminder = {
            "time": reminder_time,
            "content": reminder_content,
            "creator_uuid": reminder_creator_uuid,
            "device_uuids": reminder_device_uuids,
            "uuid": reminder_uuid
        }
        self.reminders.insert_one(reminder)
        return [True, "Reminder added!"]

    def remove_user(self, uuid):
        uuid = str(uuid)
        self.gptrackers.delete_one({"owner_uuid": uuid})
        self.users.delete_one({"uuid": uuid})
        return [True, "Deleted!"]
    def update_user(self, uuid, name, email):
        self.users.update_one({"uuid": str(uuid)}, {
            "$set":{
                "name": str(name),
                "email": str(email)
            }
        })
        return [True, "Updated!"]
    def get_user(self, email=None, uuid=None):
        search_dict = None
        if email is not None:
            search_dict = {'email': str(email)}
        elif uuid is not None:
            search_dict = {'uuid': str(uuid)}
        
        if search_dict is None:
            return [False, "No filter selected!"]
        

        result = self.users.find_one(search_dict)
        if result is None:
            return [False, "User not found!"]
        return [True, result]
    def add_user(self, name, email, plain_password):
        user_uuid = str(uuid.uuid4())
        user_hash = gpEncryption.gpEncryption.encrypt_password(str(plain_password))
        user_name = str(name)
        user_email = str(email)

        result = self.users.find_one(
            {
                'email': user_email
            }
        )

        if result is not None:
            return [False, "Account with this e-mail already exists!"]
        
        user = {
            "email": user_email,
            "hash": user_hash,
            "name": user_name,
            "uuid": user_uuid
        }

        self.users.insert_one(user)
        return [True, "User added!"]
