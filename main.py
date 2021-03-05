import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.pagelayout import PageLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput



class MainScreen(GridLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.cols = 6

        self.login = "default-none"
        self.password = "default-none"
        self.latitude = None
        self.longitude = None
        self.max_price = None
        self.max_distance = None
        self.selected_offers = None


        self.loginLabel = Label(text="login")
        self.loginTextInput = TextInput(text=self.login)
        self.passwordLabel = Label(text="password")
        self.passwordTextInput = TextInput(text=self.password)
        self.loginTGTG = Button(text="login to TgTg")

        self.SetParamsLabel = Label(text="set your params")
        self.DisplayParams = Label(text="params display")
        self.LatitudeLabel = Label(text="latitude")
        self.LatitudeTextField = TextInput(text="lat")
        self.LatitudeDisplay = Label(text="not set yet")
        self.LongitudeLabel = TextInput(text="longitude")
        self.LongitudeTextFiled = TextInput(text="long")
        self.LongitudeDisplay = TextInput(text="not set yet")
        self.MaxPriceLabel = TextInput(text="max price")
        self.MaxPriceTextField = TextInput(text="100")
        self.MaxPriceDisplay = Label(text="not set yet")
        self.MaxDistanceLabel = TextInput(text="max distance(km)")
        self.MaxDistanceTextField = TextInput(text="10.0")
        self.MaxDistanceDisplay = Label(text="not set yet")
        self.SearchPatternsLabel = Label(text="Search patterns")
        self.SearchPatternsTextField = TextInput(text="pizza, kawa")
        self.SearchPatternsDisplay = Label(text="notsetyet")
        self.SetParamsButton = Button(text="setParams")



        self.createGui()

    def add_login_widgets(self):
        self.add_widget(self.loginLabel)
        self.add_widget(self.loginTextInput)
        for i in range(4):
            self.add_widget(Label())
        self.add_widget(self.passwordLabel)
        self.add_widget(self.passwordTextInput)
        self.add_widget(self.loginTGTG)
        for i in range(3):
            self.add_widget(Label())

    def add_param_widgets(self):
        self.add_widget(self.SetParamsLabel)
        self.add_widget(Label())
        self.add_widget(self.DisplayParams)
        for i in range(3):
            self.add_widget(Label())
        self.add_widget(self.LatitudeLabel)
        self.add_widget(self.LatitudeTextField)
        self.add_widget(self.LatitudeDisplay)
        for i in range(3):
            self.add_widget(Label())
        self.add_widget(self.LongitudeLabel)
        self.add_widget(self.LongitudeTextFiled)
        self.add_widget(self.LongitudeDisplay)
        for i in range(3):
            self.add_widget(Label())
        self.add_widget(self.MaxPriceLabel)
        self.add_widget(self.MaxPriceTextField)
        self.add_widget(self.MaxPriceDisplay)
        for i in range(3):
            self.add_widget(Label())
        self.add_widget(self.MaxDistanceLabel)
        self.add_widget(self.MaxDistanceTextField)
        self.add_widget(self.MaxDistanceDisplay)
        for i in range(3):
            self.add_widget(Label())
        self.add_widget(self.SearchPatternsLabel)
        self.add_widget(self.SearchPatternsTextField)
        self.add_widget(self.SearchPatternsDisplay)
        self.add_widget(self.SetParamsButton)
        for i in range(2):
            self.add_widget(Label())





    def createGui(self):
        self.add_login_widgets()
        self.add_param_widgets()







class MyApp(App):

    def build(self):
        print("hello")
        return MainScreen()


if __name__ == '__main__':
    MyApp().run()