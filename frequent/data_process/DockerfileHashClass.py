class DockerfileHash(object):
    _pName = ''
    _fileName = ''
    _content = ''
    _hash = ''

    def fill_data_by_dict(self, d):
        self._pName = d["pName"]
        self._fileName = d["fileName"]
        self._content = d["content"]
        self._hash = d["hash"]

    def data_to_tuple(self):
        t = (self._pName,
             self._fileName,
             self._content,
             self._hash
             )
        return t
