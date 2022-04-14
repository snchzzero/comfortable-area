import xmltodict
import requests
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import csv
import  random
point = {"Сквер мира": ["54.517575 36.245943", "aqua"], "Лесной": ["54.488950 36.202834", "green"],
         "Шарик": ["54.511258 36.233710", "violet"], "Новые черемушки": ["54.519008 36.296079", "brown"],
         "Кошелек": ["54.502507 36.186061", "orange"], "Хороший": ["54.489349 36.188196", "yellow"],
         "Веснушки": ["54.485892 36.175446", "gold"], "Постовалова": ["54.508478 36.292308", "silver"],
         "Воротынск": ["54.469957 36.040122", "red"]}#, "Калуга-2": ["54.538431 36.131375", "lime"],
         #"Мстихино": ["54.562951 36.133823", "cyan"], "Мурино (Снкт.Питербург)": ["60.055597 30.431976", "salmon"],
         #"Мавзолей (Москва)": ["55.733725 37.619855", "pink"], "Саларьево (Москва)": ["55.617059 37.416548", "tomato"],
         #"Поселок Солнечный (Якутия)": ["60.302724 137.557214", "lightblue"], "Лос-Анджелес": ["33.783483 -118.194762", "olive"],
         #"Нью-Йорк": ["40.704226 -74.012791", "grey"]}
translate = {"supermarket": "Супермаркет", "pharmacy": "Аптека", "clinic": "Больница", "atm": "Банкомат",
             "bank": "Отделение банка", "food_court": "Фуд корт", "cafe": "Кафе", "restaurant": "Ресторан",
             "pub": "Паб", "fast_food": "Фаст-фуд", "kindergarten": "Детский сад", "school": "Школа",
             "post_office": "Почта", "post_box": "Почта"}

with open("Благоприятный район(pyplot).txt", "w", encoding="utf-8") as txt:
      dpi = 80
      fig = plt.figure(dpi=dpi, figsize=(5024 / dpi, 984 / dpi))
      mpl.rcParams.update({'font.size': 20})
      plt.title('Благоприятный район')

      #ax = plt.axes()  # добавляет свои значения по оси x, y
      #ax.yaxis.grid(True, zorder=1)
      #xs = range(len(shops.keys()))
      xplot = 0

      for key_p, value_p in point.items():
            shops = {"supermarket": [], "pharmacy": [], "clinic": [], "atm": [], "bank": [], "food_court": [],
                     "cafe": [], "restaurant": [], "pub": [], "fast_food": [], "kindergarten": [], "school": [],
                     "post_office": [], "post_box": []}
            position = [float(i) for i in value_p[0].split()]
            print("Координаты точки:", position[0], position[1], file=txt)
            print("Название точки:", key_p, file=txt)
            radius = 1  # в км
            print("Радиус поиска: ", radius, "км", sep="", file=txt)
            Sh05 = 0.004508
            Dl05 = 0.0076705
            d1 = {"ASh": round(position[0] - (Sh05 * radius), 5),
                  "ADl": round(position[1] - (Dl05 * radius), 5),
                  "BSh": round(position[0] + (Sh05 * radius), 5),
                  "BDl": round(position[1] + (Dl05 * radius), 5)}
            #url = "https://www.openstreetmap.org/api/0.6/map?bbox=36.20012,54.48754,36.20564,54.4893"
            url = "https://www.openstreetmap.org/api/0.6/map?bbox=" + \
                  str(d1["ADl"]) + "," + str(d1["ASh"]) + "," + str(d1["BDl"]) + "," + str(d1["BSh"])
            xml = xmltodict.parse(requests.get(url).content)

            flag = False
            name = "no name"
            key = ""
            keys = shops.keys()
            values = shops.values()

            for NodeWay in ["node", "way"]:
                  for nw in xml["osm"][NodeWay]:
                        if "tag" in nw:
                              tags = nw["tag"]
                              if isinstance(tags, list):
                                    for tag in tags:
                                          if tag["@v"] in shops.keys():
                                                flag = True
                                                key = tag["@v"]
                                          if tag["@k"] == "name":
                                                name = tag["@v"]
                                          if tag["@k"] == "operator" and name == "no name":
                                                name = tag["@v"]
                                    if flag == True:  # добавляем в словарь
                                          shops[key].append(name)
                                    name = "no name"
                                    key = ""
                                    flag = False
            total = 0
            for key, value in shops.items():
                  if len(value) > 0:
                        print(translate[key], end=": ", file=txt)
                        print(*value, sep=", ", file=txt)
                        total += len(value)
            # сортировка словаря если значений нет то убираем из словаря пару ключ: значение
            #shops = dict(filter(lambda keyvalue: len(keyvalue[1]) > 0, shops.items()))
            print("Рейтинг комфорта:", total, file=txt)
            print("---------------------------------------------------------------", file=txt)

            l1 = [len(value) for key, value in shops.items()]
            #plt.bar([x + xplot for x in xs], [len(value) for key, value in shops.items()],
                    #width=0.05, color=value_p[1], alpha=1, label=key_p, zorder=2)
            xt = range(len(shops.keys()))
            plt.bar([x + xplot for x in xt if l1[x] > 0], [i for i in l1 if i > 0],
                    width=0.08, color=value_p[1],
                    alpha=1,  # прозрачность (0-1)
                    label=key_p,
                    zorder=2)
            xplot += 0.09


plt.xticks(range(len(translate.keys())), translate.values())
fig.autofmt_xdate(rotation=45)
plt.legend(loc="upper right")
fig.savefig("Благоприятный район.png")



