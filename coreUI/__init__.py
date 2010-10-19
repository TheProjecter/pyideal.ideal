from exceptions import NotImplementedError



class Panel(object):
    name = ""
    contains = list()
    def __init__(self, name):
        self.name = name
    
    def addWidget(self, widget):
        self.contains.append(widget)
    
    def draw(self, container=None):
        raise NotImplementedError("Debe Especializarse el Panel")


class Input(object):
    name = ""
    text = ""
    def __init__(self, name, label, text, widget):
        self.name = name
        self.label = label
        self.text = text
        self.widget = widget
    
    def draw(self, container=None):
        raise NotImplementedError("Debe Especializarse el TextInput")


class ButtonInput(object):
    name = ""
    label = ""
    onClick = None
    def __init__(self, name, label):
        self.name = name
        self.label = label
    
    def draw(self, container=None):
        raise NotImplementedError("Debe Especializarse el ButtonInput")
