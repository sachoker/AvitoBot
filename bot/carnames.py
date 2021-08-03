import openpyxl

m = open(
    r'C:\Users\mv149\PycharmProjects\onlybot\venv\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell\en_US.dic',
    'r+', encoding='UTF-8')
c = open(
    r'C:\Users\mv149\PycharmProjects\onlybot\venv\lib\site-packages\enchant\data\mingw64\share\enchant\hunspell\en_ZA.dic',
    'r+', encoding='UTF-8'
)
d = open(
    r'C:\Users\mv149\PycharmProjects\onlybot\venv\lib\site-packages\enchant\data\mingw64\share\enchant\hunspell\en_ZW.dic',
    'r+', encoding='UTF-8'
)
marks = m.readlines()
models = c.readlines()
alls = d.readlines()
del marks[0]
del models[0]
del alls[0]
base = openpyxl.open("База для бота.xlsx").active
for i in list(base.iter_cols(min_row=2, max_col=1, values_only=True))[0]:
    if i not in marks:
        marks.append(i)

for i in list(base.iter_cols(min_row=2, min_col=2, max_col=2, values_only=True))[0]:
    if i not in alls:
        alls.append(i)
    for j in marks:
        if i.startswith(j):
            i = i[len(j) + 1:]
    if i not in models:
        models.append(i)

for i in marks:
    m.write(i + '\n')

for i in models:
    c.write(i + '\n')

for i in alls:
    d.write(i + '\n')

m.close()
c.close()
d.close()
