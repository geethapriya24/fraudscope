import pandas as pd
import json
import re

df = pd.read_csv("data/aml_dashboard.csv")
df = df.fillna("")

data = df.to_dict(orient="records")
json_str = json.dumps(data)

with open("dashboard/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Remove any existing embedded data
html = re.sub(r'<script>window\._DATA = .*?;</script>\n\s*', '', html, flags=re.DOTALL)

# Inject new data
inject = f"<script>window._DATA = {json_str};</script>"
html = html.replace("<script>", inject + "\n    <script>", 1)

with open("dashboard/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Real AML data embedded successfully!")
print(f"Total records embedded: {len(data)}")
