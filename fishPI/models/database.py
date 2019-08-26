
from datetime import datetime

class meta():
    
    key = None
    value = None
    added = None

    def __init__(self,key,value,added=None):
        
        self.key = key
        self.value = value
        self.added = datetime.strptime(added, '%Y-%m-%d %H:%M:%S')

   


