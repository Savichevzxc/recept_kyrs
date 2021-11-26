from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
import sqlite3
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window


class StartWindow(Screen, StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=0, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        conn = sqlite3.connect('recepts.db')
        c = conn.cursor()
        sqlite_select_query = """SELECT * from base"""
        c.execute(sqlite_select_query)
        records = c.fetchall()
        for i in range(len(records)):
            btn = Button(text=records[i][0], size_hint_y=None, height=40)
            layout.add_widget(btn)
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(layout)
        bxl = BoxLayout(pos_hint={ "y" : -0.1})
        bxl.add_widget(root)
        self.add_widget(bxl)
        conn.commit()
        conn.close()



class AddWindow(Screen):
    def takename(self):
        nazvanie = self.ids.nazvanie.text
        return nazvanie
    def takeing(self):
        ingridients = self.ids.ingridients.text
        return ingridients
    def takerec(self):
        receptik = self.ids.receptik.text
        return receptik

class BuyWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


# Designate Our .kv design file
kv = Builder.load_file('recept.kv')


class AwesomeApp(App):

    def build(self):
        conn = sqlite3.connect('recepts.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists base(nazvanie text, ingridients text, receptik text)
		""")
        conn.commit()
        conn.close()
        return kv

    def addR(self):
        conn = sqlite3.connect('recepts.db')
        c = conn.cursor()
        c.execute("""INSERT INTO base VALUES (:nazvanie, :ingridients, :receptik)""",
                  {
                      'nazvanie': AddWindow.takename(self.root.ids.dobavit),
                      'ingridients': AddWindow.takeing(self.root.ids.dobavit),
                      'receptik': AddWindow.takerec(self.root.ids.dobavit),
                  })
        #self.root.ids.dobavit = ''
        conn.commit()
        conn.close()


if __name__ == '__main__':
    AwesomeApp().run()
