class Bot:
    def __init__(self, bot): 
        self.id = bot['id']
        self.name = bot["name"]
        self.prompt = bot["prompt"]
    
    def id(self):
        return self.id 
       
    def name(self):
        return self.name 
       
    def prompt(self):
        return self.prompt