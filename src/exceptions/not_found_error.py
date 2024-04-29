class NotFoundError(Exception):
    def __init__(self, obj_name:str,obj_id:str):
        self.message = f"{obj_name} '{obj_id}' not found"
        super().__init__(self.message)