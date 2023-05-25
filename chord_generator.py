import tkinter
import tkinter.messagebox

class Chord():
    def _tone_index(self, tone):
        tone = tone.upper()
        bases = list("A B H C _ D _ E F _ G _".split())
        if not self.H_notation:
            bases[2] = "B"
            bases[1] = "_"
        index = 0
        try:
            assert tone != "_"
            index = bases.index(tone[0])
            if len(tone) > 1 and tone[1] == "#": index += 1
            if len(tone) > 1 and tone[1] == "B": index -= 1
            index %= 12
        except: self.error("Invalid tone name: '" + str(tone) + "'")
        return index

    def __init__(self, name="A", strings_string="E", use_H=True, handspan=3,
            fingers=4, barability=True):
        self.H_notation = use_H
        self.handspan = handspan
        self.fingers = fingers
        self.barability = barability

        self.best = None
        name = name.upper()
        self.name = name
        strings = list()
        for s in strings_string:
            if s.upper() == s.lower() or (self.H_notation and s == "B"):
                strings[-1] += s
            else:
                if not self.H_notation and s == "H": strings.append("B")
                else: strings.append(s)
        self.string_names = strings
        self.strings = [self._tone_index(str(s).upper()) for s in strings]

        if not self.H_notation and "H" in self.name:
            self.name.replace("H", "B", -1)
        base = self._tone_index(self.name[:2])
        self.tones = list(((base + tone) % 12)
                for tone in self._translate(self.name[1:]))

    def get_score(self, pos, uses):
        def ignore_zeros(x):
            if x is None or x == 0: return 10**9
            return x
        def ignore_None(x):
            if x is None: return -1
            return x

        score = 10000

        ma = max(pos, key=ignore_None)
        mi = min(pos, key=ignore_zeros)
        if mi is None: mi = 0
        if ma is None: return -1
        if ma - mi >= self.handspan: return -1

        zeros = pos.count(0)
        nones = pos.count(None)
        score *= zeros + 1
        pressed = len(pos) - zeros - nones
        if pressed > self.fingers:
            if not self.barability: return -1
            if 0 in pos: return -1
            barpos = min(pos, key=ignore_zeros)
            if pressed - pos.count(barpos) + 1 > self.fingers: return -1
            stage = 0
            for p in pos:
                if p == 0 and stage == 1: stage = 2
                elif p == barpos:
                    if stage == 0: stage = 1
                    elif stage == 2: return -1
            #score /= (barpos + 5) / 3
        score /= ma - mi + 1
        score /= mi + 1

        first, last = len(pos) - 1, 0
        for i in range(len(pos)):
            if pos[i] is not None and pos[i] > 0:
                first = min(first, i)
                last = max(last, i)
        if last > first - 1: score /= last - first + 1

        for val in uses.values():
            score *= val

        stage = 0
        for p in pos:
            if p is None and stage == 1: stage = 2
            else:
                if stage == 0: stage = 1
                elif stage == 2: return -1

        score /= 2**(2**(2**nones))
        score /= sum((3 if pos[i] is None else pos[i]
                ) / (i + 1) for i in range(len(pos))) + 1

        return score
        
    def generate(self):
        if not self._test_correctness(): return None

        uses = dict()
        for tone in self.tones: uses[tone] = 0
        now = []
        all = []
        bad = []

        def dive(ma, mi):
            if ma is not None:
                if ma - mi > self.handspan:
                    return None
            if len(now) >= len(self.strings):
                score = self.get_score(now, uses)
                if score >= 1:
                    all.append((score, len(all), now[:]))
                elif score > 0:
                    bad.append((score, len(bad), now[:]))
                return None
            need_none = True
            for tone in self.tones:
                new = (tone - self.strings[len(now)]) % 12
                if new == 0: need_none = False
                now.append(new)
                uses[tone] += 1
                if ma is None:
                    if new == 0: dive(None, None)
                    else: dive(new, new)
                else: dive(max(ma, new), min(mi, (new if new > 0 else mi)))
                now.pop()
                uses[tone] -= 1
            if need_none:
                now.append(None)
                dive(ma, mi)
                now.pop()

        dive(None, None)
        if len(all) == 0: all += bad
        all.sort(reverse=True)
        self.best = all

    def get(self):
        if not self._test_correctness(): return []

        if self.best is None:
            self.generate()
        return list(map(lambda x: x[2], self.best))

    def _test_correctness(self):
        try:
            assert type(self.strings) == list
            assert len(self.strings) <= 12
            assert len(self.strings) > 0
            for st in self.strings:
                assert type(st) == int
            return True
        except AssertionError:
            self.error("Wrong input parameters")
            return False

    @staticmethod
    def _translate(name):
        need = set((0, 4, 7))

        if "MI" in name:
            need.remove(4)
            need.add(3)
        elif "AUG" in name:
            need.remove(7)
            need.add(8)
        elif "DIM" in name:
            need.remove(4)
            need.remove(7)
            need.add(3)
            need.add(6)

        if "SUS2" in name:
            if 3 in need: need.remove(3)
            else: need.remove(4)
            need.add(2)
        if "SUS4" in name:
            if 3 in need: need.remove(3)
            else: need.remove(4)
            need.add(5)
        if "ADD2" in name or "9" in name: need.add(2)
        if "ADD4" in name or "11" in name: need.add(5)
        if "6" in name or "13" in name: need.add(9)

        if "MAJ7" in name: need.add(11)
        elif "7" in name: need.add(10)

        return list(need)
    
    def error(self, message):
        print(message)

###########################################################################
###########################################################################

class Program():
    def __init__(self):
        self.win_width = 720
        self.win_height = 480
        self.win_size_limit = 315
        self.root = tkinter.Tk()
        self.root.title("Chord generator -- by Ján Plachý")
        self.recreate_window()

        self.set_defaults()

        self.generate_chord_button()

        self.root.mainloop()

    def generate_chord_button(self):
        self.strings = self.string_names.get()
        self.generate_chord(*map(lambda x: (
                x if type(x) is not str else x.upper()),
                (self.chord_name.get(),
                self.strings,
                self.use_H_variable.get(),
                int(self.handspan_scale.get()),
                int(self.fingers_scale.get()),
                self.barability_variable.get())))
        self.show_chord()

    def generate_chord(self, name, strings, use_H, handspan,
            fingers, barability):
        history_name = "&".join((name, strings,
                str(handspan), str(fingers),
                str(barability), str(use_H)))
        if history_name in self.chords_memory.keys():
            ch = self.chords_memory[history_name]
        else:
            ch = Chord(name, strings, use_H, handspan, fingers, barability)
            #chords = ch.get()
            self.chords_history.append(ch)
            self.chords_memory[history_name] = ch

        self.chords_history_index = len(self.chords_history) - 1
        string_list = list()
        for s in strings:
            if s.upper() == s.lower() or (use_H and s == "B"):
                string_list[-1] += s
            else:
                if not use_H and s == "H": string_list.append("B")
                else: string_list.append(s)
        self.strings = string_list
        self.chord_to_display = 0

    def show_chord(self):
        chord = self.chords_history[self.chords_history_index].get()

        can = self.canvas
        w, h = self.cw, self.ch
        if len(chord) < 1:
            can.delete("all")
            can.create_text(w // 2, h // 2, text="No matching chords",
                    font=self.small_font)
            return None
        ch = chord[self.chord_to_display]
        l = len(ch)
        v = int(self.handspan_scale.get()) + 1
        x = w // (l + 2)
        y = h // (v + 4)

        can.delete("all")

        for i in range(l):
            can.create_rectangle(x * (i + 1), y * 1, x * (i + 2), y * 2,
                    fill="black")
            can.create_text(int(x * (i + 1.5)), int(y * 1.5),
                    text=str(self.strings[i]), font=self.small_font,
                    fill="white")
            for j in range(2, v + 3):
                can.create_rectangle(x * (i + 1), y * j,
                        x * (i + 2), y * (j + 1))

        start = min(ch, key=lambda x: (10**9 if x is None or x < 1 else x)) - 1
        end = max(ch, key=lambda x: (0 if x is None else x))
        if end > 5:
            for i in range(len(ch)):
                if ch[i] is None or ch[i] == 0: continue
                ch[i] -= start
            can.create_text(x * 0.5, y * 1.5, text=str(start),
                    font=self.small_font)

        for i in range(l):
            if ch[i] is None:
                can.create_text(x * (i + 1.5), y * 2.5, text="x",
                        fill="red", font=self.small_font)
            elif ch[i] == 0: continue
            else:
                can.create_oval(x * (i + 1) + 5, y * (int(ch[i]) + 1) + 5,
                        x * (i + 2) - 5, y * (int(ch[i]) + 2) - 5,
                        fill="gold")
        if end > 5:
            for i in range(len(ch)):
                if ch[i] is None or ch[i] == 0: continue
                ch[i] += start

    def previous_chord(self):
        if self.chord_to_display < 1: return None
        self.chord_to_display -= 1
        self.show_chord()

    def next_chord(self):
        chord = self.chords_history[self.chords_history_index].get()
        if self.chord_to_display >= len(chord) - 1: return None
        self.chord_to_display += 1
        self.show_chord()
    
    def show_history_previous(self):
        if self.chords_history_index < 1: return None
        self.chords_history_index -= 1
        self.show_chord()
        self.rewrite_others()

    def show_history_next(self):
        if self.chords_history_index > len(self.chords_history) - 2: return None
        self.chords_history_index += 1
        self.chord_to_display = 0
        self.show_chord()
        self.rewrite_others()
    
    def clear_history(self):
        self.chords_history = [self.chords_history[self.chords_history_index]]
        self.chords_history_index = 0
        self.chord_to_display = 0
        self.chords_memory = dict()
        self.generate_chord_button()
    
    def rewrite_others(self):
        ch = self.chords_history[self.chords_history_index]
        self.string_names.delete(0, "end")
        self.string_names.insert(0, "".join(ch.string_names))
        self.chord_name.delete(0, "end")
        self.chord_name.insert(0, ch.name)
        self.handspan_scale.set(ch.handspan)
        self.fingers_scale.set(ch.fingers)
        self.barability_variable.set(ch.barability)
        self.use_H_variable.set(ch.H_notation)

    def resize(self):
        strings = self.string_names.get()
        chord = self.chord_name.get(),
        handsdpan = int(self.handspan_scale.get())
        fingers = int(self.fingers_scale.get())
        barability = self.barability_variable.get()
        use_H = self.use_H_variable.get()

        self.win_width = self.win_width // 3 * 2
        self.win_height = self.win_height // 3 * 2
        if self.win_width < self.win_size_limit:
            while self.win_width < self.root.winfo_screenwidth():
                self.win_width = self.win_width * 3 // 2
                self.win_height = self.win_height * 3 // 2
            self.win_width = self.win_width // 3 * 2
            self.win_height = self.win_height // 3 * 2
        self.root.minsize(self.win_width, self.win_height)
        self.root.maxsize(self.win_width, self.win_height)

        self.recreate_window()

        self.string_names.insert(0, strings)
        self.chord_name.insert(0, chord)
        self.handspan_scale.set(handsdpan)
        self.fingers_scale.set(fingers)
        self.barability_variable.set(barability)
        self.use_H_variable.set(use_H)

        self.generate_chord_button()

    def recreate_window(self):
        for w in list(self.root.children.values()): w.destroy()
        
        self.root.geometry(f"{self.win_width}x{self.win_height}")
        self.root.attributes("-topmost", "true")
        self.root.update()
        self.small_font = f"Impact {int(self.win_height * 0.05)}"
        self.smaller_font = f"Impact {int(self.win_height * 0.025)}"

        self.title = tkinter.Label(text="Chord generator", background="gold",
                width=self.win_width,
                font=f"Impact {int(self.win_height * 0.05)}")
        self.title.pack(side="top")

        tkinter.Frame(height=int(self.win_height * 0.01)).pack(side="top")
        upper_bar = tkinter.Frame()
        upper_bar.pack(side="top")
        tkinter.Frame(height=int(self.win_height * 0.01)).pack(side="top")

        tkinter.Label(upper_bar, text=" Strings ",
                font=self.small_font).pack(side="left")
        self.string_names = tkinter.Entry(upper_bar, width=8,
                font=self.small_font)
        self.string_names.pack(side="left")

        tkinter.Label(upper_bar, text=" Chord ",
                font=self.small_font).pack(side="left")
        self.chord_name = tkinter.Entry(upper_bar, width=10,
                font=self.small_font)
        self.chord_name.pack(side="left")

        tkinter.Frame(upper_bar, width=self.win_width * 0.01).pack(side="left")
        prev_button = tkinter.Button(upper_bar, text="<", font=self.small_font,
                width=3, height=1, command=self.previous_chord)
        prev_button.pack(side="left")
        prev_button.bind("<Return>", lambda e: self.previous_chord())
        next_button = tkinter.Button(upper_bar, text=">", font=self.small_font,
                width=3, height=1, command=self.next_chord)
        next_button.pack(side="left")
        next_button.bind("<Return>", lambda e: self.next_chord())

        self.string_names.focus_set()
        self.string_names.bind("<Return>",
                lambda e: self.chord_name.focus_set())
        self.chord_name.bind("<Return>",
                lambda e: self.generate_chord_button())

        left_bar = tkinter.Frame()
        left_bar.pack(side="left")
        left_bar_scales = tkinter.Frame(left_bar)
        left_bar_scales.pack(side="top")

        handspan_bar = tkinter.Frame(left_bar_scales)
        handspan_bar.pack(side="left")
        tkinter.Label(handspan_bar, text="Span", anchor="center",
                font=self.smaller_font).pack(side="top")
        self.handspan_scale = tkinter.Scale(handspan_bar, orient="vertical",
                from_=1, to=5, length=int(self.win_height) * 0.5)
        self.handspan_scale.pack(side="top")

        finger_scale_bar = tkinter.Frame(left_bar_scales)
        tkinter.Label(finger_scale_bar, text="Fin", anchor="center",
                font=self.smaller_font).pack(side="top")
        finger_scale_bar.pack(side="left")
        self.fingers_scale = tkinter.Scale(finger_scale_bar, orient="vertical",
                from_=1, to=5, length=int(self.win_height) * 0.5)
        self.fingers_scale.pack(side="top")

        self.use_H_variable = tkinter.IntVar()
        self.use_H_checkbox = tkinter.Checkbutton(left_bar,
                text="H > B", variable=self.use_H_variable,
                font=self.smaller_font)
        self.use_H_checkbox.pack(side="bottom")

        self.barability_variable = tkinter.IntVar()
        self.barability_checkbox = tkinter.Checkbutton(left_bar,
                text="barr", variable=self.barability_variable,
                font=self.smaller_font)
        self.barability_checkbox.pack(side="bottom")

        self.canvas = tkinter.Canvas(width=int(self.win_width * 0.85),
                height=int(self.win_height * 0.7))
        self.canvas.pack(side="top")
        self.cw = int(self.win_width * 0.85)
        self.ch = int(self.win_height * 0.7)
        self.canvas.configure(background="white")


        menubar = tkinter.Menu(self.root)
        self.root.config(menu=menubar)
        menubar.add_command(label="Exit", command=self.exit,
                underline=0)
        menubar.add_command(label="Help", command=self.program_help,
                underline=0)
        menubar.add_command(label="About", command=self.program_about,
                underline=0)
        menubar.add_command(label="Generate",
                command=self.generate_chord_button, underline=0)
        menubar.add_command(label="Resize",
                command=self.resize, underline=0)
        menubar.add_command(label="History: previous", 
                command=self.show_history_previous, underline=9)
        menubar.add_command(label="History: next",
                command=self.show_history_next, underline=9)
        menubar.add_command(label="Clear history",
                command=self.clear_history, underline=0)

        self.root.bind("<Escape>", lambda e: self.exit())

    def set_defaults(self):
        self.chords_memory = dict()
        self.chords_history = []
        self.string_names.insert(0, "EADGHE")
        self.chord_name.insert(0, "A")
        self.fingers_scale.set(4)
        self.handspan_scale.set(3)
        self.barability_variable.set(True)
        self.use_H_variable.set(True)

    def exit(self):
        self.root.destroy()

    def program_about(self):
        tkinter.messagebox.showinfo(title="About",
                message="""
Generátor akordov.
Vytvoril Ján Plachý ako zápočtový program na programovanie 1, 2022/23.
Kontakt: plachyj8@natur.cuni.cz

Guitar chord generator.
Made by Ján Plachý as a semestral project for programing 1, 2022/23.
plachyj8@natur.cuni.cz
""")

    def program_help(self):
        tkinter.messagebox.showinfo(title="Help",
                message="""
Use any-case letters C, D, E, F, G, A and H (or B if "H > B" is not checked) and #, b symbols for tones (but b is interpreted as B, if "H > B" is not checked).
Chord names must start with one of those letters to be valid.
Strings must contain only those letterts and symbols to be valid.

Chord modifications are:
- "MI" for minor chord (major is default)
- "AUG" for augmented chord
- "DIM" for diminished chord
- "SUS2" and "SUS4" for suspended chords (3. changed to 2. / 4.)
- "ADD2", "ADD4" for adding 2. / 4. without removing 3.
- "6", "7", "9", "11", "13" for adding respective tones
    (but everything bigger than 7 is used only as % 7)
- "MAJ7" to add major 7. tone

The "Span" bar declares the maximal distance between any two fingers in the chords being generated.
The "Fin" bar declares the number of fingers that can be used to play chords.
The "Barr" chechbox declares the ability to use bar chords (those can have more points than number of fingers, if the highest ones can be pressed with one finger).
The "H > B" checkbox declares the use of letter H (and B for Hb) instead of B.
""")


if __name__ == "__main__":
    _chord_generator_ = Program()
