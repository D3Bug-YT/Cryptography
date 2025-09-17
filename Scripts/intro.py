from manim import *
import numpy as np
from manim import rate_functions as rf

class test(Scene):
    def construct(self):
        # --- Box ---
        box = RoundedRectangle(
            corner_radius=0.3,
            height=4,
            width=6,
            color=WHITE,
            fill_color=GRAY,
            fill_opacity=0.2,
            stroke_width=2
        )
        self.play(Create(box))

        # --- Title at top of box ---
        title = Text("Cryptography", weight=BOLD).scale(0.9)
        title.next_to(box.get_top(), DOWN, buff=0.3)
        self.play(Write(title))

        # --- Line under title ---
        underline = Line(
            box.get_left(), box.get_right()
        ).next_to(title, DOWN, buff=0.1)
        self.play(Create(underline))

        # --- Three labels stacked inside ---
        t_sym  = Text("Symmetric Key Encryption").scale(0.6).set_color(GREEN_C)
        t_asym = Text("Asymmetric Key Encryption").scale(0.6).set_color(BLUE_C)
        t_hash = Text("Hashing").scale(0.6).set_color(YELLOW_C)

        labels = VGroup(t_sym, t_asym, t_hash).arrange(DOWN, buff=0.4)
        labels.next_to(underline, DOWN, buff=0.5)

        self.wait(10)

        self.play(Write(t_sym), run_time=0.6)
        self.wait(2)
        self.play(Write(t_asym), run_time=0.6)
        self.wait(2)
        self.play(Write(t_hash), run_time=0.6)

        self.wait(10)


        self.play(Indicate(t_sym, color=GREEN_E, scale_factor=1.15, run_time=1), Indicate(t_asym, color=BLUE_E, scale_factor=1.15, run_time=1))

        self.wait(10)

        self.play(Indicate(t_hash, color=YELLOW_E, scale_factor=1.15, run_time=1))

        self.wait(5)

        others = VGroup(box, title, underline, t_sym, t_asym)
        self.play(FadeOut(others, shift=DOWN*0.2), run_time=0.6)

        self.play(
            t_hash.animate
                .scale(1.4)      # make it title-sized
                .to_edge(UP),    # move to the top
            run_time=1.5,
            rate_func=rf.ease_in_out_cubic
        )

        self.wait(5)
