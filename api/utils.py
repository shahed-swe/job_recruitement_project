from collections import OrderedDict


class Dictionary:
    def dictBack(self, data):
        for x, y in data.items():
            if type(y) == OrderedDict:
                return dict(y)
            else:
                pass
