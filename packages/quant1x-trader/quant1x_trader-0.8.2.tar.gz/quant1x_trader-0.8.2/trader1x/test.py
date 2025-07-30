import time

import pandas as pd
import xtquant.xtdata as xtdata

# 禁止显示XtQuant的hello信息
xtdata.enable_hello = False
code = "SH,SZ"
code_list = code.split(",")
start = time.time()
data = xtdata.get_full_tick(code_list)
end = time.time()
print(f"耗时: {end - start:.4f} 秒")
df = pd.DataFrame(data)
print(df['600600.SH'])

holidays = xtdata.get_holidays()
print(holidays)
