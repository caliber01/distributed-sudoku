class Host(object):
    def connect(self, server):
        raise NotImplementedError()

    def set_name(self, name):
        raise NotImplementedError()

    def load_rooms(self):
        raise NotImplementedError()

    def join_game(self, id):
        raise NotImplementedError()

    def create_room(self, name, max_users):
        raise NotImplementedError()

    def cell_edited(self, x, y, prev_value, new_value):
        raise NotImplementedError()

    def leave_room(self):
        raise NotImplementedError()

    def _request(self, **kwargs):
        raise NotImplementedError()

    def shutdown(self):
        raise NotImplementedError()


