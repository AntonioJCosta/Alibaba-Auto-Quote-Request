import requests
from bs4 import BeautifulSoup


def sellers_data(prd_name: str, suppliers_qty: int) -> list:
    base_url = "https://www.alibaba.com/corporations/"

    prod_site = requests.get(f"{base_url}{prd_name}.html")
    site_content = prod_site.content
    soup = BeautifulSoup(site_content, "html.parser")
    prod_containers = soup.findAll("div", attrs={"class": "item-main"})
    data_list = []

    # Get the data from each supplier and prevent to crash if doesn't find enough sellers
    for _, prod_containers in zip(range(suppliers_qty), prod_containers):

        company_name = prod_containers.find("a", attrs={"target": "_blank"})
        main_prods = prod_containers.find("div", attrs={"class": "value ellipsis ph"})
        dir_cont_link = prod_containers.find("a", attrs={"class": "button csp"})
        data_list.append(
            {
                "company_name": company_name.text if company_name != None else "",
                "main_prods": main_prods.text if main_prods != None else "",
                "company_website": company_name["href"] if company_name != None else "",
                "dir_cont_link": dir_cont_link["href"] if dir_cont_link != None else "",
            }
        )
    return data_list
