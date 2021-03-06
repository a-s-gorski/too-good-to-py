import kivy
# import jnius
# import android
import plyer
import oscpy
from oscpy.server import OSCThreadServer
from time import sleep
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
from tgtg import TgtgClient
import requests
import haversine as hs
from kivy.utils import platform
from kivy.clock import Clock
import math
import datetime
import string


class User:
    def __init__(self, login, password, latitude, longtitude, radius):
        self.login = login
        self.password = password
        self.latitude = latitude
        self.longtitude = longtitude
        self.radius = radius
        self.client = None

    def getLocation(self):
        return (self.longtitude, self.latitude)

    def select_offers(self):
        self.client = TgtgClient(email=self.login, password=self.password)
        items = []
        values = [i / 50 for i in range(-6, 7)]
        for x in values:
            for y in values:
                items.extend(self.client.get_items(
                    favorites_only=False,
                    latitude=self.latitude + x,
                    longitude=self.longtitude + y, radius=1000))
        # print(items[0])

        print("first_imported_items")
        print(len(items))

        return items


class OfferCommand:
    def __init__(self, item):
        self.price = item['item']['price']['minor_units'] / \
                     math.pow(10, item['item']['price']['decimals'])
        self.location = (item['pickup_location']['location']['longitude'],
                         item['pickup_location']['location']['latitude'])
        self.offer_name = item['item']['name']
        self.offer_desc = item['item']['description']
        self.items_available = item['items_available']
        self.address = item['pickup_location']['address']['address_line']
        self.shop = item['store']['store_name']


    def getPrice(self):
        return self.price

    def getLocation(self):
        return self.location

    def getItemsAvailable(self):
        return self.items_available

    def getDistance(self, current_location):
        return hs.haversine(self.location, current_location, unit=hs.Unit.METERS) / 1000

    def getName(self):
        return self.offer_name

    def getDescription(self):
        return self.offer_desc

    def getAddress(self):
        return self.address

    def getShop(self):
        return self.shop

    # def getPurchaseEnd(self):
    #     return self.purchase_end

    def getMinutesLeft(self):
        (self.purchase_end - datetime.datetime.now()).total_seconds() / 60

    def getOffer(self, user):

        offer_result = [self.getDistance(user.getLocation()), self.getShop(), self.getPrice(), self.getAddress(), self.getName()]
        return offer_result


class OfferSelector:
    def __init__(self, lattitude=21.02541225356079, longtitude=52.24983889785303, max_distance=5, searched_patterns=[],
                 max_price=50):
        self.location = (lattitude, longtitude)
        self.max_distance = max_distance
        self.searched_patterns = searched_patterns
        self.max_price = max_price
        self.selected_offers = []

    def set_max_price(self, max_price):
        self.max_price = max_price

    def set_max_distance(self, max_distance):
        self.max_distance = max_distance

    def set_searched_patterns(self, searched_patterns):
        self.searched_patterns = searched_patterns

    def check_max_distance(self, offer):
        return self.max_distance >= offer.getDistance(self.location)

    def check_max_price(self, offer):
        return self.max_price >= offer.getPrice()

    def check_items_available(self, offer):
        return offer.getItemsAvailable() > 0

    def search_patterns(self, offer):
        if not self.searched_patterns or len(self.searched_patterns) == 0:
            return True

        title = offer.getName()
        description = offer.getDescription()
        for pattern in self.searched_patterns:
            if pattern in title or pattern in description:
                return True
        return False

    def check_offer(self, offer):
        try:
            # if not self.check_max_distance(offer):
            #     print("a")
            #     return False

            if not self.check_max_price(offer):
                print("b")
                return False
            if not self.check_items_available(offer):
                print("c")
                return False
            return True
        except:
            print("ERROR or something, idk")
            return False

    def select_offers(self, user):
        items = user.select_offers()
        print(len(items))

        for item in items:
            offer = OfferCommand(item)
            if self.check_offer(offer):
                self.selected_offers.append(offer)
                print(offer.getDistance(current_location=self.location))
        print("----", len(self.selected_offers))

    def get_selected_offers(self, user):
        result_offers = [offer.getOffer(user) for offer in self.selected_offers]
        # for r in result_offers:
        #     print(len(r))
        return result_offers


# activity_port = 3001      for future development of background services
# service_port = 3000
#


class MainScreen(GridLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        # if platform=='android':
        #     from android import AndroidService
        #     service = AndroidService('my pong service', 'running')
        #     service.start('service started')
        #     self.service = service
        # osc = OSCThreadServer()
        # sock = osc.listen(address='127.0.0.1', port=activity_port)
        # osc.bind(sock, self.some_api_callback, '/some_api')
        # Clock.schedule_interval(lambda *x: osc.readQueue(sock), 0)

        # self.service = None
        self.cols = 6
        self.login = StringProperty()
        self.password = StringProperty()
        self.latitude = StringProperty()
        self.longitude = StringProperty()
        self.max_price = StringProperty()
        self.max_distance = StringProperty()
        self.searched_patterns = StringProperty()

        self.login = ""
        self.password = ""
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
        self.SearchPatternsTextField = TextInput(text=",")
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
        # self.update_offers([["10", "ikea", "10", "10", "10"], ["100", "tyskie", "123", "34", "6"],
        #                     []])  # example how to use update offers

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
        if 0 <= len(search_patterns_input) < 100:
            try:
                search_patterns_test = search_patterns_input.split(",")
                self.searched_patterns = search_patterns_input
                self.SearchPatternsDisplay.text = str(self.searched_patterns)
            except Exception:
                self.searched_patterns = ""

    def update_offers(self, offers):
        for counter, offer in enumerate(offers):
            if counter >= 10 or len(offer) != 5:
                continue
            for i in range(1, 6):
                self.Offers[counter][i].text = str(offer[i - 1])[:6]

    def login_button_pressed(self, btn):  # right now nothing more than skeleton for the future
        try:
            self.loginStatusDisplay.text = "True"
            self.login = self.loginTextInput.text
            self.password = self.passwordTextInput.text
            current_user = User(str(self.login), str(self.password), float(self.latitude), float(self.longitude), 10000)
            print(current_user.login)
            print(current_user.password)
            offer_selector = OfferSelector()
            offer_selector.select_offers(current_user)
            offers_to_display = offer_selector.get_selected_offers(current_user)
            # print(offers_to_display[0])
            # print(len(offers_to_display))
            new_offers_list = [offer for offer in offers_to_display if len(offer) == 5]
            new_offers_list = sorted(new_offers_list, key=lambda x:x[0])
            self.update_offers(new_offers_list)


        except Exception as e:  # add custom tgtgApiException
            print(e)
            self.loginStatusDisplay.text = "False"
            print("failure")

    # def some_api_callback(self, message, *args):
    #     return

    # def ping(self):
    #     osc.sendMsg('/some_api', ['ping', ], port=someotherport)


class MyApp(App):

    def build(self):
        print("hello")
        return MainScreen()


if __name__ == '__main__':
    MyApp().run()
