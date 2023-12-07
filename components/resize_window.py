import PySimpleGUI as sg

def create_resize_window():
    layout = [
        [ # resize height input
            sg.Text("height"),
            sg.Input('', enable_events=True, key='-H_INPUT-', font=('Arial Bold', 20), expand_x=True),
            sg.Text("px"),
        ],
        [
            sg.Text("width"),
            sg.Input('', enable_events=True, key='-W_INPUT-', font=('Arial Bold', 20), expand_x=True),
            sg.Text("px"),
        ],
        [
            sg.Checkbox("constrained", key='-C_BOX-')
        ],
        [
            sg.Text("Interpolation Type: "),
            sg.Combo(["Nearest Neighbor", "Bilinear", "Bicubic Spline", "Bicubic Convolution"], "Nearest Neighbor", readonly=True, key="-INTER_CHOOSER-"),
        ],
        [
            sg.Button("Resize"),
            sg.Cancel()
        ]
    ]
    
    return sg.Window('Resize Image', layout=layout, modal=True)