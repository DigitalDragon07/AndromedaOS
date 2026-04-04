class Button:
    def __init__(self, CenterPoint, linkedFunction, filex, rescaling):
        self.data = {}
        self.data["CenterPoint"] = CenterPoint
        self.data["linkedFunction"] = linkedFunction
        self.data["file"] = filex
        self.data["rescaling"] = rescaling
    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            raise AndromedaOSError("Error in __getitem__: No item named {}".format(key))
    def __setitem__(self, key, value):
        if not (key in self.data):
            AndromedaOSError.warn("Item name will never be used by AndromedaOS. Potential typo?")
        self.data[key] = value
        return
    def __str__(self):
        return "Hi"
class GhostUI(Button):
    def __init__(self, Corner1, Corner2, linkedFunction, rescaling):
        self.data = {}
        self.data["Corner1"] = Corner1
        self.data["Corner2"] = Corner2
        self.data["linkedFunction"] = linkedFunction
        self.data["rescaling"] = rescaling
        self.data["file"] = None

class Text(Button):
    def __init__(self, linkedFunction, filex, rescaling):
        self.data = {}
        self.data["linkedFunction"] = linkedFunction
        self.data["rescaling"] = rescaling
        self.data["file"] = None
        
__all__ = ["Button", "GhostUI", "Text"]
__append__ = True