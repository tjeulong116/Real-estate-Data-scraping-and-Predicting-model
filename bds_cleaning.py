from cmath import nan
from tabulate import tabulate
import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv(filepath_or_buffer="", header = 0)
headers = ["product_id", "price_range", "area", "price_per_m2", "number_of_bedrooms", "number_of_bathrooms", "number_of_stories", "front_length", "legal_status", "isFurnished", "old_address", "post_type", "isVerified", "description", "sublink"]

df = df[headers]

# profile = ProfileReport(df, title="Bds Profiling Report", explorative=True)
# profile.to_file("bds.html")

for index, row in df.iterrows():
    if "triệu/m²" in row["price_range"]:
        df.loc[index, ["price_range", "price_per_m2"]] = df.loc[index, ["price_per_m2", "price_range"]].values

    if pd.isna(row["number_of_stories"]):
        str_arr = str(row["description"]).lower().split(" ")
        for idx, str_item in enumerate(str_arr):
            if str_item.lower() == "tầng":
                #print(row["product_id"], row["sublink"])
                break

    # Convert legal status
    if not pd.isna(row["legal_status"]):
        status_lower = str(row["legal_status"]).lower()
        if "hợp đồng mua bán" in status_lower or "không sổ" in status_lower or "vi bằng" in status_lower or "đang chờ sổ" in status_lower or "sổ chung" in status_lower:
            df.loc[index, ["legal_status"]] = False
        else:
            df.loc[index, ["legal_status"]] = True
    else:
        description_lower = str(row["description"]).lower()
        if "hợp đồng mua bán" in description_lower or "chưa sổ" in description_lower or "không sổ" in description_lower or "vi bằng" in description_lower or "chờ sổ" in description_lower or "sổ chung" in description_lower:
            df.loc[index, ["legal_status"]] = False
        elif "sổ" in description_lower:
            df.loc[index, ["legal_status"]] = True



df["price_range"] = df["price_range"].replace(to_replace="Thỏa thuận", value=nan)
df.dropna(axis=0, subset=["price_range"], inplace=True)
df["price_range"] = df["price_range"].str.replace("~", "")
df["price_range"] = df["price_range"].str.replace("tỷ", "")
df["price_range"] = df["price_range"].str.replace(",", ".")
df["price_range"] = df["price_range"].astype(float)

df["area"] = df["area"].str.replace("m²", "")
df["area"] = df["area"].str.replace(",", ".")
df["area"] = df["area"].astype(float)

df["price_per_m2"] = df["price_per_m2"].str.replace("~", "")
df["price_per_m2"] = df["price_per_m2"].str.replace("triệu/m²", "")
df["price_per_m2"] = df["price_per_m2"].str.replace(",", ".")
df["price_per_m2"] = df["price_per_m2"].astype(float)

df["number_of_bedrooms"] = df["number_of_bedrooms"].str.replace("phòng", "")
df["number_of_bedrooms"] = df["number_of_bedrooms"].astype(int, errors="ignore")

df["number_of_bathrooms"] = df["number_of_bathrooms"].str.replace("phòng", "")
df["number_of_bathrooms"] = df["number_of_bathrooms"].astype(int, errors="ignore")

df["number_of_stories"] = df["number_of_stories"].str.replace("tầng", "")
df["number_of_stories"] = df["number_of_stories"].astype(int, errors="ignore")

df["front_length"] = df["front_length"].str.replace("m", "")
df["front_length"] = df["front_length"].str.replace(",", ".")
df["front_length"] = df["front_length"].astype(float, errors="ignore")

df["old_address"] = df["old_address"].str.replace("(Quận", "")
df["old_address"] = df["old_address"].str.replace("(Huyện", "")
df["old_address"] = df["old_address"].str.replace("(Thị Xã ", "")
df["old_address"] = df["old_address"].str.replace(", Hà Nội cũ)", "")
df["old_address"] = df["old_address"].str.strip()

# Remove outliers
def iqr_trimming(data: pd.DataFrame, feature: str):
    q1 = data[feature].quantile(0.25)
    q3 = data[feature].quantile(0.75)
    iqr = q3 - q1
    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr
    data = data.loc[(lower_limit < df[feature]) & (df[feature] < upper_limit)]
    return data

def percentile_trimming(data: pd.DataFrame, feature: str):
    lower_limit = df[feature].quantile(0.01)
    upper_limit = df[feature].quantile(0.99)
    data = data.loc[(lower_limit < df[feature]) & (df[feature] < upper_limit)]
    return data

before_len = len(df)
print("Số lượng bản ghi ban đầu:", before_len)
for col in ["price_per_m2"]:
    df = percentile_trimming(df, col)

print("Số lượng bản ghi sau khi loại bỏ Outlier:", len(df))
print("Số lượng bản ghi loại bỏ:", before_len - len(df))
print("Tỷ lệ bản ghi loại bỏ:", (before_len - len(df))/before_len * 100, "%")


output_header = ["product_id", "price_range", "area", "price_per_m2", "number_of_bedrooms", "number_of_bathrooms", "number_of_stories", "front_length", "legal_status", "isFurnished", "old_address", "post_type", "isVerified"]
print(tabulate(df[output_header], headers=output_header, tablefmt="psql"))
df_out = df[output_header]
df_out.to_csv(path_or_buf="", header=output_header, index=False)
