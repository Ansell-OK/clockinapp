from flet import * 
from utils import *
import datetime

def ConfirmationPage(page: Page, myPyrebase):

    date_picker = DatePicker(
        first_date=datetime.datetime(2023, 10, 1),
        last_date=datetime.datetime(2024, 12, 31),
    )

    time_picker = TimePicker(
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
    )

    course_name = TextField(label = 'Course', width = page.width * 0.9,  bgcolor=colors.TRANSPARENT, border_color=colors.WHITE)
    location_name = TextField(label = 'Lecture Hall', width = page.width * 0.9,  bgcolor=colors.TRANSPARENT, border_color=colors.WHITE)
    duration_name = TextField(label = 'Duration', width = page.width * 0.9,  bgcolor=colors.TRANSPARENT, border_color=colors.WHITE)
    level_name = Dropdown(
        width = page.width * 0.9,
        options = [
                    dropdown.Option('400'), 
                    dropdown.Option('300'), 
                    dropdown.Option('200'), 
                    dropdown.Option('100') 
        ]
    )

    def handle_create(e):
        myPyrebase.add_class(course_name.value, location_name.value, str(date_picker.value), str(time_picker.value), duration_name.value, level_name.value)
        page.go('/home')


    page.overlay.append(time_picker)
    page.overlay.append(date_picker)

    confirm_page = Container(
        height = page.height,
        padding = padding.only(
            top = 15, left = 15, right = 15, bottom = 15
        ),
        bgcolor= background_colorway,
        border_radius= 15,
        content = Column(
            [
                Row(
                    [
                    IconButton(icons.CHEVRON_LEFT, icon_color= colors.WHITE, bgcolor= colors.TRANSPARENT, on_click= lambda _: page.go('/home'))
                    ], 
                    alignment= MainAxisAlignment.SPACE_BETWEEN
                ),
                Container(height = 25),
                Text('Create Class', font_family= 'Poppins', size = 25, weight = FontWeight.W_700),
                course_name,
                Container(height = 2),
                location_name,
                Container(height = 2),
                duration_name,
                Container(height = 2),
                level_name,
                Container(height = 2),
                
                Row(
                    [
                        FloatingActionButton(
                            'Pick Time',
                            icon= icons.PUNCH_CLOCK, 
                            on_click=lambda _: time_picker.pick_time()
                        ), 
                        FloatingActionButton(
                            "Pick date",
                            icon=icons.CALENDAR_MONTH,
                            on_click=lambda _: date_picker.pick_date(),
                        )
                    ],
                    alignment = MainAxisAlignment.CENTER
                ), 
                Container(
                    on_click = lambda e: handle_create(e),
                    padding = padding.only(
                                top = 15, left = 15, right = 15, bottom = 15
                            ),
                    gradient = LinearGradient(
                        begin = alignment.center_right, 
                        end=alignment.center_left,
                        colors = colorway1_serious, 
                    ),
                    width = page.width * 0.9,
                    border_radius = 15,
                    content = Text('Create',font_family = 'Poppins', size= 25, weight = FontWeight.W_500, text_align= TextAlign.CENTER )
                    )

            ]
        )
    )


    confirmation_page = Container(
        height = page.height,
        bgcolor= background_colorway, 
        padding = padding.only(
            top =15, left = 15, right=15, bottom=15,
        ), 
        alignment= alignment.center,
        content= confirm_page
    )



    return {
        'view': confirmation_page
    }