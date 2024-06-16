from flet import * 
from utils import *

def LoginPage(page:Page, myPyrebase):


    page.fonts = {
        'Poppins': 'https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap'
    }

    email = TextField(label='Email', bgcolor=colors.TRANSPARENT, border_color= colors.WHITE, border_radius= 15, height= 65, color= colors.WHITE)
    password = TextField(label='Password', bgcolor=colors.TRANSPARENT, border_color= colors.WHITE, border_radius= 15, height= 65, color= colors.WHITE, password=True)


    def handle_sign_in_error():
        page.snack_bar = SnackBar(
            content=Text("Incorrect Info. Please Try Again.", color=colors.WHITE),
            bgcolor=colors.RED
        )
        page.snack_bar.open = True
        page.update()

    def handle_sign_in(e):
        try:
            myPyrebase.sign_in(email.value, password.value)
            password.value = ""
            page.go("/home")
        except:
            handle_sign_in_error()
            page.update()


    page_content = Column(
        [
            Row(
                [
                    IconButton(icon=icons.CANCEL_OUTLINED, icon_color= colors.WHITE, bgcolor=colors.TRANSPARENT, icon_size=15), 
                    Text('')
                ], 
                alignment= MainAxisAlignment.SPACE_BETWEEN
            ), 
            Column(
                [
                    email,
                    Container(height=10),
                    password, 
                    Container(height = 10), 
                    Container(
                            height = 65, 
                            width = 150,
                            on_click= handle_sign_in,
                            border_radius = 15,
                            gradient= LinearGradient(
                                begin= alignment.center_right, 
                                end= alignment.center_left,
                                colors= colorway1_serious, 
                                tile_mode= GradientTileMode.MIRROR
                            ), 
                            content = Row(
                                [
                                    Text('Login',size=15, color= colors.WHITE, font_family = 'Poppins')
                                ],
                                alignment = MainAxisAlignment.CENTER
                            )
                    ), 
                    Row(
                        [
                          Text('Do not have an account? ',size=15, color= colors.WHITE, font_family = 'Poppins'), 
                          TextButton('Register', on_click = lambda _: page.go('/register')) 
                        ], 
                        alignment = MainAxisAlignment.CENTER
                    )
                ], 
                horizontal_alignment= CrossAxisAlignment.CENTER
            )
        ]
    )

    login_page_content = Container(
        height = page.height * 0.45, 
        padding = padding.only(
            top =10, right=10, left = 10 , bottom = 10
        ),
        gradient= LinearGradient(
            begin= alignment.center_right, 
            end= alignment.center_left,
            colors= colorway1, 
            tile_mode= GradientTileMode.MIRROR
        ), 
        border_radius = 35,
        alignment= alignment.center,
        content = page_content

    )

    login_page = Container(
        height = page.height,
        bgcolor= background_colorway, 
        padding = padding.only(
            top =15, left = 15, right=15, bottom=15,
        ), 
        alignment= alignment.center, 
        content = login_page_content
    )


    return{
        'view': login_page
    }