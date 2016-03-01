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
