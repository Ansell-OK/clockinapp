from flet import *
from utils import * 
import requests
from datetime import datetime
from user_controls.classes import Classes

def HomePage(page: Page, myPyrebase):

    def handle_convo_stream(message):
        try:
            build_classes()
            page.upload()
        except:
            pass

    classes = []

    def build_classes():
        classes.clear()
        data = myPyrebase.get_classes()
        keys = data['classes'].keys()

        for key in keys:
            class_id = key
            course_name = data['classes'][key]['course']
            date = data['classes'][key]['date']
            time = data['classes'][key]['time']

            if date[:10] == date_text.value:
                class_tile = Classes(page, myPyrebase, class_id, course_name, date,
                                    time)
                
                classes.append(class_tile)

    

    def handle_logout(*e):
  
        myPyrebase.kill_all_streams()
        myPyrebase.sign_out()
        page.go("/")

    def open_me1(e, screen_1, screen_2, screen_3): 
        screen_1.height = 0 
        screen_2.height = 0
        screen_3.height = page.height

        page.update()

    url = 'http://worldtimeapi.org/api/timezone/Africa/Lagos'
    
    def get_data_time():
        response = requests.get(url)

        if response.status_code == 200:
            date_time = response.json().get('datetime')
            timezone = response.json().get('timezone')
            dt_object = datetime.fromisoformat(date_time)
            time = dt_object.strftime('%H:%M')
            date = date_time[:10]

            date_text.value = date
            time_text.value = time
            time_zone.value = timezone

    def on_page_load():
        print(page.height)
        if myPyrebase.check_token() == "Success":
            myPyrebase.stream_data_conversation_main(handle_convo_stream)
            get_data_time()
            page.update()
    
    date_text = Text('' ,font_family='Poppins', weight=FontWeight.W_700, size=15)
    time_text = Text('' ,font_family='Poppins', weight=FontWeight.W_700, size=50)
    time_zone = Text('Timezone' ,font_family='Poppins', weight=FontWeight.W_200, size=15)
            
    

    home_page_stack = Container(
        padding = padding.only(
            top=15, left=15, right = 15, bottom=15
        ),
        content = Column
        (
        [
            Row(
                [
                    Text('Home', weight= FontWeight.W_500, size=25, font_family='Poppins'), 
                    Text('')
                ], 
                alignment= MainAxisAlignment.SPACE_BETWEEN
            ), 
            Container(height = page.height * 0.05), 
            time_text, 
            date_text,
            Container(height =5),
            Text('Upcoming Classes' ,font_family='Poppins', weight=FontWeight.W_700, size =20),
            Container(height =2),
            Column(
                classes, 
                scroll= ScrollMode.HIDDEN, 
                height = page.height*0.35
            ), 
            Container(height =5),
            Text('Timezone' ,font_family='Poppins', weight=FontWeight.W_700, size=15),
            Container(height =3),
            Row(
                [
                    Image(src=nigeria_icon, height=15, width=15), 
                    time_zone,
                ]
            ),
            Container(
                height= 0.3, 
                bgcolor= colors.WHITE, 
                width = 270
            ), 
            Container(height=10),
            Row(
                [
                    Text('Timezone' ,font_family='Poppins', weight=FontWeight.W_200, size=15), 
                    Text('                                           '),
                    Switch(value = False)
                ],
                alignment= MainAxisAlignment.SPACE_BETWEEN
            )



        ]
        )

    )

    classes_page_stack =  Container(
        height=0,
     
         padding = padding.only(
            top=15, left=15, right = 15, bottom=15
        ), 
        content= Column
                (
                [
                   Row(
                        [
                            Text('Classes', weight= FontWeight.W_500, size=25, font_family='Poppins'), 
                            Text('')
                        ], 
                        alignment= MainAxisAlignment.SPACE_BETWEEN
                    ), 
                    Container(height = page.height * 0.05),
                    
                   Column(
                       classes, 
                       height = page.height*0.65, 
                       scroll= ScrollMode.HIDDEN
                   ), 
                    
                    Container(
                        on_click = lambda _: page.go('/confirmation'),
                        width =page.width * 0.7,
                        border_radius = 15,
                        gradient= LinearGradient(
                            begin= alignment.center_right, 
                            end=alignment.center_left, 
                            colors=colorway1
                        ), 
                        padding= padding.only(
                            top=10, right = 10, left =10, bottom = 10, 
                        ), 
                        content= Column(
                            [
                                Icon(icons.ADD_BOX_OUTLINED, color= colorway_colorway, size=25),
                                Text('Add Class', font_family= 'Poppins', size=19, weight = FontWeight.W_400)
                            ], 
                            horizontal_alignment= CrossAxisAlignment.CENTER, 
                            alignment= MainAxisAlignment.CENTER
                        )
                    )
                ], 
                height= page.height,
                scroll=ScrollMode.HIDDEN, 
               
                
                )

    )

    clock_page_stack =  Container(
        height=0,
         padding = padding.only(
            top=15, left=15, right = 15, bottom=15
        ),
        content = Column
        (
        [
            Row(
                [
                    Text('Clock', weight= FontWeight.W_500, size=25, font_family='Poppins'), 
                    Text('')
                ], 
                alignment= MainAxisAlignment.SPACE_BETWEEN
            ), 
            Container(height = page.height * 0.05), 
            time_text,
            date_text,
            Container(height=5), 
            Container(
                bgcolor= colors.WHITE,
                border_radius = 100,
                height= 200, 
                width = 200, 
                content = Image(src=big_clock_icon, width=200, height=200)
            ), 
            Container(height =5),
            Text('Timezone' ,font_family='Poppins', weight=FontWeight.W_700, size=15),
            Container(height =3),
            Row(
                [
                    Image(src=nigeria_icon, height=15, width=15), 
                    time_zone,
                ]
            ),
            Container(
                height= 0.3, 
                bgcolor= colors.WHITE, 
                width = page.width * 0.5
            ), 
            Container(height=10),
            Row(
                [
                    Text('Timezone' ,font_family='Poppins', weight=FontWeight.W_200, size=15), 
                    Switch(value = False)
                ],
                width = page.width * 0.5,
                alignment= MainAxisAlignment.SPACE_BETWEEN
            )
        ]
        )

    )

    home_page_content = Row(
        [
            Column(
                [
                   Image(src=logo_icon, width= 25, height = 25),
                   Container(height=150), 
                   Container(
                       on_click = lambda e: open_me1(e, classes_page_stack, clock_page_stack, home_page_stack),
                       content= Column(
                           [
                             Image(src=home_icon, width=30, height=30), 
                             Text('Home',size=15, color= colors.WHITE, font_family = 'Poppins')
                           ], 
                           horizontal_alignment= CrossAxisAlignment.CENTER
                       )
                   ),
                   Container(height=20),
                   Container(
                        on_click = lambda e: open_me1(e, home_page_stack, classes_page_stack, clock_page_stack),
                       content= Column(
                           [
                             Image(src=clock_icon, width=30, height=30), 
                             Text('Clock',size=15, color= colors.WHITE, font_family = 'Poppins')
                           ], 
                           horizontal_alignment= CrossAxisAlignment.CENTER
                       )
                   ), 
                   Container(height=20),
                   Container(
                        on_click = lambda e: open_me1(e, home_page_stack, clock_page_stack, classes_page_stack),
                       content= Column(
                           [
                             Image(src=classes_icon, width=30, height=30), 
                             Text('Classes',size=10, color= colors.WHITE, font_family = 'Poppins')
                           ], 
                           horizontal_alignment= CrossAxisAlignment.CENTER
                       )
                   ),
                   Container(height = page.height * 0.02), 
                   Container(
                        on_click=handle_logout,
                       content= Column(
                           [
                             Image(src=power_icon, width=30, height=30), 
                             Text('Logout',size=10, color= colors.WHITE, font_family = 'Poppins')
                           ], 
                           horizontal_alignment= CrossAxisAlignment.CENTER
                       )
                   )
                ], 
                width= 50, 
                height = page.height, 
                horizontal_alignment= CrossAxisAlignment.CENTER
            ),
            Container(
                height= page.height, 
                bgcolor= colors.WHITE, 
                width=0.1
            ),
            Container(
                content = Stack(
                    [classes_page_stack, 
                    clock_page_stack, 
                    home_page_stack]
                )
            )
            
        ],

    )

    home_page = Container(
        height = page.height,
        bgcolor= background_colorway, 
        padding = padding.only(
            top =15, left = 15, right=15, bottom=15,
        ), 
        content = home_page_content 
    )


    return{
        'view': home_page, 
        'load': on_page_load
    }