from tkinter import *
from tkinter.tix import *
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import pygame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from miditime.miditime import MIDITime    #miditime library
import matplotlib.pyplot as plt
import soundfile as sf
from PIL import ImageTk, Image 
from music21 import converter,instrument 

# create window
window = Tk()

#window title
window.title("Sonify box")

#window size
window.geometry("900x700")

#window icon
#window.iconbitmap('F:/CP_project/CP_project/gui_imp_2/images/new_wave.jpg')


# add theme sun and valley theme 
style = ttk.Style(window)
window.call("source", "Sun-Valley-ttk-theme-master/sun-valley.tcl")
window.call("set_theme", "light")

frame_front = Frame(window)
frame_front.place( width = 900, height = 700)

img_pho=Image.open("F:\CP_project\CP_project\gui_imp_2\images\SOnifybox.png")
img = ImageTk.PhotoImage(img_pho)

label_front = Label(frame_front, image = img)
label_front.pack()

#create menubar
menu_bar = Menu(window)
window.config(menu = menu_bar)


# open a text or csv file
def open_file():
    clear_optionlist()
    fr4.tkraise()
    fr4.place(height=700, width=900)

    return None
    

# open sonification window
def sonify_open():

    save()

    window2.tkraise()
    window2.place(height=700,width=900)

    sonifi_window()

    return None
    


# create menu item 
file_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Dataset setup", menu=file_menu)

file_menu.add_command(label ="Open", command=open_file)
file_menu.add_separator()
file_menu.add_command(label ="Exit", command=window.quit)

sonic_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Sonification", menu=sonic_menu)
sonic_menu.add_command(label ="Sonify", command=sonify_open)


# frame for open ...........................
fr4= ttk.Frame(window, style='Card.TFrame')

# Frame for TreeView
fr1 = ttk.LabelFrame(fr4, text="Data",relief="ridge")
fr1.place(height=400, width=900)

# Frame for open file dialog
fr2 = ttk.LabelFrame(fr4, text="Settings",relief="ridge")
fr2.place(height=225, width=800,relx=0.045, rely=0.6 )

# Frame for select variables
#fr2= ttk.LabelFrame(fr4, text="Select time variable",relief="ridge")
#fr2.place(height=100, width=350,relx=0.575, rely=0.7)

# Buttons
b1_fr2 = ttk.Button(fr2, text="Select Data file", command=lambda: File_dialog(),style="Accent.TButton")
b2_fr2 = ttk.Button(fr2, text="Load file to application", command=lambda: Load_excel_data(), style="Accent.TButton")

b1_fr2.place(rely=0.80, relx=0.16)
b2_fr2.place(rely=0.80, relx=0.5)

# The file/file path text
label_file0 = ttk.Label(fr2, text="File :")
label_file0.place(rely=0.01, relx=0.025)

label_file = ttk.Label(fr2, text="No File Selected")
label_file.place(rely=0.01, relx=0.2)

label_file1 = ttk.Label(fr2, text="Start :")
label_file1.place(rely=0.2, relx=0.2)

label_file2 = ttk.Label(fr2, text="End :")
label_file2.place(rely=0.2, relx=0.4)

label_file3 = ttk.Label(fr2, text="Resampling :")
label_file3.place(rely=0.48, relx=0.025)

label_file4 = ttk.Label(fr2, text="Select time variable* :")
label_file4.place(rely=0.175, relx=0.7)

label_file5 = ttk.Label(fr2, text="Dateoffsets :")
label_file5.place(rely=0.43, relx=0.2)

label_file6 = ttk.Label(fr2, text="function :")
label_file6.place(rely=0.43, relx=0.55)

label_file7 = ttk.Label(fr2, text="Data range :")
label_file7.place(rely=0.25, relx=0.025)

label_file4 = ttk.Label(fr2, text="* - This section must be selected\n    before you sonify your data.")
label_file4.place(rely=0.8, relx=0.75)

u1 = StringVar(fr2,value = '0') 
e1 = Entry(fr2, textvariable=u1)
e1.place(rely=0.3, relx=0.2)

u2 = StringVar(fr2,value = '0') 
e2 = Entry(fr2, textvariable=u2)
e2.place(rely=0.3, relx=0.4)

# Treeview Widget
tv1 = ttk.Treeview(fr1)
tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

treescrolly = Scrollbar(fr1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
treescrollx = Scrollbar(fr1, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

# Select time variable
n1_fr3 = StringVar()
global cmb1_fr3
cmb1_fr3 = ttk.Combobox(fr2, width = 27, textvariable = n1_fr3)
cmb1_fr3.place(rely=0.3, relx=0.68)

# Select dateoffset
n2_fr3 = StringVar()
cmb2_fr3 = ttk.Combobox(fr2, width = 27, textvariable = n2_fr3)
cmb2_fr3.place(rely=0.55, relx=0.2)
cmb2_fr3.set('None')

# Add values for dateoffset
# 'W'- one week, 'M'- calandar month end, 'Q'-calandar Quarter end
# 'A'- year end, 'D'- one absolute day, 'H'- one hour, 'min'- one minute
# 'S'- one second, 'ms'- one millsecond, 'us'- one microsecond, 'N'-one nanosecond
cmb2_fr3['values'] = ['None','W','M','Q','A','D','H','min','S','ms','us','N']

# Select function
n3_fr3 = StringVar()
cmb3_fr3 = ttk.Combobox(fr2, width = 27, textvariable = n3_fr3)
cmb3_fr3.place(rely=0.55, relx=0.55)
cmb3_fr3.set('None')
# Add values for function 
cmb3_fr3['values'] = ['None','mean','sum','std','max','min','median']
# upsampling - https://towardsdatascience.com/upsample-with-an-average-in-pandas-c029032c57ca this part was deleted 

def File_dialog():
    """This Function will open the file explorer and assign the chosen file path to label_file"""
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("CSV Files","*.csv"),("All Files", "*.*")))
    
    label_file["text"] = filename

    return None


def Load_excel_data():
    """If the file selected is valid this will load the file into the Treeview"""
    clear_data()
    file_path = label_file["text"]

    try:
        excel_filename = r"{}".format(file_path)
        global df1

        result = messagebox.askquestion("Dataset", "Do your file have headers?", icon='warning')
        
        if result == 'yes':
        
            if (excel_filename[-4:] == ".csv"):
                df1 = pd.read_csv(excel_filename)
            elif(excel_filename[-4:] == ".txt"):
                df1 = pd.read_csv(excel_filename, sep='\t')
            else:
                df1 = pd.read_excel(excel_filename)
        else:
            if (excel_filename[-4:] == ".csv"):
                df1 = pd.read_csv(excel_filename,header=None)
            elif(excel_filename[-4:] == ".txt"):
                df1 = pd.read_csv(excel_filename, sep='\t',header=None)
            else:
                df1 = pd.read_excel(excel_filename,header=None)

    except ValueError:
        messagebox.showerror("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        messagebox.showerror("Information", f"No such file as {file_path}")
        return None
        
   # df_row, df_col = df1.shape
    #arr_row=[]

    #for i in range(10):
    #    aa=0
    #    for j in range(df_col):

    #        val_new = df1.iat[i,j]

    #        if (isinstance(val_new,str)==True): 
                #print(val_new)
    #            ai = 0 
    #            for cha in val_new:
                    
    #                if (cha.isalpha() == True):
                        #print(cha)
    #                    ai+=1
                #print(ai)
    #            if ai == 0:
    #                aa+=1
                
    #        else:

    #            aa=999  # for other variables
    #    if aa!=df_col and aa!=999: 
    #        arr_row.append(i)
    #    print(arr_row)

    #for ii in range(len(arr_row)):
    #    df1.drop(arr_row[ii], axis=0, inplace=True)  # remove additional lines 

    start =int( e1.get())
    end = int(e2.get())

    if (start !=0) or (end != 0):
        df1 = df1[start:end]   
    else:
        pass

    if (cmb2_fr3.get() != 'None') and (cmb3_fr3.get() != 'None') :
        df1[cmb1_fr3.get()] = pd.to_datetime(df1[cmb1_fr3.get()])
        df1=df1.set_index(cmb1_fr3.get())
        if cmb3_fr3.get()=='mean':
            df1 = df1.resample(cmb2_fr3.get()).mean().reset_index()
        if cmb3_fr3.get()=='std':
            df1 = df1.resample(cmb2_fr3.get()).std().reset_index()
        if cmb3_fr3.get()=='max':
            df1 = df1.resample(cmb2_fr3.get()).max().reset_index()
        if cmb3_fr3.get()=='min':
            df1 = df1.resample(cmb2_fr3.get()).min().reset_index()
        if cmb3_fr3.get()=='sum':
            df1 = df1.resample(cmb2_fr3.get()).sum().reset_index()
        if cmb3_fr3.get()=='median':
            df1 = df1.resample(cmb2_fr3.get()).median().reset_index()

    else:
        pass

    tv1["column"] = list(df1.columns)
    combo_box()
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = df1.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    
    messagebox.showinfo("Information", "Please select 'Time variable' before sonifying data.")

    return None

def save():

    global cmb1_val
    global options_list_soni

    cmb1_val = cmb1_fr3.get()

    n = tv1["column"] 
    
    options_list_soni= []
    for i in n:
        if i!=cmb1_val:
            options_list_soni.append(i)

    return options_list_soni

def clear_optionlist():

    options_list_soni= []

    return options_list_soni
    
def clear_data():

    tv1.delete(*tv1.get_children())

    return None

# add column names to combo box
def combo_box():

    n = tv1["column"] 
    cmb1_fr3['values'] = n
    
    return n

window2 = ttk.Frame(window, style='Card.TFrame')

window3 = ttk.LabelFrame(window2, text='Method',height=380,width=900,relief="ridge")
window3.grid(row=0, column=0,sticky="Ew")

window1 = ttk.LabelFrame(window2,height=320,width=900,relief="ridge")
window1.grid(row=1, column=0,sticky="Ew")

def sonifi_window():
    
    # for method
    v_soni = IntVar()

    rdb1_soni =ttk.Radiobutton(window3,text="Parameter mapping :",variable=v_soni, value=1)
    rdb2_soni =ttk.Radiobutton(window3,text="Audification :",variable=v_soni, value=2)
    rdb1_soni.place(x=30, y=10)
    rdb2_soni.place(x=30, y=290)

    v1_soni = IntVar()

    rdb3_soni =ttk.Radiobutton(window3,text="Pitch",variable=v1_soni, value=1)
    rdb4_soni =ttk.Radiobutton(window3,text="Amplitude",variable=v1_soni, value=2)

    rdb3_soni.place(x=100, y=40)
    rdb4_soni.place(x=500, y=40)

    #global options_list_soni
    var1_soni =StringVar(window3) 
    var2_soni = StringVar(window3) 
    option_menu1_soni = ttk.OptionMenu(window3, var1_soni, *options_list_soni)
    option_menu2_soni = ttk.OptionMenu(window3, var2_soni, *options_list_soni)

    option_menu1_soni.place(x=170,y=40)
    option_menu2_soni.place(x=600,y=40)


    #for wav
    var9_soni = StringVar(window3) 
    option_menu9_soni = ttk.OptionMenu(window3, var9_soni, *options_list_soni)
    option_menu9_soni.place(x=40, y=317)


    L7_soni = ttk.Label(window3, text="Pitch :")
    L8_soni = ttk.Label(window3, text="Amplitude :")
    L9_soni = ttk.Label(window3, text="Time(s) :")
    L10_soni = ttk.Label(window3, text="Tempo :")
    L11_soni = ttk.Label(window3, text="For Pitch range (Start) :")
    L12_soni = ttk.Label(window3, text="Number of ranges :")
    L13_soni = ttk.Label(window3, text="Note Duration(s) :")

    L7_soni.place(x=100, y=100)
    L8_soni.place(x=100, y=165)
    L10_soni.place(x=100, y=230)
    L9_soni.place(x=700, y=295)
    L11_soni.place(x=500, y=100)
    L12_soni.place(x=500, y=165)
    L13_soni.place(x=500, y=230)

    w1_soni = Scale(window3, from_=0, to=127, orient=HORIZONTAL,length=250, tickinterval=25, resolution=1)
    w2_soni = Scale(window3, from_=0, to=127, orient=HORIZONTAL,length=250, tickinterval=25, resolution=1)
    w3_soni = Scale(window3, from_=0, to=127, orient=HORIZONTAL,length=250, tickinterval=25, resolution=1)
    w4_soni = Scale(window3, from_=0, to=8, orient=HORIZONTAL,length=130, tickinterval=2, resolution=1)
    w5_soni = Scale(window3, from_=0, to=8, orient=HORIZONTAL,length=130, tickinterval=2, resolution=1)
    w6_soni = Scale(window3, from_=0, to=30, orient=HORIZONTAL,length=130, tickinterval=10, resolution=0.5)

    w1_soni.set(60)
    w2_soni.set(60)
    w3_soni.set(120)
    w4_soni.set(0)
    w5_soni.set(4)
    w6_soni.set(0.5)

    w1_soni.place(x=170, y=100)
    w2_soni.place(x=170, y=165)
    w3_soni.place(x=170, y=230)
    w4_soni.place(x=640, y=100)
    w5_soni.place(x=640, y=165)
    w6_soni.place(x=640, y=230)

    u1_soni = StringVar(window3,value = '10000') 
    e1_soni = Entry(window3,textvariable=u1_soni)
    e1_soni.place(x=700, y=322)

    # for wav file 
    L13_soni = ttk.Label(window3, text="Sample rate :")
    L13_soni.place(x=220, y=295)
    u2_soni = StringVar(window3,value = '1000') 
    e2_soni = Entry(window3,textvariable=u2_soni)
    e2_soni.place(x=220, y=322)

    # for saving file 
    L13_soni = ttk.Label(window3, text="Save as :")
    L13_soni.place(x=400, y=295)

    u3_soni = StringVar(window3,value = 'pitch.mid')
    e3_soni = Entry(window3,textvariable=u3_soni)
    e3_soni.place(x=400, y=322)


    def sonify():

        global df
        df = pd.DataFrame()
        pitch = w1_soni.get()
        amplitude = w2_soni.get()
        tempo = w3_soni.get()
        pitch_range = w4_soni.get()
        number_of_ranges = w5_soni.get()  
        time = int(e1_soni.get())
        sample_rate = int(e2_soni.get())
        save = e3_soni.get()
        note_duration = w6_soni.get()
        plt.close()
        if (v_soni.get() == 1):
            if (v1_soni.get() == 1):
                print(cmb1_val)
                df['Time'] = df1.loc[:,cmb1_fr3.get()]
                global col_1
                col_1 =var1_soni.get()
                #print(df.iat[0,0])
                #print(type(df.iat[0,0]))
                if (cmb2_fr3.get() != 'None') and (cmb3_fr3.get() != 'None') :
                    df['Time'] = pd.to_datetime(df['Time'])
                else:
                    if (check_float(df.iat[0,0])==True):
                        df['Time'] = pd.to_numeric(df['Time'])
                    else:
                        df['Time'] = pd.to_datetime(df['Time'])
                    
                df['Pitch'] = df1.loc[:,col_1] 
                df['Pitch'] = pd.to_numeric(df['Pitch'])

                dis_plot(df)

                data_min=min(df['Pitch'])
                data_max=max(df['Pitch'])
                
                data_df = df.to_dict(orient="index")

                my_data = []
                for i in data_df.values():           
                    my_data.append(i)
            
                mymidi = MIDITime(tempo, save, time, pitch_range, number_of_ranges)
                if (type(df['Time'].iloc[0])==pd._libs.tslibs.timestamps.Timestamp):

                    my_data_epoched = [{'days_since_epoch': mymidi.days_since_epoch(d['Time']), 'Pitch': d['Pitch']} for d in my_data]
                    my_data_timed = [{'beat': mymidi.beat(d['days_since_epoch']), 'Pitch': d['Pitch']} for d in my_data_epoched]
                
                else:
                    my_data_timed = [{'beat': mymidi.beat(d['Time']), 'Pitch': d['Pitch']} for d in my_data]


                start_time = my_data_timed[0]['beat']
                
                note_list = []

                for d in my_data_timed:
                    note_list.append([
                        d['beat'] - start_time,
                        mag_to_pitch_tuned(d['Pitch'],data_min,data_max,mymidi),
                        amplitude,  
                        note_duration  
                    ])
                
                mymidi.add_track(note_list)
                mymidi.save_midi()

            if (v1_soni.get() ==2):

                df['Time'] = df1.loc[:,cmb1_val]
                global col_2
                col_2 =var2_soni.get()

                if (cmb2_fr3.get() != 'None') and (cmb3_fr3.get() != 'None') :
                    df['Time'] = pd.to_datetime(df['Time'])
                else:
                    if (check_float(df.iat[0,0])==True):
                        df['Time'] = pd.to_numeric(df['Time'])
                    else:
                        df['Time'] = pd.to_datetime(df['Time'])

                df['Velocity'] = df1.loc[:,col_2]
                df['Velocity'] = pd.to_numeric(df['Velocity'])

                dis_plot(df)

                data_min_velo=min(df['Velocity'])
                data_max_velo=max(df['Velocity'])

                data_df = df.to_dict(orient="index")

                my_data = []
                for i in data_df.values():
                    my_data.append(i)

                mymidi = MIDITime(tempo, save, time)

                if (type(df['Time'].iloc[0])==pd._libs.tslibs.timestamps.Timestamp):
                    my_data_epoched = [{'days_since_epoch': mymidi.days_since_epoch(d['Time']), 'Velocity': d['Velocity']} for d in my_data]
                    my_data_timed = [{'beat': mymidi.beat(d['days_since_epoch']), 'Velocity': d['Velocity']} for d in my_data_epoched]
                    
                else:
                    my_data_timed = [{'beat': mymidi.beat(d['Time']), 'Velocity': d['Velocity']} for d in my_data]

                start_time = my_data_timed[0]['beat']
                
                note_list = []

                for d in my_data_timed:
                    note_list.append([d['beat'] - start_time,
                                    pitch,
                                    scale_pct_velo(d['Velocity'],data_min_velo,data_max_velo),  # velocity 
                                    note_duration  # duration, in beats
            
                    ])
                mymidi.add_track(note_list)
                mymidi.save_midi()

        elif (v_soni.get()==2):
            df['col'] = df1.loc[:,var9_soni.get()]
            data_array = pd.to_numeric(df['col']).to_numpy()
            sf.write(save, data_array, sample_rate)
            dis_plot(df)
        
        else:
            messagebox.showerror("Information", "Please select one method to continue.")

    def check_float(potential_float):
    
        try:
            float(potential_float)
            return True
        except ValueError:
            return False

    def mag_to_pitch_tuned(Para,data_min,data_max,mymidi):

        scale_pct = mymidi.linear_scale_pct(data_min, data_max, Para)

        c_major = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

        note = mymidi.scale_to_note(scale_pct, c_major)

        midi_pitch = mymidi.note_to_midi_pitch(note)

        return midi_pitch

    def scale_pct_velo(para,data_min,data_max):
        D21= int((127-10)*((para-data_min)/(data_max-data_min))+10) 
        return D21

    # Buttons

    b1_soni = ttk.Button(window3, text="Sonify",command = lambda: sonify(),style="Accent.TButton")
    b1_soni.place(x=550, y=316)

    b5_soni = ttk.Button(window1, text = "Play",command = lambda:Listen(),style="Accent.TButton")
    b5_soni.place(x=806,y=10)

    b6_soni = ttk.Button(window1, text = "Pause",command =lambda: pause(),style="Accent.TButton")
    b6_soni.place(x=800,y=70)

    b7_soni = ttk.Button(window1, text = "Unpause",command = lambda:unpause(),style="Accent.TButton")
    b7_soni.place(x=790,y=130)

    b8_soni = ttk.Button(window1, text = "Stop",command = lambda:stop(),style="Accent.TButton")
    b8_soni.place(x=804,y=190)


    def Listen():
        sound_file = e3_soni.get()

        pygame.init()
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    def pause():
        pygame.init()
        pygame.mixer.music.pause()
    
    def unpause():
        pygame.init()
        pygame.mixer.music.unpause()
        
    def stop():
        pygame.init()
        pygame.mixer.music.stop()


    # show plot
    def dis_plot(df):
    
        # the figure that will contain the plot
        fig = Figure(figsize = (15, 5),
                    dpi = 50)
    
        # adding the subplot
        plot1 = fig.add_subplot(111)
        if len(df.columns)!= 1:
            plot1.plot(df.iloc[:, 1])
        else:
            plot1.plot(pd.to_numeric(df['col']))
    
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,
                                master = window1)  
        canvas.draw()
    
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().place(x=0,y=0)
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                    window)
        toolbar.update()

#show window
window.mainloop()