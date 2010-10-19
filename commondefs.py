

class InProgressError(StandardError):
    def __init__(self, statusmsg):
        super(InProgressError, self).__init__(statusmsg)
