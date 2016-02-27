class JenskipperError(Exception):

    pass


class CyclicDependency(JenskipperError):

    def __init__(self, nodes):
        super(CyclicDependency, self).__init__(
            'involved nodes: %s' % ', '.join(str(n) for n in nodes)
        )
        self.nodes = nodes


class RepositoryNotFound(JenskipperError):

    def __init__(self, from_dir):
        super(RepositoryNotFound, self).__init__(
            'could not find a Jenskipper repository in %s and its parents' %
            from_dir
        )
        self.from_dir = from_dir
