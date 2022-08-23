import webbrowser
from time import sleep

import pyautogui as pg


def auto_contact(seller_cont_link: str, seller_msg: str) -> None:
    webbrowser.open(seller_cont_link, new=2)
    sleep(5)
    pg.press("tab", presses=2)
    pg.typewrite(seller_msg)
    send_inq_img = pg.locateCenterOnScreen(
        "./media/send_inquiry.png", confidence=0.7, grayscale=True
    )
    # Click on image if it's available, otherwise, don't click on it.
    pg.click(send_inq_img if send_inq_img != None else ...)
    return None
