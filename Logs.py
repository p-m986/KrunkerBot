import json
import asyncio
import os
from datetime import datetime


absolute_path = os.path.dirname(os.path.abspath(__file__))
file_path = absolute_path + '/BotLogs.json'

class logevents():
    def __init__(self):
        self.errors = {}
        self.restarts = {}
        self.errorid = None
        self.restartid = None

    # Asynchronously Fetching the last id number from the last log for errors and restarts to use so that two
    # different instances dont use the same ids

    # Its not working rn it can still make duplicate ids will fix it later        
    async def fetch_ids(self):
        with open(file_path, 'r') as f:
            data = json.load(f)
        self.errorid = data['errors'][-1]['id'] + 1
        self.restartid = data['restarts'][-1]['id'] + 1
        return
    

    async def log_error(self, class_name, function_name, message):
        # Set the ids for the next entry
        await self.fetch_ids()

        # Set time of the entry
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # Load the data from the file
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Edit the specific errors
        self.errors['id'] = self.errorid
        self.errors['timestamp'] = timestamp
        self.errors['class_name'] = class_name
        self.errors['function_name'] = function_name
        self.errors['message'] = message


        data['errors'].append(self.errors)

        # Rewrite the whole file with the updated data
        with open(file_path, 'w') as f:
            json.dump(data, f)

        return self.errorid
    

    async def log_restart(self):
        # Set the ids for the next entry
        await self.fetch_ids()

        # Set time of the entry
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # Load the data from the log file
        with open(file_path, "r") as f:
            data = json.load(f)
        
        # Add the restart log
        self.restarts["id"] = self.restartid
        self.restarts["timestamp"] = timestamp
        data['restarts'].append(self.restarts)

        # Write the new data to the file
        with open(file_path, 'w') as f:
            json.dump(data, f)
        
        return self.restartid


# Testing the above class and its methods
if __name__ == '__main__':
    obj = logevents()
    asyncio.run(obj.log_error('__main__', '__main__', 'This is a test error'))
    print(obj.errorid)