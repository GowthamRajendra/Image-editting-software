import PySimpleGUI as sg

def create_paintify_window():
    layout = [
        [
            sg.Text("Stroke length", pad=((0, 26),(25,0))),
            sg.Slider((1,20), default_value=0, orientation="h", key="-S_LEN-"),
        ],
        [
            sg.Text("Stroke width", pad=((0, 29),(25,0))),
            sg.Slider((1,20), default_value=0, orientation="h", key="-S_WID-"),
            sg.Button("Paint", size=(10,1), pad=((5),(20,0))),
        ],
        [
            sg.Text("Threshold", pad=((0, 45),(25,0))),
            sg.Slider((0,255), default_value=0, orientation="h", key="-THRESHOLD-"),
            sg.Cancel(size=(10,1), pad=((5),(20,0))),
        ]  
    ]

    return sg.Window('Paintify', layout=layout, keep_on_top=True, modal=True)