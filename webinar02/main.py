from drone import create_drones


def main():
    drones = create_drones()

    for drone in drones:
        print(drone)
        if hasattr(drone, "increase_speed"):
            drone.increase_speed(10)
            print(f"Speed increased: {drone.speed}")
        if hasattr(drone, "decrease_speed"):
            drone.decrease_speed(5)
            print(f"Speed decreased: {drone.speed}")

        # Приклад даних відео (замість справжнього відео)
        video_data = b"example video data"
        drone.start_video_stream(video_data)


if __name__ == "__main__":
    main()
