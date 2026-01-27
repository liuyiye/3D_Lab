import pydicom
import csv

ds1 = pydicom.dcmread(r'C:\1.dcm')  
ds2 = pydicom.dcmread(r'C:\2.dcm')
output = r'C:\diff.csv'
diff = {}

def compare_datasets(ds1, ds2):
    tags1 = {e.tag for e in ds1 if e.tag != (0x7fe0, 0x0010)}
    tags2 = {e.tag for e in ds2 if e.tag != (0x7fe0, 0x0010)}
    
    for tag in tags1 | tags2:
        if tag not in tags1:
            diff[tag] = [ds2[tag].keyword, '', ds2[tag].value]
        elif tag not in tags2:
            diff[tag] = [ds1[tag].keyword, ds1[tag].value, '']
        elif ds1[tag].value != ds2[tag].value:
            diff[tag] = [ds1[tag].keyword, ds1[tag].value, ds2[tag].value]

compare_datasets(ds1.file_meta, ds2.file_meta)
compare_datasets(ds1, ds2)

with open(output, 'w', encoding='utf8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Tag', 'Keyword', 'Value1', 'Value2'])
    for tag, values in diff.items():
        writer.writerow([tag, *values])
