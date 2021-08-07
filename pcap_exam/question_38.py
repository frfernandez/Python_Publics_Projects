print("Example 1")
class CriticalError(Exception):
    def __init__(self,message='ERROR MESSAGE A'):
        Exception.__init__(self,message)

raise CriticalError
raise CriticalError("ERROR MESSAGE B")

print("Example 2")
class CriticalError(Exception):
    def __init__(self,message='ERROR MESSAGE A'):
        Exception.__init__(self,message)

raise CriticalError("ERROR MESSAGE B")
