import pushbullet

from misc.log import logger

log = logger.get_logger(__name__)


class Pushbullet:
    NAME = "Pushbullet"

    def __init__(self, access_token, device=None, sender='Traktarr'):
        self.access_token = access_token
        self.device = device
        self.sender = sender
        log.debug("Initialized Pushbullet notification agent")

    def send(self, **kwargs):
        if not self.access_token:
            log.error("You must specify an access_token when initializing this class")
            return False

        # send notification
        try:
            pb = pushbullet.Pushbullet(self.access_token)

            if self.device is not None:
                for i in pb.devices:
                    if i.device_iden == self.device or i.nickname == self.device:
                        i.push_note(self.sender, kwargs['message'])
            else:
                pb.push_note(self.sender, kwargs['message'])

            return True

        except Exception:r
            log.exception("Error sending notification via Pushbullet")
        return False
