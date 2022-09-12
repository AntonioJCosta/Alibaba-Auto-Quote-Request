from time import time

import PySimpleGUI as sg
from auto_contact import auto_contact
from create_interface import create_interface
from data_to_excel import data_to_excel
from InterfaceKeys import InterfaceKeys
from sellers_data import sellers_data

keys = InterfaceKeys()

if __name__ == "__main__":
    itf_event, itf_values = create_interface()
    sellers_qty = itf_values[keys.sellers_qty]
    prd_name = itf_values[keys.prd_name]
    sellers_msg = itf_values[keys.seller_msg]
    destn_dir = itf_values[keys.destn_dir]
    if itf_event == keys.submit:
        init_time = time()
        sellers_data_list = sellers_data(prd_name, sellers_qty)
        data_to_excel(destn_dir, prd_name, sellers_data_list)
        end_time = time()
        if not itf_values[keys.auto_cont]:
            sg.popup_auto_close(
                "Sucess",
                f"Your search for new sellers was finished with sucess! \n\n Execution time:{round(end_time - init_time, 2)}",
                auto_close_duration=6,
            )
            exit()
        for value in sellers_data_list:
            cont_link = value["dir_cont_link"]
            auto_contact(cont_link, sellers_msg)
            end_time = time()
        sg.popup_auto_close(
            "Sucess",
            f"Sellers contacted with sucess! \n\n Execution time: {round(end_time - init_time, 2)}",
            auto_close_duration=6,
        )
