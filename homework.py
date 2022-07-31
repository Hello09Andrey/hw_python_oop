from dataclasses import asdict, dataclass


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
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        time_in_min = self.duration * 60  # Время в минутах
        cal = (coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
        return cal * self.weight / self.M_IN_KM * (time_in_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        # наследуем функциональность конструктора из класса-родителя
        super().__init__(action, duration, weight)
        # добавляем новую функциональность: свойство height
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        time = self.duration * 60  # Время в минутах
        cal = ((self.get_mean_speed())**2 // self.height) * coeff_calorie_2
        return (coeff_calorie_1 * self.weight + cal * self.weight) * time


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

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
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        sp = (self.length_pool * self.count_pool / self.M_IN_KM)
        return sp / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: int = 2
        cal = (self.get_mean_speed() + coeff_calorie_1)
        return cal * coeff_calorie_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout = {'SWM': Swimming,
               'RUN': Running,
               'WLK': SportsWalking}
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
