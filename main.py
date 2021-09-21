import random as rd
import time

import pandas as pd
import pyautogui
import pyperclip
import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup

suppliers_list = []

list_themes = sg.theme_list()
sg.theme(rd.choice(list_themes))

layout = [
    [sg.Text("Enter the product name and description for the supplier:")],
    [sg.Text("Product name", size=(30, 1)), sg.InputText(key="product_name")],
    [
        sg.Text("Message to seller", size=(30, 1)),
        sg.InputText(key="seller_message"),
    ],
    [
        sg.Text("How many suppliers?", size=(30, 1)),
        sg.Spin([i for i in range(40)], initial_value=0, key="suppliers_number"),
    ],
    [
        sg.Text("Destination folder: "),
        sg.FolderBrowse(button_text="Search", key="destination_folder"),
    ],
    [
        sg.Text("Enter the name of your browser", size=(25, 1)),
        sg.InputText(key="browser_name"),
    ],
    [
        [sg.Text("Automatic contact?", size=(15, 1))],
        sg.Radio(
            "Yes - Automatic contact.",
            "RADIO",
            key="automatic_contact",
            enable_events=True,
        ),
        sg.Radio("No - Just data in a sheet.", "RADIO"),
    ],
    [
        sg.Submit(button_text="Submit", key="Submit"),
        sg.Button("Clean"),
        sg.Exit(button_text="Exit", key="Exit"),
    ],
]

window = sg.Window("Supplier Search - Alibaba", layout, size=(500, 300))


def Clear_input():
    for key in values:
        window[key]("")
    return None


def Attach_file():

    locate_image("media/attach.PNG")
    pyautogui.click(x=374, y=132)
    time.sleep(1)

    locate_image("media/open.png")


def locate_image(arg0):
    attach = pyautogui.locateOnScreen(arg0, confidence=0.7)
    pyautogui.click(attach)
    time.sleep(1)


def Auto_contact():

    base_url = "https://www.alibaba.com/corporations/"
    product_name = values["product_name"]
    seller_message = values["seller_message"]
    suppliers_number = values["suppliers_number"]

    response_site_seller = requests.get(base_url + product_name + ".html")
    content_site_seller = response_site_seller.content
    seller_website = BeautifulSoup(content_site_seller, "html.parser")
    sellers_data = seller_website.findAll("div", attrs={"class": "item-main"})

    # open browser
    pyautogui.press("winleft")
    time.sleep(2)

    pyautogui.write(values["browser_name"])
    delay_time(0.5, 1)
    for index, seller_data in zip(range(int(suppliers_number)), sellers_data):

        company_name = seller_data.find("a", attrs={"target": "_blank"})
        main_products = seller_data.find("div", attrs={"class": "value ellipsis ph"})
        contact_supplier_link = seller_data.find("a", attrs={"class": "button csp"})

        if contact_supplier_link:

            suppliers_list.append(
                [company_name.text, main_products.text, company_name["href"], contact_supplier_link["href"]]
            )
            time.sleep(1)

            # open new window

            pyautogui.hotkey("ctrl", "t")
            time.sleep(1)

            # Fixing bug from PyautoGUI library
            pyperclip.copy(contact_supplier_link["href"])

            # write web site address

            pyautogui.hotkey("ctrl", "v")
            delay_time(1, 5)
            # select textbox

            pyautogui.press("tab", presses=2)

            # write default message

            pyautogui.write(seller_message)
            time.sleep(1)

            # Attach_file()

            # send inquiry
            send_inquiry = pyautogui.locateOnScreen("media/send_inquiry.png", confidence=0.8)
            pyautogui.click(send_inquiry)

        else:
            suppliers_list.append([company_name.text, main_products.text, company_name["href"], ""])

    Collect_data()


def delay_time(arg0, arg1):
    time.sleep(arg0)
    # load seller website

    pyautogui.press("enter")
    time.sleep(arg1)


def Collect_data_only():

    base_url = "https://www.alibaba.com/corporations/"
    product_name = values["product_name"]
    suppliers_number = values["suppliers_number"]

    response_site_seller = requests.get(base_url + product_name + ".html")
    content_site_seller = response_site_seller.content
    seller_website = BeautifulSoup(content_site_seller, "html.parser")
    sellers_data = seller_website.findAll("div", attrs={"class": "item-main"})

    for index, seller_data in zip(range(int(suppliers_number)), sellers_data):

        company_name = seller_data.find("a", attrs={"target": "_blank"})
        main_products = seller_data.find("div", attrs={"class": "value ellipsis ph"})
        contact_supplier_link = seller_data.find("a", attrs={"class": "button csp"})

        if contact_supplier_link:

            suppliers_list.append(
                [company_name.text, main_products.text, company_name["href"], contact_supplier_link["href"]]
            )

        else:
            suppliers_list.append([company_name.text, main_products.text, company_name["href"], ""])

    Collect_data()


def Collect_data():

    destination_folder = values["destination_folder"]
    product_name = values["product_name"]
    collected_data = pd.DataFrame(
        suppliers_list, columns=["Company name", "Main products", "Website", "contact supplier link"]
    )
    collected_data.to_excel(destination_folder + "\\" + str(product_name) + "suppliers" + ".xlsx", index=False)


def main():
    while True:
        try:
            event, values = window.read()
            if event in [sg.WIN_CLOSED, "Exit"]:
                break
            if event == "Clean":
                Clear_input()
            if event == "Submit":
                sg.popup("Search has beggin.")
                Clear_input()
                while True:
                    if values["automatic_contact"]:
                        application_begin_time = time.time()
                        Auto_contact()
                        end_application_time = time.time()
                        sg.popup(
                            f"Sellers successfully contacted!\n\nExecution time: {end_application_time - application_begin_time} Seconds"
                        )
                    else:
                        application_begin_time = time.time()
                        Collect_data_only()
                        end_application_time = time.time()
                        sg.popup(
                            f"Data successfully collected!\n\nExecution time: {end_application_time - application_begin_time} Seconds"
                        )
                    break
        except ValueError:
            sg.popup("Something went wrong. Try again")
    window.close()


if __name__ == "__main__":
    main()
