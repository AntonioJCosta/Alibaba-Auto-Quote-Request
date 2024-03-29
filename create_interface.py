from random import choice

import PySimpleGUI as sg

from clear_input import clear_input
from InterfaceKeys import InterfaceKeys

keys = InterfaceKeys()


def create_interface() -> tuple:
    # Get a list of all themes avaliable
    themes_list = sg.theme_list()
    # Choices a random theme
    sg.theme(choice(themes_list))
    layout = [
        [sg.Text("Enter the product name and description for the supplier:")],
        [
            sg.Text("Product name", size=(30, 1)),
            sg.InputText(key=keys.prd_name),
        ],
        [
            sg.Text("Message to seller", size=(30, 1)),
            sg.InputText(key=keys.seller_msg),
        ],
        [
            sg.Text("How many suppliers?", size=(30, 1)),
            sg.Spin(
                [i for i in range(1, 40)],
                initial_value=1,
                key=keys.sellers_qty,
            ),
        ],
        [
            sg.Text("Directory of destiny"),
            sg.FolderBrowse(button_text="Search", key=keys.destn_dir),
        ],
        [
            [sg.Text("Automatic contact?", size=(15, 1))],
            sg.Radio(
                "Yes - Automatic contact.",
                "RADIO",
                key=keys.auto_cont,
            ),
            sg.Radio(
                "No - Just data in a excel file",
                "RADIO",
                key=keys.data_in_excel,
            ),
        ],
        [
            sg.Submit(button_text="Submit", key=keys.submit),
            sg.Button("Clear", key=keys.clear),
            sg.Exit(button_text="Exit", key=keys.exit),
        ],
    ]

    window = sg.Window(
        "Auto Search for Sellers On Alibaba e-commerce", layout, size=(500, 300)
    )
    while True:
        event, values = window.read()
        if event == keys.clear:
            clear_input(values, window)
            continue
        if event in (sg.WIN_CLOSED, keys.exit):
            sg.popup("Bye!", "Thanks for using my program!")
            window.close()
            exit()
        if event == keys.submit:
            try:
                if 0 <= int(values[keys.sellers_qty]) >= 40:
                    sg.popup(
                        "Error",
                        "You must enter a number greater than 0 and less than 40",
                    )
                    continue
            except ValueError:
                sg.popup(
                    "Error",
                    "You must enter a number character on the sellers quantity spinbox",
                )
                continue
            if values[keys.prd_name] == "":
                sg.popup("Error", "You must enter a product name")
                continue
            if values[keys.destn_dir] == "":
                sg.popup("Error", "You must enter a directory")
                continue
            if values[keys.auto_cont] and values[keys.seller_msg] == "":
                sg.popup("Error", "You must enter a message to seller")
                continue

        sg.popup("Sucess!", "Your search for new sellers has been submitted")
        clear_input(values, window)
        return event, values
