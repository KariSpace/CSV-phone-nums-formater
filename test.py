from csvConverter import main
import pandas as pd

main('test.csv')

ok = pd.read_csv('ok_file.csv', sep=";")
phones = ok['phone'].unique()
if len(phones) == 1:
    print('Vsye zaebis\'')
else:
    print('Hueta, blya ' * 3)
