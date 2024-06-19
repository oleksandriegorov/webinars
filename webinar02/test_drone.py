import pytest
from drone import CombatDrone, SurveillanceDrone, Ammunition


def test_combat_drone():
    drone = CombatDrone(120, 1.5, 1.5, 0.5, 500, 50, [Ammunition("граната", 5)])
    assert drone.drone_type == "ударний"
    assert drone.camera_resolution == "низька"
    assert "граната" in [ammo.name for ammo in drone.ammunition]


def test_surveillance_drone():
    drone = SurveillanceDrone(100, 1.2, 1.2, 0.4, 300, 30, "висока")
    assert drone.drone_type == "спостереження"
    assert drone.camera_resolution == "висока"


def test_speed_methods():
    drone = CombatDrone(120, 1.5, 1.5, 0.5, 500, 50, [Ammunition("граната", 5)])
    drone.increase_speed(10)
    assert drone.speed == 130
    drone.decrease_speed(20)
    assert drone.speed == 110


if __name__ == "__main__":
    pytest.main()
