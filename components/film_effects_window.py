import PySimpleGUI as sg

def create_film_window():
    layout = [
        [
            sg.Text("Saturation", pad=((0, 26),(25,0))),
            sg.Slider((-255, 255), default_value=0, key="-SAT-", orientation="horizontal", enable_events=True),
            sg.Button("Apply", size=(10,1), pad=((5),(20,0))),
        ],  
        [
            sg.Text("Contrast", pad=((0, 35),(25,0))),
            sg.Slider((-1, 1), resolution=0.01, default_value=0, key="-CON-", orientation="horizontal", enable_events=True),
            sg.Button("Save settings", size=(10,1), pad=((5),(20,0))),
            sg.Button("Load settings", size=(10,1), pad=((5),(20,0))),
        ],
        [
            sg.Text("Color palette", pad=((0, 10),(25,0))),
            sg.Slider((-255, 255), default_value=0, key="-PAL-", orientation="horizontal", enable_events=True),
            sg.Button("Reset", size=(10,1), pad=((5),(20,0))),
            sg.Cancel(size=(10,1), pad=((5),(20,0))),
        ] 
    ]

    return sg.Window('Film Effects', layout=layout, modal=True)