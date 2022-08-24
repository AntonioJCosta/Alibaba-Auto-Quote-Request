from dataclasses import dataclass


@dataclass(frozen=True)
class InterfaceKeys:
    prd_name = "prd_name"
    seller_msg = "seller_msg"
    sellers_qty = "sellers_qty"
    destn_dir = "destn_dir"
    auto_cont = "auto_cont"
    data_in_excel = "data_in_excel"
    submit = "submit"
    clear = "clear"
    exit = "exit"
