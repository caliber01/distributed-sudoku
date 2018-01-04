import common.protocol as protocol


def error_by_code(code):
    if code == protocol.TOO_LATE:
        return TooLateError()
    elif code == protocol.ROOM_NOT_FOUND:
        return RoomNotFoundError()
    elif code == protocol.FULL_ROOM:
        return FullRoomError()
    else:
        return ProtocolError()


class ProtocolError(ValueError):
    def __init__(self, code=protocol.RESPONSE_ERROR, *args):
        super(ProtocolError, self).__init__(*args)
        self.code = code


class TooLateError(ProtocolError):
    def __init__(self):
        super(TooLateError, self).__init__(protocol.TOO_LATE)


class FullRoomError(ProtocolError):
    def __init__(self):
        super(FullRoomError, self).__init__(protocol.FULL_ROOM)


class RoomNotFoundError(ValueError):
    def __init__(self):
        super(RoomNotFoundError, self).__init__(protocol.ROOM_NOT_FOUND)
