import pandas as pd

file_name = '陈述句作业3.xlsx'
processed_file_name = '{}_转换.csv'.format(file_name[:-5])

# 读取Excel（跳过标题行）
df = pd.read_excel(file_name, sheet_name='Sheet1', header=1)
if '中文' not in df.columns:
    # 对于某些 excel，第一行就是标题
    df = pd.read_excel(file_name, sheet_name='Sheet1')

# 生成英文句子
def generate_english(row):
    parts = []
    for col in ['疑问词', '时表词', '主语', '句剩', '动词', '其他']:
        if col in row and pd.notna(row[col]):
            parts.append(str(row[col]).strip())
    return ' '.join(parts).capitalize() + '?'

# 处理数据
if '时态' in df.columns:
    result_df = df[['中文', '时态', '英文']]
# '提示' 这一列是我手动加入到原始 excel中的，
#  因为比如 陈述句作业3.xlsx 中，会有一些提示，比如这句话是表示能力，表示推测等
elif '提示' in df.columns:
    result_df = df[['提示', '中文', '英文']]
else:
    result_df = df[['中文', '英文']]


# Process unnecessary lines and merge lines with '中文' field empty
# 1. 删除英文字段为 "?" 的行
df = result_df[result_df['英文'] != '?']

# 2. 合并中文为空的行（英文合并到上一行，用 " | " 分隔）
for i in range(1, len(df)):
    if pd.isna(df.loc[i, '中文']):  # 如果当前行的中文为空
        prev_en = df.loc[i-1, '英文']  # 获取上一行的英文
        curr_en = df.loc[i, '英文']    # 获取当前行的英文
        if pd.notna(curr_en):         # 如果当前行的英文不为空
            df.loc[i-1, '英文'] = f"{prev_en} | {curr_en}"  # 合并英文
        df = df.drop(i)  # 删除当前行
    # 删除中文是 '中文'的句子
    elif df.loc[i, '中文'] == '中文':
        df = df.drop(i)


# 重置索引
df = df.reset_index(drop=True)

print ("merge sucess")

# 二进制模式写入CSV（兼容旧版pandas）
with open(processed_file_name, 'wb') as f:
    df.to_csv(
        f,
        index=False,
        encoding='utf-8'
    )



# real solve my problem, Actually remove the line break of the last line
with open(processed_file_name, 'r', encoding='utf-8') as file:
    content = file.read()

# 如果末尾有换行符，去掉最后一个换行符
if content.endswith('\n'):
    print ("文件最后一行有空行（换行符）")
    content = content[:-1]

# 重新写入文件（覆盖原文件）
with open(processed_file_name, 'w', encoding='utf-8', newline='') as file:
    file.write(content)

print("转换完成，且已移除文件末尾的换行符 【{}】".format(processed_file_name))

if __name__ == '__main__':
    pass
