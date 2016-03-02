class JenskipperError(Exception):

    pass


class CyclicDependency(JenskipperError):

    def __init__(self, nodes):
        super(CyclicDependency, self).__init__(
            'involved nodes: %s' % ', '.join(str(n) for n in nodes)
        )
        self.nodes = nodes


class OverwriteError(JenskipperError):

    pass


class ConfError(JenskipperError):

    def __init__(self, conf, validation_results):
        self.conf = conf
        self.validation_results = validation_results
        super(ConfError, self).__init__('configuration validation failed')
