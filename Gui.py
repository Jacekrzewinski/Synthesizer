from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import *
from tkinter import ttk
import matplotlib
import pyaudio
import numpy as np
from mpmath import *
import matplotlib.pyplot as plot
import csv
matplotlib.use("TkAgg")


class Synthetizer(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.make_widgets()
        self.BPM = 60

    def make_widgets(self):
        self.winfo_toplevel().title("Syntetizer GUI")
        # self.winfo_toplevel().geometry("800x600")

        # Frequency modulation
        self.FreqModFrame = LabelFrame(self, text="Frequency Modulation")
        self.FreqModFrame.grid(row=0, column=0, columnspan=5, rowspan=5)
        Label(self.FreqModFrame, text="Modulation funcion:").grid(row=0, column=0, sticky=NE)
        self.FreqModOption = ttk.Combobox(self.FreqModFrame, values=["none", "sine", "sqare", "triangle", "saw"])
        self.FreqModOption.grid(row=0, column=1)
        self.FreqModOption.current(0)
        Label(self.FreqModFrame, text="Frequency:").grid(row=1, column=0, sticky=NE)
        self.FreqModFreq = Entry(self.FreqModFrame)
        self.FreqModFreq.grid(row=1, column=1)
        self.FreqModFreq.insert(0, "0")
        Label(self.FreqModFrame, text="Hz").grid(row=1, column=2, sticky=NE)
        Label(self.FreqModFrame, text="Amplitude:").grid(row=2, column=0, sticky=NE)
        self.FreqModAmp = Entry(self.FreqModFrame)
        self.FreqModAmp.grid(row=2, column=1)
        self.FreqModAmp.insert(0, "0")
        Label(self.FreqModFrame, text="").grid(row=2, column=2, sticky=NE)

        # Amplitude modulation
        self.AmpModFrame = LabelFrame(self, text="Amplitude Modulation")
        self.AmpModFrame.grid(row=5, column=0, columnspan=5, rowspan=5)
        Label(self.AmpModFrame, text="Modulation funcion:").grid(row=0, column=0, sticky=NE)
        self.AmpModOption = ttk.Combobox(self.AmpModFrame, values=["none", "sine", "sqare", "triangle", "saw"])
        self.AmpModOption.grid(row=0, column=1)
        self.AmpModOption.current(0)
        Label(self.AmpModFrame, text="Frequency:").grid(row=1, column=0, sticky=NE)
        self.AmpModFreq = Entry(self.AmpModFrame)
        self.AmpModFreq.grid(row=1, column=1)
        self.AmpModFreq.insert(0, "0")
        Label(self.AmpModFrame, text="Hz").grid(row=1, column=2, sticky=NE)
        Label(self.AmpModFrame, text="Amplitude:").grid(row=2, column=0, sticky=NE)
        self.AmpModAmp = Entry(self.AmpModFrame)
        self.AmpModAmp.grid(row=2, column=1)
        self.AmpModAmp.insert(0, "0")
        Label(self.AmpModFrame, text="").grid(row=2, column=2, sticky=NE)

        # Synthesis settings
        self.SynthSetFrame = LabelFrame(self, text="Synthesis settings")
        self.SynthSetFrame.grid(row=6, column=5, columnspan=9, rowspan=5)
        Label(self.SynthSetFrame, text="Tuning frequency:").grid(row=0, column=0, sticky=NE)
        self.tFreq = Entry(self.SynthSetFrame)
        self.tFreq.insert(0, '440')
        self.tFreq.grid(row=0, column=1, sticky=E)
        Label(self.SynthSetFrame, text="Hz").grid(row=0, column=2, sticky=NE)
        Label(self.SynthSetFrame, text="Base funcion:").grid(row=1, column=0, sticky=NE)
        self.BaseSynthFunction = ttk.Combobox(self.SynthSetFrame, values=["sine", "sqare", "triangle", "saw"])
        self.BaseSynthFunction.grid(row=1, column=1)
        self.BaseSynthFunction.current(0)
        Label(self.SynthSetFrame, text="Choose instrument:").grid(row=2, column=0, sticky=NE)
        self.Instrument = ttk.Combobox(self.SynthSetFrame, values=["pure tone","Piano","Violin"])
        self.Instrument.grid(row=2, column=1)
        self.Instrument.current(0)

        # ADSR
        self.ADSRFrame = LabelFrame(self, text="ADSR")
        self.ADSRFrame.grid(row=0, column=6, columnspan=10, rowspan=5)
        self.Fig = Figure(figsize=(7, 2), dpi=50)
        self.Plot = self.Fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.Fig, self.ADSRFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=9, rowspan=4)
        A = StringVar(self, value='0.2')
        A.trace("w", lambda name, index, mode, A=A: self.paintADSR())
        Label(self.ADSRFrame, text="A").grid(row=5, column=0)
        self.ADSR_A = Entry(self.ADSRFrame, width=10, justify=RIGHT, textvariable=A)

        self.ADSR_A.grid(row=5, column=1)
        Label(self.ADSRFrame, text="[s] D").grid(row=5, column=2)
        A = StringVar(self, value='0.2')
        A.trace("w", lambda name, index, mode, A=A: self.paintADSR())
        self.ADSR_D = Entry(self.ADSRFrame, width=10, justify=RIGHT, textvariable=A)

        self.ADSR_D.grid(row=5, column=3)
        Label(self.ADSRFrame, text="[s] S").grid(row=5, column=4)
        A = StringVar(self, value='80')
        A.trace("w", lambda name, index, mode, A=A: self.paintADSR())
        self.ADSR_S = Spinbox(self.ADSRFrame, from_=0, to=100, width=10, justify=RIGHT, textvariable=A,
                              command=lambda: self.paintADSR())

        self.ADSR_S.grid(row=5, column=5, columnspan=2)
        Label(self.ADSRFrame, text="% R").grid(row=5, column=7)
        A = StringVar(self, value='0.2')
        A.trace("w", lambda name, index, mode, A=A: self.paintADSR())
        self.ADSR_R = Entry(self.ADSRFrame, width=10, justify=RIGHT, textvariable=A)

        self.ADSR_R.grid(row=5, column=8)
        Label(self.ADSRFrame, text="[s]").grid(row=5, column=9)

        self.paintADSR()
        #
        self.button1 = Button(self, text="Button1", command=lambda: self.fbutton1())
        self.button1.grid(row=6, column=14)
        self.button2 = Button(self, text="Button2", command=lambda: self.fbutton2())
        self.button2.grid(row=7, column=14)

        # keyboard
        self.Keyboard = Frame(self)
        self.Keyboard.grid(columnspan=45, row=12, column=0, rowspan=3)
        Label(self.Keyboard, text="choose octave").grid(column=0, row=0, columnspan=3)
        self.KeyOctave = ttk.Combobox(self.Keyboard, values=[str(i).zfill(2) for i in range(0, 10)], width=10)
        self.KeyOctave.current(4)
        self.KeyOctave.grid(row=0, column=4, columnspan=4)
        self.KeyC = Button(self.Keyboard, width=10, height=15, bg='white', command=lambda: self.PianoKeyCallback(0),
                           text="C", fg='black', anchor='s')
        self.KeyC.grid(row=1, column=0, rowspan=3, columnspan=4)
        self.KeyCis = Button(self.Keyboard, width=5, height=10, bg='black', command=lambda: self.PianoKeyCallback(1),
                             text="Cis", fg='white', anchor='s')
        self.KeyCis.grid(row=1, column=2, rowspan=2, columnspan=2)
        self.KeyD = Button(self.Keyboard, width=10, height=15, bg='white', command=lambda: self.PianoKeyCallback(2),
                           text="D", fg='black', anchor='s')
        self.KeyD.grid(row=1, column=5, rowspan=3, columnspan=4)
        self.KeyDis = Button(self.Keyboard, width=5, height=10, bg='black', command=lambda: self.PianoKeyCallback(3),
                             text="Dis", fg='white', anchor='s')
        self.KeyDis.grid(row=1, column=5 + 2, rowspan=2, columnspan=2)
        self.KeyE = Button(self.Keyboard, width=10, height=15, bg='white', command=lambda: self.PianoKeyCallback(4),
                           text="E", fg='black', anchor='s')
        self.KeyE.grid(row=1, column=10, rowspan=3, columnspan=4)
        self.KeyF = Button(self.Keyboard, width=10, height=15, bg='white', command=lambda: self.PianoKeyCallback(5),
                           text="F", fg='black', anchor='s')
        self.KeyF.grid(row=1, column=20, rowspan=3, columnspan=4)
        self.KeyFis = Button(self.Keyboard, width=5, height=10, bg='black', command=lambda: self.PianoKeyCallback(6),
                             text="Fis", fg='white', anchor='s')
        self.KeyFis.grid(row=1, column=20 + 2, rowspan=2, columnspan=2)
        self.KeyG = Button(self.Keyboard, width=10, height=15, bg='white', command=lambda: self.PianoKeyCallback(7),
                           text="G", fg='black', anchor='s')
        self.KeyG.grid(row=1, column=25, rowspan=3, columnspan=4)
        self.KeyGis = Button(self.Keyboard, width=5, height=10, bg='black', command=lambda: self.PianoKeyCallback(8),
                             text="Gis", fg='white', anchor='s')
        self.KeyGis.grid(row=1, column=25 + 2, rowspan=2, columnspan=2)
        self.KeyA = Button(self.Keyboard, width=10, height=15, bg='white', command=lambda: self.PianoKeyCallback(9),
                           text="A", fg='black', anchor='s')
        self.KeyA.grid(row=1, column=30, rowspan=3, columnspan=4)
        self.KeyAis = Button(self.Keyboard, width=5, height=10, bg='black', command=lambda: self.PianoKeyCallback(10),
                             text="Ais", fg='white', anchor='s')
        self.KeyAis.grid(row=1, column=30 + 2, rowspan=2, columnspan=2)
        self.KeyH = Button(self.Keyboard, width=10, height=15, bg='white', command=lambda: self.PianoKeyCallback(11),
                           text="H", fg='black', anchor='s')
        self.KeyH.grid(row=1, column=35, rowspan=3, columnspan=4)
        self.KeyC1 = Button(self.Keyboard, width=10, height=15, bg='white', command=lambda: self.PianoKeyCallback(12),
                            text="C+", fg='black', anchor='s')
        self.KeyC1.grid(row=1, column=40, rowspan=3, columnspan=4)

    def PianoKeyCallback(self, key):
        # example can delete or modify
        flag = 0
        O = self.KeyOctave.current();
        if key == 12:
            key = 0;
            O = O + 1;

        switcher = {
            0: "C",
            1: "Cis",
            2: "D",
            3: "Dis",
            4: "E",
            5: "F",
            6: "Fis",
            7: "G",
            8: "Gis",
            9: "A",
            10: "Ais",
            11: "H",
        }
        if self.AmpModOption.current() != 0 or self.AmpModFreq.get() != "0" or self.AmpModAmp.get() != "0":
            flag = flag +1
            print("AmpMod On")
        if self.FreqModOption.current() != 0 or self.FreqModFreq.get() != "0" or self.FreqModAmp.get() != "0":
            flag = flag +2
            print("FreqMod On")

        self.playaudio(key,O,flag)

        print(switcher.get(key) + str(O))

    def paintADSR(self):
        self.Plot.cla();
        self.Plot.plot([0, float(self.ADSR_A.get())], [0, 100], color="red")
        self.Plot.plot([float(self.ADSR_A.get()), float(self.ADSR_A.get()) + float(self.ADSR_D.get())],
                       [100, float(self.ADSR_S.get())], color="blue")
        self.Plot.plot([float(self.ADSR_A.get()) + float(self.ADSR_D.get()),
                        float(self.ADSR_A.get()) + float(self.ADSR_D.get()) + 1],
                       [float(self.ADSR_S.get()), float(self.ADSR_S.get())], color="cyan")
        self.Plot.plot([float(self.ADSR_A.get()) + float(self.ADSR_D.get()) + 1,
                        float(self.ADSR_A.get()) + float(self.ADSR_D.get()) + 1 + float(self.ADSR_R.get())],
                       [float(self.ADSR_S.get()), 0], color="magenta")
        self.Fig.tight_layout()
        self.canvas.draw()

    def fbutton1(self):
        self.playFromFile()

    def fbutton2(self):
        print('button2')

    def waveType(self, fs, duration, f):
        print(self.BaseSynthFunction.get())
        if self.BaseSynthFunction.get() == "sine":
            # generate samples, note conversion to float32 array
            samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)
        if self.BaseSynthFunction.get() == "sqare":
            samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)
            for i, el in enumerate(samples):
                if el > 0:
                    samples[i] = 1
                if el < 0:
                    samples[i] = -1

        if self.BaseSynthFunction.get() == "triangle":
            samples = ((2 * np.arcsin(np.sin(2 * np.pi * np.arange(fs * duration) * f / fs))) / np.pi).astype(np.float32)

        if self.BaseSynthFunction.get() == "saw":
            samples = (-((2 * np.arctan(1/(np.tan(np.pi * np.arange(fs * duration) * f / fs)))) / np.pi)).astype(
                np.float32)
        return samples
    def amplitudeModulation(self,samples,fs,duration):
        values = ["none", "sine", "sqare", "triangle", "saw"]
        Option = self.AmpModOption.get()
        if self.AmpModAmp.get() != 0:
            Amod = 1 - float(self.AmpModAmp.get())
        else:
            Amod = 1

        if self.AmpModFreq.get() != 0:
            Fmod = float(self.AmpModFreq.get())
        else:
            Fmod = float(self.tFreq.get())

        if Option == values[0]:
            Option = self.BaseSynthFunction.get()

        if Option == values[1]:
            mSamples = (np.sin(2 * np.pi * np.arange(fs * duration) * Fmod / fs)).astype(np.float32)
            mSamples = [el * Amod for el in mSamples]
            retVal = [i*j for i, j in zip(samples, mSamples)]
            retVal = np.array(retVal, dtype=np.float32)
            # plt.subplot(3, 1, 1)
            # plt.title('Frequency Modulation')
            # plt.plot(mSamples)
            # plt.ylabel('Amplitude')
            # plt.xlabel('mSamples')
            # plt.subplot(3, 1, 2)
            # plt.plot(samples)
            # plt.ylabel('Amplitude')
            # plt.xlabel('samples')
            # plt.subplot(3, 1, 3)
            # plt.plot(retVal)
            # plt.ylabel('Amplitude')
            # plt.xlabel('retVal')
            # plt.show()
            return retVal
        if Option == values[2]:
            mSamples = (np.sin(2 * np.pi * np.arange(fs * duration) * Fmod / fs)).astype(np.float32)
            mSamples = [el * Amod for el in mSamples]
            for i, el in enumerate(mSamples):
                if el > 0:
                    mSamples[i] = 1
                if el < 0:
                    mSamples[i] = -1
            retVal = [i * j for i, j in zip(samples, mSamples)]
            retVal = np.array(retVal, dtype=np.float32)
            return retVal
        if Option == values[3]:
            mSamples = ((2 * np.arcsin(np.sin(2 * np.pi * np.arange(fs * duration) * Fmod / fs))) / np.pi).astype(
                np.float32)
            mSamples = [el * Amod for el in mSamples]
            retVal = [i * j for i, j in zip(samples, mSamples)]
            retVal = np.array(retVal, dtype=np.float32)
            return retVal
        if Option == values[4]:
            mSamples = (-((2 * np.arctan(1 / (np.tan(np.pi * np.arange(fs * duration) * Fmod / fs)))) / np.pi)).astype(
                np.float32)
            mSamples = [el * Amod for el in mSamples]
            retVal = [i * j for i, j in zip(samples, mSamples)]
            retVal = np.array(retVal, dtype=np.float32)
            return retVal
    def frequencyModulation(self):
        values = ["none", "sine", "sqare", "triangle", "saw"]
        Option = self.FreqModOption.get()
        if self.FreqModAmp.get() != 0:
            Amod = float(self.FreqModAmp.get())
        else:
            Amod = 1

        if self.FreqModFreq.get() != 0:
            Fmod = float(self.FreqModFreq.get())
        else:
            Fmod = float(self.tFreq.get())

        if Option == values[0]:
            Option = self.BaseSynthFunction.get()
        if Option == values[1]:
            time = np.arange(44100.0) / 44100.0
            modulator_frequency = float(self.FreqModFreq.get())
            modulator = (np.sin(2.0 * np.pi * modulator_frequency * time) * Amod) + float(self.tFreq.get())
            sum = 0
            for i in range(0,len(modulator)):
                sum = sum+ (modulator[i]/44100)
            product = np.zeros_like(modulator)

            for i, t in enumerate(time):
                product[i] = np.sin(2. * np.pi * (sum * t + modulator[i]))
            # plt.subplot(3, 1, 1)
            # plt.title('Frequency Modulation')
            # plt.plot(modulator)
            # plt.ylabel('Amplitude')
            # plt.xlabel('Modulator signal')
            # plt.subplot(3, 1, 2)
            # plt.plot(samples)
            # plt.ylabel('Amplitude')
            # plt.xlabel('Carrier signal')
            # plt.subplot(3, 1, 3)
            # plt.plot(product)
            # plt.ylabel('Amplitude')
            # plt.xlabel('Output signal')
            # plt.show()
            product = np.array(product, dtype=np.float32)
            return product
        if Option == values[2]:
            time = np.arange(44100.0) / 44100.0
            modulator_frequency = float(self.FreqModFreq.get())
            modulator = (np.sin(2.0 * np.pi * modulator_frequency * time) * Amod)
            for i, el in enumerate(modulator):
                if el > 0:
                    modulator[i] = 1
                if el < 0:
                    modulator[i] = -1
            modulator = [el + float(self.tFreq.get()) for el in modulator]
            sum = 0
            for i in range(0,len(modulator)):
                sum = sum + (modulator[i]/44100)
            product = np.zeros_like(modulator)
            for i, t in enumerate(time):
                product[i] = np.sin(2. * np.pi * (sum * t + modulator[i]))
            product = np.array(product, dtype=np.float32)
            return product
        if Option == values[3]:
            time = np.arange(44100.0) / 44100.0
            modulator_frequency = float(self.FreqModFreq.get())
            modulator = ((2 * np.arcsin(np.sin(2 * np.pi * modulator_frequency * time)))* Amod / np.pi)+ float(self.tFreq.get())
            sum = 0
            for i in range(0, len(modulator)):
                sum = sum + (modulator[i] / 44100)
            product = np.zeros_like(modulator)
            for i, t in enumerate(time):
                product[i] = ((2 * np.arcsin(np.sin(2 * np.pi * (sum * t + modulator[i])))) / np.pi)
            product = np.array(product, dtype=np.float32)
            return product
        if Option == values[4]:
            time = np.arange(44100.0) / 44100.0
            modulator_frequency = float(self.FreqModFreq.get())
            modulator = (-((2 * np.arctan(1 / (np.tan(np.pi * modulator_frequency * time)))) * Amod / np.pi))+ float(self.tFreq.get())
            sum = 0
            for i in range(0, len(modulator)):
                sum = sum + (modulator[i] / 44100)
            product = np.zeros_like(modulator)
            for i, t in enumerate(time):
                product[i] = (-((2 * np.arctan(1 / (np.tan(np.pi * (sum * t + modulator[i]))))) / np.pi))
            product = np.array(product, dtype=np.float32)
            return product
    def getBaseFrequency(self,key,O):
        if key == 12:
            baseFrequency = 0.
            return baseFrequency
        oArray = -4,-3,-2,-1,0,1,2,3,4,5
        nArray = (-9/12),(-8/12),(-7/12),(-6/12),(-5/12),(-4/12),(-3/12),(-2/12),(-1/12),0,(1/12),(2/12),(3/12)
        Ft = self.tFreq.get()
        O = oArray[int(O)]
        n = nArray[key]
        baseFrequency = (float(2) ** (float(O) + float(n)))*float(Ft)
        return baseFrequency
    def harmonic(self,instrument,fs,duration,f):
        if instrument == "piano":
            pianoH = [-15., -15.9, -33.9, -30.7, -53.5, -29.7, -43.3, -40.6, -40.5,
                      -46.5, -48.5,-48.9,-61.9,-48.9,-65.9,-64.2,-69.5]
            pianoA = np.zeros_like(pianoH)
            for i in range(0, len(pianoH)):
                pianoA[i] = 10 ** (pianoH[i] / 20)
            samples = self.waveType(fs, duration, f)
            product = np.zeros_like(samples)
            for i in range(1,len(pianoA)+1):
                temp = (pianoA[i-1] * self.waveType(fs, duration, (i*f)))/len(pianoA)
                product = product + temp
            product = np.array(product, dtype=np.float32)
        if instrument == "violin":
            violinH = [-10.3, -17.9, -18.9, -24.7, -21.7, -24.6, -31.5, -27., -26.4,
                      -51.8, -45.8,-38.6,-51.1,-41.9,-47.9,-44.9,-48.8,-51.7,-58.9]
            violinA = np.zeros_like(violinH)
            for i in range(0, len(violinH)):
                violinA[i] = 10 ** (violinH[i] / 20)
            samples = self.waveType(fs, duration, f)
            product = np.zeros_like(samples)
            for i in range(1, len(violinA) + 1):
                temp = (violinA[i - 1] * self.waveType(fs, duration, (i * f))) / len(violinA)
                product = product + temp
            product = np.array(product, dtype=np.float32)
        return product
    def getInstrument(self,fs, duration, f):
        if self.Instrument.current() == 0:        #pure tone
            samples = self.waveType(fs, duration, f)
            return samples
        if self.Instrument.current() == 1:        #piano
            samples = self.harmonic("piano", fs, duration, f)
            return samples
        if self.Instrument.current() == 2:        #violin
            samples = self.harmonic("violin", fs, duration, f)
            return samples
    def ADSR(self,samples):
        A = float(self.ADSR_A.get())
        D = float(self.ADSR_D.get())
        S = int(self.ADSR_S.get())
        R = float(self.ADSR_R.get())
        product = np.zeros_like(samples)
        A_len = int(len(samples) * A)
        D_len = int(len(samples) * D)
        R_len = int(len(samples) * R)
        S_len = int(len(samples) - (A_len+D_len+R_len))
        sum = 0
        for i in range(0,A_len):
            sum = sum + (100/A_len)/100
            product[i] = sum
        for i in range(A_len, A_len + D_len):
            sum = sum - ((100-S)/D_len)/100
            product[i] = sum
        for i in range(A_len + D_len, A_len + D_len + S_len):
            product[i] = S/100
        for i in range(A_len + D_len + S_len, A_len + D_len + S_len+R_len):
            sum = sum - (S / D_len) / 100
            product[i] = sum
        retVal = product * samples
        retVal = np.array(retVal, dtype=np.float32)
        return retVal
    def playFromFile(self):
        keytable = ["c","cis","d","dis","e","f","fis","g","gis","a","ais","h","p"]
        with open('plik1.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                print(row)
                for i in range(0,len(keytable)):
                    if keytable[i] == row[1]:
                        print(keytable[i])
                        key = i
                        self.playaudio( key, int(row[2]), 0,row[0])
                        i = i+1
                        break
    def playaudio(self,key,O,flag, note = "1"):
        noteArray = "1","1/2","1/4","1/8","1/16"
        noteArrayVal = float(60/self.BPM),float(30/self.BPM),float(15/self.BPM),float(7.5/self.BPM),float(3.75/self.BPM)
        for i in range(0,4):
            if noteArray[i] == note:
                duration = noteArrayVal[i] # in seconds, may be float
        p = pyaudio.PyAudio()
        #volume = 0.3  # range [0.0, 1.0] / ADSR instead
        fs = 44100  # sampling rate, Hz, integer
        f = self.getBaseFrequency(key,O)  # sine frequency, Hz, may be float
        samples = self.getInstrument(fs, duration, f)

        if flag == 1:
            samples = self.amplitudeModulation( samples, fs, duration)
        if flag == 2:
            samples = self.frequencyModulation()
        if flag == 3:
            samples1 = self.amplitudeModulation(samples, fs, duration)
            samples2 = self.frequencyModulation()
            samples = [i*j for i, j in zip(samples1, samples2)]
            samples = np.array(samples, dtype=np.float32)

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True)

        # play. May repeat with different volume values (if done interactively)
        samples = self.ADSR(samples)
        stream.write(samples)

        stream.stop_stream()
        stream.close()

        p.terminate()


if __name__ == "__main__":
    root = Tk()

    Synth = Synthetizer(root)
    #Synth.harmonic("sad")
    root.mainloop()
