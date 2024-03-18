from DBConnection import connect_db
from insert_data_to_db import insert_data_to_db

# call the main method to read all data from pdf
# call table 1 method
params_transfer1 = ['IA20210708290327','IA','20210702','20210708','RFR0020E','290327','XI FENG','20180209','Active','CITISTAR FINANCIAL INC (FQ6)','AI FINANCIAL POWER GROUP (GK4)']

# call table 2 method
params_transfer2 = ['IA20210708290327','FIRST YEAR COMMISSION ANNUITIES','CHEN, YING','1814113350','47303','20210701','Deposit SF','12.5','','','0.04','0.5','0.5']
# call table 3 method
params_transfer3 = ['IA20210708290327','212946','AI FINANCIAL POWER G','20210702','Transfer XFR','0','741.29','741.29','0']
# check whether duplicate data and insert
db_connection = connect_db()
cursor = db_connection.cursor()
cursor.execute('Select * from CommissionInfo where CommissionID=?', params_transfer1[0])
entry=cursor.fetchone()
if entry is None:
    insert_data_to_db(db_connection, 1, params_transfer1)
    insert_data_to_db(db_connection, 2, params_transfer2)
    insert_data_to_db(db_connection, 3, params_transfer3)
else:
    print ('Duplicate data')
db_connection.commit()
cursor.close()

#for i in range(len(params_transfer)):
#    if params_transfer[i] :
#        insert_data_to_db(db_connection, params_transfer[i] )
#        print("Data inserted successfully.")
#    else:
#        print("No data to insert.")
