import tkinter as tk
from tkinter import font as tkfont

class NoirDetectiveGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Последний глоток: Детектив Джек Харпер")
        self.root.geometry("850x600")
        self.root.resizable(False, False)

        # Цветовая палитра
        self.bg_color = "#fff"  # Белый фон
        self.text_color = "#000"  # Черный текст
        self.input_bg = "#eee"  # Светло-серый ввод
        self.input_fg = "#000"  # Черный текст ввода

        self.root.configure(bg=self.bg_color)

        # Текстовое поле
        self.text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED, 
                          height=22, font=tkfont.Font(family="Courier", size=11),
                          bg=self.bg_color, fg=self.text_color, bd=1,
                          insertbackground=self.text_color, highlightthickness=0)
        self.text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Рамка для ввода
        self.entry_frame = tk.Frame(root, bg=self.bg_color)
        self.entry_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Поле ввода
        self.entry = tk.Entry(self.entry_frame, font=tkfont.Font(family="Courier", size=11),
                            bg=self.input_bg, fg=self.input_fg, bd=1,
                            insertbackground=self.input_fg, highlightthickness=0)
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Return>", self.process_input)

        # Игровые переменные
        self.scene = "intro"
        self.inventory = {
            "gun": False,
            "photo": False,
            "note": False,
            "whiskey": False
        }
        self.known_info = {
            "mickey": False,
            "sheriff": False,
            "debt": False
        }
        self.relationships = {
            "lilian": 0,
            "bartender": 0
        }
        # Переменные для сцены "office"
        self.cabinet_inspected = False
        self.has_pistol = False
        self.search_result = {}
        self.dock_clue = False #Улика на пристани

        self.show_scene()

        # Фокус на поле ввода в начале игры
        self.entry.focus_set()

    def show_scene(self):
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)

        if self.scene == "intro":
            self.text.insert(tk.END, """
            Последний глоток: Детектив Джек Харпер
            ---------------------------------------
        Детективная игра, где вы играете за частного детектива
        Джека Харпера, погрязшего в долгах и пороках. 
        Вам предстоит раскрыть дело об исчезновении мужа 
        Лилиан Блэквуд, столкнувшись с мафией, коррумпированными
        копами и опасными тайнами.
            
        Действующие лица:
        - Джек Харпер: Главный герой, детектив.
        - Лилиан Блэквуд: Клиентка, жена пропавшего.
        - Дэвид Блэквуд: Пропавший муж Лилиан, бухгалтер
        - в компании Микки О'Мелли.
        - Шериф Билл Корум: Коррумпированный шериф.
        - Микки "Кулак" Омелли: Босс мафии.
        - Бармен: Местный бармен, может знать полезную информацию.
            
        Как играть:
        Вводите цифры, соответствующие выбранным вариантам,
        и нажмите Enter для продолжения игры.
            
        Удачи, детектив!
        \n1. (Жмите Enter, чтобы начать игру)
        """)

        elif self.scene == "office":
            self.show_office()

        elif self.scene == "lilian_story":
            self.text.insert(tk.END, """
            ИСТОРИЯ ЛИЛИАН
            ------------------------
            Лилиан садится в кресло напротив Джека. Её глаза полны слез,
            а в голосе дрожит тревога.
            "Он не вернулся прошлой ночью. 
            Обычно он всегда предупреждает...
            У него были какие-то дела, о которых он не говорил."
            
            Я (Джек Харпер): "Дела говорите? 
            У всех нас есть свои скелеты в шкафу."

            Лилиан Блэквуд: "Харпер, мне нужна твоя помощь!
            Мой муж Дэвид исчез!"
            Я: "Что за работа была у вашего мужа?"
            Лилиан Блэквуд: "Он был бухгалтером...
            в компании Микки О'Мелли..."

            1. Взяться за дело.
            2. "Может, у вашего мужа была любовница?"
            3. Отказаться от дела.
            """)
            

        elif self.scene == "dark_street":
             self.text.insert(tk.END, """
            ТЕМНАЯ УЛИЦА
            ----------------------
            Вы выходите на темную грязную улицу.
            Лилиан идет рядом, кутаясь в пальто.
            Фонари мерцают, отбрасывая длинные тени.
            Мимо проходят подозрительные типы, бросая на вас косые взгляды.
            
            Я: "Что ж, начнем поиски, миссис Блэквуд."
            
            1. Отправиться в Квартал Лилиан
            2. Опросить прохожих
            """)

        elif self.scene == "street_question":
            self.text.insert(tk.END, """
            ОПРОС ПРОХОЖИХ
            -------------------------
            Вы пытаетесь остановить несколько прохожих,
            но они шарахаются от вас,
            как от чумного. Один из них бормочет:
            "Держитесь подальше, коп!"
            Кажется, здесь не любят копов... или детективов.
            
            \n1. (Жмите Enter, чтобы продолжить)
            """)

        elif self.scene == "apartment":
            text = """
            КВАРТАЛ ЛИЛИАН
            --------------------------
            Вы осматриваете квартал вокруг дома Лилиан.
            Тихие улочки, дорогие магазины,
            чувствуется запах больших денег.
            Но даже здесь есть свои темные уголки.
            
            Я: "Нужно быть внимательным, в таких местах
            любят прятаться секреты."

            1. Осмотреть кабинет Дэвида
            2. Поговорить с соседкой
            3. Осмотреть спальню
            4. Отправиться в бар "Сирена"
            """
            if self.dock_clue:
                text += "\n5. Отправиться к Шерифу"
            self.text.insert(tk.END, text)

        elif self.scene == "sheriff_office":
            text = """
            ОФИС ШЕРИФА БИЛЛА
            ------------------------------
            Грязный офис в захолустном городке. На столе - бутылка виски,
            старая фотография и толстый слой пыли. Шериф Билл Корум -
            самый коррумпированный коп в округе.
            Он смотрит на вас с ненавистью.
            
            Я: "Шериф, у вас тут уютно, как на помойке."
            """
            if self.dock_clue:
                text += "\n1. Предъявить улику и обвинить шерифа."
            text += "\n5. Уйти из офиса шерифа."
            self.text.insert(tk.END, text)

        elif self.scene == "sheriff_confrontation":
          if self.inventory["gun"]:
            self.text.insert(tk.END, """
                ШЕРИФ: "Ах ты, сукин сын! Думаешь, ты меня переиграешь?"
                Шериф выхватывает пистолет, но ты быстрее! Выстрел!
                Шериф падает на пол.
                ШЕРИФ (умирая): "О'Мелли... это он... 
                Дэвид узнал слишком много о его делах...
                он отмывал деньги для Микки... прости..."

                \n1. (Жмите Enter, чтобы продолжить)
                """)
          else:
            self.text.insert(tk.END, """
                ШЕРИФ: "Зря ты сунул нос в это дело, детектив!
                Ты слишком много узнал."
                Шериф выхватывает пистолет и стреляет.
                
                \n1. (Жмите Enter, чтобы продолжить)
                """)
            self.restart_button = tk.Button(self.root, text="Начать заново", command=self.restart_game,
                                          bg=self.bg_color, fg=self.text_color,
                                          font=tkfont.Font(family="Courier", size=11))
            self.restart_button.pack(pady=10)
            self.text.config(state=tk.DISABLED)
            return

        elif self.scene == "mickey_office":
             text = """
            ОФИС МИККИ О'МЕЛЛИ
            ------------------------------
            Дорогой офис в центре города. Вид на город, дорогая мебель...
            Микки "Кулак" Омелли контролирует этот город, и он не любит,
            когда ему мешают.
            
            Я: "Микки, шериф Корум мертв.
            Он рассказал мне про Дэвида Блэквуда."
            \n1. "Зачем ты убил Дэвида?"
            """
             self.text.insert(tk.END, text)

        elif self.scene == "mickey_response":
            self.text.insert(tk.END, """
            МИККИ: "Блэквуд? Он украл у меня деньги, вот и все.
            А ты, Харпер, лучше забудь об этом."
            
            1. "Где сейчас Блэквуд?"
            2. "Что на 12-й пристани?"
            """)

        elif self.scene == "warehouse":
             text = """
            ЗАБРОШЕННЫЙ СКЛАД
            -----------------------------
            Темное и опасное место за городом. Воняет крысами, плесенью
            и смертью. Здесь Омелли проворачивает свои грязные дела.
            
            Я: "Что ж, пришло время узнать, что здесь происходит."
            \n1. Осмотреть склад
            """
             self.text.insert(tk.END,text)

        elif self.scene == "dock":
            text = """
            12-Я ПРИСТАНЬ
            -----------------------------
            Мрачное место. Чайки кричат, волны бьются о сваи.
            Кажется, здесь недавно что-то разгружали.
            
            Я: "Что ж, посмотрим, что тут можно найти. 
            Может, хоть какой-то след Дэвида."
            \n1. Осмотреть место разгрузки
            """
            if not self.dock_clue:
              text += "\n2. Уйти с пристани"
            self.text.insert(tk.END, text)

        elif self.scene == "final":
             self.text.insert(tk.END, """
            ФИНАЛ
            ----------------
            Всё кончено.
            Остался только последний глоток виски и горький привкус правды.
            \n1. (Жмите Enter, чтобы продолжить)
            """)
        elif self.scene == "bar":
            text = """
            БАР "СИРЕНА"
            -----------------------
            В баре "Сирена" воняет потом, дешёвым пивом и безысходностью.
            За стойкой - огромный бугай с татуировкой якоря на бицепсе.
            В углу двое играют в карты, бросая на вас косые взгляды.
            
            Я: "Отличное место, чтобы промочить горло
            и узнать пару секретов."

            1. Поговорить с барменом
            2. Спросить про Микки
            """
            if self.relationships["bartender"] >= 3:
              text += "\n3. Отправиться на 12-ю пристань"
            elif self.relationships["bartender"] > 0:
              text += "\nКажется, бармену есть, что рассказать, но он еще не готов делиться информацией. Может, стоит поговорить с ним еще?"
            text += "\n4. Вернуться на улицу"

            self.text.insert(tk.END, text)

        elif self.scene == "study":
            self.text.insert(tk.END, """
            КАБИНЕТ ДЭВИДА
            --------------------------
            В кабинете вы находите:
            - Фотографию Дэвида с Микки "Кулаком" Омелли
            - Бухгалтерские книги с подозрительными записями
            - Письмо с угрозами: "Ты знаешь, что будет,
            если не вернешь долг"
             \n1. (Жмите Enter, чтобы продолжить)
            """)
            self.inventory["photo"] = True
            self.known_info["debt"] = True

        elif self.scene == "neighbor":
            self.text.insert(tk.END, """
            CОСЕДКА
            --------------------------
            Миссис Хиггинс, пожилая соседка, шепчет:
            "Дэвид? Он вернулся той ночью... весь в крови!
            Кричал что-то про
            'проклятые доки' и 'долг Микки'. Потом снова ушел -
            и больше его не видели."

            \n1. (Жмите Enter, чтобы продолжить)
             """)

        elif self.scene == "bedroom":
            self.text.insert(tk.END, """
            СПАЛЬНЯ
            --------------------------
            В спальне вы замечаете:
            - Полупустую бутылку виски на тумбочке
            - Женское белье, небрежно брошенное на кровать
            - Запах дешевых сигарет, хотя Лилиан курит дорогие
            
            \n1. (Жмите Enter, чтобы продолжить)
             """)
            self.inventory["whiskey"] = True

        elif self.scene == "ask_mickey":
            if self.known_info["mickey"]:
                self.ask_mickey_logic()
            else:
                self.text.insert(tk.END, """
                Вы спрашиваете про Микки Омелли. Бармен тут же мрачнеет:
                "Не стоит задавать таких вопросов, детектив.
                Это опасно для вашего здоровья."

                Один из посетителей, косясь на вас, добавляет:
                "Микки не любит, когда о нем спрашивают. Особенно копы."
                 \n1. (Жмите Enter, чтобы продолжить)
                """)
                
        elif self.scene == "bartender":
            bartender_dialogues = [
                """
                Джо протирает стойку тряпкой.
                "Блэквуд? Дэвид Блэквуд? Слышал о таком.
                Он крутился тут недавно."
                \n1. (Жмите Enter, чтобы продолжить)""",

                """
                Джо наливает себе выпить.
                "Этот Блэквуд... скользкий тип. Не доверяю я ему.
                Всегда казалось, что он что-то мутит за спиной у Микки."
                \n1. (Жмите Enter, чтобы продолжить)""",

                """
                Джо оглядывается по сторонам.
                "Слышал, Дэвид якшался с Микки О'Мелли.
                Но это не точно. Хотя, кто знает,
                что у них там происходило..."
                \n1. (Жмите Enter, чтобы продолжить)"""
            ]
            dialogue_index = min(self.relationships["bartender"], 2)  # 0, 1, или 2
            self.text.insert(tk.END, bartender_dialogues[dialogue_index])

        elif self.scene == "dock_search":
            self.dock_clue = True
            self.text.insert(tk.END, """
            Осматривая место разгрузки, вы находите обрывок бумаги.
            На нем - часть бухгалтерской записи и подпись: "Б.К."
            Кажется, это инициалы шерифа Билла Корума.
            Что-то здесь явно не чисто.
            
            1. Вернуться в Квартал Лилиан (Жмите Enter)
            """)

        elif self.scene == "good_ending":
            self.text.insert(tk.END, """
            ФИНАЛ: ПОСЛЕДНИЙ ГЛОТОК
            
            Вы врываетесь с револьвером! Перестрелка.
            Микки ранен, его люди бегут.
            Дэвид Блэквуд жив, но избит. 
            Он шепчет: "Они подставили меня... 
            Документы в сейфе..."
            
            Лилиан плачет от облегчения. Вы получаете щедрую награду.
            Но в городе, где правят деньги и преступность,
            это лишь временная победа...
            \n1. (Жмите Enter, чтобы продолжить)
            """)

        elif self.scene == "bad_ending":
            self.text.insert(tk.END, """
            ФИНАЛ: ПОСЛЕДНИЙ ГЛОТОК
            ----------------------------
            Шериф (Перед тем как выстрелить):
            "Зря ты сунул нос в это дело, детектив!
            Ты слишком много узнал."
            """)
            self.restart_button = tk.Button(self.root, text="Начать заново", command=self.restart_game,
                                          bg=self.bg_color, fg=self.text_color,
                                          font=tkfont.Font(family="Courier", size=11))
            self.restart_button.pack(pady=10)
            self.text.config(state=tk.DISABLED)
            return

        self.text.config(state=tk.DISABLED)
        self.text.see(tk.END)

    def show_office(self):
        text = """
        Кабинет Джека
        ---------------------------
        Время полдень, но в моем кабинете царит вечная ночь. 
        Запах дешевого виски въелся в стены, как въедается отчаяние
        в душу старого детектива. 
        Долги растут, как сорняки, но есть кое-что, что растёт быстрее -
        моё отвращение к этому городу. Дверь открывается с треском,
        и на пороге появляется она - Лилиан Блэквуд.
        
        Я (Джек Харпер): "Еще одна головная боль на мою бедную голову."

        Лилиан Блэквуд: "Харпер, мне нужна твоя помощь! Мой муж исчез!"

        1. "Расскажите мне все, что знаете"
        2. "Чем занимался ваш муж?"
        3. "Мои услуги стоят дорого"
        """

        # Добавляем опцию осмотра офиса, если еще не осмотрели
        if not self.cabinet_inspected:
            text += "\n4. Осмотреть офис"
        else:  # Если осмотрели, добавляем опцию открыть сейф, если он не открыт
            if not self.has_pistol:
                text += "\n4. Открыть сейф"
            else:
                text += "\nВы уже открыли сейф и взяли револьвер."
        self.text.insert(tk.END, text)

        # Добавляем результат поиска, если он был
        if "office_result" in self.search_result:
            self.text.insert(tk.END, "\n" + self.search_result["office_result"])
    def process_input(self, event):
        cmd = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)

        next_scene = None  # Переменная для определения следующей сцены

        if self.scene == "intro":
            next_scene = "office"

        elif self.scene == "office":
            if cmd == "1":
                next_scene = "lilian_story"
            elif cmd == "2":
                self.known_info["debt"] = True
                next_scene = "lilian_story"
            elif cmd == "3":
                self.relationships["lilian"] += 1
                next_scene = "lilian_story"
            elif cmd == "4":
                self.office_search()
                return  # show_scene вызовется в office_search

        elif self.scene == "lilian_story":
             if cmd == "1":
              next_scene = "dark_street"
             elif cmd =="2":
                self.end_game("Лилиан в ярости покидает ваш офис.\n\nВы потеряли клиента и не продвинулись ни на шаг в расследовании.")
                return
             elif cmd == "3":
                 self.end_game("Вы решаете не связываться с этим делом. Микки О'Мелли - слишком опасный противник.\n\nВаши долги остаются, и вы топите горе в виски.")
                 return

        elif self.scene == "dark_street":
             if cmd == "1":
               next_scene = "apartment"
             elif cmd == "2":
               next_scene = "street_question"

        elif self.scene == "street_question":
            next_scene = "dark_street"

        elif self.scene == "apartment":
            if cmd == "1":
                next_scene = "study"
            elif cmd == "2":
                next_scene = "neighbor"
            elif cmd == "3":
                next_scene = "bedroom"
            elif cmd == "4":
                next_scene = "bar"
            elif cmd == "5" and self.dock_clue:
                next_scene = "sheriff_office"

        elif self.scene == "bar":
            if cmd == "1":
                next_scene = "bartender" # Поговорить с барменом
            elif cmd == "2":
                next_scene = "ask_mickey" #Идем спрашивать за Микки
            elif cmd == "3":
                if self.relationships["bartender"] >= 3:
                  next_scene = "dock"
                else:
                  self.text.config(state=tk.NORMAL)
                  self.text.insert(tk.END, "\nБармен еще не настолько пьян, чтобы рассказывать тебе все.")
                  self.text.config(state=tk.DISABLED)
                  self.show_scene()#Обновляем сцену
                  return
            elif cmd == "4":
                next_scene = "apartment" #На выход

        elif self.scene == "bedroom":
             next_scene = "apartment"

        elif self.scene == "study":
            next_scene = "apartment"

        elif self.scene == "neighbor":
            next_scene = "apartment"
        
        elif self.scene == "ask_mickey":
             next_scene = "bar" #Теперь возвращаемся в бар
        
        elif self.scene == "bartender":
            self.relationships["bartender"] += 1
            next_scene = "bar"

        elif self.scene == "dock":
            if cmd == "1":
              next_scene = "dock_search"
            elif cmd == "2":
              next_scene = "apartment"
            
        elif self.scene == "dock_search":
             next_scene = "apartment" #Идем в апартаменты

        elif self.scene == "sheriff_office":
            if cmd == "1" and self.dock_clue:
              next_scene = "sheriff_confrontation"
            elif cmd == "5":
              next_scene = "apartment"
            else:
              self.text.config(state=tk.NORMAL)
              self.text.insert(tk.END, "\nУ вас недостаточно улик, чтобы обвинить шерифа.")
              self.text.config(state=tk.DISABLED)
              self.show_scene()#Обновляем сцену
              return

        elif self.scene == "sheriff_confrontation":
          if self.inventory["gun"]:
            self.scene = "mickey_office"
            self.show_scene()
          else:
            self.end_game("""
                ФИНАЛ: ПОСЛЕДНИЙ ГЛОТОК
                -------------------------------
                Шериф (Перед тем как выстрелить):
                "Зря ты сунул нос в это дело, детектив!
                Ты слишком много узнал."
                """)
            return

        elif self.scene == "mickey_office":
            next_scene = "mickey_response"

        elif self.scene == "mickey_response":
            next_scene = "warehouse"
        elif self.scene == "warehouse":
            if cmd == "1":
              if self.has_pistol:
                next_scene = "good_ending"
              else:
                next_scene = "bad_ending"

        elif self.scene == "good_ending":
          self.end_game("Вы выжили")
          return
        elif self.scene == "bad_ending":
          self.end_game("Вы погибли")
          return 

        # Всегда переходим к следующей сцене, если она определена
        if next_scene:
           self.scene = next_scene
           self.show_scene()
           return

        self.show_scene() #Если нет определенной сцены, обновим текущую.
    
    def ask_mickey_logic(self):
        if not self.inventory["gun"]:
            self.end_game("""
                Бармен не оценил твою настойчивость. Пара громил вышвыривают тебя из бара.
                С сотрясением мозга и парой сломанных ребер, ты решаешь, что это дело не стоит свеч.
                """)
        else:
            self.text.insert(tk.END, """
                Ты выкладываешь на стойку свой револьвер. Бармен бледнеет и начинает говорить:
                "Ходят слухи, что Микки и шериф Корум вместе занимаются контрабандой. Говорят, что-то везут через доки."
                \n5. Вернуться в бар
                """)
            self.known_info["sheriff"] = True

    def office_search(self):
        if not self.cabinet_inspected:
            self.cabinet_inspected = True
            result = "Вы тщательно осмотрели офис и обнаружили старый сейф, спрятанный за картиной. Кажется, он заперт на кодовый замок."
        elif not self.has_pistol:
            self.has_pistol = True
            self.inventory["gun"] = True
            result = "С трудом проворачивая ржавый механизм, вы открываете сейф. Внутри - старый, но смазанный револьвер 38-го калибра и пачка патронов. Кажется, он еще послужит."
        else:
            result = "Здесь больше ничего интересного нет."

        self.search_result["office_result"] = result
        self.show_scene()

    def end_game(self, message):
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, message)
        
        self.restart_button = tk.Button(self.root, text="Начать заново", command=self.restart_game,
                                          bg=self.bg_color, fg=self.text_color,
                                          font=tkfont.Font(family="Courier", size=11))
        self.restart_button.pack(pady=10)
        self.text.config(state=tk.DISABLED)

    def restart_game(self):
        self.scene = "intro"
        self.inventory = {
            "gun": False,
            "photo": False,
            "note": False,
            "whiskey": False
        }
        self.known_info = {
            "mickey": False,
            "sheriff": False,
            "debt": False
        }
        self.relationships = {
            "lilian": 0,
            "bartender": 0
        }
        # Переменные для сцены "office"
        self.cabinet_inspected = False
        self.has_pistol = False
        self.search_result = {}
        self.dock_clue = False

        if hasattr(self, 'restart_button'):
            self.restart_button.destroy()

        self.show_scene()
        self.entry.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    game = NoirDetectiveGame(root)
    root.mainloop()