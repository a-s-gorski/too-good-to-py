
import kivy

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.pagelayout import PageLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
import tgtg
import requests
import haversine



class MainScreen(GridLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.cols = 6
        self.login = StringProperty()
        self.password = StringProperty()
        self.latitude = StringProperty()
        self.longitude = StringProperty()
        self.max_price = StringProperty()
        self.max_distance = StringProperty()
        self.searched_patterns = StringProperty()

        self.login = "default-none"
        self.password = "default-none"
        self.latitude = str(52.23)
        self.longitude = str(21.01)
        self.max_price = str(100)
        self.max_distance = str(10)
        self.loginSuccessful = False
        self.selected_offers = []
        self.searched_patterns = ""
        self.offer_id_list = [i for i in range(1, 11)]
        self.distance_list = [None for _ in range(10)]
        self.shop_list = [None for _ in range(10)]
        self.price_list = [None for _ in range(10)]
        self.address_list = [None for _ in range(10)]
        self.Offers = [[Label(text="") for _ in range(6)] for _ in range(10)]

        self.loginLabel = Label(text="log")
        self.loginTextInput = TextInput(text=self.login)
        self.loginStatusLabel = Label(text="login \n status")
        self.loginStatusDisplay = Label(text=str(self.loginSuccessful))

        self.passwordLabel = Label(text="pass")
        self.passwordTextInput = TextInput(text=self.password)

        self.loginTGTG = Button(text="login")
        self.loginTGTG.bind(on_press=self.login_button_pressed)

        self.SetParamsLabel = Label(text="set \n params")
        self.DisplayParams = Label(text="params ")

        self.LatitudeLabel = Label(text="lat.")
        self.LatitudeTextField = TextInput(text="lat")
        self.LatitudeDisplay = Label(text=self.latitude)

        self.LongitudeLabel = Label(text="long.")
        self.LongitudeTextFiled = TextInput(text="long")
        self.LongitudeDisplay = Label(text=self.longitude)

        self.MaxPriceLabel = Label(text="max \n price")
        self.MaxPriceTextField = TextInput(text="100")
        self.MaxPriceDisplay = Label(text=self.max_price)

        self.MaxDistanceLabel = Label(text="max \n dist(km)")
        self.MaxDistanceTextField = TextInput(text="10.0")
        self.MaxDistanceDisplay = Label(text=self.max_distance)

        self.SearchPatternsLabel = Label(text="Src \n patt")
        self.SearchPatternsTextField = TextInput(text="pizza, kawa")
        self.SearchPatternsDisplay = Label(text=self.searched_patterns)

        self.SetParamsButton = Button(text="set \n Params")
        self.SetParamsButton.bind(on_press=self.pressed_params_button)

        self.OffersNumberLabel = Label(text="id")
        self.DistanceLabel = Label(text="dist \n (km)")
        self.ShopLabel = Label(text="shop")
        self.PriceLabel = Label(text="price")
        self.AddressLabel = Label(text="addr")
        self.NameLabel = Label(text="name")

        self.create_gui()
        self.update_offers([["10", "ikea", "10", "10", "10"], ["100", "tyskie", "123", "34", "6"],
                            []])  # example how to use update offers

    def add_login_widgets(self):
        self.add_widget(self.loginLabel)
        self.add_widget(self.loginTextInput)
        self.add_widget(self.loginStatusLabel)
        self.add_widget(self.loginStatusDisplay)
        for i in range(2):
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

    def add_offers_widgets(self):
        self.add_offers_labels()

    def add_offers_labels(self):
        self.add_widget(self.OffersNumberLabel)
        self.add_widget(self.DistanceLabel)
        self.add_widget(self.ShopLabel)
        self.add_widget(self.PriceLabel)
        self.add_widget(self.AddressLabel)
        self.add_widget(self.NameLabel)
        for i in range(10):
            self.Offers[i][0].text = str(self.offer_id_list[i])
            for j in range(6):
                self.add_widget(self.Offers[i][j])

    def create_gui(self):
        self.add_login_widgets()
        self.add_param_widgets()
        self.add_offers_widgets()

    def pressed_params_button(self, btn):
        latitude_input = str(self.LatitudeTextField.text)
        longitude_input = str(self.LongitudeTextFiled.text)
        max_price_input = str(self.MaxPriceTextField.text)
        max_distance_input = str(self.MaxDistanceTextField.text)
        search_patterns_input = str(self.SearchPatternsTextField.text)
        print("hello")
        print(self.latitude)

        if 0 < len(latitude_input) < 10:
            try:
                latitude_input = float(latitude_input)
                self.latitude = latitude_input
                # self.LatitudeDisplay.text = self.latitude
            except ValueError:
                pass
        if 0 < len(longitude_input) < 10:
            try:
                longitude_input = float(longitude_input)
                self.longitude = longitude_input
                self.LongitudeDisplay.text = str(self.longitude)
            except ValueError:
                pass
        if 0 < len(max_price_input) < 10:
            try:
                max_price_input = int(max_price_input)
                self.max_price = max_price_input
                self.MaxPriceDisplay.text = str(self.max_price)
            except ValueError:
                pass
        if 0 < len(max_distance_input) < 5:
            try:
                max_distance_input = int(max_distance_input)
                self.max_distance = max_distance_input
                self.MaxDistanceDisplay.text = str(self.max_distance)
            except ValueError:
                pass
        if 0 < len(search_patterns_input) < 100:
            try:
                search_patterns_test = search_patterns_input.split(",")
                self.searched_patterns = search_patterns_input
                self.SearchPatternsDisplay.text = str(self.searched_patterns)
            except Exception:
                pass

    def update_offers(self, offers):
        for counter, offer in enumerate(offers):
            if counter >= 10 or len(offer) != 5:
                continue
            for i in range(1, 6):
                self.Offers[counter][i].text = str(offer[i - 1])

    def login_button_pressed(self, btn):  # right now nothing more than skeleton for the future
        try:
            self.loginStatusDisplay.text = "True"
            request = requests.get("http://www.kite.com", timeout=0.5)
            print("success")

            # define client
            # move on
            # here will be loging function
            # later add custom button for searching offers
            # and move here classes from backend
        except Exception:  # add custom tgtgApiException
            self.loginStatusDisplay.text = "False"
            print("failure")



class MyApp(App):

    def build(self):
        print("hello")
        return MainScreen()


if __name__ == '__main__':
    MyApp().run()
