import inspect
import os
import json

class Document:
    def __init__(self, obj=None, **kwargs):
        self.table_name = f"tab{self.__class__.__name__}"
        self.obj = obj
        if self.obj:
            self.validate_mandatory_fields()
        

    def read_json_file(self):
        file_path = os.path.dirname(inspect.getfile(self.__class__))
        json_file = os.path.join(file_path, f"{self.__class__.__name__}.json")
        with open(json_file, "r") as json_file:
            return json.load(json_file)["fields"]
        
        
    def validate_mandatory_fields(self):
        missing = list()
        fields = self.read_json_file()
        for field in fields:
            _is_reqd_field = field.get("reqd") or False
            if _is_reqd_field:
                try:
                    obj_fields = self.obj.get("fields")
                    reqd_field = obj_fields.get(field)
                    if not reqd_field:
                        missing.append(field)
                except AttributeError:
                    raise AttributeError(
                        f"Expected field {field} in {self.obj}, None found."
                    )
        if missing:
            raise Exception(f"Required field(s) {', '.join(missing)}")
