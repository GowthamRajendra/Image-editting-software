import PySimpleGUI as sg

def create_gauss_window():
    layout = [
        [
            sg.Text(
                text='Gaussian Filter',
                justification='center',
                font=('Arial Bold', 15),
            ),
            sg.Slider(
                range=(1, 15), 
                default_value=0, 
                resolution=1, 
                tick_interval=7, 
                orientation='horizontal',
                key='-GAU_SLIDER-',
                expand_x=True
            ),
            sg.Button('Apply'),
            sg.Button('Reset'),
            sg.Cancel()
        ],
    ]

    return sg.Window('Gaussian Blur', layout=layout, keep_on_top=True, modal=True)
