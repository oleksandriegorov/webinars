import pytest


@pytest.fixture(params=[10, 20, 30])
def resource(request):
    # Setup
    res = request.param
    return res


def test_resource_usage(resource):
    assert resource in [10, 20, 30]


if __name__ == "__main__":
    pytest.main()
