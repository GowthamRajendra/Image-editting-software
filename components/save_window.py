import PySimpleGUI as sg

def create_save_window():
    layout = [
        [
            sg.Text("filename"),
            sg.Input('', key='-S_INPUT-', font=('Arial Bold', 20), expand_x=True),
            sg.Text(".jpg")
        ],
        [
            sg.Button('Save'),
            sg.Cancel()
        ]
    ]

    return sg.Window('Save Image', layout=layout, keep_on_top=True, modal=True)