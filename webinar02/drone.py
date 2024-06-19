import requests
from typing import List
from collections import deque


class Ammunition:
    def __init__(self, name: str, weight: float):
        self.name = name
        self.weight = weight

    def __str__(self):
        return f"Ammunition(name={self.name}, weight={self.weight}kg)"


class Drone:
    def __init__(
        self,
        speed: int,
        width: float,
        depth: float,
        height: float,
        engine_power: int,
        load_capacity: float,
        drone_type: str,
        camera_resolution: str = None,
        stream_url: str = None,
    ):
        self._speed = speed
        self.width = width
        self.depth = depth
        self.height = height
        self.engine_power = engine_power
        self.load_capacity = load_capacity
        self.drone_type = drone_type
        self.camera_resolution = (
            camera_resolution if drone_type == "спостереження" else "низька"
        )
        self.stream_url = stream_url
        self.video_buffer = deque()

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value: int):
        if value < 0:
            raise ValueError("Speed cannot be negative")
        self._speed = value

    def increase_speed(self, increment: int):
        self.speed += increment

    def decrease_speed(self, decrement: int):
        if self.speed - decrement < 0:
            raise ValueError("Speed cannot be negative")
        self.speed -= decrement

    def start_video_stream(self, video_data: bytes):
        if not self.stream_url:
            raise ValueError("Stream URL is not set")

        try:
            response = requests.post(self.stream_url, data=video_data)
            response.raise_for_status()
            if response.status_code != 200:
                raise requests.RequestException(
                    f"Unexpected status code: {response.status_code}"
                )
        except requests.RequestException as e:
            print(f"Error streaming video: {e}. Saving to buffer.")
            self.video_buffer.append(video_data)

    def __str__(self):
        return f"Drone(type={self.drone_type}, speed={self.speed}, dimensions=({self.width}x{self.depth}x{self.height}), engine_power={self.engine_power}, load_capacity={self.load_capacity}, camera_resolution={self.camera_resolution})"


class CombatDrone(Drone):
    def __init__(
        self,
        speed: int,
        width: float,
        depth: float,
        height: float,
        engine_power: int,
        load_capacity: float,
        ammunition: List[Ammunition],
        stream_url: str = None,
    ):
        super().__init__(
            speed=speed,
            width=width,
            depth=depth,
            height=height,
            engine_power=engine_power,
            load_capacity=load_capacity,
            drone_type="ударний",
            stream_url=stream_url,
        )
        self.ammunition = ammunition

    def __str__(self):
        ammo_str = ", ".join(str(ammo) for ammo in self.ammunition)
        return f"CombatDrone(speed={self.speed}, dimensions=({self.width}x{self.depth}x{self.height}), engine_power={self.engine_power}, load_capacity={self.load_capacity}, ammunition=[{ammo_str}])"


class SurveillanceDrone(Drone):
    def __init__(
        self,
        speed: int,
        width: float,
        depth: float,
        height: float,
        engine_power: int,
        load_capacity: float,
        camera_resolution: str,
        stream_url: str = None,
    ):
        super().__init__(
            speed=speed,
            width=width,
            depth=depth,
            height=height,
            engine_power=engine_power,
            load_capacity=load_capacity,
            drone_type="спостереження",
            camera_resolution=camera_resolution,
            stream_url=stream_url,
        )

    def __str__(self):
        return f"SurveillanceDrone(speed={self.speed}, dimensions=({self.width}x{self.depth}x{self.height}), engine_power={self.engine_power}, load_capacity={self.load_capacity}, camera_resolution={self.camera_resolution})"


# Функція для створення дронів
def create_drones():
    combat_drones = [
        CombatDrone(
            speed=120,
            width=1.5,
            depth=1.5,
            height=0.5,
            engine_power=500,
            load_capacity=50,
            ammunition=[Ammunition(name="граната", weight=5)],
            stream_url="http://example.com/stream_combat_1",
        ),
        CombatDrone(
            speed=150,
            width=2.0,
            depth=2.0,
            height=0.7,
            engine_power=700,
            load_capacity=100,
            ammunition=[
                Ammunition(name="граната", weight=5),
                Ammunition(name="ракета", weight=15),
            ],
            stream_url="http://example.com/stream_combat_2",
        ),
    ]

    surveillance_drones = [
        SurveillanceDrone(
            speed=100,
            width=1.2,
            depth=1.2,
            height=0.4,
            engine_power=300,
            load_capacity=30,
            camera_resolution="висока",
            stream_url="http://example.com/stream_surveil_1",
        ),
        SurveillanceDrone(
            speed=110,
            width=1.8,
            depth=1.8,
            height=0.6,
            engine_power=400,
            load_capacity=60,
            camera_resolution="дуже висока",
            stream_url="http://example.com/stream_surveil_2",
        ),
    ]

    return combat_drones + surveillance_drones
