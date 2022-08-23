from time import time

import PySimpleGUI as sg

from auto_contact import auto_contact
from create_interface import create_interface
from data_to_excel import data_to_excel
from sellers_data import sellers_data

if __name__ == "__main__":
    itf_event, itf_values = create_interface()
    sellers_qty = itf_values["sellers_qty"]
    prd_name = itf_values["prd_name"]
    sellers_msg = itf_values["seller_msg"]
    destn_dir = itf_values["destn_dir"]
    if itf_event == "Submit":
        sg.popup("Your search for new sellers has begin")
        init_time = time()
        sellers_data = sellers_data(prd_name, sellers_qty)
        data_to_excel(destn_dir, prd_name, sellers_data)
        end_time = time()
        if not itf_values["auto_cont"]:
            sg.popup_auto_close(
                f"Your search for new sellers was finished with sucess! \n\n Execution time:{round(end_time - init_time, 2)}",
                auto_close_duration=6,
            )
        else:
            for value in sellers_data:
                for cont_link in value["seller_cont_link"]:
                    auto_contact(cont_link, sellers_msg)
                    end_time = time()
            sg.popup_auto_close(
                f"Sellers contacted with sucess! \n\n Execution time: {round(end_time - init_time, 2)}",
                auto_close_duration=6,
            )
