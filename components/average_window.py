import PySimpleGUI as sg

def create_average_window():
    layout = [
        [
            sg.Text(
                text='Average filter',
                justification='center',
                font=('Arial Bold', 15),
            ),
            sg.Slider(
                range=(1, 15), 
                default_value=0, 
                resolution=1, 
                tick_interval=7, 
                orientation='horizontal',
                key='-AVG_SLIDER-',
                expand_x=True
            ),
            sg.Button('Apply'),
            sg.Button('Reset'),
            sg.Cancel()
        ],
    ]

    return sg.Window('Average Blur', layout=layout, modal=True)