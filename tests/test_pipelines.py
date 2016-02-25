from jenskipper import pipelines


def test_format_pipe_bits():
    bits = {'A': (['B', 'C'], 'SUCCESS')}
    assert pipelines.format_pipes_bits(bits).splitlines() == ['B > A', 'C > A']
    bits = {'C': (['B'], 'SUCCESS'), 'B': (['A'], 'FAILURE')}
    assert pipelines.format_pipes_bits(bits).splitlines() == ['A ~> B > C']


def test_parse_pipelines():
    pipes = pipelines.parse_pipelines('B > A\nC > A')
    assert pipes == {'A': (['B', 'C'], 'SUCCESS')}
    pipes = pipelines.parse_pipelines('A ~> B > C')
    assert pipes == {'C': (['B'], 'SUCCESS'), 'B': (['A'], 'FAILURE')}
