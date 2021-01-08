from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import *
from tkinter import ttk
import matplotlib
import pyaudio
import numpy as np
from mpmath import *
matplotlib.use("TkAgg")


class Synthetizer(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.make_widgets()
        self.BPM = 120

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
        self.Instrument = ttk.Combobox(self.SynthSetFrame, values=["pure tone"])
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
        self.playaudio(key,O)

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
        print(self.BPM)

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
    def getBaseFrequency(self,key,O):
        oArray = -4,-3,-2,-1,0,1,2,3,4,5
        nArray = (-9/12),(-8/12),(-7/12),(-6/12),(-5/12),(-4/12),(-3/12),(-2/12),(-1/12),0,(1/12),(2/12),(3/12)
        Ft = self.tFreq.get()
        O = oArray[int(O)]
        n = nArray[key]
        baseFrequency = (float(2) ** (float(O) + float(n)))*float(Ft)
        return baseFrequency
    def playaudio(self,key,O,note = "1/4"):
        BPM = 60
        noteArray = "1","1/2","1/4","1/8","1/16"
        noteArrayVal = 1,0.5,0.25,0.125,0.0625
        for i in range(0,4):
            if noteArray[i] == note:
                duration = noteArrayVal[i] # in seconds, may be float
        p = pyaudio.PyAudio()
        volume = 0.2  # range [0.0, 1.0]
        fs = 44100  # sampling rate, Hz, must be integer
        f = self.getBaseFrequency(key,O)  # sine frequency, Hz, may be float
        samples = self.waveType( fs, duration, f)

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True)

        # play. May repeat with different volume values (if done interactively)
        stream.write(volume * samples)

        stream.stop_stream()
        stream.close()

        p.terminate()


if __name__ == "__main__":
    root = Tk()

    Synth = Synthetizer(root)
    #Synth.playaudio()
    root.mainloop()
