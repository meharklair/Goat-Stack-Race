#----------------------------------------------------
# Stack implementation
#----------------------------------------------------

class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):      
        try:
            return self.items.pop()
        except IndexError:
            raise Exception
    def peek(self):     
        try:
            return self.items[len(self.items)-1] 
        except IndexError:
            raise Exception('Cannot peek into empty list')     
    
    def is_empty(self):
        return self.items == []
    
    def size(self):
        return len(self.items)
    
    def __str__(self):
        stackAsString = ''
        for item in self.items:
            stackAsString += item + ' '
        return (stackAsString)
        