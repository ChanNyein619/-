import math


class Metrics:
    @staticmethod
    def __transform(values: list, additional=None):
        need_transform = False
        for val in values:
            if val > 1:
                need_transform = True
                break
        if additional is not None and additional > 1:
            need_transform = True
        if need_transform:
            x = max(values)
            for i in range(len(values)):
                values[i] = values[i] / x
            if additional is not None:
                additional = additional / x
        if additional is not None:
            return values, additional
        else:
            return values

    @staticmethod
    def get_mse(values: list, predicted):
        values, predicted = Metrics.__transform(values, predicted)
        result = 0
        for val in values:
            result += math.pow((val - predicted), 2)
        return result / (len(values) - 1)

    @staticmethod
    def __get_mean(values: list):
        result = 0
        for val in values:
            result += val
        return result / len(values)

    @staticmethod
    def __get_dispersion(values: list, mean):
        result = 0
        for val in values:
            result += math.pow((val - mean), 2)
        return result / len(values)

    @staticmethod
    def get_std(values: list):
        values = Metrics.__transform(values)
        mean = Metrics.__get_mean(values)
        dispersion = Metrics.__get_dispersion(values, mean)
        return math.sqrt(dispersion)
