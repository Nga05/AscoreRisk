
import random
import glob
import pandas as pd
from pathlib import Path



# # count - > value_counts()
# # trường hợp cust có nhiều hơn 1 ID
# # check ko lấy random
# # thêm source lấy data từ database
# # lưu file csv
# # thêm ID_no vào response ucả droll
# data = [{"ID": 123, "score": 520}, {"ID": 456, "score": 530}, {"ID": 123, "score": 520}]
# df = pd.DataFrame.from_dict(data, orient='columns')
# print(df)
# df_new = df.groupby(['ID'], as_index=False).value_counts(['']).rename(columns={"count":"num_of_cis"})
# print(df_new)
# print(df_new.drop(["score"], axis=1))  # .drop(["score"], axis=1, inplace=True))



# dbfilepath = str(Path(__file__).parent / "xml/f1_data/f1_ascore_input.csv")
# f1_data = pd.read_csv(dbfilepath, index_col=1).T.to_dict()
# for val in f1_data.values():
#     print(type(val))
#     # print(val)
#     for k2, v2 in val.items():
#         if (k2=='APPLICATION_NUMBER') and (v2=='APPL00250581'):
#             print(val)
#             df_f1 = pd.DataFrame.from_dict(val, orient="columns")
#     break
#         # print(k, val)
# print(df_f1)



dbfilepath = str(Path(__file__).parent / "xml/f1_data/f1_ascore_input.csv")
f1_data = pd.read_csv(dbfilepath)
v2='APPL00250581'
df_f1=f1_data.loc[f1_data.APPLICATION_NUMBER==v2]
print(df_f1['DECISION_DATE'].values)
df_f1 = df_f1.reset_index(drop=True)
print(df_f1)