import glob
import shutil
import tarfile
import numpy as np
import pandas as pd
import re
import sys
import wx
import requests
import os
import urllib.request


class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        # ファイルパスをテキストフィールドに表示
        for file in filenames:
            print(file)
        self.window.file_paths = filenames
        dialog = wx.MessageDialog(self.window, 'ファイル読み込み完了', 'ファイルを読み込みました')
        dialog.ShowModal()
        dialog.Destroy()
        return True


class MyFrame(wx.Frame):
    def __init__(self):
        self.file_paths = []
        self.is_calculate_now = False
        wx.Frame.__init__(self, None, title="knet converter", size=(500, 200))
        p = wx.Panel(self)
        label = wx.StaticText(p, wx.ID_ANY, 'ここにファイルをドロップしてください', style=wx.SIMPLE_BORDER | wx.TE_CENTER)
        label.SetBackgroundColour("#e0ffff")
        # ドロップ対象の設定
        label.SetDropTarget(MyFileDropTarget(self))
        button = wx.Button(p, wx.ID_ANY, u'変換を実行')
        self.Bind(wx.EVT_BUTTON, self.show_dialog, button)
        # レイアウト
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(label, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)
        layout.Add(button, flag=wx.EXPAND | wx.ALL, border=10)
        p.SetSizer(layout)
        self.Show()

    def click_button(self):
        print("click")
        with wx.ProgressDialog(parent=self, title='変換中', message='0/'+str(len(self.file_paths))+'ファイル', maximum=len(self.file_paths)) as dlg:
            for i in range(len(self.file_paths)):
                dlg.Update(i, str(i)+'/'+str(len(self.file_paths))+'ファイル')
                path = self.file_paths[i]
                # 解凍
                with tarfile.open(path, 'r:gz') as t:
                    t.extractall(path='temp')
                files = glob.glob('./temp/**', recursive=True)
                file_num = len(files)
                # k-net
                if(file_num < 7):
                    convert_knet2csv(files)
                # kik-net
                else:
                    convert_kiknet2csv(files)
        print("finish convert")
        dialog = wx.MessageDialog(self, 'ファイル変換が完了しました', '完了')
        dialog.ShowModal()
        dialog.Destroy()
        self.is_calculate_now = False

    def show_dialog(self, event):
        if self.is_calculate_now is False:
            dlg = wx.MessageDialog(None,
                '変換を実行しますか？',
                'Message Dialog',
                wx.YES_NO)
            result = dlg.ShowModal()
            if result == wx.ID_YES:
                self.is_calculate_now = True
                self.click_button()
            dlg.Destroy()
        else:
            dialog = wx.MessageDialog(self, '今計算中です', 'エラー', wx.ICON_ERROR)
            dialog.ShowModal()
            dialog.Destroy()

def convert_knet2csv(files):
    for file in files:
        # file = "NIG0190410231756.NS"
        if(not (".EW" in file or ".NS" in file or ".UD" in file)):
            continue
        # import data (earthquake)
        data = pd.read_csv(file,header=None)
        # import station data
        #data_station = pd.read_csv("sitepub_all_sj.csv", encoding="shift-jis")
        #print(data_station)

        # Scale Factor
        scale_factor = 0.0
        for row in data[13:14].itertuples():
            val = str(row[1])
            val1 = float(re.findall(r'Scale Factor(.*)\(gal\)',val)[0])
            val2 = float(re.findall(r'\(gal\)/(.*)',val)[0])
            scale_factor = val1/val2

        # direction wave
        direction = ""
        for row in data[12:13].itertuples():
            val = str(row[1])
            direction = re.findall(r'.?-.?',val)[0]
            if(direction=="N-S"):
                direction="NS"
            elif (direction == "E-W"):
                direction = "EW"
            elif (direction == "U-D"):
                direction = "UD"

        # sampling frec(Hz)
        sampling_frec = 0.0
        for row in data[10:11].itertuples():
            val = str(row[1])
            sampling_frec = float(re.findall(r'\(Hz\)(.*)Hz',val)[0])

        # station code
        station_code = ""
        for row in data[5:6].itertuples():
            val = str(row[1])
            station_code = (re.findall(r'Station Code      (.*)',val)[0])
        #station_place = str(data_station[data_station['code'].str.contains(station_code)]["place"].values[0])

        # wave data
        data_earthquake = data[17:]
        array_earthquake = []
        for row in data_earthquake.itertuples():
            temp_list = row[1].split(" ")
            for val in temp_list:
                if(val==""):
                    continue
                else:
                    array_earthquake.append(float(val)*scale_factor)
        array_earthquake = np.array(array_earthquake)
        print(array_earthquake)

        # average wave
        ave_wave = np.mean(array_earthquake)

        # final wave
        array_earthquake = array_earthquake - ave_wave
        # plt.plot(array_earthquake)
        # plt.show()

        output_data = pd.DataFrame(array_earthquake)
        output_data.to_csv("save_dir/"+station_code+"_"+str(direction)+".csv", encoding="shift-jis", header=[station_code+"_"+str(direction)+" "+str(sampling_frec)+"(Hz) unit:(gal)"])
    shutil.rmtree('./temp/')


def convert_kiknet2csv(files):
    for file in files:
        # file = "temp/TCGH161103111446.NS1"
        if(not (".EW" in file or ".NS" in file or ".UD" in file)):
            continue
        # import data (earthquake)
        data = pd.read_csv(file,header=None)
        # import station data
        #data_station = pd.read_csv("sitepub_all_sj.csv", encoding="shift-jis")
        #print(data_station)

        # Scale Factor
        scale_factor = 0.0
        for row in data[13:14].itertuples():
            val = str(row[1])
            val1 = float(re.findall(r'Scale Factor(.*)\(gal\)',val)[0])
            val2 = float(re.findall(r'\(gal\)/(.*)',val)[0])
            scale_factor = val1/val2

        # direction wave
        direction = ""
        for row in data[12:13].itertuples():
            val = str(row[1])
            direction_val = int(re.findall(r'Dir.(.*)',val)[0])
            if(direction_val == 1):
                direction="NS1"
            elif (direction_val == 2):
                direction = "EW1"
            elif (direction_val == 3):
                direction = "UD1"
            elif (direction_val == 4):
                direction = "NS2"
            elif (direction_val == 5):
                direction = "EW2"
            elif (direction_val == 6):
                direction = "UD2"

        # sampling frec(Hz)
        sampling_frec = 0.0
        for row in data[10:11].itertuples():
            val = str(row[1])
            sampling_frec = float(re.findall(r'\(Hz\)(.*)Hz',val)[0])

        # station code
        station_code = ""
        for row in data[5:6].itertuples():
            val = str(row[1])
            station_code = (re.findall(r'Station Code      (.*)',val)[0])
        #station_place = str(data_station[data_station['code'].str.contains(station_code)]["place"].values[0])

        # wave data
        data_earthquake = data[17:]
        array_earthquake = []
        for row in data_earthquake.itertuples():
            temp_list = row[1].split(" ")
            for val in temp_list:
                if(val==""):
                    continue
                else:
                    array_earthquake.append(float(val)*scale_factor)
        array_earthquake = np.array(array_earthquake)
        print(array_earthquake)

        # average wave
        ave_wave = np.mean(array_earthquake)

        # final wave
        array_earthquake = array_earthquake - ave_wave
        # plt.plot(array_earthquake)
        # plt.show()

        output_data = pd.DataFrame(array_earthquake)
        output_data.to_csv("save_dir/"+station_code+"_"+str(direction)+".csv", encoding="shift-jis", header=[station_code+"_"+str(direction)+" "+str(sampling_frec)+"(Hz) unit:(gal)"])
    shutil.rmtree('./temp/')


if __name__=="__main__":
    save_dir = "save_dir"
    if(not os.path.exists(save_dir)):
        os.mkdir(save_dir)
    if(os.path.exists("./temp")):
        shutil.rmtree('./temp/')
    app = wx.App()
    MyFrame()
    app.MainLoop()
