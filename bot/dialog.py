from checker import check_all, check_one
from bot import base


class Prostavka:
    def __init__(self, name: str, costs: list, articul: str, krep: str, comment: str, photo: str):
        self.name = name
        self.costs = costs
        self.articul = articul
        self.krep = krep
        self.comment = comment
        self.photo = photo


def dialog():
    answer = yield "Здравствуйте, для заказа напишите марку и модель вашей машины в виде \"марка, модель\""
    carmark, carname = answer.rstrip('.!').split(',')
    carmarkt = check_one(carmark)
    carnamet = check_one(carname, 'en_ZA')
    car = carmarkt + ' ' + carnamet
    if check_again(car):
        answer = yield from generations(car)


def check_again(sugestion):
    answer = yield f"Вы имели в виду {sugestion}?"
    while not ("да" in answer.lower() or "нет" in answer.lower()):
        answer = yield "Да или нет?"
    return 'да' in answer.lower()


def generations(car):
    gen = []
    for i in list(base.iter_cols(min_col=2, max_col=2))[0]:
        if i.value == car:
            gen.append(base.cell(i.row, i.col_index + 1).value)
    if len(gen) > 1:
        s = ''
        for cnt, i in enumerate(gen):
            s = s + str(cnt + 1) + ')' + f' {i}\n'
        ans = yield "Выберите поколение вашего автомобиля(напишите его номер):\n" + s
        ans = int(ans)
        ans = gen[ans - 1]
        yield from modif(ans)
    else:
        yield from modif(gen[0])


def modif(gen):
    mod = []
    for i in list(base.iter_cols(min_col=3, max_col=3))[0]:
        if i.value == gen:
            mod.append(base.cell(i.row, i.col_index + 1).value)
    if len(mod) > 1:
        s = ''
        for cnt, i in enumerate(mod):
            s = s + str(cnt + 1) + ')' + f' {i}\n'
        ans = yield "Выберите модификацию вашего автомобиля(напишите его номер):\n" + s
        ans = int(ans)
        ans = mod[ans - 1]
        yield from choose_direction(ans)
    else:
        yield from choose_direction(mod[0])


def choose_direction(mod):
    dir = []
    prostavki = []
    for i in list(base.iter_cols(min_col=4, max_col=4))[0]:
        if i.value == mod:
            name = base.cell(i.row, i.col_index + 1).value
            dir.append(name)
            prostavki.append(Prostavka(name,
                                       [int(base.cell(i.row, i.col_index + 4).value),
                                        int(base.cell(i.row, i.col_index + 5).value),
                                        int(base.cell(i.row, i.col_index + 6).value),
                                        int(base.cell(i.row, i.col_index + 7).value)],
                                       base.cell(i.row, i.col_index + 2).value, base.cell(i.row, i.col_index + 3),
                                       base.cell(i.row, i.col_index + 8), base.cell(i.row, i.col_index + 9)
                                       ))
    if len(dir) == 2:
        s = ''
        dir.append("Передние и задние")
        for cnt, i in enumerate(dir):
            s = s + str(cnt + 1) + ')' + f' {i}\n'
        ans = yield "Выберите тип проставок вашего автомобиля(напишите его номер):\n" + s
        ans = int(ans)
        ans -= 1
        yield from get_height(prostavki, dir[ans])
    elif len(dir) == 3:
        s = ''
        dir.append("Передние и задние")
        dir.append("Полный комплект")
        for cnt, i in enumerate(dir):
            s = s + str(cnt + 1) + ')' + f' {i}\n'
        ans = yield "Выберите тип проставок вашего автомобиля(напишите его номер):\n" + s
        yield from get_height(prostavki, dir[ans])
    else:
        yield from get_height(prostavki, dir[0])


def get_height(prostavki, dir):
    heights = []
    costs = []
    if dir == 'Передние проставки' or dir == 'Задние проставки' or dir == 'Удлинители':
        for i in prostavki:
            if i.name == dir:
                for cnt, j in enumerate(i.costs):
                    if j:
                        heights.append(f'{cnt + 2}0mm')
                        costs.append(j)
    elif dir == 'Передние и задние':
        for i in prostavki:
            if i.name == 'Передние проставки' or i.name == 'Задние проставки':
                for cnt, j in enumerate(i.costs):
                    if j:
                        try:
                            costs[cnt] += j
                        except:
                            costs.append(j)
                            heights.append(f'{cnt + 2}0mm')
    else:
        for i in prostavki:
            for cnt, j in enumerate(i.costs):
                if j:
                    try:
                        costs[cnt] += j
                    except:
                        costs.append(j)
                        heights.append(f'{cnt + 2}0mm')
    s = ''
    for cnt, h in enumerate(heights):
        s = s + str(cnt + 1) + ')' + f' {h}\n'
    ans = yield 'Выберите высоту проставки:\n' + s
    ans = int(ans) - 1
    cost = costs[ans]
    yield from get_itog(cost)


def get_itog(cost):
    yield f"Итоговая цена {cost}"
