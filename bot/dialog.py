from bot.checker import check_one
from bot import base, ROOT_DIR, bot
from bot.loger import get_logger
from datetime import datetime
import gspread

logger = get_logger(__name__)


class Prostavka:
    def __init__(self, name: str, costs: list, articul: str, krep: str, comment: str, photo: str):
        self.name = name
        self.costs = costs
        self.articul = articul
        self.krep = krep
        self.comment = comment
        self.photo = photo
        self.cost = 0

    def set_height(self, height):
        self.height = height

    def set_cost(self, cost: int):
        self.cost = cost


class Client:
    mark = ''
    model = None
    generation = None
    modification = None
    prostavki = {}
    dostavka = 0
    cost = 0
    comment = ''
    name = ''
    city = ''
    address = ''
    phone = ''
    chat_id = ''

    def __init__(self):
        self.gc = gc = gspread.service_account(filename=fr'{ROOT_DIR}\root-finder-311719-de7496d4f565.json')
        self.sh = gc.open("Карточка клиента").sheet1

    def write_itog(self):
        self.calculate_dostavka()
        now = datetime.now().strftime("%d-%m-%Y")
        self.sh.append_row([self.chat_id, now, self.generation, self.mark, self.model, self.modification,
                            self.prostavki.get('Передние проставки', ['Нет', 'Нет', 'Нет'])[0],
                            self.prostavki.get('Передние проставки', ['Нет', 'Нет', 'Нет'])[1],
                            self.prostavki.get('Задние проставки', ['Нет', 'Нет', 'Нет'])[0],
                            self.prostavki.get('Задние проставки', ['Нет', 'Нет', 'Нет'])[1],
                            self.prostavki.get('Удлинители', ['Нет', 'Нет', 'Нет'])[0],
                            self.prostavki.get('Удлинители', ['Нет', 'Нет', 'Нет'])[1],
                            self.prostavki.get('Передние проставки', ['Нет', 'Нет', 'Нет'])[2],
                            self.prostavki.get('Задние проставки', ['Нет', 'Нет', 'Нет'])[2],
                            self.prostavki.get('Удлинители', ['Нет', 'Нет', 'Нет'])[2],
                            self.dostavka,
                            self.cost,
                            self.comment,
                            'Avito',
                            None,
                            None,
                            self.phone,
                            self.name,
                            self.city,
                            self.address,
                            ])

    def calculate_dostavka(self):
        self.dostavka = bot.get_sdek_price(self.address)

    def add_prostavrka(self, prostavka: Prostavka):
        self.prostavki.update({prostavka.name: [prostavka.height, prostavka.articul, prostavka.cost]})

    def calculate_cost(self):
        for i in self.prostavki.values():
            self.cost += i[2]


def dialog():
    car = yield "Здравствуйте, для заказа напишите марку и модель вашей машины в виде \"марка модель\" (например Volvo C30, тойота камри)"
    logger.info(car)
    cars = check_one(car)
    logger.info(cars)
    s = 'Выберите подходящий вариант:\n'
    for cnt, i in enumerate(cars):
        s = s + f'{cnt + 1}) ' + i[0]
    ans = yield s
    car = cars[int(ans) - 1][0][:-1]
    client = Client()
    client.model = car
    for i in client.model.split()[:-1]:
        client.mark += i
    yield from generations(client, car)


def generations(client, car):
    gen = []
    logger.info(car)
    for i in list(base.iter_cols(min_col=2, max_col=2))[0]:
        val = base.cell(i.row, i.col_idx + 1).value
        if i.value == car and val not in gen:
            gen.append(val)
    logger.info(gen)
    if len(gen) > 1:
        s = ''
        for cnt, i in enumerate(gen):
            s = s + str(cnt + 1) + ')' + f' {i}\n'
        ans = ''
        while not ans.isdigit():
            ans = yield "Выберите поколение вашего автомобиля(напишите его номер):\n" + s
        ans = int(ans)
        ans = gen[ans - 1]
        client.generation = ans
        yield from modif(client, ans)
    else:
        client.generation = gen[0]
        yield from modif(client, gen[0])


def modif(client, gen):
    mod = []
    for i in list(base.iter_cols(min_col=3, max_col=3))[0]:
        val = base.cell(i.row, i.col_idx + 1).value
        if i.value == gen and val not in mod:
            mod.append(val)
    if len(mod) > 1:
        s = ''
        for cnt, i in enumerate(mod):
            s = s + str(cnt + 1) + ')' + f' {i}\n'
        ans = ''
        while not ans.isdigit():
            ans = yield "Выберите модификацию вашего автомобиля(напишите его номер):\n" + s
        ans = int(ans)
        ans = mod[ans - 1]
        client.modification = ans
        yield from choose_direction(client, ans)
    else:
        client.modification = mod[0]
        yield from choose_direction(client, mod[0])


def choose_direction(client, mod):
    dir = []
    prostavki = []
    for i in list(base.iter_cols(min_col=4, max_col=4))[0]:
        name = base.cell(i.row, i.col_idx + 1).value
        if i.value == mod and name not in dir:
            dir.append(name)
            prostavki.append(Prostavka(name,
                                       [int(base.cell(i.row, i.col_idx + 4).value or 0),
                                        int(base.cell(i.row, i.col_idx + 5).value or 0),
                                        int(base.cell(i.row, i.col_idx + 6).value or 0),
                                        int(base.cell(i.row, i.col_idx + 7).value or 0)],
                                       base.cell(i.row, i.col_idx + 2).value, base.cell(i.row, i.col_idx + 3),
                                       base.cell(i.row, i.col_idx + 8), base.cell(i.row, i.col_idx + 9),

                                       ))
    if len(dir) == 2:
        s = ''
        dir.append("Передние и задние")
        for cnt, i in enumerate(dir):
            s = s + str(cnt + 1) + ')' + f' {i}\n'
        ans = ''
        while not ans.isdigit():
            ans = yield "Выберите тип проставок вашего автомобиля(напишите его номер):\n" + s
        ans = int(ans) - 1
        yield from get_height(client, prostavki, dir[ans])
    elif len(dir) == 3:
        s = ''
        dir.append("Передние и задние")
        dir.append("Полный комплект")
        for cnt, i in enumerate(dir):
            s = s + str(cnt + 1) + ')' + f' {i}\n'
        ans = yield "Выберите тип проставок вашего автомобиля(напишите его номер):\n" + s
        ans = int(ans) - 1
        yield from get_height(client, prostavki, dir[ans])
    else:
        yield from get_height(client, prostavki, dir[0])


def get_height(client, prostavki, dir):
    itog = []
    if dir == 'Передние проставки' or dir == 'Задние проставки' or dir == 'Удлинители':
        for i in prostavki:
            if i.name == dir:
                s = ''
                for cnt, j in enumerate(i.costs):
                    if j:
                        s += f'{cnt + 1})' + f'{cnt + 2}0mm\n'
                h = 's'
                while not h.isdigit():
                    h = yield f'Выберите высоту {dir}:\n' + s
                h = int(h) - 1
                i.set_height(f'{h + 2}0mm')
                i.set_cost(i.costs[h])
                itog.append(i)

    elif dir == 'Передние и задние':
        for i in prostavki:
            if i.name == 'Передние проставки' or i.name == 'Задние проставки':
                s = ''
                for cnt, j in enumerate(i.costs):
                    if j:
                        s += f'{cnt + 1})' + f'{cnt + 2}0mm\n'
                h = ''
                while not h.isdigit():
                    h = yield f'Выберите высоту {i.name}:\n' + s
                h = int(h) - 1
                i.set_height(f'{h + 2}0mm')
                i.set_cost(i.costs[h])
                itog.append(i)

    else:
        for i in prostavki:
            s = ''
            for cnt, j in enumerate(i.costs):
                if j:
                    s += f'{cnt + 1})' + f'{cnt + 2}0mm\n'
            h = 'a'
            while not h.isdigit():
                h = yield f'Выберите высоту {i.name}:\n' + s
            h = int(h) - 1
            i.set_height(f'{h + 2}0mm')
            i.set_cost(i.costs[h])
            itog.append(i)
    for i in itog:
        client.add_prostavrka(i)
    client.calculate_cost()
    yield from get_dostavka(client)


def get_dostavka(client: Client):
    s = f'Ваш заказ:\n{client.modification}\n'
    for cnt, i in enumerate(client.prostavki.items()):
        s += f'{cnt + 1}) ' + i[0] + " " + i[1][0] + " " + str(i[1][2]) + '\n'
    s += f'Общая стоймость:{client.cost}\n'
    s += 'Если у вас есть вопрос или коментарий для меня, напишите его, если нет, то напишите \"нет\"'
    ans = yield s
    client.comment = ans
    s = 'Доставка осуществляется с помощью сдэк, для заготовки к оформлению введите ваше ФИО'
    ans = yield s
    client.name = ans
    ans = yield 'Введите свой номер телефона'
    client.phone = ans
    ans = yield 'Введите ваш город'
    client.city = ans
    ans = yield 'Введите адрес пункта сдэк'
    client.address = ans
    client.write_itog()
    yield from get_itog(client)


def get_itog(client):
    yield f"Доставка стоит примерно {client.dostavka}\nИтоговая цена {client.cost}"
