class ClientProxy(object):
    @property
    def id(self):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

    @property
    def room(self):
        raise NotImplementedError()

    def notify_start_game(self, **kwargs):
        raise NotImplementedError()

    def notify_people_changed(self, **kwargs):
        raise NotImplementedError()

    def notify_sudoku_solved(self, **kwargs):
        raise NotImplementedError()

    def notify_sudoku_changed(self, **kwargs):
        raise NotImplementedError()

    def shutdown(self):
        raise NotImplementedError()
