import pandas as pd
import xml.etree.ElementTree as ET

def clean_crimes():
    with open("CrimesbyCountyandAgencySince1990.xml", "r") as f:
        xml_data = f.read()

    root = ET.fromstring(xml_data)

    data_rows = []
    outer_row = root.find('row')
    for inner_row in outer_row.findall('row'):
        if inner_row is not None:
            row_data = {child.tag: child.text for child in inner_row}
            data_rows.append(row_data)

    df = pd.DataFrame(data_rows)
    df = df.dropna()
    df = df[df['months_reported'].astype(int) == 12]
    df = df[~df['year'].astype(int).between(1990, 2000)]

    numeric_columns = [
        'total_index_crimes', 'violent', 'murder', 'forcible_rape', 'robbery',
        'aggravated_assault', 'property', 'burglary', 'larceny', 'motor_vehicle_theft'
    ]

    for col in numeric_columns + ['year']:
        df[col] = df[col].astype(int)

    df = df.groupby(['county', 'year'], as_index=False)[numeric_columns].sum()
    df.to_xml("CrimesbyCountyandAgencySince2010.xml", index=False)

def clean_unemployment():
    df = pd.read_csv('LocalAreaUnemploymentStatistics1976.csv')
    df = df[~df['Year'].astype(int).between(1976, 2000)]
    df = df.drop(columns=['Month'])
    df = df.groupby(['Area', 'Year'], as_index=False).mean(numeric_only=True)
    df.to_csv("LocalAreaUnemploymentStatistics2010.csv", index=False)
    
if __name__ == '__main__':
    clean_crimes()
    clean_unemployment()
