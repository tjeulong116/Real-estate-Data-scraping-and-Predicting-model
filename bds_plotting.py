import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

#Read file
data = pd.read_csv(filepath_or_buffer="", header = 0)

# sns.histplot(data=data, x="price_range", kde=True, color="blue")
# plt.title("Distribution of Price")
# plt.xlabel("Billions VND")
# plt.ylabel("Frequency")

# sns.boxplot(data=data, x="price_range", color="blue")

# sns.histplot(data=data, x="area", kde=True, color="blue")
# plt.title("Distribution of Area")
# plt.xlabel("Area (m2)")
# plt.ylabel("Frequency")

# sns.boxplot(data=data, x="area", color="blue")

# sns.histplot(data=data, x="price_per_m2", kde=True, color="blue")
# plt.title("Distribution of Price per m2")
# plt.xlabel("Price per m2 (Millions VND/m2)")
# plt.ylabel("Frequency")

# sns.boxplot(data=data, x="price_per_m2", color="blue")

# sns.countplot(data=data, y="number_of_bedrooms", order=data["number_of_bedrooms"].value_counts(ascending=True).index, color="blue")
# plt.title("Count of Number of bedrooms")
# plt.xlabel("Frequency")
# plt.ylabel("Number of bedrooms")

#sns.boxplot(data=data, x="number_of_bedrooms", color="blue")

# sns.countplot(data=data, y="number_of_bathrooms", order=data["number_of_bathrooms"].value_counts(ascending=True).index, color="blue")
# plt.title("Count of Number of bathrooms")
# plt.xlabel("Frequency")
# plt.ylabel("Number of bathrooms")

# sns.boxplot(data=data, x="number_of_bathrooms", color="blue")

# sns.countplot(data=data, y="number_of_stories", order=data["number_of_stories"].value_counts(ascending=True).index, color="blue")
# plt.title("Distribution of Number of stories")
# plt.xlabel("Frequency")
# plt.ylabel("Number of stories")

# sns.histplot(data=data, x="front_length", kde=True, color="blue")
# plt.title("Distribution of Front Length")
# plt.xlabel("Front Length")
# plt.ylabel("Frequency")

# sns.boxplot(data=data, x="front_length", color="blue")

# sns.countplot(data=data, y="old_address", order=data["old_address"].value_counts(ascending=True).index, color="blue")
# #sns.boxplot(data=data, x="price_range", color="blue")
# plt.title("Count of Districts")
# plt.xlabel("Frequency")
# plt.ylabel("District")
# plt.tight_layout()

# Scatterplot
# sns.scatterplot(data=data, x="area", y="price_range")

# Heatmap
# sns.heatmap(data.corr(numeric_only=True), annot=True, cmap="YlGnBu")

# Geographic analysis
filter_district = []
for key, value in data.groupby("old_address")["product_id"].count().to_dict().items():
    if value < 10:
        filter_district.append(key)

# ppm_per_district = (data.query(f"old_address not in {filter_district}")
#                     .groupby("old_address")["price_per_m2"]
#                     .mean().sort_values())
# ppm_per_district.plot.barh()

# price_per_district = (data.query(f"old_address not in {filter_district}")
#                     .groupby("old_address")["price_range"]
#                     .mean().sort_values())
# price_per_district.plot.barh()

plt.show()


