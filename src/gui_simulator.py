#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt

# --- tvoje importy (ponech stejné názvy modulů) ---
from simulator.simulator import Simulator
from citizens import (
    AdvancedVoterND, 
    AdvancedVoterNDBool, 
    SimpleVoter,
    SimpleAdvancedVoter,
    SimpleVoter2D,
    SimpleAdvancedVoter2D,
    AdvancedVoter2D
    
)
from voting_systems import (
    PluralityVotingSystem,
    CondorcetVotingSystem,
    ApprovalVotingSystem,
    InstantRunoffVotingSystem,
    ScoringVotingSystem,
)
from graphPlotter import (
    plot_approvals_2D,
    plot_scores_2D,
    plot_results_per_rounds_2D,
    plot_results_2D,
    print_percantage_results,  # (ano, v původním kódu je překlep)
)
from citizensGenerators import ClusteredVoterGenerator, Uniform2DVoterGenerator, UniformGenerator
from citizensGenerators.CZVotersCandidates import candidates, clusters_v2


class VotingSimulatorGUI(tk.Tk): 
    def __init__(self):
        super().__init__()
        self.title("Voting Simulator – GUI")
        self.geometry("1500x900")

        # --- Stav / výchozí hodnoty ---
        self.voting_system_map = {
            "Plurality": PluralityVotingSystem,
            "Condorcet": CondorcetVotingSystem,
            "Approval": ApprovalVotingSystem,
            "Instant Runoff (IRV)": InstantRunoffVotingSystem,
            "Scoring": ScoringVotingSystem,
        }
        self.voter_model_map = {
            # "SimpleVoter": SimpleVoter,
            # "SimpleAdvancedVoter": SimpleAdvancedVoter,
            "SimpleVoter2D": SimpleVoter2D,
            "SimpleAdvancedVoter2D": SimpleAdvancedVoter2D,
            "AdvancedVoter2D": AdvancedVoter2D,
            # "AdvancedVoterND": AdvancedVoterND,
            # "AdvancedVoterNDBool": AdvancedVoterNDBool,
        }

        self.voters_generator_map: dict[str, UniformGenerator] = {
            "UniformGenerator": Uniform2DVoterGenerator,
            "ClustersGenerator": ClusteredVoterGenerator
        }

        self.var_voting_system = tk.StringVar(value="Plurality")
        self.var_voter_model = tk.StringVar(value="AdvancedVoter2D")
        self.var_voters_generator = tk.StringVar(value="ClustersGenerator")
        self.var_num_voters = tk.IntVar(value=1500)
        self.var_left_bound = tk.DoubleVar(value=-15.0)
        self.var_right_bound = tk.DoubleVar(value=15.0)

        # Approval
        self.var_approval_distance = tk.DoubleVar(value=3.0)

        # Scoring
        self.var_max_score = tk.IntVar(value=3)
        self.var_score_limits = tk.StringVar(value="1,3")

        # ND / otázky
        self.var_size_of_questions = tk.StringVar(value="")  # prázdné = nepoužít

        # IRV
        self._irv_figs = []
        self._irv_round_idx = 0

        # --- UI rozvržení ---
        self._build_controls()
        self._build_output()
        self._build_plot_canvas()

    def _build_controls(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(frm, text="Volební systém").grid(row=0, column=0, sticky="w")
        ttk.Combobox(
            frm, textvariable=self.var_voting_system, values=list(self.voting_system_map.keys()), state="readonly", width=28
        ).grid(row=1, column=0, sticky="we", pady=(0, 8))

        ttk.Label(frm, text="Model voliče").grid(row=2, column=0, sticky="w")
        ttk.Combobox(
            frm, textvariable=self.var_voter_model, values=list(self.voter_model_map.keys()), state="readonly", width=28
        ).grid(row=3, column=0, sticky="we", pady=(0, 8))

        ttk.Label(frm, text="Generátor voličů").grid(row=4, column=0, sticky="w")
        ttk.Combobox(
            frm, textvariable=self.var_voters_generator, values=list(self.voters_generator_map.keys()), state="readonly", width=28
        ).grid(row=5, column=0, sticky="we", pady=(0, 8))

        sep1 = ttk.Separator(frm, orient="horizontal")
        sep1.grid(row=6, column=0, sticky="we", pady=6)

        # Základní parametry
        ttk.Label(frm, text="Počet voličů").grid(row=7, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.var_num_voters).grid(row=8, column=0, sticky="we", pady=(0, 6))

        ttk.Label(frm, text="Levý / pravý limit (generátor)").grid(row=9, column=0, sticky="w")
        lrp = ttk.Frame(frm)
        lrp.grid(row=10, column=0, sticky="we", pady=(0, 6))
        ttk.Entry(lrp, width=8, textvariable=self.var_left_bound).pack(side=tk.LEFT)
        ttk.Label(lrp, text=" až ").pack(side=tk.LEFT, padx=4)
        ttk.Entry(lrp, width=8, textvariable=self.var_right_bound).pack(side=tk.LEFT)

        ttk.Label(frm, text="size_of_questions (ND/NDBool) – volitelné").grid(row=11, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.var_size_of_questions).grid(row=12, column=0, sticky="we", pady=(0, 6))

        sep2 = ttk.Separator(frm, orient="horizontal")
        sep2.grid(row=13, column=0, sticky="we", pady=6)

        # Approval parametry
        lab_approval = ttk.LabelFrame(frm, text="Approval nastavení")
        lab_approval.grid(row=14, column=0, sticky="we", pady=(0, 6))
        ttk.Label(lab_approval, text="approval_distance").pack(anchor="w")
        ttk.Entry(lab_approval, textvariable=self.var_approval_distance).pack(fill="x")

        # Scoring parametry
        lab_scoring = ttk.LabelFrame(frm, text="Scoring nastavení")
        lab_scoring.grid(row=15, column=0, sticky="we", pady=(0, 6))
        rowf = ttk.Frame(lab_scoring)
        rowf.pack(fill="x")
        ttk.Label(rowf, text="max_score").pack(side=tk.LEFT)
        ttk.Entry(rowf, width=6, textvariable=self.var_max_score).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Label(lab_scoring, text="score_limits (např. 1,3)").pack(anchor="w", pady=(6, 0))
        ttk.Entry(lab_scoring, textvariable=self.var_score_limits).pack(fill="x")

        sep3 = ttk.Separator(frm, orient="horizontal")
        sep3.grid(row=16, column=0, sticky="we", pady=6)

        btn = ttk.Button(frm, text="Spustit simulaci", command=self.run_simulation)
        btn.grid(row=17, column=0, sticky="we", pady=(4, 0))

        frm.grid_columnconfigure(0, weight=1)

    def _on_container_resize(self, event):
        """Resize callback vázaný na <Configure> plot_containeru."""
        fig = getattr(self.canvas, "figure", None)
        if fig is None:
            return
        dpi = fig.get_dpi()
        w_in = max(event.width  / dpi, 1)
        h_in = max(event.height / dpi, 1)
        fig.set_size_inches(w_in, h_in, forward=True)
        self.canvas.draw_idle()

    def _build_output(self):
        right = ttk.Frame(self, padding=(0, 10, 10, 10))
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.output = ScrolledText(right, height=10)
        self.output.pack(side=tk.BOTTOM, fill=tk.X)

        self.plot_container = ttk.Frame(right)
        self.plot_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.plot_container.update_idletasks()

    def _build_plot_canvas(self):
        # Předpřipravený Matplotlib canvas (pokud plot funkce vrací figuru, použijeme ji)
        self.figure = plt.figure(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_container)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # pod plátnem panel s ovládáním kol IRV
        self.irv_controls = ttk.Frame(self.plot_container)
        self.irv_controls.pack(side=tk.BOTTOM, fill=tk.X)

        self.irv_round_label = ttk.Label(self.irv_controls, text="Round -/-")
        self.irv_round_label.pack(side=tk.LEFT, padx=(6, 0))

        self.irv_next_btn = ttk.Button(self.irv_controls, text="Next round", command=self._on_irv_next)
        self.irv_next_btn.pack(side=tk.RIGHT, padx=6, pady=4)

        # hned po inicializaci – až se GUI srovná do layoutu
        self.after(0, lambda: self._fit_canvas_to_container())
        # a dál necháme běžet i automatický resize
        self.plot_container.bind("<Configure>", self._on_container_resize)

        # defaultně skryj (zobrazí se jen u IRV)
        self._set_irv_controls_visible(False)

    def _set_irv_controls_visible(self, visible: bool):
        state = "normal" if visible else "disabled"
        self.irv_next_btn.configure(state=state)
        # label necháme viditelný jen když je IRV aktivní
        self.irv_round_label.configure(text="Round -/-")
        if visible:
            self.irv_controls.pack_configure(side=tk.BOTTOM, fill=tk.X)
        else:
            # deaktivace tlačítka stačí; kdybys to chtěl fakt schovat:
            # self.irv_controls.pack_forget()
            pass

    def _show_irv_round(self, idx: int):
        if not self._irv_figs:
            return
        idx = max(0, min(idx, len(self._irv_figs) - 1))
        self._irv_round_idx = idx
        fig = self._irv_figs[idx]

        # přepoj figuru do canvasu
        self.canvas.figure = fig
        self._fit_canvas_to_container(fig)
        try:
            fig.set_constrained_layout(True)
        except Exception:
            pass

        # přepočti velikost na aktuální panel
        w = self.plot_container.winfo_width()
        h = self.plot_container.winfo_height()
        if w > 1 and h > 1:
            dpi = fig.get_dpi()
            fig.set_size_inches(max(w/dpi, 1), max(h/dpi, 1), forward=True)

        self.canvas.draw_idle()

        # aktualizuj popisek + stav tlačítka
        self.irv_round_label.configure(text=f"Round {idx+1}/{len(self._irv_figs)}")
        if idx >= len(self._irv_figs) - 1:
            self.irv_next_btn.configure(state="disabled")
        else:
            self.irv_next_btn.configure(state="normal")

    def _on_irv_next(self):
        self._show_irv_round(self._irv_round_idx + 1)

    def _fit_canvas_to_container(self, fig=None):
        fig = fig or self.canvas.figure
        if fig is None:
            return
        # zajisti, že máme aktuální rozměry
        self.update_idletasks()
        w = self.plot_container.winfo_width()
        h = self.plot_container.winfo_height()
        if w <= 1 or h <= 1:
            return
        dpi = fig.get_dpi()
        fig.set_size_inches(max(w/dpi, 1), max(h/dpi, 1), forward=True)
        try:
            fig.set_constrained_layout(True)
        except Exception:
            pass
        self.canvas.draw_idle()


    def log(self, text: str):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.update_idletasks()

    def run_simulation(self):
        self.output.delete("1.0", tk.END)
        # Vymazat předchozí plátno
        self.figure.clf()
        self.canvas.draw()

        try:
            # Parametry z UI
            voting_system_cls = self.voting_system_map[self.var_voting_system.get()]
            voter_model_cls = self.voter_model_map[self.var_voter_model.get()]
            num_voters = int(self.var_num_voters.get())
            left = float(self.var_left_bound.get())
            right = float(self.var_right_bound.get())

            # Volitelné size_of_questions
            size_of_questions_str = self.var_size_of_questions.get().strip()
            size_of_questions = None
            if size_of_questions_str:
                size_of_questions = int(size_of_questions_str)

            # Volby pro daný systém
            options = {}
            if voting_system_cls is ApprovalVotingSystem:
                options["approval_distance"] = float(self.var_approval_distance.get())
            elif voting_system_cls is ScoringVotingSystem:
                max_score = int(self.var_max_score.get())
                options["max_score"] = max_score
                limits = [int(x) for x in self.var_score_limits.get().split(",")]
                if len(limits) != max_score - 1:
                    raise ValueError("score_limits musí být max_score - 1 čísel oddělených čárkou, např. 1,3")
                options["score_limits"] = limits

            # Generace voličů
            generator_class = self.voters_generator_map[self.var_voters_generator.get()]
            generator = Uniform2DVoterGenerator(left, right)
            if generator_class is ClusteredVoterGenerator:
                generator = ClusteredVoterGenerator(left, right, clusters=clusters_v2)

            if size_of_questions is not None:
                voters = generator.generate(num_voters, voter_model_cls, size_of_questions=size_of_questions)
            else:
                voters = generator.generate(num_voters, voter_model_cls)

            avg = sum([sum(getattr(v, "political_affiliation", [])) for v in voters]) / max(1, len(voters))
            self.log(f"Průměrné skóre odpovědí voličů: {avg:.3f}")

            # Simulace
            candidates_copy = candidates[:]
            sim = Simulator(voting_system_cls, voters, candidates_copy, options=options)
            results, winner = sim.run()

            # Textové shrnutí
            self.log(f"Volební systém: {self.var_voting_system.get()}")
            self.log(f"Model voliče: {self.var_voter_model.get()}")
            self.log(f"Počet voličů: {num_voters}")
            self.log(f"Vítěz: {getattr(winner, 'name', str(winner))}")

            # Rozhodnutí o vizualizaci
            if voter_model_cls in (AdvancedVoterND, AdvancedVoterNDBool):
                self.log("Použit ND/NDBool model – graf se neplotuje (nelze 2D).")
                if voting_system_cls is PluralityVotingSystem:
                    # Tisk procent do textového pole (funkce jinak tiskne na stdout)
                    self.log("Procenta (Plurality):")
                    try:
                        # Zachycení výpisu print_percantage_results do stringu
                        import io, contextlib
                        buf = io.StringIO()
                        with contextlib.redirect_stdout(buf):
                            print_percantage_results(results)
                        self.log(buf.getvalue().strip())
                    except Exception as e:
                        self.log(f"Chyba při tisku procent: {e}")
                return

            # 2D grafy – použijeme tvé plot funkce
            fig_before = plt.gcf()

            if voting_system_cls is ApprovalVotingSystem:
                fig = plot_approvals_2D(voters, candidates, results, winner, sim.voting_system.approval_distance)
                self.log(ApprovalVotingSystem.str_results(results))

            elif voting_system_cls is ScoringVotingSystem:
                fig = plot_scores_2D(
                    voters, candidates, results, winner, sim.voting_system.score_limits
                )
                self.log(ScoringVotingSystem.str_results(results))
                
            elif voting_system_cls is InstantRunoffVotingSystem:
                figs = plot_results_per_rounds_2D(voters, candidates, results, winner)
                self._irv_figs = figs or []
                if self._irv_figs:
                    self._set_irv_controls_visible(True)
                    self._show_irv_round(0)   # zobraz 1. kolo
                else:
                    self._set_irv_controls_visible(False)
                    self.log("IRV: Nebyla vrácena žádná figura pro kola.")

                if figs:
                    # zobraz první kolo do panelu
                    self.canvas.figure = figs[0]
                    self.canvas.draw()
                    # volitelně si ulož pro přepínání kol
                    self._irv_figs = figs

            elif voting_system_cls is PluralityVotingSystem:
                # Procenta do textu
                try:
                    import io, contextlib
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        print_percantage_results(results)
                    self.log(buf.getvalue().strip())
                except Exception as e:
                    self.log(f"Chyba při tisku procent: {e}")

                fig = plot_results_2D(voters, candidates, results, winner)
            elif voting_system_cls is CondorcetVotingSystem:
                self.log(CondorcetVotingSystem.str_results(results))
                self.canvas.figure.clf()
                self.canvas.draw_idle()
                # Shrink/hide canvas
                self.canvas_widget.pack_forget()
                # Let log window expand
                self.output.pack_forget()
                self.output.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            else:
                # Condorcet – žádná speciální 2D funkce, ale můžeš si doplnit vlastní vizualizaci.
                self.log("Neznámá vizualizace.")

            # Pokud tvoje plot funkce již otevřela okno (plt.show()), respektujeme to.
            # Zkusíme ale ještě embednout aktuální figuru do canvasu okna:
            try:
                # fig = plt.gcf()
                # self._set_irv_controls_visible(False)
                if (fig is not fig_before or len(fig.axes) > 0) and fig is not None:
                    self.figure.clf()
                    # Překreslit figuru do našeho canvasu:
                    # Pozn.: nejjednodušší je vykreslit přímo figuru, ale zde to uděláme "přepnutím" aktivní figury
                    # a překreslením canvasu. Pokud se ti to nebude líbit, nech ploty jen ve vlastním okně.
                    self.canvas.figure = fig 
                    self._fit_canvas_to_container(fig)
                    self.canvas.draw()  # aby byl prázdný canvas připraven
                    self.output.pack_forget()
                    self.output.pack(side=tk.BOTTOM, fill=tk.X)   # menší výška
                    self.canvas_widget.pack(fill=tk.BOTH, expand=True)
                    # Nic víc tu dělat nemusíme – tvoje plot funkce obvykle volají plt.show().
                else:
                    # Kdyby žádná osa nebyla, nedá se embednout – nic neděláme.
                    pass
            except Exception as e:
                self.log(f"Embed plátna selhal: {e}")

        except Exception as e:
            messagebox.showerror("Chyba", f"Simulace selhala: {e}")
            self.log(f"Chyba: {e}")
            self.canvas.figure.clf()
            self.canvas.draw_idle()


if __name__ == "__main__":
    app = VotingSimulatorGUI()
    app.mainloop()
