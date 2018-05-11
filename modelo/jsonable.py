"""
"""
import json


class Jsonable(object):
    """
    """
    def serialize(self, outputFile=None):
        """
        """
        if outputFile:
            json.dump(self, outputFile, default=lambda o: o.__dict__, sort_keys=True, indent=4)

        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @classmethod
    def deserialize(cls, obj):
        """
        """
        if type(obj) == file:
            ret = cls(**json.load(obj))

        else:
            ret = cls(**json.loads(obj))

        return ret

    def __repr__(self):
        return self.serialize()
