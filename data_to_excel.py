from pandas import DataFrame


def data_to_excel(destn_dir: str, prd_name: str, sellers_data: list) -> None:
    sellers_data_df = DataFrame(sellers_data)
    # Remove unused value on the dataframe
    sellers_data_df.drop(["dir_cont_link"], axis=1, inplace=True)
    sellers_data_df.to_excel(
        f"{destn_dir}\\{prd_name.title()} Sellers.xlsx", index=False
    )
    return None
