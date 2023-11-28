import PySimpleGUI as sg

def create_menu_bar():
    layout = [
        ["File", ["Open Image", "Save as", "Exit"]],
        ["Image", ["Resize", "Undo All"]],
        ["Colors", ["Histogram Equalization", "Film Effects"]],
        ["Filters", [["Blur", ["Average", "Gaussian"]], "Paintify"]],
    ]

    return sg.Menu(layout)