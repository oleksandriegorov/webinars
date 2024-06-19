import pytest
from unittest.mock import patch, MagicMock
from drone import CombatDrone, SurveillanceDrone, Ammunition
import requests


def test_combat_drone():
    drone = CombatDrone(
        120,
        1.5,
        1.5,
        0.5,
        500,
        50,
        [Ammunition("граната", 5)],
        stream_url="http://example.com/stream_combat",
    )
    assert drone.drone_type == "ударний"
    assert drone.camera_resolution == "низька"
    assert "граната" in [ammo.name for ammo in drone.ammunition]


def test_surveillance_drone():
    drone = SurveillanceDrone(
        100,
        1.2,
        1.2,
        0.4,
        300,
        30,
        "висока",
        stream_url="http://example.com/stream_surveil",
    )
    assert drone.drone_type == "спостереження"
    assert drone.camera_resolution == "висока"


def test_speed_methods():
    drone = CombatDrone(
        120,
        1.5,
        1.5,
        0.5,
        500,
        50,
        [Ammunition("граната", 5)],
        stream_url="http://example.com/stream_combat",
    )
    drone.increase_speed(10)
    assert drone.speed == 130
    drone.decrease_speed(20)
    assert drone.speed == 110


def test_start_video_stream_success():
    drone = SurveillanceDrone(
        100,
        1.2,
        1.2,
        0.4,
        300,
        30,
        "висока",
        stream_url="http://example.com/stream_surveil",
    )
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


def test_start_video_stream_failure_connection_error():
    drone = SurveillanceDrone(
        100,
        1.2,
        1.2,
        0.4,
        300,
        30,
        "висока",
        stream_url="http://example.com/stream_surveil",
    )
    video_data = b"example video data"

    with patch("requests.post") as mocked_post:
        mocked_post.side_effect = requests.RequestException("Connection error")

        drone.start_video_stream(video_data)
        mocked_post.assert_called_once_with(
            "http://example.com/stream_surveil", data=video_data
        )
        assert len(drone.video_buffer) == 1
        assert drone.video_buffer[0] == video_data


def test_start_video_stream_failure_http_error():
    drone = SurveillanceDrone(
        100,
        1.2,
        1.2,
        0.4,
        300,
        30,
        "висока",
        stream_url="http://example.com/stream_surveil",
    )
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
