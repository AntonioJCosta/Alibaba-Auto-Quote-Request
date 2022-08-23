from pandas import DataFrame


def data_to_excel(destn_dir: str, prd_name: str, sellers_data):
    sellers_data_frame = DataFrame(
        sellers_data, columns=["Company", "Main Products", "Website", "Direct Contact"]
    )
    # Deletes unused data on DataFrame
    # updt_data_frame = sellers_data_frame.drop(["Direct Contact"], axis=1)
    # Transforms seller DataFrame to an excel file.

    sellers_data_frame.to_excel(
        f"{destn_dir}\\{prd_name.title()} Sellers.xlsx", index=False
    )
    return None
