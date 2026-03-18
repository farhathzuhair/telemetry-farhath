import tkinter as tk
from tkinter import ttk
import serial
import firebase_admin
from firebase_admin import credentials, db
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ================= FIREBASE =================

cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred,{
    'databaseURL':'https://loramonitoring-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

firebase_ref = db.reference("sensor_data")

# ================= SERIAL =================

ser = serial.Serial(
    port="COM8",
    baudrate=115200,
    timeout=1
)

# ================= DATA =================

temp_data=[]
hum_data=[]
soil_data=[]
light_data=[]

MAX_DATA=20

# ================= ROOT =================

root=tk.Tk()
root.title("Telemetry Control Panel")
root.geometry("1300x850")
root.configure(bg="#0f172a")

# ================= SIDEBAR =================

sidebar=tk.Frame(root,width=200,bg="#020617")
sidebar.pack(side="left",fill="y")

title=tk.Label(
    sidebar,
    text="TELEMETRY",
    font=("Segoe UI",18,"bold"),
    fg="#38bdf8",
    bg="#020617"
)
title.pack(pady=20)

menu_items=["Dashboard","Sensors","Nodes","Logs"]

for m in menu_items:

    btn=tk.Label(
        sidebar,
        text=m,
        font=("Segoe UI",11),
        fg="white",
        bg="#020617",
        pady=10
    )

    btn.pack(fill="x")

# ================= MAIN AREA =================

main=tk.Frame(root,bg="#0f172a")
main.pack(side="right",expand=True,fill="both")

# ================= TOP STATUS =================

status_frame=tk.Frame(main,bg="#0f172a")
status_frame.pack(fill="x",pady=10)

node_label=tk.Label(
    status_frame,
    text="NODE: -",
    font=("Segoe UI",16),
    fg="white",
    bg="#0f172a"
)

node_label.pack(side="left",padx=20)

system_status=tk.Label(
    status_frame,
    text="ONLINE",
    font=("Segoe UI",14,"bold"),
    fg="#22c55e",
    bg="#0f172a"
)

system_status.pack(side="right",padx=20)

# ================= SENSOR GAUGES =================

sensor_frame=tk.Frame(main,bg="#0f172a")
sensor_frame.pack(pady=10)

def create_sensor(name,color,col):

    frame=tk.Frame(
        sensor_frame,
        bg="#1e293b",
        width=200,
        height=120
    )

    frame.grid(row=0,column=col,padx=20)
    frame.pack_propagate(False)

    label=tk.Label(
        frame,
        text=name,
        font=("Segoe UI",10),
        fg="#94a3b8",
        bg="#1e293b"
    )

    label.pack(pady=5)

    progress=ttk.Progressbar(
        frame,
        orient="horizontal",
        length=160,
        mode="determinate"
    )

    progress.pack(pady=10)

    value=tk.Label(
        frame,
        text="0",
        font=("Segoe UI",18,"bold"),
        fg=color,
        bg="#1e293b"
    )

    value.pack()

    return progress,value

temp_bar,temp_value=create_sensor("Temperature","#f87171",0)
hum_bar,hum_value=create_sensor("Humidity","#22c55e",1)
soil_bar,soil_value=create_sensor("Soil","#facc15",2)
light_bar,light_value=create_sensor("Light","#38bdf8",3)

# ================= GRAPH =================

graph_frame=tk.Frame(main,bg="#0f172a")
graph_frame.pack(pady=20)

fig,ax=plt.subplots(figsize=(7,4))
fig.patch.set_facecolor("#0f172a")
ax.set_facecolor("#1e293b")

canvas=FigureCanvasTkAgg(fig,master=graph_frame)
canvas.get_tk_widget().pack()

# ================= TELEMETRY LOG =================

log_frame=tk.Frame(main,bg="#0f172a")
log_frame.pack(fill="both",expand=True,pady=10)

columns=("time","node","temp","hum","soil","light")

table=ttk.Treeview(
    log_frame,
    columns=columns,
    show="headings"
)

for c in columns:
    table.heading(c,text=c.upper())

table.pack(fill="both",expand=True)

# ================= GRAPH UPDATE =================

def update_graph():

    ax.clear()

    ax.plot(temp_data,color="red",label="Temp")
    ax.plot(hum_data,color="green",label="Hum")
    ax.plot(soil_data,color="yellow",label="Soil")
    ax.plot(light_data,color="cyan",label="Light")

    ax.legend()
    canvas.draw()

# ================= SERIAL READ =================

def read_serial():

    if ser.in_waiting:

        data=ser.readline().decode().strip()

        print(data)

        if "ID:" in data:

            try:

                parts=data.split(",")

                node=parts[0].split(":")[1]
                temp=float(parts[1].split(":")[1])
                hum=float(parts[2].split(":")[1])
                soil=int(parts[3].split(":")[1])
                light=int(parts[4].split(":")[1])

                node_label.config(text="NODE: "+node)

                temp_value.config(text=str(temp))
                hum_value.config(text=str(hum))
                soil_value.config(text=str(soil))
                light_value.config(text=str(light))

                temp_bar["value"]=temp
                hum_bar["value"]=hum
                soil_bar["value"]=soil
                light_bar["value"]=light

                temp_data.append(temp)
                hum_data.append(hum)
                soil_data.append(soil)
                light_data.append(light)

                if len(temp_data)>MAX_DATA:
                    temp_data.pop(0)
                    hum_data.pop(0)
                    soil_data.pop(0)
                    light_data.pop(0)

                update_graph()

                table.insert("",0,values=(
                    "LIVE",
                    node,
                    temp,
                    hum,
                    soil,
                    light
                ))

                firebase_ref.push({
                    "node":node,
                    "temperature":temp,
                    "humidity":hum,
                    "soil":soil,
                    "light":light
                })

            except Exception as e:
                print("Parsing error:",e)

    root.after(1000,read_serial)

# ================= START =================

read_serial()

root.mainloop()