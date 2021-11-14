from typing import ClassVar
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return str(f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM: ClassVar[float] = 1000
    LEN_STEP: ClassVar[float] = 0.65

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    MIN_IN_A_HOUR: ClassVar[float] = 60
    COEFF_CALORIES_1: ClassVar[float] = 18
    COEFF_CALORIES_2: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        avg_speed = self.get_mean_speed()

        return ((self.COEFF_CALORIES_1 * avg_speed
                - self.COEFF_CALORIES_2) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_A_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    COEFF_CAL_1: ClassVar[float] = 0.035
    COEFF_CAL_2: ClassVar[float] = 0.029
    MIN_IN_A_HOUR: ClassVar[float] = 60

    def get_spent_calories(self) -> float:
        dist = self.action * self.LEN_STEP / self.M_IN_KM
        speed = dist / self.duration
        return ((self.COEFF_CAL_1 * self.weight + (speed ** 2 // self.height)
                * self.COEFF_CAL_2 * self.weight)
                * self.duration * self.MIN_IN_A_HOUR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: float

    LEN_STEP: ClassVar[float] = 1.38
    RATIO_1: ClassVar[float] = 1.1
    RATIO_2: ClassVar[float] = 2

    def get_spent_calories(self) -> float:
        return((self.get_mean_speed() + self.RATIO_1) * self.RATIO_2
               * self.weight)

    def get_mean_speed(self) -> float:
        return(self.length_pool
               * self.count_pool
               / self.M_IN_KM
               / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dictionary = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    if workout_type in dictionary:
        return dictionary.get(workout_type)(*data)
    raise KeyError(f"'{workout_type}' - данный тип тренировки не подходит")


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
