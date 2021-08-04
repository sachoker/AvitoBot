from checker import check_all, check_one
from bot import base


def dialog():
    answer = yield "Здравствуйте, для заказа напишите марку и модель вашей машины в виде \"марка, модель\""
    carmark, carname = answer.rstrip('.!').split(',')
    carmarkt = check_one(carmark)
    carnamet = check_one(carname)
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
        ans = yield "Выберите поколение вашего автомобиля(напишите его номер):" + s
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
        ans = yield "Выберите модификацию вашего автомобиля(напишите его номер):" + s
        ans = mod[ans - 1]
        yield from choose_direction(ans)
    else:
        yield from choose_direction(mod[0])


def choose_direction(mod):
    dir = []
    for i in list(base.iter_cols(min_col=4, max_col=4))[0]:
        if i.value == mod:
            dir.append(base.cell(i.row, i.col_index + 1).value)
    if len(dir) == 2:
        s = ''
        for cnt, i in enumerate(dir):
            s = s + str(cnt + 1) + ')' + f' {i}\n'
        s = s + "3) Передние и задние"
        ans = yield "Выберите тип проставок вашего автомобиля(напишите его номер):" + s
        ans -= 1
        yield from get_height(mod, ans)
    else:
        yield from get_height(mod, dir[0])


def get_height(mod, dir):
    pass
