

class WeaknessStack:
    def __init__(self, icon_width, kind, power, power_secondary=-1):
        self._iwidth = icon_width
        self._kind = kind
        self._power = power
        self._power_secondary = self._power_secondary