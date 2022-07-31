from dataclasses import asdict, dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    GET_MESSEAGE: str = ('Тип тренировки: {training_type};'
                         ' Длительность: {duration:.3f} ч.;'
                         ' Дистанция: {distance:.3f} км;'
                         ' Ср. скорость: {speed:.3f} км/ч;'
                         ' Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.GET_MESSEAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Не запустился расчет каллорий')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    BODY_MASS_INDEX: int = 18
    COEFF_CALORIE: int = 20

    def get_spent_calories(self) -> float:
        time_in_min: float = self.duration * 60  # Время в минутах
        calories_burn_min = (self.BODY_MASS_INDEX * self.get_mean_speed()
                             - self.COEFF_CALORIE) * self.weight / self.M_IN_KM
        return calories_burn_min * (time_in_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    BODY_MASS_INDEX: float = 0.035  # Коэффициент массы тела
    COEFF_CALORIE: float = 0.029
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        # наследуем функциональность конструктора из класса-родителя
        super().__init__(action, duration, weight)
        # добавляем новую функциональность: свойство height
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_min: float = self.duration * self.MIN_IN_HOUR
        calories_burn_min = (self.BODY_MASS_INDEX * self.weight
                             + ((self.get_mean_speed())**2 // self.height)
                             * self.COEFF_CALORIE * self.weight)
        return calories_burn_min * duration_min


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    BODY_MASS_INDEX: float = 1.1
    COEFF_CALORIE: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        # наследуем функциональность конструктора из класса-родителя
        super().__init__(action, duration, weight)
        # добавляем новую функциональность: свойство length_pool, count_pool
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        sp: float = (self.length_pool * self.count_pool / self.M_IN_KM)
        return sp / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        cal: float = (self.get_mean_speed() + self.BODY_MASS_INDEX)
        return cal * self.COEFF_CALORIE * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: Dict[str, Type[Training]] = {'SWM': Swimming,
                                          'RUN': Running,
                                          'WLK': SportsWalking}
    if workout_type not in workout:
        raise KeyError(f'Получен неизвестный тип тренировки: {workout_type}')
    return workout[workout_type](*data)


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
