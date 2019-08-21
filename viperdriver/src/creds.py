import logging
import keyring

from viperlib import jsondata
from viperdriver.src import *

logger = logging.getLogger(__name__)

class creds(jsondata):

    _srctype = None
    _handle = None
    _krk = None

    @property
    def type(self):
        return self._srctype

    @type.setter
    def type(self, val):
        self._srctype = val
        if val == CREDS_TYPE_PLAIN:
            self.filename = CREDS_F_NAME

    def load(self):
        assert self.user is not None, 'User key is not set. (Note: user key is not \'uid\'. Used for naming login info set.)'
        if self._srctype == CREDS_TYPE_PLAIN:
            assert self.location is not None, 'Location is not set.'
            self.get_from_file()
            self.contents = self.contents[self.user]
        elif self._srctype == CREDS_TYPE_SECURE:
            self.get_from_keyring()
        else:
            raise ValueError('Expected \'json\' or \'keyring\' only.')

    @property
    def keyring_key(self):
        return self._krk

    @keyring_key.setter
    def keyring_key(self, val):
        self._krk = val

    def get_from_keyring(self):
        try:
            uid = keyring.get_password(self._krk, self.user)
        except AttributeError:
            logger.critical('Could not get value for ' + self.user + ' from keyring key ' + self._krk + '. Make sure the key has been set (python -m keyring set ' + self._krk + ' ' + self.user + ').')
            exit(2)
        self.contents.update( {"uid": uid} )
        self.contents.update( {"pwd": keyring.get_password(self.contents["uid"], 'pwd')} )
