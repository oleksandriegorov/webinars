import pytest
from unittest.mock import patch, MagicMock
from drone import CombatDrone, SurveillanceDrone, Ammunition
import requests


@pytest.fixture  # setup/teardown fixture
def combat_drone():
    print("\nPreparing a combat drone")
    yield CombatDrone(  # setup and tear down fixture
        speed=120,
        width=1.5,
        depth=1.5,
        height=0.5,
        engine_power=500,
        load_capacity=50,
        ammunition=[Ammunition(name="граната", weight=5)],
        stream_url="http://example.com/stream_combat",
    )
    print("\nDisassembling a combat drone")


@pytest.fixture  # basic fixture
def surveillance_drone():
    return SurveillanceDrone(
        speed=100,
        width=1.2,
        depth=1.2,
        height=0.4,
        engine_power=300,
        load_capacity=30,
        camera_resolution="висока",
        stream_url="http://example.com/stream_surveil",
    )


@pytest.fixture(autouse=True)  # auto-use fixture
def rocket_ammunition():
    print("\nПостачаю ракету ...")
    yield Ammunition(name="ракета", weight=50.3)
    print("\nСкільки раз кажу - використовуй, коли постачаю :-| ")


@pytest.fixture  # wrapper for auto-use with arguments
def get_rocket_ammunition(rocket_ammunition):
    return rocket_ammunition


@pytest.fixture(
    params=[
        Ammunition(name=f"ракета №{i}", weight=((20 - i) / 3) + i) for i in range(10)
    ]
)  # Parametrized fixture
def rocket_assortment(request):
    return request.param


@pytest.fixture  # basic fixture using auto-use
def heavy_combat_drone(rocket_ammunition):
    return CombatDrone(
        speed=80,
        width=2.2,
        depth=1.8,
        height=0.8,
        engine_power=600,
        load_capacity=80,
        ammunition=[rocket_ammunition],
        stream_url="http://example.com/stream_surveil",
    )


def test_combat_drone(combat_drone):
    drone = combat_drone
    assert drone.drone_type == "ударний"
    assert drone.camera_resolution == "низька"
    assert "граната" in [ammo.name for ammo in drone.ammunition]


def test_surveillance_drone(surveillance_drone):
    drone = surveillance_drone
    assert drone.drone_type == "спостереження"
    assert drone.camera_resolution == "висока"


def test_heavy_combat_drone(heavy_combat_drone, rocket_assortment):
    drone = heavy_combat_drone
    assert drone.drone_type == "ударний"
    assert drone.camera_resolution == "низька"
    assert "ракета" in [ammo.name for ammo in drone.ammunition]
    drone.ammunition.append(rocket_assortment)
    for idx, ammo in enumerate(drone.ammunition):
        print(f"Firing {ammo.name} #{idx+1}")


def test_speed_methods(combat_drone):
    drone = combat_drone
    drone.increase_speed(10)
    assert drone.speed == 130
    drone.decrease_speed(20)
    assert drone.speed == 110


def test_start_video_stream_success(surveillance_drone):
    drone = surveillance_drone
    video_data = b"example video data"

    with patch("requests.post") as mocked_post:
        mocked_response = MagicMock()
        mocked_response.raise_for_status.return_value = None
        mocked_response.status_code = 200
        mocked_post.return_value = mocked_response

        drone.start_video_stream(video_data)
        mocked_post.assert_called_once_with(
            "http://example.com/stream_surveil", data=video_data
        )
        assert len(drone.video_buffer) == 0


def test_start_video_stream_failure_connection_error(surveillance_drone):
    drone = surveillance_drone
    video_data = b"example video data"

    with patch("requests.post") as mocked_post:
        mocked_post.side_effect = requests.RequestException("Connection error")

        drone.start_video_stream(video_data)
        mocked_post.assert_called_once_with(
            "http://example.com/stream_surveil", data=video_data
        )
        assert len(drone.video_buffer) == 1
        assert drone.video_buffer[0] == video_data


def test_start_video_stream_failure_http_error(surveillance_drone):
    drone = surveillance_drone
    video_data = b"example video data"

    with patch("requests.post") as mocked_post:
        mocked_response = MagicMock()
        mocked_response.raise_for_status.side_effect = requests.RequestException(
            "HTTP error"
        )
        mocked_response.status_code = 500
        mocked_post.return_value = mocked_response

        drone.start_video_stream(video_data)
        mocked_post.assert_called_once_with(
            "http://example.com/stream_surveil", data=video_data
        )
        assert len(drone.video_buffer) == 1
        assert drone.video_buffer[0] == video_data


if __name__ == "__main__":
    pytest.main()
