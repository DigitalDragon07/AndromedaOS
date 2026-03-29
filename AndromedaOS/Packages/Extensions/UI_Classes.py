class Button():
    def __init___(self, CenterPoint, linkedFunction, filex, rescaling):
        self.CenterPoint = CenterPoint
        self.linkedFunction = linkedFunction
        self.file = filex
        self.rescaling = rescaling
    def __getitem__(self, key):
        if key == "CenterPoint":
            return self.CenterPoint
        elif key == "linkedFunction":
            return self.linkedFunction
        elif key == "file":
            return self.file
        elif key == "rescaling":
            return self.rescaling
        else:
            raise AndromedaOSError("Error in __getitem__: No item named {}".format(key))