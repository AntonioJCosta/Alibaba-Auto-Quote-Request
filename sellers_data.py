import sys

import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup


def sellers_data(prd_name: str, suppliers_qty: int) -> list:
    base_url = "https://www.alibaba.com/corporations/"

    prod_search_content = requests.get(f"{base_url}{prd_name}.html").content
    soup = BeautifulSoup(prod_search_content, "html.parser")
    prod_containers = soup.findAll("div", attrs={"class": "factory-card"})
    if prod_containers == []:
        sg.popup("No results found for this product", "Please, try another product.")
        sys.exit(1)
    data_list = []

    # Get the data from each supplier and prevent to crash if doesn't find enough sellers
    try:
        for _, container in zip(range(suppliers_qty), prod_containers):

            main_prods = container.find("ul", attrs={"class": "capability"})
            dir_cont_link = container.find("a", attrs={"class": "button csp"})
            company_name = container.find("a", attrs={"target": "_blank"})
            company_website = (
                f'https:{company_name["href"] if company_name is not None else ""}'
            )
            get_website = requests.get(company_website)
            website_content = get_website.content
            soup = BeautifulSoup(website_content, "html.parser")
            dir_cont_link = [
                link["href"]
                for link in soup.findAll(
                    "a",
                    attrs={"class": "shop-component-KeyButton ContactSupplier message"},
                    href=True,
                )
            ]
            data_list.append(
                {
                    "company_name": company_name.text
                    if company_name is not None
                    else "",
                    "main_prods": main_prods.text if main_prods is not None else "",
                    "company_website": company_website
                    if company_name is not None
                    else "",
                    "dir_cont_link": dir_cont_link[0]
                    if dir_cont_link[0] is not None
                    else "",
                }
            )
    except Exception as e:
        sg.popup("Error", f"Error: {e}")
        sys.exit(1)
    return data_list
