import pandas as pd
import xml.etree.ElementTree as ET

def clean_crimes():
    # Read xml and extract inner rows (pd.read_xml, tries to read the outer tree element)
    with open("CrimesbyCountyandAgencySince1990.xml", "r") as f:
        xml_data = f.read()

    root = ET.fromstring(xml_data)

    data_rows = []
    outer_row = root.find('row')
    for inner_row in outer_row.findall('row'):
        if inner_row is not None:
            row_data = {child.tag: child.text for child in inner_row}
            data_rows.append(row_data)

    # Remove every entry for years 1990 - 2000
    df = pd.DataFrame(data_rows)
    df = df[~df['year'].astype(int).between(1990, 2010)]
    df.to_xml("CrimesbyCountyandAgencySince2010.xml", index=False)

def clean_unemployment():
    df = pd.read_csv('LocalAreaUnemploymentStatistics1976.csv')
    print(df)
    print(df.columns)
    df = df[~df['Year'].astype(int).between(1976, 2010)]
    print(df)
    df.to_csv("LocalAreaUnemploymentStatistics2010.csv", index=False)
    
    
if __name__ == '__main__':
    clean_crimes()
    clean_unemployment()