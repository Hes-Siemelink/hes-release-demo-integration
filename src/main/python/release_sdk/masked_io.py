from io import TextIOWrapper


class MaskedIO(TextIOWrapper):
    def __init__(self, buffer):
        super().__init__(buffer, line_buffering=True, write_through=False)
        self._secrets = []

    @property
    def secrets(self):
        return self._secrets

    @secrets.setter
    def secrets(self, secrets):
        self._secrets = secrets

    def write(self, s):
        d = s
        for secret in self.secrets:
            if secret:
                d = d.replace(secret, '********')
        self.buffer.write(d)
