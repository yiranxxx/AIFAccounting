import camelot
import os

os.chdir(r"D:\AIF Intern\Accounting\test")

tables = camelot.read_pdf("2021.pdf", flavor='stream', pages="3,4")
tables.export('foo.csv', f='csv')
#tables[0].to_csv('extract_detail.csv')

#camelot.plot(tables[0], kind='contour').show()
