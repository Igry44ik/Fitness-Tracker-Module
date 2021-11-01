SWM = 'SWM'
RUN = 'RUN'
WLK = 'WLK'


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                + f'Длительность: {self.duration:.3f} ч.; '
                + f'Дистанция: {self.distance:.3f} км; '
                + f'Ср. скорость: {self.speed:.3f} км/ч; '
                + f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    training_name = 'Training'

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

        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info = InfoMessage(self.training_name, self.duration,
                                    self.get_distance(), self.get_mean_speed(),
                                    self.get_spent_calories())
        return training_info


class Running(Training):
    """Тренировка: бег."""
    training_name = 'Running'

    def get_spent_calories(self) -> float:
        ratio_1 = 18
        ratio_2 = 20
        spent_calories = ((ratio_1 * self.get_mean_speed() - ratio_2)
                          * self.weight / self.M_IN_KM * self.duration * 60)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_name = 'SportsWalking'

    def __init__(self, action, duration, weight, height) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        ratio_3 = 0.035
        ratio_4 = 0.029
        spent_calories = ((ratio_3 * self.weight + (self.get_mean_speed()**2
                                                    // self.height
                                                    ) * ratio_4 * self.weight
                           ) * self.duration * 60)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    training_name = 'Swimming'

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = ((self.length_pool * self.count_pool / self.M_IN_KM)
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        ratio_5 = 1.1
        ratio_6 = 2
        spent_calories = ((self.get_mean_speed() + ratio_5)
                          * ratio_6 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        package = {
            SWM: Swimming,
            RUN: Running,
            WLK: SportsWalking
        }
        return package.get(workout_type)(*data)
    except KeyError:
        raise KeyError('Нет такого кода тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        (SWM, [720, 1, 80, 25, 40]),
        (RUN, [15000, 1, 75]),
        (WLK, [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
