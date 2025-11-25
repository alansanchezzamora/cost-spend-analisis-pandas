import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_json("aws_cloud_costs.json")


#####
# Which AWS Cost is the most expensive?
#####

cost_by_service = (
    df.groupby("Service")["Cost"]
    .sum()
    .sort_values(ascending=False)
    .nlargest(5)
    .to_frame(name="Cost")
)
total = cost_by_service["Cost"].sum()
cost_by_service["Percent"] = ((cost_by_service["Cost"] / total) * 100).round(2)
print(cost_by_service)


cost_by_service.head(10).plot(kind="bar")
plt.title("Costo total por servicio AWS")
plt.ylabel("Costo ($)")
plt.xlabel("Servicio")
plt.tight_layout()
plt.show()

#############
# Which Account spends more
#############
costs_by_account = (
    df.groupby("account_id")["Cost"]
    .sum()
    .sort_values(ascending=False)
    .nlargest(5)
    .to_frame(name="Cost")
)
total = costs_by_account["Cost"].sum()
costs_by_account["Percent"] = ((costs_by_account["Cost"] / total) * 100).round(2)
print(costs_by_account)

################
# Most expensive region
################
costs_by_region = (
    df.groupby("Region")["Cost"]
    .sum()
    .sort_values(ascending=False)
    .nlargest(5)
    .to_frame(name="Cost")
)
total = costs_by_region["Cost"].sum()
costs_by_region["Percent"] = ((costs_by_region["Cost"] / total) * 100).round(2)
print(costs_by_region)

##########
# Month Trend
############
df["Date"] = pd.to_datetime(df["Date"])
monthly_cost = df.resample("M", on="Date")["Cost"].sum()
print(monthly_cost)

monthly_cost.plot(kind="line")

plt.title("AWS Monthly Cloud Spend")
plt.xlabel("Month")
plt.ylabel("Cost ($)")
plt.tight_layout()
plt.show()


#################
# Pivot
###############


pivot = df.pivot_table(
    values="Cost", index="account_id", columns="Service", aggfunc="sum", fill_value=0
)
print(pivot)
print("Most expensive account:", pivot.sum(axis=1).idxmax())


#############
# Daily Cost Trend
#############
print("\n=== Analysis: Daily Positive Cost Variation ===")

df["Date"] = pd.to_datetime(df["Date"])

daily_cost = df.resample("D", on="Date")["Cost"].sum()

daily_variation = daily_cost.diff()

positive_variation = daily_variation[daily_variation > 0]

positive_df = pd.DataFrame(
    {
        "DailyCost": daily_cost.loc[positive_variation.index],
        "PositiveVariation": positive_variation,
    }
)

top5_positive = positive_df.sort_values(by="PositiveVariation", ascending=False).head(5)

print("\n=== Top 5 Days with the Largest Positive Cost Variations ===")
print(top5_positive)

plt.figure(figsize=(12, 5))
positive_variation.plot(kind="line")

plt.title("Daily Positive AWS Cost Variation (Only Increases)")
plt.xlabel("Date")
plt.ylabel("Cost Increase ($)")
plt.tight_layout()
plt.show()
