import random


class Option:
    def __init__(self, option, weight):
        self.option = option
        self.weight = weight

    def __str__(self):
        return f"{self.option},{self.weight}"

    def __repr__(self):
        return f"Option({self.__str__()})"


class RollTable:
    def __init__(self, options: [Option] = None, rolltables: [Option] = None):
        if rolltables is None:
            rolltables = []
        if options is None:
            options = []
        self.options = options
        self.rolltables = rolltables

    def __call__(self, rec_step=False):
        if rec_step:
            options = [i.option for i in self.options]
            weights = [i.weight for i in self.options]
        else:
            options = [i.option for i in self.options] + [i.option for i in self.rolltables]
            weights = [i.weight for i in self.options] + [i.weight for i in self.rolltables]

        res = random.choices(options, weights=weights)[0]
        if res in [i.option for i in self.rolltables]:
            res = res(rec_step=True)
        return res

    @property
    def total_weight(self):
        return sum([i.weight for i in self.options] + [i.weight for i in self.rolltables])

    def __repr__(self):
        res = ""
        for i in self.options:
            res += f"{i.option}:{1 / self.total_weight},"
        for i in self.rolltables:
            for j in i.option.options:
                res += f"t:{j.option}:{j.weight / i.option.total_weight * i.weight / self.total_weight},"
        return res

    def __str__(self):
        res = ""
        for i in self.options:
            res += f"{i.option},"
        for i in self.rolltables:
            for j in i.option.options:
                res += f"t:{j.option},"
        return res
