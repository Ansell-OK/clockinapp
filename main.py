from flet import * 
from route.flet_router import Router
from db.flet_pyrebase import PyrebaseWrapper

def main(page:Page):
    page.window_height = 914
    page.padding = 0 
    page.adaptive = 0 

    page.fonts = {
        'Poppins': 'https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap'
    }
    
    myPyrebase = PyrebaseWrapper(page)
    myRouter = Router(page, myPyrebase)

    page.on_route_change = myRouter.route_change

    page.add(
        myRouter.body
    )

    page.go('/')


app(target=main)