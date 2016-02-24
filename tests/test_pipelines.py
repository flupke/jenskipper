from jenskipper import pipelines


def test_format_pipe_bits():
    bits = {'A': (['B', 'C'], 'SUCCESS')}
    assert pipelines.format_pipe_bits(bits).splitlines() == ['B > A', 'C > A']
    bits = {'C': (['B'], 'SUCCESS'), 'B': (['A'], 'FAILURE')}
    assert pipelines.format_pipe_bits(bits).splitlines() == ['A ~> B > C']
