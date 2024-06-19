import pytest
from unittest.mock import patch, MagicMock
from drone import CombatDrone, SurveillanceDrone, Ammunition
import requests


@pytest.fixture
def combat_drone():
    return CombatDrone(
        speed=120,
        width=1.5,
        depth=1.5,
        height=0.5,
        engine_power=500,
        load_capacity=50,
        ammunition=[Ammunition(name="граната", weight=5)],
        stream_url="http://example.com/stream_combat",
    )


@pytest.fixture
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


def test_combat_drone(combat_drone):
    drone = combat_drone
    assert drone.drone_type == "ударний"
    assert drone.camera_resolution == "низька"
    assert "граната" in [ammo.name for ammo in drone.ammunition]


def test_surveillance_drone(surveillance_drone):
    drone = surveillance_drone
    assert drone.drone_type == "спостереження"
    assert drone.camera_resolution == "висока"


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
