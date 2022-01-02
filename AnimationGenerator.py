import tkinter as tk
import json
import os
from tkinter import ttk
from tkinter import filedialog as fd
from typing import Dict, Any

from PIL import ImageTk, Image, ImageDraw


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title('Animation Generator')
        self.master.resizable(False, False)
        self.master.geometry('800x600+200+10')

        self.game_name = tk.StringVar()

        self.BG_Frame = tk.Frame(self.master, bg='Black')
        self.BG_Frame.place(relwidth=1, relheight=1)

        self.Text_Frame = tk.Frame(self.master, bg='Grey')
        self.Text_Frame.place(x=250, y=50, height=500, width=500)

        self.instruction_text = tk.Text(self.Text_Frame, width=90, bg='Grey')
        self.instruction_text.insert(tk.INSERT,
                                     'Instructions for the animation Generator First start by saving an image of the playfield in PNG form and make sure the final resolution of the image is 1200 H by 600 W')
        self.instruction_text.pack()

        ## Left Side Buttons
        self.Game_Name_Label = tk.Label(self.master, text='Enter Game Name Below', fg='White', bg='Black')
        self.Game_Name_Label.pack()
        self.Game_Name_Label.place(x=20, y=25, height=15, width=200)

        self.Game_Name = tk.Entry(self.master, text='Enter Game Name Here', justify='center',
                                  textvariable=self.game_name)
        self.Game_Name.pack()
        self.Game_Name.place(x=20, y=50, height=25, width=200)

        self.Button_Layout = tk.Button(self.master, text='Create LED Layout', command=self.layout_window, bg='Grey')
        self.Button_Layout.pack()
        self.Button_Layout.place(x=20, y=100, height=40, width=200)

        self.Button_Create_Anim = tk.Button(self.master, text='Create Lightshow', command=self.lightshow_window,
                                            bg='Grey')
        self.Button_Create_Anim.pack()
        self.Button_Create_Anim.place(x=20, y=150, height=40, width=200)

        self.Button_Info = tk.Button(self.master, text='Software Version', command=self.test_variable, bg='Grey')
        self.Button_Info.pack()
        self.Button_Info.place(x=20, y=250, height=40, width=200)

        self.Create_Seq = tk.Button(self.master, text='Create Lightshow Sequence', command=self.test_variable, bg='Grey')
        self.Create_Seq.pack()
        self.Create_Seq.place(x=20, y=200, height=40, width=200)

        self.Button_Quit = tk.Button(self.master, text='Quit', command=self.close_windows, bg='Grey')
        self.Button_Quit.pack()
        self.Button_Quit.place(x=20, y=300, height=40, width=200)

    ##

    def layout_window(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        gamename_dir = dir_path + '\gamename.txt'
        gametext = self.game_name.get()
        print(gametext)

        text = open(gamename_dir, 'w')
        text.write(gametext)
        text.close()

        self.layout_window = tk.Toplevel(self.master)
        self.app = Layout_Window(self.layout_window)

    def lightshow_window(self):
        self.Animation_Creator = tk.Toplevel(self.master)
        self.app = animation_creator(self.Animation_Creator)

    def close_windows(self):
        self.master.destroy()

    def test_variable(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(dir_path)
        save_path = dir_path + '\Layout Files\layout.json'

        f = open(save_path)

        data = json.load(f)

        for i in data:
            print(i, data[i]['X Pos'], data[i]['Y Pos'])

        f.close()


class Layout_Window:
    LED_Positions: dict[Any, Any]

    def __init__(self, master):
        self.playfield = None
        self.img = None
        self.file = None
        self.overlay_Name = '0'
        self.x = 0
        self.y = 0
        self.LED_Count = 0
        self.LED_Positions = {}

        dir_path = os.path.dirname(os.path.realpath(__file__))
        gamename = open(dir_path + '/gamename.txt')
        self.name = gamename.read()

        self.master = master
        self.master.geometry('600x800+1100+100')
        self.master.title('Layout Generator for %s' % self.name)
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, height=800, width=600, bg='Grey')
        self.canvas.pack()

        self.imageframe = tk.Frame(self.master)
        self.imageframe.place(x=200, y=50, height=700, width=350)

        self.Button_Layout = tk.Button(self.master, text='Open Playfield', command=self.open_image, bg='Grey')
        self.Button_Layout.pack()
        self.Button_Layout.place(x=20, y=50, height=40, width=100)

        self.Button_Info = tk.Button(self.master, text='Clear Layout', command=self.clear_layout, bg='Grey')
        self.Button_Info.pack()
        self.Button_Info.place(x=20, y=100, height=40, width=100)

        self.Button_Quit = tk.Button(self.master, text='Save Layout', command=self.save_layout, bg='Grey')
        self.Button_Quit.pack()
        self.Button_Quit.place(x=20, y=150, height=40, width=100)

    def close_windows(self):
        self.master.destroy()

    def open_image(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        img_path = dir_path + '\Playfield Images'
        self.file = fd.askopenfilename(
            filetypes=(('PNG', '*.png'),),
            initialdir=img_path)
        splitfile = self.file.split('.')
        splitfile.insert(1, '_Overlay')
        self.overlay_Name = splitfile[0] + splitfile[1] + '.' + splitfile[2]
        str(self.overlay_Name)
        print(self.overlay_Name)

        playfield = Image.open(self.file)
        playfield_overlay = playfield
        playfield_overlay.save(self.overlay_Name)

        render = ImageTk.PhotoImage(playfield)
        self.img = tk.Label(self.imageframe, image=render)
        self.img.image = render
        self.img.place(x=0, y=0)

        self.img.bind('<Button-1>', self.add_LED)

    def add_LED(self, event):
        radius = 5
        color = 'White'

        LED_Number = 'LED_' + str(self.LED_Count)

        x, y = event.x, event.y

        DICT_NAME = LED_Number
        DICT_NAME = {
            "Number": self.LED_Count,
            "X Pos": x,
            "Y Pos": y
        }
        print(DICT_NAME)

        self.LED_Positions.update({LED_Number: DICT_NAME})
        self.LED_Count = self.LED_Count + 1

        image = Image.open(self.overlay_Name)
        draw = ImageDraw.Draw(image)

        minx = x - radius
        miny = y - radius
        maxx = x + radius
        maxy = y + radius
        draw.ellipse((minx, miny, maxx, maxy), outline='red', width=1, fill=color)

        if self.x == 0 and self.y == 0:
            self.x = x
            self.y = y
        else:
            points = [(x, y), (self.x, self.y)]
            draw.line(points, width=2, fill='Green')
            self.x = x
            self.y = y

        image.save(self.overlay_Name)

        playfield = Image.open(self.overlay_Name)

        render = ImageTk.PhotoImage(playfield)
        self.img = tk.Label(self.imageframe, image=render)
        self.img.image = render
        self.img.place(x=0, y=0)

        self.img.bind('<Button-1>', self.add_LED)

    def clear_layout(self):
        playfield = Image.open(self.file)
        playfield_overlay = playfield
        playfield_overlay.save(self.overlay_Name)

        render = ImageTk.PhotoImage(playfield)
        self.img = tk.Label(self.imageframe, image=render)
        self.img.image = render
        self.img.place(x=0, y=0)

        self.img.bind('<Button-1>', self.add_LED)

        self.x = 0
        self.y = 0
        LED_Positions = {}
        self.LED_Count = 0

    def save_layout(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(dir_path)
        save_path = dir_path + '\Layout Files' + '\\' + self.name + '_layout.json'

        jsonString = json.dumps(self.LED_Positions)
        jsonFile = open(save_path, "w")
        jsonFile.write(jsonString)
        jsonFile.close()
        self.close_windows()


class animation_creator:
    def __init__(self, master):
        self.master = master
        self.master.geometry('400x200+1100+100')
        self.master.title('Animation Generator')
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, height=200, width=400, bg='Grey')
        self.canvas.pack()

        self.Button_Layout = tk.Button(self.master, text='Select Layout', command=self.open_layout, bg='Grey')
        self.Button_Layout.pack()
        self.Button_Layout.place(x=20, y=30, height=40, width=150)

        self.LayoutText = tk.StringVar()
        self.LayoutText.set('Select Layout JSON File')
        self.Layout_Label = tk.Label(self.master, textvariable=self.LayoutText, fg='Black', bg='Grey')
        self.Layout_Label.pack()
        self.Layout_Label.place(x=180, y=30, height=50, width=180)

        self.Animation_Button = tk.Button(self.master, text='Select Animation', command=self.open_animation, bg='Grey')
        self.Animation_Button.pack()
        self.Animation_Button.place(x=20, y=80, height=40, width=150)

        self.Animation_Text = tk.StringVar()
        self.Animation_Text.set('Select Animation Directory')
        self.Animation_Label = tk.Label(self.master, textvariable=self.Animation_Text, fg='Black', bg='Grey')
        self.Animation_Label.pack()
        self.Animation_Label.place(x=180, y=80, height=50, width=180)

        self.Create_Animation = tk.Button(self.master, text='Create Animation', command=self.create_animation,
                                          bg='Grey')
        self.Create_Animation.pack()
        self.Create_Animation.place(x=20, y=130, height=40, width=250)

    def open_layout(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        layout_path = dir_path + '\Layout Files'
        trunkate = len(layout_path) + 1
        self.file = fd.askopenfilename(
            filetypes=(('json', '*.json'),),
            initialdir=layout_path)
        layoutname = self.file[trunkate:]
        print(layoutname)

        self.LayoutText.set(layoutname)

        layout = open(self.file)

        self.layout_data = json.load(layout)

        # for i in self.layout_data:
        #     print(i, self.layout_data[i]['X Pos'], self.layout_data[i]['Y Pos'])

        layout.close()

    def open_animation(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        ani_path = dir_path + '\Animation Files'
        self.animation_path = fd.askdirectory(
            initialdir=ani_path
        )
        trunkate = len(ani_path) + 1
        self.animation_name = self.animation_path[trunkate:]
        print(self.animation_name)

        self.Animation_Text.set(self.animation_name)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        array_path = dir_path + '\Animation Arrays' + '\\' + self.animation_name
        os.mkdir(array_path)

    def create_animation(self):
        index = 0
        LED_POS_X = []
        LED_POS_Y = []
        images = os.listdir(self.animation_path)
        frame_dict = {}

        # print(self.layout_data)

        for i in self.layout_data:
            # print(i, self.layout_data[i]['X Pos'], self.layout_data[i]['Y Pos'])
            LED_POS_X.append(self.layout_data[i]['X Pos'])
            # print(self.layout_data[i]['X Pos'])
            LED_POS_Y.append(self.layout_data[i]['Y Pos'])
            # print(self.layout_data[i]['Y Pos'])
            # print(LED_POS_X[index], LED_POS_Y[index])
            index = index + 1

        index = 0
        for j in images:
            framelist = []
            led_index = 0
            frame_dir = self.animation_path + '\\' + j
            frame = Image.open(frame_dir)

            for k in self.layout_data:
                led_state = 0
                led_value = 0
                coordinate = LED_POS_X[led_index], LED_POS_Y[led_index]

                led_value_tuple = frame.getpixel(coordinate)
                led_value_list = list(led_value_tuple)
                if led_value_list[0] > 125:
                    led_state = 1
                else:
                    led_state = 0
                # print('%s is %d' %(k, led_state))

                framelist.append(led_state)

                led_index = led_index + 1

            # print(framelist)
            DICT_NAME = j
            DICT_NAME = {
                'LED State': framelist
            }

            frame_dict.update({self.animation_name + str(index): DICT_NAME})
            index = index + 1
        print(frame_dict)
        print('Writing to Text File')

        dir_path = os.path.dirname(os.path.realpath(__file__))
        array_path = dir_path + '\Animation Arrays' + '\\' + self.animation_name

        animation_array = open(array_path + '\\' + self.animation_name + '.txt', 'w')

        line = []
        frame_list = []
        frame_heading = 'char *' + self.animation_name + '[] = { '
        animation_array.write(frame_heading)

        for x in frame_dict:
            frame_list.append('"')
            frame_list.append(x + '", ')
        last_item = frame_list[-1]
        frame_list.remove(last_item)
        frame_list.append(x +'"};')
        animation_array.writelines(frame_list)
        animation_array.write("\n\n\n\n")

        frame_list = []


        for x, y in frame_dict.items():
            line_heading = 'const long ' + x + "[] PROGMEM =\n"
            animation_array.write(line_heading)
            line.append('{')
            for y in frame_dict[x]['LED State']:
                if y == 1:
                    line.append('0xFFFFFF' + ', ')
                else:
                    line.append('0x000000' + ', ')
            last_elemement = line[-1]
            line.remove(last_elemement)
            if last_elemement == 1:
                line.append('0xFFFFFF};')
            else:
                line.append('0x000000};')

            animation_array.writelines(line)
            line = []
            animation_array.write("\n")

        animation_array.close()


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
