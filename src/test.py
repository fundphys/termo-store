from tkinter import * 
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import math 
def jobModbusTCP():
    getDI=master.execute(1,cst.READ_INPUT_REGISTERS, 0, 7)

    if int(getDI[0]) % 2: 
        canv.itemconfig(diFig1,fill='red') 
    if not int(getDI[0]) % 2: 
        canv.itemconfig(diFig1,fill='green') 
    if int(getDI[1]) % 2: 
        canv.itemconfig(diFig2,fill='red') 
    if not int(getDI[1]) % 2 : 
        canv.itemconfig(diFig2,fill='green') 
    root.after(1000, jobModbusTCP)


master = modbus_tcp.TcpMaster(host='192.168.15.72', port=502)
master.set_timeout(1.0)

root = Tk() 
#im = PhotoImage(file='bg.gif') 
canv = Canvas(root,width=1900,height=950,bg="black",bd=0, highlightthickness=0, relief='ridge')
canv.place(x=0, y=25) 
#canv.create_image(1, 1,anchor=NW, image=im) 
diFig1=canv.create_rectangle(10,10,30,30,fill='gray', outline='black')
diFig2=canv.create_oval(50,50,80,80,fill='gray', outline='black')
root.after(1, jobModbusTCP)
root.mainloop()