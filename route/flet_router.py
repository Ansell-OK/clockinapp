from flet import * 
from pages.login import LoginPage 
from pages.register import RegisterPage 
from pages.home import HomePage 
from pages.details import DetailsPage
from pages.edit import ConfirmationPage


class Router(UserControl):
    def __init__(self, page, myPyrebase):
        self.page = page
        self.myPyrebase = myPyrebase
        self.routes = {
            '/': LoginPage(page, myPyrebase),
            '/register': RegisterPage(page, myPyrebase),
            '/home': HomePage(page, myPyrebase),
            '/confirmation': ConfirmationPage(page, myPyrebase)
        }
        self.body = Container(content=self.routes['/']["view"])
    def route_change(self, route):
        route_path = route.route.split("?")[0]
        if route_path in self.routes:
            self.body.content = self.routes[route_path].get("view")
            if self.routes[route_path].get("load"):
                self.routes[route_path].get("load")()
        elif route_path == "/details":
            params = self.parse_route_params(route.route)
            class_id = params.get("class_id")
            if class_id:
                class_page = DetailsPage(self.page, self.myPyrebase, class_id)
                self.body.content = class_page["view"]
                class_page["load"]() 
        self.page.update()
    
    def parse_route_params(self, route):
        params = {}
        if "?" in route:
            param_str = route.split("?")[1]
            for param in param_str.split("&"):
                key, value = param.split("=")
                params[key] = value
        return params