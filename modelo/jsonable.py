"""
"""
import json


class Jsonable(object):
    """
    """
    def serialize(self):
        """
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @classmethod
    def deserialize(cls, obj):
        """
        """
        return cls(**json.loads(obj))

    def __repr__(self):
        return self.serialize()
