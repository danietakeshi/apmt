import pandas as pd

df_user_info = pd.read_parquet('user_info.parquet')
df_user_letter = pd.read_parquet('user_letter.parquet')

df_result = df_user_info.set_index('nome').join(df_user_letter.set_index('nome'), rsuffix='_l')

print(df_result.columns)

md_file = ''

for index, row in df_result.iterrows():
    md_file = md_file + \
    f"""
![img-{index}]({row['image']}) \n
{index.strip()}  \n
{row['campo_missionario'].strip()}
{row['conjuge'].strip()}
{row['filho'.strip()]}
{row['email'.strip()]}
{row['endereco'.strip()]}
{row['codigo'].strip()} \n
{row['full_text'].strip()} \n
<div style='page-break-after: always;'></div>
    """

#print(md_file)
    
with open('report.md', 'w', encoding='utf-8') as f:
    f.writelines(md_file)
