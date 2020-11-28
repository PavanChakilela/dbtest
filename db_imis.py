from pathlib import Path
import sqlite3
from sqlite3 import Connection
import streamlit as st
import pandas as pd

URI_SQLITE_DB = "imis1.db"

@st.cache(hash_funcs={Connection: id})
def get_connection(path: str):
    """Put the connection in cache to reuse if path does not change between Streamlit reruns.
    NB : https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    """
    return sqlite3.connect(path, check_same_thread=False)
   
def delete_data_db(conn: Connection):
	conn.execute('DELETE FROM employee')
	conn.commit()

def delete_all_upload_report(conn: Connection):
	conn.execute('DELETE FROM uploadreport')
	conn.commit()    
    
def get_all_data(conn: Connection):
    df = pd.read_sql("SELECT * FROM employee", con=conn)
    return df
    
def get_all_upload_report(conn: Connection):
    df = pd.read_sql("SELECT * FROM uploadreport ORDER BY Upload_timestamp DESC", con=conn)
    return df    
    
def init_db_upload_report(conn: Connection):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS uploadreport
            (
                Report_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                File_Name TEXT,
                Upload_Status TEXT,
                Upload_timestamp DEFAULT (datetime('now', 'localtime'))
            );"""
    )
    conn.commit()
    
        
def init_db(conn: Connection):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS employee
            (
                Customer_Id INT,
                Customer_Name TEXT,
                Associate_Id INT,
                Associate_Name TEXT,
                Designation TEXT,
                Grade_Id TEXT,
                Job_Code TEXT,
                Project_Id	INT,
                Project_Name	TEXT,
                Project_Status	TEXT,
                Project_Billability	TEXT,
                Start_Date	TEXT,
                End_Date	TEXT,
                Associate_Billability	TEXT,
                Operation_Role	TEXT,
                Allocation_Percentage	INT,
                Offshore_Onsite	TEXT,
                Country     TEXT,
                Location	TEXT,
                Location_Description	TEXT,
                Hire_Date	TEXT,
                Manager_Id	INT,
                Manager_Name	TEXT,
                Supervisor_Id	INT,
                Supervisor_Name	TEXT,
                Horizontal_Solution1	TEXT,
                Horizontal_Solution2	TEXT,
                Horizontal_Solution3	TEXT,
                Department_Id	TEXT,
                Department_Name	TEXT,
                IsCritical	TEXT,
                Seat_Number	TEXT,
                Allocation_Status	TEXT,
                Date_Of_Joining	TEXT,
                Actual_Project_Role	TEXT,
                Billability_Reason	TEXT,
                Reason_Description	TEXT,
                Secondary_State_Tag	TEXT,
                Designation_Id	TEXT,
                Grade_Description	TEXT
            );"""
    )
    conn.commit()
    
def save_to_db(conn: Connection, df):    
    for i in range(len(df)):
        #st.write(df.loc[i, 'Customer_Id'], df.loc[i, 'Customer_Name'], df.loc[i, 'Associate_Id'], df.loc[i, 'Associate_Name'], df.loc[i, 'Designation'])
    
        cols = """  Customer_Id, Customer_Name,                                                                 \
                    Associate_Id, Associate_Name, Designation, Grade_Id, Job_Code, Project_Id, Project_Name,    \
                    Project_Status, Project_Billability, Start_Date, End_Date, Associate_Billability,           \
                    Operation_Role, Allocation_Percentage, Offshore_Onsite, Country, Location,                  \
                    Location_Description, Hire_Date, Manager_Id, Manager_Name, Supervisor_Id,                   \
                    Supervisor_Name, Horizontal_Solution1, Horizontal_Solution2, Horizontal_Solution3,          \
                    Department_Id, Department_Name, IsCritical, Seat_Number, Allocation_Status,                 \
                    Date_Of_Joining, Actual_Project_Role, Billability_Reason, Reason_Description,   
                    Secondary_State_Tag, Designation_Id, Grade_Description"""
        
        insert_query = f'INSERT INTO employee({cols}) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        #st.write(df.loc[i, 'Customer_Id'], df.loc[i, 'Customer_Name'],df.loc[i, 'Associate_Id'],df.loc[i, 'Associate_Name']  )
        #st.write(type(df.loc[i, 'Customer_Id']), type(df.loc[i, 'Customer_Name']),type(df.loc[i, 'Associate_Id']),type(df.loc[i, 'Associate_Name'])  )
        conn.execute(insert_query,(
                                    int(df.loc[i, 'Customer_Id']),          \
                                    str(df.loc[i, 'Customer_Name']),        \
                                    int(df.loc[i, 'Associate_Id']),         \
                                    str(df.loc[i, 'Associate_Name']),       \
                                    str(df.loc[i, 'Designation']),          \
                                    str(df.loc[i, 'Grade_Id']),             \
                                    str(df.loc[i, 'Job_Code']),             \
                                    int(df.loc[i, 'Project_Id']),           \
                                    str(df.loc[i, 'Project_Name']),         \
                                    str(df.loc[i, 'Project_Status']),       \
                                    str(df.loc[i, 'Project_Billability']),  \
                                    str(df.loc[i, 'Start_Date']),           \
                                    str(df.loc[i, 'End_Date']),             \
                                    str(df.loc[i, 'Associate_Billability']),\
                                    str(df.loc[i, 'Operation_Role']),       \
                                    int(df.loc[i, 'Allocation_Percentage']),\
                                    str(df.loc[i, 'Offshore_Onsite']),      \
                                    str(df.loc[i, 'Country']),              \
                                    str(df.loc[i, 'Location']),             \
                                    str(df.loc[i, 'Location_Description']), \
                                    str(df.loc[i, 'Hire_Date']),            \
                                    int(df.loc[i, 'Manager_Id']),           \
                                    str(df.loc[i, 'Manager_Name']),         \
                                    int(df.loc[i, 'Supervisor_Id']),        \
                                    str(df.loc[i, 'Supervisor_Name']),      \
                                    str(df.loc[i, 'Horizontal_Solution1']), \
                                    str(df.loc[i, 'Horizontal_Solution2']), \
                                    str(df.loc[i, 'Horizontal_Solution3']), \
                                    str(df.loc[i, 'Department_Id']),        \
                                    str(df.loc[i, 'Department_Name']),      \
                                    str(df.loc[i, 'IsCritical']),           \
                                    str(df.loc[i, 'Seat_Number']),          \
                                    str(df.loc[i, 'Allocation_Status']),    \
                                    str(df.loc[i, 'Date_Of_Joining']),      \
                                    str(df.loc[i, 'Actual_Project_Role']),  \
                                    str(df.loc[i, 'Billability_Reason']),   \
                                    str(df.loc[i, 'Reason_Description']),   \
                                    str(df.loc[i, 'Secondary_State_Tag']),  \
                                    str(df.loc[i, 'Designation_Id']),       \
                                    str(df.loc[i, 'Grade_Description'])  
                        ))                               
        conn.commit()

def save_to_db_upload_report(conn: Connection, filename, status):    
    #st.write(filename, status)
    
    cols = """  File_Name, Upload_Status  """
    
    insert_query = f'INSERT INTO uploadreport({cols}) VALUES (?,?)'
    
    conn.execute(insert_query,(str(filename), str(status)))  
                             
    conn.commit()

