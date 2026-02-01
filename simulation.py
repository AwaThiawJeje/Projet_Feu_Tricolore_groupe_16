import tkinter as tk
from tkinter import ttk
import turtle
import random
import time
from database import Database
from voiture import Voiture
from feutricolore import FeuTricolore


class Simulation:
    def __init__(self, racine):
        self.scenario_combobox = None
        self.root = racine
        self.root.title("Feu de circulation Thiès ")
        self.root.geometry("1300x850")
        self.root.configure(bg="#0f172a")

        self.db = Database()
        self.running = False
        self.paused = False
        self.scenario = "Normal"
        self.voitures = []
        self.last_spawn = time.time()

        self.setup_ui()

        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor("#064e3b")
        self.screen.tracer(0)

        self.register_pro_shapes()
        self.dessiner_intersection()

        self.feux = {
            "E": FeuTricolore(self.screen, -110, -110),
            "W": FeuTricolore(self.screen, 110, 110),
            "N": FeuTricolore(self.screen, -110, 110),
            "S": FeuTricolore(self.screen, 110, -110)
        }
        self.set_feux("EW", "GREEN")

        self.set_feux("NS", "RED")

        self.cycle_timer = time.time()
        self.animer()

    def register_pro_shapes(self):
        #VOITURE HORIZONTALE (Pour Est / Ouest)
        sh = turtle.Shape("compound")
        # 1. Le Corps
        sh.addcomponent(((10, -25), (10, 25), (-10, 25), (-10, -25)), "white", "black")
        # 2. Le Pare-brise
        sh.addcomponent(((8, 5), (8, 18), (-8, 18), (-8, 5)), "#7dd3fc", "black")
        # 3. Phare Avant Gauche
        sh.addcomponent(((-4, 22), (-4, 25), (-8, 25), (-8, 22)), "yellow", "black")
        # 4. Phare Avant Droit
        sh.addcomponent(((8, 22), (8, 25), (4, 25), (4, 22)), "yellow", "black")
        # Enregistrement de la forme verticale
        self.screen.register_shape("car_h", sh)

        # --- VOITURE VERTICALE (Pour Nord / Sud) ---
        sv = turtle.Shape("compound")
        # Corps
        sv.addcomponent(((-10, -20), (10, -20), (10, 20), (-10, 20)), "white", "black")
        # Pare-brise
        sv.addcomponent(((-8, 8), (8, 8), (8, 16), (-8, 16)), "#7dd3fc", "black")
        # Phares
        sv.addcomponent(((-8, 18), (-5, 18), (-5, 20), (-8, 20)), "yellow", "black")
        sv.addcomponent(((5, 18), (8, 18), (8, 20), (5, 20)), "yellow", "black")
        self.screen.register_shape("car_v", sv)

    def setup_ui(self):
        side = tk.Frame(self.root, bg="#1e293b", width=300, padx=20, pady=20)
        side.pack(side=tk.LEFT, fill=tk.Y)
        side.pack_propagate(False)
        tk.Label(side, text="Panneau de contrôle", fg="#3b82f6", bg="#1e293b", font=("Arial", 15, "bold")).pack(pady=20)
        self.btn_main = tk.Button(side, text="DÉMARRER", bg="#10b981", fg="white", font=("Arial", 11, "bold"),
                                  command=self.toggle, relief="flat", pady=10)
        self.btn_main.pack(fill=tk.X, pady=5)
        self.btn_pause = tk.Button(side, text="PAUSE / REPRENDRE", bg="#3b82f6", fg="white", font=("Arial", 10, "bold"),
                                   command=self.pause_only, relief="flat", pady=10)
        self.btn_pause.pack(fill=tk.X, pady=5)
        tk.Button(side, text="STOP / RESET", bg="#ef4444", fg="white", font=("Arial", 10, "bold"), command=self.reset,
                  relief="flat", pady=10).pack(fill=tk.X, pady=5)
        tk.Label(side, text="SCÉNARIO", fg="#94a3b8", bg="#1e293b", font=("Arial", 9, "bold")).pack(anchor="w",
                                                                                                    pady=(20, 5))
        self.scenario_combobox = ttk.Combobox(side, values=["Normal", "Heure de Pointe", "Mode Nuit", "Mode Manuel"],
                                    state="readonly")
        self.scenario_combobox.current(0)

        self.scenario_combobox.pack(fill=tk.X)
        self.scenario_combobox.bind("<<ComboboxSelected>>", lambda e: self.set_scenario())
        self.btn_manual = tk.Button(side, text="CHANGER LES FEUX", bg="#8b5cf6", fg="white", font=("Arial", 10, "bold"),
                                    command=self.mode_manuel, relief="flat", pady=12)
        self.lbl_v = tk.Label(side, text="Véhicules Actifs: 0", bg="#0f172a", fg="#10b981", font=("Consolas", 11),
                              pady=15)
        self.lbl_v.pack(fill=tk.X, pady=20)
        self.logs = tk.Listbox(side, bg="#0f172a", fg="#64748b", borderwidth=0, font=("Consolas", 8))
        self.logs.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.root, width = 950, height = 700, bg="#064e3b", highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

#ajoute
    def dessiner_intersection(self):
        t = turtle.RawTurtle(self.screen)
        t.hideturtle()

        t.speed(0)

        t.penup()
        road_w = 160

        # Dessin à partir du CENTRE (0,0)
        t.color("#1f2937")
        # Route Horizontale
        t.goto(-500, -80)

        t.begin_fill()
        for _ in range(2): 
            t.forward(1000)
            t.left(90)
            t.forward(road_w)
            t.left(90)
        t.end_fill()
        # Route Verticale
        t.goto(-80, -500)

        t.begin_fill()
        for _ in range(2): 
            t.forward(road_w)
            t.left(90)
            t.forward(1000)
            t.left(90)
        t.end_fill()

        # Lignes jaunes
        t.color("#fde047")

        t.pensize(2)
        t.goto(-500, 0)

        t.setheading(0)
        for _ in range(25): 
            t.pendown()
            t.forward(20)
            t.penup()
            t.forward(20)
        t.goto(0, -500)

        t.setheading(90)
        for _ in range(25): 
            t.pendown()
            t.forward(20)
            t.penup()
            t.forward(20)

        # Passages piétons
        def pieton(x, y, orient):
            t.penup()

            t.goto(x, y)

            t.setheading(orient)

            t.color("white")
            for _ in range(8):
                t.pendown()

                t.begin_fill()
                for _ in range(2): 
                    t.forward(30)
                    t.left(90)
                    t.forward(10)
                    t.left(90)
                t.end_fill()

                t.penup()

                t.right(90)

                t.forward(20)

                t.left(90)

        pieton(-130, 65, 0)

        pieton(100, 65, 0)
        pieton(-65, -130, 90)

        pieton(-65, 100, 90)

    def set_feux(self, group, state):
        if group == "EW":
            self.feux["E"].state = state

            self.feux["W"].state = state
        else:
            self.feux["N"].state = state

            self.feux["S"].state = state

    def mode_manuel(self):
        if self.scenario == "Mode Manuel":
            if self.feux["E"].state == "GREEN":
                self.set_feux("EW", "ORANGE")
                self.root.after(1000, lambda: [self.set_feux("EW", "RED"), self.set_feux("NS", "GREEN")])
                self.db.log("USER_ACTION", "Changement Manuel: NS Vert", self.scenario)
            else:
                self.set_feux("NS", "ORANGE")
                self.root.after(1000, lambda: [self.set_feux("NS", "RED"), self.set_feux("EW", "GREEN")])
                self.db.log("USER_ACTION", "Changement Manuel: EW Vert", self.scenario)

    def toggle(self):
        if not self.running:
            self.running = True

            self.paused = False
            self.db.log("SYSTEM", "Démarrage Simulation", self.scenario)
        else:
            self.reset()

    def pause_only(self):
        self.paused = not self.paused
        self.db.log('SIMULATION', 'Pause / reprise', self.scenario)

    def reset(self):
        self.running = False

        self.paused = False
        for v in self.voitures:
            v.t.clear()
            v.t.hideturtle()
        self.voitures = []
        self.db.log ('SIMULATION', 'Reinitialisation', self.scenario)

        self.refresh_logs()

    def set_scenario(self):
        self.scenario = self.scenario_combobox.get()
        self.db.log("SCENARIO", self.scenario, self.scenario)
        if self.scenario == "Mode Manuel":
            self.btn_manual.pack(fill=tk.X, pady=10, after=self.scenario_combobox)
        else:
            self.btn_manual.pack_forget()

    def refresh_logs(self):
        self.logs.delete(0, tk.END)
        for l in self.db.get_logs(): self.logs.insert(tk.END, f"[{l[0]}] {l[2]}")

    def animer(self):
        if self.running and not self.paused:
            now = time.time()
            dur = 8 if self.scenario != "Heure de Pointe" else 12
            if self.scenario not in ["Mode Nuit", "Mode Manuel"]:
                if now - self.cycle_timer > dur:
                    self.cycle_timer = now
                    if self.feux["E"].state == "GREEN":
                        self.set_feux("EW", "ORANGE")
                        self.root.after(2000, lambda: [self.set_feux("EW", "RED"), self.set_feux("NS", "GREEN")])
                    else:
                        self.set_feux("NS", "ORANGE")
                        self.root.after(2000, lambda: [self.set_feux("NS", "RED"), self.set_feux("EW", "GREEN")])
            elif self.scenario == "Mode Nuit":
                s = "ORANGE" if int(now * 2) % 2 == 0 else "BLACK"
                self.set_feux("EW", s)

                self.set_feux("NS", s)
            rate = 2.5 if self.scenario != "Heure de Pointe" else 1.0
            if now - self.last_spawn > rate:
                self.last_spawn = now
                d = random.choice(["N", "S", "E", "W"])
                c = random.choice(["#ef4444", "#3b82f6", "#facc15", "#db2777", "#ffffff", "#8b5cf6"])
                self.voitures.append(Voiture(self.screen, d, c))
            for v in self.voitures[:]:
                v.stopped = False

                v.speed = v.base_speed
                x, y = v.t.position()
                st = self.feux[v.direction].state
                dist = 112
                if (v.direction == "E" and -dist - 40 < x < -90) or (v.direction == "W" and 90 < x < dist + 40) or \
                        (v.direction == "N" and -dist - 40 < y < -90) or (v.direction == "S" and 90 < y < dist + 40):
                    if st == "RED":
                        v.stopped = True
                    elif st == "ORANGE":
                        v.speed *= 0.35
                for o in self.voitures:
                    if o != v and o.direction == v.direction and v.t.distance(o.t) < 65:
                        if (v.direction == "E" and o.t.xcor() > x) or (v.direction == "W" and o.t.xcor() < x) or \
                                (v.direction == "N" and o.t.ycor() > y) or (v.direction == "S" and o.t.ycor() < y):
                            v.stopped = True
                v.move()
                if v.is_off_screen():
                    v.t.clear()

                    v.t.hideturtle()

                    self.voitures.remove(v)
            self.lbl_v.config(text=f"Véhicules Actifs: {len(self.voitures)}")
            self.refresh_logs()
        for l in self.feux.values(): l.dessiner()
        self.screen.update()

        self.root.after(30, self.animer)

