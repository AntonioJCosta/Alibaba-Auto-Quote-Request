from random import choice

import PySimpleGUI as sg

from clear_input import clear_input


def create_interface() -> tuple:
    # Get a list of all themes avaliable
    themes_list = sg.theme_list()
    # Choices a random theme
    sg.theme(choice(themes_list))
    layout = [
        [sg.Text("Enter the product name and description for the supplier:")],
        [sg.Text("Product name", size=(30, 1)), sg.InputText(key="prd_name")],
        [
            sg.Text("Message to seller", size=(30, 1)),
            sg.InputText(key="seller_msg"),
        ],
        [
            sg.Text("How many suppliers?", size=(30, 1)),
            sg.Spin([i for i in range(40)], initial_value=0, key="sellers_qty"),
        ],
        [
            sg.Text("Directory of destiny"),
            sg.FolderBrowse(button_text="Search", key="destn_dir"),
        ],
        [
            [sg.Text("Automatic contact?", size=(15, 1))],
            sg.Radio(
                "Yes - Automatic contact.",
                "RADIO",
                key="auto_cont",
                enable_events=True,
            ),
            sg.Radio("No - Just data in a sheet.", "RADIO"),
        ],
        [
            sg.Submit(),
            sg.Button("Clear"),
            sg.Exit(),
        ],
    ]

    window = sg.Window(
        "Auto Sellers Search On Alibaba e-commerce", layout, size=(500, 300)
    )
    while True:
        event, values = window.read()
        if event == "Clear":
            clear_input(values, window)
        return event, values
