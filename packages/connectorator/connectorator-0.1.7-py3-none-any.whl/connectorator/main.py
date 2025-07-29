DISCONNECTED = "Disconnected"
CONNECTED = "Connected"


class NotRealInterfaceError(Exception):
    """Interface NE NASTOYASCSCHIY!"""

    def __str__(self):
        nested_error_msg = super().__str__()
        return f"Error Code: Magic Number, Message: {nested_error_msg}"


class UnrealStatusError(Exception):
    """THIS INTERFACE DOES NOT LOOK LIKE IT SHOULD."""

    def __str__(self):
        nested_error_msg = super().__str__()
        return f"Not interesting. {nested_error_msg}"


class Connnector:
    """Defines connection between devices."""

    _statuses = [
        DISCONNECTED,
        CONNECTED,
    ]

    def __init__(self, side_a, side_b):
        self.side_a = side_a
        self.side_b = side_b
        self.status = DISCONNECTED

    @staticmethod
    def normalize(side_x):  # noqa: WPS602
        def vsp(substr):
            if substr in side_x:
                return True
            else:
                return False

        if not isinstance(side_x, str):
            raise NotRealInterfaceError("Use string, Luke")
        side_x = side_x.lower()
        if any(map(vsp, ["ge", "et", "gi"])):
            """This is a possibly real interface."""
        else:
            raise NotRealInterfaceError("Try to be REAL interface: ['ge', 'et', 'gi']")
        if side_x[-1].isdigit():
            return side_x
        else:
            raise NotRealInterfaceError("Your interface should have a num in the end!")

    def connect(self):
        if self.status == CONNECTED:
            print("Interface has been ALREADY connected, you had late! Try to disconnect!")
            return
        self.status = CONNECTED
        print(f"Clutch! Interface has been connected. Line changed state to UP on {self.side_a} and {self.side_b}")

    def disconnect(self):
        if self.status == DISCONNECTED:
            print("Interface has been ALREADY disconnected, you had late! Try to connect!")
            return
        self.status = DISCONNECTED
        print(f"Clutch! Line going down on {self.side_a} and {self.side_b}")

    @property
    def side_a(self):
        return self._side_a

    @side_a.setter
    def side_a(self, side_x):
        self._side_a = self.normalize(side_x)

    @property
    def side_b(self):
        return self._side_b

    @side_b.setter
    def side_b(self, side_x):
        self._side_b = self.normalize(side_x)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not isinstance(value, str):
            raise UnrealStatusError("Choose visely. Give me the String!")
        if value.capitalize() in self._statuses:
            self._status = value.capitalize()
        else:
            raise UnrealStatusError(f"This status is unreal! Use one of supported: {self._statuses}")
