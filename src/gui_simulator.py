#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt

# --- Your imports (keep module names the same) ---
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
    print_percantage_results,  # (yes, there is a typo in the original code)
)
from citizensGenerators import ClusteredVoterGenerator, Uniform2DVoterGenerator, UniformGenerator
from citizensGenerators.CZVotersCandidates import candidates, clusters_v2


class VotingSimulatorGUI(tk.Tk): 
    def __init__(self):
        super().__init__()
        self.title("Voting Simulator – GUI")
        self.geometry("1500x900") 

        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- State / Default Values ---
        self.voting_system_map = {
            "Plurality": PluralityVotingSystem,
            "Condorcet": CondorcetVotingSystem,
            "Approval": ApprovalVotingSystem,
            "Instant Runoff (IRV)": InstantRunoffVotingSystem,
            "Scoring": ScoringVotingSystem,
        }
        self.voter_model_map = {
            "SimpleVoter2D": SimpleVoter2D,
            "SimpleAdvancedVoter2D": SimpleAdvancedVoter2D,
            "AdvancedVoter2D": AdvancedVoter2D,
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

        # ND / Questions
        self.var_size_of_questions = tk.StringVar(value="")  # empty = do not use

        # IRV
        self._irv_figs = []
        self._irv_round_idx = 0

        # --- UI Layout ---
        self._build_controls()
        self._build_output()
        self._build_plot_canvas()

    def _build_controls(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(frm, text="Voting System").grid(row=0, column=0, sticky="w")
        ttk.Combobox(
            frm, textvariable=self.var_voting_system, values=list(self.voting_system_map.keys()), state="readonly", width=28
        ).grid(row=1, column=0, sticky="we", pady=(0, 8))

        ttk.Label(frm, text="Voter Model").grid(row=2, column=0, sticky="w")
        ttk.Combobox(
            frm, textvariable=self.var_voter_model, values=list(self.voter_model_map.keys()), state="readonly", width=28
        ).grid(row=3, column=0, sticky="we", pady=(0, 8))

        ttk.Label(frm, text="Voter Generator").grid(row=4, column=0, sticky="w")
        ttk.Combobox(
            frm, textvariable=self.var_voters_generator, values=list(self.voters_generator_map.keys()), state="readonly", width=28
        ).grid(row=5, column=0, sticky="we", pady=(0, 8))

        sep1 = ttk.Separator(frm, orient="horizontal")
        sep1.grid(row=6, column=0, sticky="we", pady=6)

        # Basic Parameters
        ttk.Label(frm, text="Number of Voters").grid(row=7, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.var_num_voters).grid(row=8, column=0, sticky="we", pady=(0, 6))

        ttk.Label(frm, text="Left / Right Bound (Generator)").grid(row=9, column=0, sticky="w")
        lrp = ttk.Frame(frm)
        lrp.grid(row=10, column=0, sticky="we", pady=(0, 6))
        ttk.Entry(lrp, width=8, textvariable=self.var_left_bound).pack(side=tk.LEFT)
        ttk.Label(lrp, text=" to ").pack(side=tk.LEFT, padx=4)
        ttk.Entry(lrp, width=8, textvariable=self.var_right_bound).pack(side=tk.LEFT)

        ttk.Label(frm, text="size_of_questions (ND/NDBool) – optional").grid(row=11, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.var_size_of_questions).grid(row=12, column=0, sticky="we", pady=(0, 6))

        sep2 = ttk.Separator(frm, orient="horizontal")
        sep2.grid(row=13, column=0, sticky="we", pady=6)

        # Approval settings
        lab_approval = ttk.LabelFrame(frm, text="Approval Settings")
        lab_approval.grid(row=14, column=0, sticky="we", pady=(0, 6))
        ttk.Label(lab_approval, text="approval_distance").pack(anchor="w")
        ttk.Entry(lab_approval, textvariable=self.var_approval_distance).pack(fill="x")

        # Scoring settings
        lab_scoring = ttk.LabelFrame(frm, text="Scoring Settings")
        lab_scoring.grid(row=15, column=0, sticky="we", pady=(0, 6))
        rowf = ttk.Frame(lab_scoring)
        rowf.pack(fill="x")
        ttk.Label(rowf, text="max_score").pack(side=tk.LEFT)
        ttk.Entry(rowf, width=6, textvariable=self.var_max_score).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Label(lab_scoring, text="score_limits (e.g. 1,3)").pack(anchor="w", pady=(6, 0))
        ttk.Entry(lab_scoring, textvariable=self.var_score_limits).pack(fill="x")

        sep3 = ttk.Separator(frm, orient="horizontal")
        sep3.grid(row=16, column=0, sticky="we", pady=6)

        btn = ttk.Button(frm, text="Run Simulation", command=self.run_simulation)
        btn.grid(row=17, column=0, sticky="we", pady=(4, 0))

        frm.grid_columnconfigure(0, weight=1)

    def _on_container_resize(self, event):
        """Resize callback tied to the <Configure> event of the plot_container."""
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
        self.output.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

        self.plot_container = ttk.Frame(right)
        self.plot_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.plot_container.update_idletasks()

    def _build_plot_canvas(self):
        self.figure = plt.figure(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_container)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # IRV round control panel
        self.irv_controls = ttk.Frame(self.plot_container)
        self.irv_controls.pack(side=tk.BOTTOM, fill=tk.X)

        self.irv_round_label = ttk.Label(self.irv_controls, text="Round -/-")
        self.irv_round_label.pack(side=tk.LEFT, padx=(6, 0))

        self.irv_next_btn = ttk.Button(self.irv_controls, text="Next round", command=self._on_irv_next)
        self.irv_next_btn.pack(side=tk.RIGHT, padx=6, pady=4)

        self.after(0, lambda: self._fit_canvas_to_container())
        self.plot_container.bind("<Configure>", self._on_container_resize)

        self._set_irv_controls_visible(False)

    def _set_irv_controls_visible(self, visible: bool):
        state = "normal" if visible else "disabled"
        self.irv_next_btn.configure(state=state)
        self.irv_round_label.configure(text="Round -/-")
        if visible:
            self.irv_controls.pack_configure(side=tk.BOTTOM, fill=tk.X)

    def _show_irv_round(self, idx: int):
        if not self._irv_figs:
            return
        idx = max(0, min(idx, len(self._irv_figs) - 1))
        self._irv_round_idx = idx
        fig = self._irv_figs[idx]

        self.canvas.figure = fig
        self._fit_canvas_to_container(fig)
        try:
            fig.set_constrained_layout(True)
        except Exception:
            pass

        w = self.plot_container.winfo_width()
        h = self.plot_container.winfo_height() - 40 # reserve space for axes labels
        if w > 1 and h > 1:
            dpi = fig.get_dpi()
            fig.set_size_inches(max(w/dpi, 1), max(h/dpi, 1), forward=True)

        self.canvas.draw_idle()

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
        self.update_idletasks()
        w = self.plot_container.winfo_width()
        h = self.plot_container.winfo_height() - 40 # reserve space for axes labels
        if w <= 1 or h <= 1:
            return
        dpi = fig.get_dpi()
        fig.set_size_inches(max(w/dpi, 1), max(h/dpi, 1), forward=True)
        try:
            fig.set_constrained_layout(True)
        except Exception:
            pass
        self.canvas.draw_idle()

    def on_closing(self):
        """Kills the simulation and closes the application completely."""
        plt.close('all')      
        self.quit()           
        self.destroy()        
        sys.exit(0)           

    def log(self, text: str):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.update_idletasks()

    def run_simulation(self):
        self.output.delete("1.0", tk.END)
        self.figure.clf()
        self.canvas.draw()

        try:
            voting_system_cls = self.voting_system_map[self.var_voting_system.get()]
            voter_model_cls = self.voter_model_map[self.var_voter_model.get()]
            num_voters = int(self.var_num_voters.get())
            left = float(self.var_left_bound.get())
            right = float(self.var_right_bound.get())

            size_of_questions_str = self.var_size_of_questions.get().strip()
            size_of_questions = None
            if size_of_questions_str:
                size_of_questions = int(size_of_questions_str)

            options = {}
            if voting_system_cls is ApprovalVotingSystem:
                options["approval_distance"] = float(self.var_approval_distance.get())
            elif voting_system_cls is ScoringVotingSystem:
                max_score = int(self.var_max_score.get())
                options["max_score"] = max_score
                limits = [int(x) for x in self.var_score_limits.get().split(",")]
                if len(limits) != max_score - 1:
                    raise ValueError(f"score_limits must be {max_score - 1} numbers separated by commas, e.g. 1,3")
                options["score_limits"] = limits

            # Voter generation
            generator_class = self.voters_generator_map[self.var_voters_generator.get()]
            generator = Uniform2DVoterGenerator(left, right)
            if generator_class is ClusteredVoterGenerator:
                generator = ClusteredVoterGenerator(left, right, clusters=clusters_v2)

            if size_of_questions is not None:
                voters = generator.generate(num_voters, voter_model_cls, size_of_questions=size_of_questions)
            else:
                voters = generator.generate(num_voters, voter_model_cls)

            avg = sum([sum(getattr(v, "political_affiliation", [])) for v in voters]) / max(1, len(voters))
            self.log(f"Average voter response score: {avg:.3f}")

            # Simulation
            candidates_copy = candidates[:]
            sim = Simulator(voting_system_cls, voters, candidates_copy, options=options)
            results, winner = sim.run()

            # Text summary
            self.log(f"Voting System: {self.var_voting_system.get()}")
            self.log(f"Voter Model: {self.var_voter_model.get()}")
            self.log(f"Voter Count: {num_voters}")
            self.log(f"Winner: {getattr(winner, 'name', str(winner))}")

            # Visualization decision
            if voter_model_cls in (AdvancedVoterND, AdvancedVoterNDBool):
                self.log("ND/NDBool model used – graph cannot be plotted (not 2D).")
                if voting_system_cls is PluralityVotingSystem:
                    self.log("Percentages (Plurality):")
                    try:
                        import io, contextlib
                        buf = io.StringIO()
                        with contextlib.redirect_stdout(buf):
                            print_percantage_results(results)
                        self.log(buf.getvalue().strip())
                    except Exception as e:
                        self.log(f"Error printing percentages: {e}")
                return

            fig_before = plt.gcf()

            if voting_system_cls is ApprovalVotingSystem:
                fig = plot_approvals_2D(voters, candidates, results, winner, sim.voting_system.approval_distance)
                self.log(ApprovalVotingSystem.str_results(results))

            elif voting_system_cls is ScoringVotingSystem:
                fig = plot_scores_2D(voters, candidates, results, winner, sim.voting_system.score_limits)
                self.log(ScoringVotingSystem.str_results(results))
                
            elif voting_system_cls is InstantRunoffVotingSystem:
                figs = plot_results_per_rounds_2D(voters, candidates, results, winner)
                self._irv_figs = figs or []
                if self._irv_figs:
                    self._set_irv_controls_visible(True)
                    self._show_irv_round(0)   
                else:
                    self._set_irv_controls_visible(False)
                    self.log("IRV: No figures were returned for rounds.")

                if figs:
                    self.canvas.figure = figs[0]
                    self.canvas.draw()

            elif voting_system_cls is PluralityVotingSystem:
                try:
                    import io, contextlib
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        print_percantage_results(results)
                    self.log(buf.getvalue().strip())
                except Exception as e:
                    self.log(f"Error printing percentages: {e}")

                fig = plot_results_2D(voters, candidates, results, winner)
            elif voting_system_cls is CondorcetVotingSystem:
                self.log(CondorcetVotingSystem.str_results(results))
                self.canvas.figure.clf()
                self.canvas.draw_idle()
                self.canvas_widget.pack_forget()
                self.output.pack_forget()
                self.output.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            else:
                self.log("Unknown visualization.")

            try:
                if (fig is not fig_before or len(fig.axes) > 0) and fig is not None:
                    self.figure.clf()
                    self.canvas.figure = fig 
                    self._fit_canvas_to_container(fig)
                    self.canvas.draw()  
                    self.output.pack_forget()
                    self.output.pack(side=tk.BOTTOM, fill=tk.X)
                    self.canvas_widget.pack(fill=tk.BOTH, expand=True)
            except Exception as e:
                self.log(f"Canvas embedding failed: {e}")

        except Exception as e:
            messagebox.showerror("Error", f"Simulation failed: {e}")
            self.log(f"Error: {e}")
            self.canvas.figure.clf()
            self.canvas.draw_idle()


if __name__ == "__main__":
    print("Starting GUI simulator...")
    app = VotingSimulatorGUI()
    app.mainloop()