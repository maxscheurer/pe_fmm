import pandas as pd
df = pd.read_csv("cppe_runs/solvated_50_errors_serial_intel.csv")

cols = ["p", "theta", "time"]
data = []
for ii, theta in enumerate([0.2, 0.3, 0.5, 0.7, 0.99]):
    for exp_order in [3, 5, 7]:
        time = df[f"time_{theta}_{exp_order}"][0]
        data.append([exp_order, theta, time])
data.append([0, 0.0, df[f"time_direct"][0]])
df_cppe = pd.DataFrame(data, columns=cols)
pt = pd.pivot(df_cppe, index='theta', columns='p', values='time')
print(pt)
print("direct", df['time_direct'][0])