test:
	py.test

test_cov:
	py.test --cov jenskipper --cov-report term-missing
