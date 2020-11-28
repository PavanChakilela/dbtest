import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import openpyxl
import os
import base64
from io import BytesIO
import xlrd
from datetime import datetime

# Database Functions
from db_imis import *

# Open CSV (unsed currently)
@st.cache(persist=True, allow_output_mutation=True)
def explore_data_csv(dataset):
    df = pd.read_csv(dataset)
    dataset.seek(0)
    return df
       
#select specific sheet from the excel for processing
def select_sheet_excel(my_datafile, sheets, key):
    #for i in range(len(sheets)):
    #    df = pd.read_excel(my_datafile, sheet_name = sheets[i])
    
    sheet_choice = st.radio(f"Select the appropriate sheet for processing from ==> ({my_datafile.name})",sheets, key=key)
    
    df = pd.read_excel(my_datafile, sheet_name = sheet_choice)
    return df 
    
# To Improve speed and cache data
@st.cache(persist=True, allow_output_mutation=True)
def explore_data(my_datafile):
    all_sheet = pd.ExcelFile(my_datafile)   
    sheets = all_sheet.sheet_names
    return sheets  
    
# Open Excel and Select specific sheets in an excel for processing
def file_excel_explore_data(my_datafile, key):
    sheets = explore_data(my_datafile)   
        
    df = select_sheet_excel(my_datafile, sheets, key)
    return df     
    
def to_excel_dev(df1, df2, sh1, sh2, filename, df3=None):
    output = BytesIO()
    writer = pd.ExcelWriter(output)
    df1.to_excel(writer, sheet_name=sh1, index = True)
    df2.to_excel(writer, sheet_name=sh2, index = True)
    if df3 is None:
        testa = 0
    else:    
        df3.to_excel(writer, sheet_name=sh1, startrow = len(df1.index)+4, index = True) #Hard coded startrow=20 to be removed ???
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df1, df2, sh1, sh2, filename, df3=None):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe1, dataframe2, sheetname1, sheetname2, filename
    out: href string
    """
    val = to_excel_dev(df1, df2, sh1, sh2, filename, df3)
    b64 = base64.b64encode(val)  # val looks like b'...' 
    n = datetime.now()
    filename_timestamp = f'{filename}_{n.year}_{n.month}_{n.day}_{n.hour}_{n.minute}_{n.second}.xlsx'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download={filename_timestamp}>Download as **({filename_timestamp})** file</a>' # decode b'abc' => abc    

#Still Pending ???
def file_selector(folder_path='./downloads'):
	filenames = os.listdir(folder_path)
	selected_filename = st.selectbox('Select a file', filenames)
	return os.path.join(folder_path, selected_filename)
       
#Convert to FTE from Allocation %    
def conv_alloc_FTE(proj_data):     
    proj_data['FTE'] = proj_data['Allocation_Percentage']/100.0

    return proj_data     
    
#Map Designations 
def map_designations(proj_data):     
    pd.options.mode.chained_assignment = None  # default='warn'
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E80", 'Designation'] = "PAT"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E82", 'Designation'] = "PAT"     #Analyst Trainee considered as PAT
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E85", 'Designation'] = "PAT"     #Programmer Trainee considered as PAT
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E90", 'Designation'] = "PAT"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E75", 'Designation'] = "PA"      #Programmer considered as PA
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E70", 'Designation'] = "PA"   
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E65", 'Designation'] = "A" 
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "N65", 'Designation'] = "A"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E60", 'Designation'] = "SA"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "N60", 'Designation'] = "SA"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E50", 'Designation'] = "M"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "N50", 'Designation'] = "M"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E45", 'Designation'] = "SM"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "N45", 'Designation'] = "SM"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E40", 'Designation'] = "AD"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "N40", 'Designation'] = "AD"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E35", 'Designation'] = "D"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "N35", 'Designation'] = "D"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E33", 'Designation'] = "SD"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "N33", 'Designation'] = "SD"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E30", 'Designation'] = "SD"      #SBU Head - Practice considered as SD
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E25", 'Designation'] = "SD"      #SBU Head - MDU considered as SD
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "E20", 'Designation'] = "SD"      #SBU Leader - INS considered as SD
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "C80", 'Designation'] = "CWR"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "C75", 'Designation'] = "CWR"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "C70", 'Designation'] = "CWR"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "C65", 'Designation'] = "CWR"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "C60", 'Designation'] = "CWR"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "C50", 'Designation'] = "CWR"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "C45", 'Designation'] = "CWR"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "C40", 'Designation'] = "CWR"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "C35", 'Designation'] = "CWR"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "C33", 'Designation'] = "CWR"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "NC4", 'Designation'] = "CWR"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "NC2", 'Designation'] = "CWR"
    proj_data.loc[proj_data.loc[:, 'Grade_Id'] == "C97", 'Designation'] = "CWR"
    return proj_data     
    
#Calculate and Display FTE counts 
def display_FTE_count(proj_data):      
    
    c1,c2,c3, c4 = st.beta_columns([1.2,1,1,1])
            
    with c1:
        with st.beta_expander("Count of Associates"):
            st.write(len(proj_data))

    with c2:
        with st.beta_expander("Total FTE"):
            st.write(proj_data['FTE'].sum().round(2))

    with c3:
        with st.beta_expander("Onsite FTE"):
            on_filter = (proj_data['Offshore_Onsite'] == 'Onsite')
            st.write(proj_data[on_filter]['FTE'].sum().round(2)) 

    with c4:
        with st.beta_expander("Offshore FTE"):
            off_filter = (proj_data['Offshore_Onsite'] == 'Offshore')
            st.write(proj_data[off_filter]['FTE'].sum().round(2))
    return proj_data  

def get_new_labels(sizes, labels):
    new_labels = [label if size > 1 else '' for size, label in zip(sizes, labels)]
    return new_labels
    
def my_autopct(pct):
    return ('%1.1f%%' % pct) if pct > 5 else '' 

#calc percentages of pie 
def cal_pie_percentages(proj_FTE_matrix, location):            
    f1 = (proj_FTE_matrix.loc["PAT",location] + proj_FTE_matrix.loc["PA",location]) / (proj_FTE_matrix.loc["TOTAL",location]) * 100.0
    f2 = (proj_FTE_matrix.loc["A",location]) / (proj_FTE_matrix.loc["TOTAL",location]) * 100.0
    f3 = (proj_FTE_matrix.loc["SA",location]) / (proj_FTE_matrix.loc["TOTAL",location]) * 100.0
    f4 = (proj_FTE_matrix.loc["M",location]) / (proj_FTE_matrix.loc["TOTAL",location]) * 100.0
    f5 = (proj_FTE_matrix.loc["SM",location] + proj_FTE_matrix.loc["AD",location] +\
          proj_FTE_matrix.loc["D",location] + proj_FTE_matrix.loc["SD",location]) / (proj_FTE_matrix.loc["TOTAL",location]) * 100.0
    fracs =  [f1, f2, f3, f4, f5] 
    return fracs

#DataFrame for Project FTE split
    #       Offshore    Onsite  TOTAL
    #PAT
    #PA
    #A
    #SA
    #M
    #SM
    #AD
    #D
    #SD
    #CWR
    #TOTAL
def display_FTE_designation_split(proj_data):    
    proj_FTE_matrix = pd.DataFrame({'Offshore' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \
                                      'Onsite' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \
                                       'TOTAL' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]})
    
    # round to two decimal places in python pandas 
    pd.set_option('precision', 2)   
    
    proj_FTE_matrix['Designation'] = "PAT PA A SA M SM AD D SD CWR TOTAL".split()
    proj_FTE_matrix.set_index('Designation', inplace=True)
    
    designation_list = ["PAT", "PA", "A", "SA", "M", "SM", "AD", "D", "SD", "CWR", "TOTAL"]
    location_list = ["Offshore", "Onsite"]
    
    #Per each Designation & Location
    for designation in designation_list:
        for location in location_list:
            des_filter = (proj_data['Designation'] == designation) & (proj_data['Offshore_Onsite'] == location)
            proj_FTE_matrix.loc[designation,location] = proj_data[des_filter]['FTE'].sum()
    
    #Total Offshore
    des_filter = (proj_data['Offshore_Onsite'] == 'Offshore')
    proj_FTE_matrix.loc['TOTAL','Offshore'] = proj_data[des_filter]['FTE'].sum()
        
    #Total Onsite    
    des_filter = (proj_data['Offshore_Onsite'] == 'Onsite')
    proj_FTE_matrix.loc['TOTAL','Onsite'] = proj_data[des_filter]['FTE'].sum()

    #Total Column (sum of Offshore & Onsite rows)
    proj_FTE_matrix.loc[:,'TOTAL'] = proj_FTE_matrix.loc[:,'Offshore'] + proj_FTE_matrix.loc[:,'Onsite']
    
    c1,c2 = st.beta_columns([1.5,2])
     
    #Display FTE Designation Matrix View 
    with c1:
        cm = sns.light_palette("green", as_cmap=True) 
        st.dataframe(proj_FTE_matrix.style.background_gradient(cmap=cm))

    with c2:
        labels = 'PA-', 'A', 'SA', 'M', 'SM+'
        f1 = 0
        f2 = 0
        f3 = 0
        f4 = 0 
        f5 = 0
                    
        # Make figure and axes
        fig, axs = plt.subplots(2, 2)          
                    
        # TOTAL pie plot
        if proj_FTE_matrix.loc["TOTAL","TOTAL"] > 0:
            total_fracs = cal_pie_percentages(proj_FTE_matrix, "TOTAL")        
            axs[0, 0].set_title("Overall")    
            patches, texts, autotexts = axs[0, 0].pie(total_fracs, labels=get_new_labels(total_fracs, labels), autopct=my_autopct, textprops={'size': 'smaller'}, \
                                        shadow=True, explode=(0, 0, 0, 0, 0), startangle=90)  
            plt.setp(autotexts, size='x-small')
            autotexts[0].set_color('white')        
        
        # TOTAL On/Off ratio
        if proj_FTE_matrix.loc["TOTAL","TOTAL"] > 0:
            f1 = (proj_FTE_matrix.loc["TOTAL","Onsite"]) / (proj_FTE_matrix.loc["TOTAL","TOTAL"]) * 100.0
            f2 = (proj_FTE_matrix.loc["TOTAL","Offshore"]) / (proj_FTE_matrix.loc["TOTAL","TOTAL"]) * 100.0
            axs[0, 1].set_title("On/Off Ratio")
            axs[0, 1].pie([f1, f2], labels=['On', 'Off'], autopct='%.0f%%', shadow=True, explode=(0, 0), startangle=90)
                      
        #Offshore pie plot   
        if proj_FTE_matrix.loc["TOTAL","Offshore"] > 0:
            off_fracs = cal_pie_percentages(proj_FTE_matrix, "Offshore")
            axs[1, 0].set_title("Offshore")    
            patches, texts, autotexts = axs[1, 0].pie(off_fracs, labels=get_new_labels(off_fracs, labels), autopct=my_autopct, textprops={'size': 'smaller'}, \
                                        shadow=True, explode=(0, 0, 0, 0, 0), startangle=90)  
            plt.setp(autotexts, size='x-small')
            autotexts[0].set_color('white')
        
        #Onsite pie plot   
        if proj_FTE_matrix.loc["TOTAL","Onsite"] > 0:
            on_fracs = cal_pie_percentages(proj_FTE_matrix, "Onsite")
            axs[1, 1].set_title("Onsite")    
            patches, texts, autotexts = axs[1, 1].pie(on_fracs, labels=get_new_labels(on_fracs, labels), autopct=my_autopct, textprops={'size': 'smaller'}, \
                                        shadow=True, explode=(0, 0, 0, 0, 0), startangle=90)  
            plt.setp(autotexts, size='x-small')
            autotexts[0].set_color('white')                                

        st.pyplot(fig) 
    
    return proj_data, proj_FTE_matrix
    
# MultiSelect based on Location / Designation / Department / StartDate / EndDate / AssociateName / Supervisor
def filter_specific_criteria(proj_data, proj2_data):    
    menu_list = st.multiselect("",("Location","Designation","Department","StartDate","EndDate","AssociateName","Supervisor"), key="fil2")
    st.write("You selected",len(menu_list),"fields")
               
    filt_loc = []
    filt_des = []
    filt_dep = []
    filt_name = []
    filt_startdate = []
    filt_enddate = []
    filt_supervisor = []
    for menu_2 in menu_list:
    
        menu_Location = proj2_data['Offshore_Onsite'].unique().tolist()
        menu_Designation = proj2_data['Designation'].unique().tolist()  
        menu_Department = proj2_data['Department_Name'].unique().tolist()
        menu_StartDate = proj2_data['Start_Date'].unique().tolist()
        menu_EndDate = proj2_data['End_Date'].unique().tolist()
        menu_associate_name = proj2_data['Associate_Name'].unique().tolist()
        menu_Supervisor = proj2_data['Supervisor_Name'].unique().tolist()
        
        if menu_2 == "Location":
            st.subheader("Chose Location")
            filt_loc = st.multiselect("",menu_Location, key="loc")
            
            #Apply Filter
            proj2_filter = (proj2_data['Offshore_Onsite'].isin(filt_loc))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]
                            
        elif menu_2 == "Designation":
            st.subheader("Chose Designation")
            filt_des = st.multiselect("",menu_Designation, key="des")
            
            #Apply Filter
            proj2_filter = (proj2_data['Designation'].isin(filt_des))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]
            
        elif menu_2 == "Department":
            st.subheader("Chose Department")
            filt_dep = st.multiselect("",menu_Department, key="dep")    
            
            #Apply Filter
            proj2_filter = (proj2_data['Department_Name'].isin(filt_dep))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]
            
        elif menu_2 == "AssociateName":
            st.subheader("Chose AssociateName")
            filt_name = st.multiselect("",menu_associate_name, key="nam")    
            
            #Apply Filter
            proj2_filter = (proj2_data['Associate_Name'].isin(filt_name))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]   

        elif menu_2 == "StartDate":
            st.subheader("Chose StartDate")
            filt_startdate = st.multiselect("",menu_StartDate, key="stdate")    
            
            #Apply Filter
            proj2_filter = (proj2_data['Start_Date'].isin(filt_startdate))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]   

        elif menu_2 == "EndDate":
            st.subheader("Chose EndDate")
            filt_enddate = st.multiselect("",menu_EndDate, key="endate")    
            
            #Apply Filter
            proj2_filter = (proj2_data['End_Date'].isin(filt_enddate))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]   

        elif menu_2 == "Supervisor":
            st.subheader("Chose Supervisor")
            filt_supervisor = st.multiselect("",menu_Supervisor, key="sup")    
            
            #Apply Filter
            proj2_filter = (proj2_data['Supervisor_Name'].isin(filt_supervisor))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]
                     
    #Display Filtered Dataframe
    st.dataframe(proj2_data[['Associate_Id', 'Associate_Name', 'Designation', 'Project_Name', 'FTE', 'Offshore_Onsite', \
                             'Department_Name', 'Start_Date', 'End_Date', 'Supervisor_Name']], height=200)
    
    return proj_data, proj2_data
    
#compare 2 diff sheets    
def data_diff3(df1, df2):
    comparison_values = df1.eq(df2) 
    #st.dataframe(comparison_values)
    rows,cols=np.where(comparison_values==False)
    print(rows, cols)
    for item in zip(rows,cols):
        df1.iloc[item[0], item[1]] = '{} --> {}'.format(df1.iloc[item[0], item[1]],df2.iloc[item[0], item[1]])
    st.dataframe(df1)  
    df1.to_csv('diff.csv') 

def dataframe_difference(df1, df2, which=None):
    """Find rows which are different."""
    comparison_df = pd.merge(df1, df2, indicator=True, how='outer')
    if which is None:
        diff_df = comparison_df[comparison_df['_merge'] != 'both']
    else:
        diff_df = comparison_df[comparison_df['_merge'] == which]
    return diff_df    
    

#Check if "FTE view of Merged 2 sheets (MBM & BTM)"
def file_upload_2(data1):    
    st.sidebar.warning("Do you want to Merge with 2nd IMIS file?")
    my_dataset2 = st.sidebar.file_uploader("Upload 2nd IMIS Allocation File in XLSX format", type=["xlsx"], key="file2")
    data3=data1
    if my_dataset2 is not None:
        #Open IMIS file2
        data2 = file_excel_explore_data(my_dataset2, key="FTEsh2") 
                
        #Append this file2 IMIS contents
        #data3 = data1.append(data2, ignore_index=True, sort=False) 
        data3 = pd.concat([data1, data2], sort=False, ignore_index=True) 
    return data3, my_dataset2  

def pipeline_opp_handling():
    pipe_dataset1 = st.sidebar.file_uploader("Upload Bulk Upload File in XLSX format", type=["xlsx"], key="opp1")
    if pipe_dataset1 is not None:

        #Open PipeLine Opportunity File for Bulk Upload
        pipe_data1 = file_excel_explore_data(pipe_dataset1, key="Oppsh1")
        
        #Opportunities Specific
        st.subheader("Show Opportunity details")          
                  
        pipe_data1['TCV'] = pipe_data1['Total Deal Value']
        pipe_data1['COGTCV'] = pipe_data1['Cogni Revenue $']
      
        #Display project specific DataFrame for the selected List of Projects
        st.dataframe(pipe_data1)
        
        c1,c2 = st.beta_columns([1,1.25])
    
        #Display Shared vs Small TCV
        with c1:
            # Make figure and axes
            fig, axs = plt.subplots(1,1)
                                                
            shared_filter = (pipe_data1['Segment'] == 'Shared')            
            shared_tcv = pipe_data1[shared_filter]['TCV'].sum()/1000000.0
                       
            small_filter = (pipe_data1['Segment'] == 'Small')            
            small_tcv = pipe_data1[small_filter]['TCV'].sum()/1000000.0
                        
            shared_cogtcv = pipe_data1[shared_filter]['COGTCV'].sum()/1000000.0
            small_cogtcv = pipe_data1[small_filter]['COGTCV'].sum()/1000000.0            
                                    
            xaxis = ["SHC-TCV", "SHC-COG", "SC-TCV", "SC-COG"]
            yaxis = [shared_tcv, shared_cogtcv, small_tcv, small_cogtcv]
            plt.bar(xaxis, yaxis)

            plt.title("(Shared vs Small) vs (Overall Deal vs Cog) in Mil")
            plt.ylabel("in USD mil")
            plt.xlabel("(Shared vs Small) vs (Overall Deal vs Cog)")
            
            for i in range(len(yaxis)):
                plt.annotate(str(yaxis[i]), xy=(i,yaxis[i]), ha='center')
               
            st.pyplot(fig)

        with c2:                        
            # Make figure and axes
            fig, axs = plt.subplots(1,1)
            plt.title("Application vs TCV view (in USD Mil)")
            plt.xlabel("TCV in USD Mil")
            plt.ylabel("Application")
            axs.barh(pipe_data1['Application'], pipe_data1['TCV']/1000000.0 )
               
            st.pyplot(fig)
        
        # Multi Plots
        if st.checkbox("Dynamic Multi Column Plot for TCV vs COGTCV"):
            st.text("Bar Charts By Target/Columns")

            all_columns_names = pipe_data1.columns.tolist()
            all_columns_names.remove('TCV')
            all_columns_names.remove('Total Deal Value')
            all_columns_names.remove('COGTCV')
            all_columns_names.remove('Cogni Revenue $')                
            
            primary_col = st.multiselect('Select Primary Column To Group By',all_columns_names, default="Segment", key="pri")
            selected_column_names = st.multiselect('Select Columns',['TCV', 'COGTCV'], default="TCV", key="sec")
            plot_choice = st.radio("",("Vert Plot", "Hz Plot"))
            st.text("Generating Plot for: {} and {}".format(primary_col,selected_column_names))
            if selected_column_names:
                vc_plot = pipe_data1.groupby(primary_col)[selected_column_names].sum()/1000000.0
                st.write(vc_plot)        
            else:
               vc_plot = pipe_data1.iloc[:,-1].value_counts()
            
            if plot_choice == "Vert Plot":        
                st.write(vc_plot.plot(kind='bar'))
            else:
                st.write(vc_plot.plot(kind='barh'))
                
            #enable download as hyperlink
            st.markdown(get_table_download_link(vc_plot, pipe_data1, 'Pipeline-Opp', 'Original', 'OppDown1'), unsafe_allow_html=True)
                
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
            
def display_trends(proj_data, proj_FTE_matrix):
    
    # round to two decimal places in python pandas 
    pd.set_option('precision', 2)   

    #Generate pivot for FTE COUNTS
    pivot_proj_FTE_count = pd.DataFrame(proj_data)
    pivot_proj_FTE_count.rename(columns = {'Project_Name':'ProjectName'}, inplace = True)
    pivot_proj_FTE_count["FTE"] = pivot_proj_FTE_count["Allocation_Percentage"]/100.0
        
    #use cross tab for % normalization at index level i.e. project-name
    pivot_proj_FTE_count2 = pd.crosstab([pivot_proj_FTE_count.ProjectName], \
                                        columns=pivot_proj_FTE_count.Designation, \
                                        values=pivot_proj_FTE_count.FTE, aggfunc=sum, margins=True, margins_name="FTETotal")
    
    #pivot_proj_FTE = pd.pivot_table(proj_data, index=["Project_Name"], columns=["Designation"], \
    #                                           values=["Allocation_Percentage"], aggfunc='sum',  margins=True)                                         
    #pivot_proj_FTE.rename(columns = {'Allocation_Percentage':'FTE'}, inplace = True)
    #pivot_proj_FTE["FTE"] = pivot_proj_FTE["FTE"]/100.0
    
    pivot_proj_FTE_count2.replace(np.nan,0.0, inplace=True)
    cm2 = sns.light_palette("green", as_cmap=True)
    st.dataframe(pivot_proj_FTE_count2.style.background_gradient(cmap=cm2))
    
    #extend to % FTE per each row
    pivot_proj_FTE_pct = pd.DataFrame(proj_data)
    pivot_proj_FTE_pct.rename(columns = {'Project_Name':'ProjectName'}, inplace = True)
    pivot_proj_FTE_pct["FTE"] = pivot_proj_FTE_pct["Allocation_Percentage"]/100.0
                                                  
    #use cross tab for % normalization at index level i.e. project-name
    pivot_proj_FTE_pct2 = pd.crosstab([pivot_proj_FTE_pct.ProjectName], \
                                        columns=pivot_proj_FTE_pct.Designation, \
                                        values=pivot_proj_FTE_pct.FTE, aggfunc=sum, margins=True, margins_name="FTETotal", normalize='index')                                               
    
    #convert all values into 100%    
    pivot_proj_FTE_pct2 = pivot_proj_FTE_pct2[:] * 100
    cm3 = sns.light_palette("green", as_cmap=True)
    st.dataframe(pivot_proj_FTE_pct2.style.background_gradient(cmap=cm3))
    
    df = pivot_proj_FTE_count2  # FTE count
    df2 = pivot_proj_FTE_pct2   # FTE % at project level (row-wise)    
    
    #enable download as hyperlink
    st.markdown(get_table_download_link(pivot_proj_FTE_count2, proj_data, 'Pivot-%-FTE', 'OverallFTE', 'FTE-%-Pivot', pivot_proj_FTE_pct2), unsafe_allow_html=True)

    all_columns_names = df.columns.tolist()
    all_columns_names.remove('FTETotal')
    type_of_plot = st.selectbox("Select the Type of Plot for ***FTE Trend#***", ["barh", "bar", "line", "area"])
    selected_column_names = st.multiselect('Select Columns To Plot', all_columns_names, default="A", key="tre1")
    
    st.success("Customizable Plot (1. **FTE-Count-View**) & (2. **FTE % View**) of: {} for :: {}".format(type_of_plot,selected_column_names))
    
    c1,c2 = st.beta_columns([1,1])
            
    #Display 
    with c1:
        fig, axs = plt.subplots()
        #fig = plt.figure()
        plt.title("FTE Trend Plots")
        plt.ylabel("FTE count#")
        
        #Remove FTETotal Row for FTE count - to provide better readability in the graphs 
        df3 = df[:-1]

        custom_plot = df3[selected_column_names]
        st.write(custom_plot.plot(kind=type_of_plot))
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        
    #Display 
    with c2:
        fig1, axs = plt.subplots()
        plt.title("FTE Trend Plots")
        plt.ylabel("FTE count#")
        # FTETotal is still not working in FTE% pivot / crosstab
        for column in selected_column_names:
            if column == 'FTETotal':
                selected_column_names.remove('FTETotal')
        custom_plot = df2[selected_column_names]
        st.write(custom_plot.plot(kind=type_of_plot))
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
     
#                       Offshore    Onsite
#   A-
#   SA+
#   Current_SPAN
#   Target_Conversion
#   Revised_SPAN
def span_details(proj_data, proj_FTE_matrix):     
    
    proj_SPAN_matrix = pd.DataFrame({'Offshore' : [0.0, 0.0, 0.0, 0.0, 0.0], \
                                      'Onsite'  : [0.0, 0.0, 0.0, 0.0, 0.0], })
    
    # round to two decimal places in python pandas 
    pd.set_option('precision', 2)   
    
    proj_SPAN_matrix['typeDesignation'] = "A- SA+ Current_SPAN Target_Conversion Revised_SPAN".split()
    proj_SPAN_matrix.set_index('typeDesignation', inplace=True)
    
    location_list = ["Offshore", "Onsite"]
    target_span = dict({"Offshore" : 3, "Onsite" : 0.25})
    
    for location in location_list:
        proj_SPAN_matrix.loc["A-",location] = proj_FTE_matrix.loc["PAT"][location] + \
                                                proj_FTE_matrix.loc["PA"][location] + \
                                                proj_FTE_matrix.loc["A"][location]
                                                
        proj_SPAN_matrix.loc["SA+",location] = proj_FTE_matrix.loc["SA"][location] + \
                                                 proj_FTE_matrix.loc["M"][location] + \
                                                 proj_FTE_matrix.loc["SM"][location] + \
                                                 proj_FTE_matrix.loc["AD"][location] + \
                                                 proj_FTE_matrix.loc["D"][location] + \
                                                 proj_FTE_matrix.loc["SD"][location] + \
                                                 proj_FTE_matrix.loc["CWR"][location]
                                                 
        x = proj_SPAN_matrix.loc["A-",location]
        y = proj_SPAN_matrix.loc["SA+",location]
        
        proj_SPAN_matrix.loc["Current_SPAN",location] = x / y
        
        target = target_span.get(location)
    
        #Considering only Designation SWAP as the lever
        proj_SPAN_matrix.loc["Target_Conversion",location] = (target * y - x)/(1 + target)
        
        conv_target = (target * y - x)/(1 + target)
        
        #Considering only Designation SWAP as the lever
        proj_SPAN_matrix.loc["Revised_SPAN",location] = (x + conv_target)/(y - conv_target)
        
                                                
    c1, c2, c3 = st.beta_columns([1.8,1, 1])
    
    #Display FTE Designation Matrix View 
    with c1:
        cm = sns.light_palette("green", as_cmap=True) 
        st.success("***Current*** SPAN;")
        st.write("Target_Conv assumed ONLY from SA+ to A-")
        st.dataframe(proj_SPAN_matrix.style.background_gradient(cmap=cm))
        
        proj_SPAN_rev_matrix = proj_SPAN_matrix 
        #cm = sns.light_palette("green", as_cmap=True) 
        #st.success("Revised SPAN Based on Your Levers")
        #st.dataframe(proj_SPAN_rev_matrix.style.background_gradient(cmap=cm))        

    with c2:
        st.write("Apply Offshore Levers")
        off_promotion = st.number_input("Promotion (A to SA)",0.0,10.0, step = 1.0, key="oflev1")
        off_a_rampup = st.number_input("A- RampUp",0.0,20.0, step = 1.0, key="oflev2")
        off_a_rampdown = st.number_input("A- RampDown",0.0,20.0, step = 1.0, key="oflev3")
        off_sa_rampup = st.number_input("SA+ RampUp",0.0,20.0, step = 1.0, key="oflev4")
        off_sa_rampdown = st.number_input("SA+ RampDown",0.0,20.0, step = 1.0, key="oflev5")
        
        location = "Offshore"
        x = proj_SPAN_rev_matrix.loc["A-",location]
        y = proj_SPAN_rev_matrix.loc["SA+",location]
        
        x = (x - off_promotion + off_a_rampup  - off_a_rampdown)
        y = (y + off_promotion + off_sa_rampup - off_sa_rampdown)
        
        proj_SPAN_rev_matrix.loc["A-",location] = x
        proj_SPAN_rev_matrix.loc["SA+",location] = y
        proj_SPAN_rev_matrix.loc["Current_SPAN",location] = x / y
        
        target = target_span.get(location)
    
        #Considering only Designation SWAP as the lever
        proj_SPAN_rev_matrix.loc["Target_Conversion",location] = (target * y - x)/(1 + target)
        
        conv_target = (target * y - x)/(1 + target)
        
        #Considering only Designation SWAP as the lever
        proj_SPAN_rev_matrix.loc["Revised_SPAN",location] = (x + conv_target)/(y - conv_target)
        
    with c3:
        st.write("Apply Onsite Levers")
        on_promotion = st.number_input("Promotion (A to SA)",0.0,10.0, step = 1.0, key="onlev1")
        on_a_rampup = st.number_input("A- RampUp",0.0,20.0, step = 1.0, key="onlev2")
        on_a_rampdown = st.number_input("A- RampDown",0.0,20.0, step = 1.0, key="onlev3")
        on_sa_rampup = st.number_input("SA+ RampUp",0.0,20.0, step = 1.0, key="onlev4")
        on_sa_rampdown = st.number_input("SA+ RampDown",0.0,20.0, step = 1.0, key="onlev5")
        
        location = "Onsite"
        x = proj_SPAN_rev_matrix.loc["A-",location]
        y = proj_SPAN_rev_matrix.loc["SA+",location]
        
        x = (x - on_promotion + on_a_rampup  - on_a_rampdown)
        y = (y + on_promotion + on_sa_rampup - on_sa_rampdown)
        
        proj_SPAN_rev_matrix.loc["A-",location] = x
        proj_SPAN_rev_matrix.loc["SA+",location] = y
        proj_SPAN_rev_matrix.loc["Current_SPAN",location] = x / y
        
        target = target_span.get(location)
    
        #Considering only Designation SWAP as the lever
        proj_SPAN_rev_matrix.loc["Target_Conversion",location] = (target * y - x)/(1 + target)
        
        conv_target = (target * y - x)/(1 + target)
        
        #Considering only Designation SWAP as the lever
        proj_SPAN_rev_matrix.loc["Revised_SPAN",location] = (x + conv_target)/(y - conv_target) 

    with c1:
        cm = sns.light_palette("green", as_cmap=True) 
        st.success("***Revised*** SPAN Based on Your Levers")
        st.dataframe(proj_SPAN_rev_matrix.style.background_gradient(cmap=cm))        
    
def view_FTE_multi_purpose(data):       
    #Project Specific
    st.success("Show Project specific **Associate, FTE & Pyramid** details")
    
    #Remove duplicate project-ids
    #project_list = data['Project_Id'].unique().tolist()
    project_list = data['Project_Name'].unique().tolist()
    
    #selection based on projects list
    proj_wish = st.radio("All Projects / Select MutiProjects?",("All","SelectedProject(s)"))
    if proj_wish == "All":
        project_id_list = project_list
    else:     
        project_id_list = st.multiselect("Pls select project(s)", project_list, key="fil1")
    
    #List of projects for which query is needed
    proj_filt1 = data['Project_Name'].isin(project_id_list)
    
    #New dataframe of PROJ selected using multiselect
    proj_data = data[proj_filt1]
    
    #Convert to FTE from Allocation %   
    proj_data = conv_alloc_FTE(proj_data)
                
    #Map Designations   
    proj_data = map_designations(proj_data)        
    
    #Display project specific DataFrame for the selected List of Projects
    st.dataframe(proj_data[['Associate_Id', 'Associate_Name', 'Designation', 'Project_Name', \
    'FTE', 'Offshore_Onsite', 'Department_Name', 'Start_Date', 'End_Date', 'Supervisor_Name']], height=200)
              
    #Calculate and Display FTE TOTAL counts               
    proj_data = display_FTE_count(proj_data)
    
    #DataFrame for Project FTE split
    proj_data, proj_FTE_matrix = display_FTE_designation_split(proj_data)
                                
    #enable download as hyperlink
    st.markdown(get_table_download_link(proj_FTE_matrix, proj_data, 'FTE1-Split', 'FTE1', 'FTE-view'), unsafe_allow_html=True)    
       
    #MultiSelect based on Location / Designation / Department / StartDate / EndDate / AssociateName / Supervisor
    #New dataframe : PROJ2 before filter same as PROJ
    proj2_data = proj_data
    if st.checkbox("Filter based on Location, Designation, Department, StartDate, EndDate, AssociateName, Supervisor"): 
        proj_data, proj2_data = filter_specific_criteria(proj_data, proj2_data)
        
        #Calculate and Display FTE TOTAL counts               
        proj2_data = display_FTE_count(proj2_data)
                        
        proj2_data, proj_FTE_matrix = display_FTE_designation_split(proj2_data)
                            
        #enable download as hyperlink
        st.markdown(get_table_download_link(proj_FTE_matrix, proj2_data, 'FTE2-Split', 'FTE2', 'FTE-Filter-view'), unsafe_allow_html=True) 

    #Plot line graphs
    if st.checkbox("Interested in SPAN?"): 
        st.info("Quick Summary table of **FTE counts & SPAN** details:")
        span_details(proj_data, proj_FTE_matrix)    
        
    #Plot line graphs for FTE count & FTE % at each Designation level
    if st.checkbox("Interested in FTE Trends? (at Project level)"): 
        st.info("Quick Summary table of **FTE counts & percentages**:")
        display_trends(proj_data, proj_FTE_matrix)         
    
#@st.cache(persist=True, allow_output_mutation=True, hash_funcs={Connection: id})
def clean_db_fn(conn):
    #delete all existing data
    delete_all_upload_report(conn)
    delete_data_db(conn)
    
    #Displat all as DataFrame
    emp_df = get_all_data(conn)
    return emp_df    
    
def main():

    html_temp = """
		<div style="background-color:{};padding:1px;border-radius:2px">
		<h2 style="color:{};text-align:center;">ProjectManager Dashboard </h2>
		</div>
		"""
    st.markdown(html_temp.format('royalblue','white'),unsafe_allow_html=True)
    
    menu = ["Project FTE View", "Compare 2 versions", "Pipeline Opp", "RevRec", "AdminUpload", "About"]
    choice = st.sidebar.selectbox("Select Option",menu)

    if choice == "Project FTE View":
        
        html_temp2 = """ <h3 style="color:{};text-align:center;">FTE View </h3> """
        st.markdown(html_temp2.format('royalblue','white'),unsafe_allow_html=True)
        
        #Check if we want to view from existing DB OR New File Upload
        option_data_view = st.sidebar.radio("ViewFromDB / UploadManually?",("DB","Upload"))
        if option_data_view == "DB":
            st.write("Initiating DB connection...")
            conn = get_connection(URI_SQLITE_DB)
            init_db(conn)
            st.write("DB connection established!")
            
            #Display all as DataFrame
            emp_df = get_all_data(conn)
            upload_Rep = get_all_upload_report(conn)          
            
            #Display only if DB data is available
            if len(emp_df) > 0:
                st.info(f"Display current database from the file ==> ***{upload_Rep['File_Name'][0]}***!")
                with st.beta_expander('Complete View',expanded=False):
                    st.dataframe(emp_df) 

                #Show FTE Pyramid, Trends, SPAN details.    
                view_FTE_multi_purpose(emp_df)    
            else:
                st.warning("No data from DB. Pls go for Upload Options...")
        
        elif option_data_view == "Upload":
            my_dataset = st.sidebar.file_uploader("Upload IMIS Allocation File in XLSX format", type=["xlsx"], key="upload1")
        
            if my_dataset is not None:
                #Open IMIS file
                data1 = file_excel_explore_data(my_dataset, key="FTEsh1")
                
                #Default Dataframe
                data = data1
                
                #Check if "FTE view of Merged 2 sheets (MBM & BTM)" & append to DATA
                data, filename2 = file_upload_2(data1)
                
                #All Projects, All Associates as-is dataframe
                st.info("Refer Original records of ALL Projects / Associates details")
        
                with st.beta_expander('Complete View (as-is IMIS report)',expanded=False):
                    st.dataframe(data)
                    
                #Replace Column Names
                data.columns = data.columns.str.replace(' ','_')
                # renaming the column 
                data.rename(columns = {"Offshore/Onsite": "Offshore_Onsite"}, inplace = True)                    
                
                #Show FTE Pyramid, Trends, SPAN details.    
                view_FTE_multi_purpose(data)
 
    elif choice == "Compare 2 versions":
        
        my_dataset1 = st.sidebar.file_uploader("Upload 1st IMIS Allocation File in CSV format", type=["csv"], key="ver1")
        if my_dataset1 is not None:

            #Open IMIS file1
            data1 = file_excel_explore_data(my_dataset1, key="Comparesh1")

        my_dataset2 = st.sidebar.file_uploader("Upload 2nd IMIS Allocation File in CSV format", type=["csv"], key="ver1")
        if my_dataset2 is not None:

            #Open IMIS file2
            data2 = file_excel_explore_data(my_dataset2, key="Comparesh2")        
        
            #Compare 2 versions
            st.subheader("Comparision of 2 versions")
                
            with st.beta_expander('Complete View (as-is IMIS report1)',expanded=False):
                st.dataframe(data1)
            
            with st.beta_expander('Complete View (as-is IMIS report2)',expanded=False):
                st.dataframe(data2)            
                
            #Project Specific
            st.subheader("Comparision Report -- PENDING DB ???")
            
            #Compare - PENDING ???
            #diff_df = dataframe_difference(data1, data2)
            #if st.button("Download as diff.csv to Current Folder"):
            #    diff_df.to_csv('diff.csv')    

    elif choice == "Pipeline Opp":
    
        html_temp2 = """ <h3 style="color:{};text-align:center;">PipeLine Opportunity View </h3> """
        st.markdown(html_temp2.format('royalblue','white'),unsafe_allow_html=True)
        
        pipeline_opp_handling()    

    elif choice == "AdminUpload":
        html_temp2 = """ <h3 style="color:{};text-align:center;">File Upload View </h3> """
        st.markdown(html_temp2.format('royalblue','white'),unsafe_allow_html=True)
        
        st.write("Initiating DB connection...")
        conn = get_connection(URI_SQLITE_DB)
        init_db(conn)
        init_db_upload_report(conn)
        st.write("DB connection established!")
        
        c1,c2 = st.beta_columns([2, 1])
        
        with c1:
            upload_Rep = get_all_upload_report(conn)
            st.info("History of Files Uploaded...")
            st.dataframe(upload_Rep)         
        with c2:
            #Displat all as DataFrame
            emp_df = get_all_data(conn)
            st.info("Display current database!")
            st.dataframe(emp_df, height=120)     

        #Clean DB and refresh
        st.success("**Clean/Purge Database**")
        if st.checkbox("Clean DB?"):
            emp_df = clean_db_fn(conn)
            st.write("Clean DB done!")
            st.dataframe(emp_df)
                
        imis_file = st.sidebar.file_uploader("Upload IMIS Allocation File in XLSX format", type=["xlsx"], key="AdmUp1")
        if imis_file is not None:

            #Open IMIS file
            imis_df1 = file_excel_explore_data(imis_file, key="IMIS-UP1")
            
            #Default Dataframe
            imis_df = imis_df1
                
            #Check if "FTE view of Merged 2 sheets (MBM & BTM)" & append to DATA
            #imis_file2 = imis_file
            imis_df, imis_file2 = file_upload_2(imis_df1)            
                      
            #Replace Column Names
            imis_df.columns = imis_df.columns.str.replace(' ','_')
            # renaming the column 
            imis_df.rename(columns = {"Offshore/Onsite": "Offshore_Onsite"}, inplace = True) 
            st.dataframe(imis_df)
                                    
            if st.checkbox("Save IMIS data to DB? (Clean DB is mandatory)"):            
                #delete all existing data
                delete_data_db(conn)
                st.write("Clean DB done!")
                
                #Displat all as DataFrame
                emp_df = get_all_data(conn)
                st.dataframe(emp_df)            
            
                # Store in DB
                # Check if 2nd file uploaded 
                if imis_file2 is None:
                    conc_filename = imis_file.name
                else:
                    conc_filename = imis_file.name + imis_file2.name
                st.write(conc_filename)
                save_to_db_upload_report(conn, conc_filename, "success")
                save_to_db(conn, imis_df)
            
                #Displat all as DataFrame
                emp_df = get_all_data(conn)
                st.success("Here is the revised DB!")
                st.dataframe(emp_df, height=180)
            
                  
if __name__ == '__main__':
    main()