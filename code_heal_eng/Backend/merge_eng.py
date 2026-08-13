import argparse
from pathlib import Path
import re

import pandas as pd


DEFAULT_FILE_NAME = '陈述句作业1.xlsx'
SHEET_NAME = 'Sheet1'

# 不同句子类型的英文生成方式不一样，后续有新作业时只需要往这里加规则。
SENTENCE_STRUCTURES = [
    {
        'name': '疑问句',
        'columns': ['疑问词', '时表词', '主语', '句剩', '动词', '其他'],
        'suffix': '?',
    },
    {
        'name': '主谓宾/主系表陈述句',
        'columns': ['主', '谓/系', '宾/表', '其他'],
        'suffix': '',
    },
    {
        'name': '双宾语陈述句',
        'columns': ['主', '谓', '间宾', '直宾'],
        'suffix': '',
    },
]


def clean_cell(value):
    if pd.isna(value):
        return ''
    return str(value).strip()


def has_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def read_excel(file_path):
    for header in (1, 0):
        df = pd.read_excel(file_path, sheet_name=SHEET_NAME, header=header)
        if '中文' in df.columns:
            return df
    raise ValueError('没有找到“中文”列，请检查 Excel 表头')


def find_sentence_structure(df):
    for structure in SENTENCE_STRUCTURES:
        if all(col in df.columns for col in structure['columns']):
            return structure
    return None


def capitalize_first(sentence):
    if not sentence:
        return sentence
    return sentence[0].upper() + sentence[1:]


def generate_english(row, structure):
    parts = []
    for col in structure['columns']:
        value = clean_cell(row.get(col))
        if value:
            parts.append(value)

    sentence = capitalize_first(' '.join(parts))
    if sentence and structure['suffix'] and not sentence.endswith(structure['suffix']):
        sentence += structure['suffix']
    return sentence


def ensure_english_column(df):
    if '英文' in df.columns:
        df['英文'] = df['英文'].apply(clean_cell)
        return df, '已有英文列'

    structure = find_sentence_structure(df)
    if structure is None:
        raise ValueError('没有“英文”列，也没有匹配到可拼接英文的句型列')

    df['英文'] = df.apply(lambda row: generate_english(row, structure), axis=1)
    return df, structure['name']


def select_output_columns(df):
    if '时态' in df.columns:
        return ['中文', '时态', '英文']
    if '提示' in df.columns:
        return ['提示', '中文', '英文']
    return ['中文', '英文']


def clean_and_merge_rows(result_df):
    cleaned_rows = []

    for _, row in result_df.iterrows():
        row_dict = {col: clean_cell(row.get(col)) for col in result_df.columns}
        chinese = row_dict.get('中文', '')
        english = row_dict.get('英文', '')

        if not english or english == '?':
            continue
        if chinese == '中文':
            continue

        if chinese:
            cleaned_rows.append(row_dict)
            continue

        # 空中文行只在它确实是一条英文替代表达时合并。章节标题、注释、二级表头会被跳过。
        if cleaned_rows and not has_chinese(english):
            previous_english = cleaned_rows[-1]['英文']
            cleaned_rows[-1]['英文'] = f'{previous_english} | {english}'

    return pd.DataFrame(cleaned_rows, columns=result_df.columns)


def write_csv_without_trailing_newline(df, output_path):
    content = df.to_csv(index=False, encoding='utf-8')
    if content.endswith('\n'):
        content = content[:-1]
    output_path.write_text(content, encoding='utf-8', newline='')


def convert_excel(file_name):
    base_dir = Path(__file__).resolve().parent
    file_path = Path(file_name)
    if not file_path.is_absolute():
        file_path = base_dir / file_path

    output_path = file_path.with_name(f'{file_path.stem}_转换.csv')
    df = read_excel(file_path)
    df, english_source = ensure_english_column(df)

    output_columns = select_output_columns(df)
    result_df = df.loc[:, output_columns].copy()
    result_df = clean_and_merge_rows(result_df)
    write_csv_without_trailing_newline(result_df, output_path)

    print(f'英文来源：{english_source}')
    print(f'转换完成：{file_path.name} -> {output_path.name}，共 {len(result_df)} 行')
    return output_path


def parse_args():
    parser = argparse.ArgumentParser(description='将英语作业 Excel 清洗成前端可用的 CSV')
    parser.add_argument(
        'file_name',
        nargs='?',
        default=DEFAULT_FILE_NAME,
        help=f'要转换的 Excel 文件名，默认：{DEFAULT_FILE_NAME}',
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    convert_excel(args.file_name)
