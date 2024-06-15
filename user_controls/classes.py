from flet import * 
from utils import *

class Classes(UserControl):
    def __init__(self, page, myPyrebase, class_id, course_name, date, time):
        super().__init__()
        self.page = page 
        self.myPyrebase = myPyrebase
        self.class_id = class_id
        self.course_name = course_name
        self.date = date
        self.time = time


    def go_to_class(self, e):
        class_url = f'/details?class_id={self.class_id}'
        self.page.go(class_url)

    
    def build(self):
        return Container(
                        on_click=self.go_to_class,
                        width=290, 
                        border_radius= 15, 
                        padding = padding.only(
                            top=10, left = 10, right = 10, bottom = 10
                        ),
                        gradient= LinearGradient(
                            colors= colorway1_serious, 
                            begin=alignment.center_right, 
                            end= alignment.center_left
                        ), 
                        content = Column(
                            [
                                Row(
                                    [
                                        Text(f'{self.date[:10]}' ,font_family='Poppins', weight=FontWeight.W_200, size=15), 
                                        Icon(icons.TIMELINE, size=20, color=colors.WHITE)

                                    ], 
                                    alignment= MainAxisAlignment.SPACE_BETWEEN
                                ),
                                Row(
                                    [
                                        Text(f'{self.course_name}' ,font_family='Poppins', weight=FontWeight.W_200, size=15), 
                                        Text('')

                                    ], 
                                    alignment= MainAxisAlignment.SPACE_BETWEEN
                                ),
                                Row(
                                    [
                                        Text(f'{self.time[:5]}' ,font_family='Poppins', weight=FontWeight.W_600, size=25), 
                                        Icon(icons.ARROW_DROP_DOWN, color=colors.WHITE, size=25)

                                    ], 
                                    alignment= MainAxisAlignment.SPACE_BETWEEN
                                )
                            ]
                        )
                    )