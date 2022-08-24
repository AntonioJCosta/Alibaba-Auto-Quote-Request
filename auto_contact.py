import random
import webbrowser
from time import sleep

import pyautogui as pg


def auto_contact(seller_cont_link: str, seller_msg: str) -> None:
    webbrowser.open(seller_cont_link, new=2)
    sleep(random.randint(5, 6))
    pg.press("tab", presses=2)
    sleep(random.randint(1, 2))
    pg.typewrite(seller_msg)
    send_inq_img = pg.locateCenterOnScreen(
        "./media/send_inquiry.png", confidence=0.7, grayscale=True
    )
    if send_inq_img != None:
        pg.click(send_inq_img)
    return None
