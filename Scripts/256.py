from manim import *
from manim import rate_functions as rf


CHUNK = 16

def make_hash_block(hex_str: str, chunk: int = CHUNK, scale: float = 0.9) -> Mobject:
    chunks = [hex_str[i:i+chunk] for i in range(0, len(hex_str), chunk)]
    stack_tex = r"\shortstack[l]{" + r"\\ ".join([rf"\texttt{{{c}}}" for c in chunks]) + "}"
    return Tex(stack_tex).scale(scale)

def build_row(y: float, left_input_mobj: Mobject, digest_hex: str,
              chunk: int = CHUNK, scale: float = 0.9):
    func      = Tex(r"\text{HashAlgorithm}", arg_separator="").scale(0.9)
    lpar      = Tex(r"\big(").scale(0.9)
    rpar      = Tex(r"\big)").scale(0.9)
    eq        = Tex("=").scale(0.9)
    right_blk = make_hash_block(digest_hex, chunk=chunk, scale=scale)

    # Parenthesis alignment
    if isinstance(left_input_mobj, ImageMobject):
        VGroup(lpar, rpar).match_y(left_input_mobj)
    else:
        VGroup(lpar, rpar).match_y(left_input_mobj)

    left_group = Group(func, lpar, left_input_mobj, rpar).arrange(RIGHT, buff=0.05, aligned_edge=ORIGIN)
    row = Group(left_group, eq, right_blk).arrange(RIGHT, buff=0.35)

    # Anchor ‘=’ at x=0 and place row so '=' is at y
    row.shift(RIGHT * (0 - eq.get_center()[0]))
    row.shift(UP * (y - eq.get_center()[1]))

    return row, (func, left_input_mobj, lpar, rpar, eq, right_blk)



class HashingDemo(Scene):
    def construct(self):
        t_hash = Text("Hashing").scale(0.84).set_color(YELLOW_C)
        t_hash.to_edge(UP)
        self.add(t_hash)
        self.wait(5)


        infinity = MathTex(r"\infty").set_color(WHITE).scale(2)
        noteq    = MathTex(r">").scale(2)
        two256   = MathTex(r"2^{256}").set_color(WHITE).scale(2)

        grp = VGroup(infinity, noteq, two256).arrange(RIGHT, buff=0.6).move_to(ORIGIN)


        # new
        grp.next_to(t_hash, DOWN, buff=1)
        dx = t_hash.get_center()[0] - noteq.get_center()[0]
        grp.shift(dx * RIGHT)




        br_in  = Brace(infinity, direction=DOWN, buff=0.15)
        lbl_in = Text("Inputs", weight=MEDIUM).scale(0.5).next_to(br_in, DOWN, buff=0.1).set_color(WHITE)

        br_out  = Brace(two256, direction=UP, buff=0.15)
        lbl_out = Text("Outputs", weight=MEDIUM).scale(0.5).next_to(br_out, UP, buff=0.1).set_color(WHITE)


        self.play(Write(infinity), run_time=0.5)
        self.play(FadeIn(br_in), Write(lbl_in), run_time=0.5)
        self.wait(5)
        self.play(Write(noteq), run_time=0.5)
        self.play(Write(two256), run_time=0.5)
        self.play(FadeIn(br_out), Write(lbl_out), run_time=0.5)
        self.wait(10)

        left_alt = MathTex(r"2^{2^{64}-1}").set_color(WHITE)
        left_alt.match_height(infinity)  # ensure same visual size as the ∞ you already drew



        # Reuse copies of the '>' and 2^{256} so scale/style match perfectly
        gt_alt    = noteq.copy()
        two256_alt = two256.copy()

        # Arrange and place directly under the existing ∞ > 2^{256}
        eq_anchor = VGroup(infinity, noteq, two256)
        eq2 = VGroup(left_alt, gt_alt, two256_alt).arrange(RIGHT, buff=0.6)
        eq2.next_to(eq_anchor, DOWN, buff=0.75)
        eq2.set_x(eq_anchor.get_center()[0])  # center under the first equation

        # Animate the new line
        self.play(Write(left_alt), Write(gt_alt), Write(two256_alt), run_time=0.8)

        self.wait(10)

        new_eq = VGroup(left_alt, gt_alt, two256_alt)




        content = VGroup(infinity, noteq, two256, br_in, lbl_in, br_out, lbl_out)

        content.generate_target()
        content.target.scale(0.5)
        content.target.next_to(t_hash, DOWN, buff=0.3)

        # Find the target-position of the '>' inside the target group
        idx = content.submobjects.index(noteq)                 # same order in target
        noteq_target = content.target.submobjects[idx]
        dx = t_hash.get_center()[0] - noteq_target.get_center()[0]
        content.target.shift(dx * RIGHT)

        self.play(
            MoveToTarget(content),
            FadeOut(new_eq, shift=0.05*DOWN),
            run_time=0.8,
        )

        '''
        self.play(
            content.animate.scale(0.5).next_to(t_hash, DOWN, buff=0.3).set_x(t_hash.get_center()[0]),
            FadeOut(new_eq, shift=DOWN*0.05),
            run_time=0.8,
        )
        '''

        self.wait(5)

        input1 = Tex(r"\texttt{Input1}", arg_separator="").scale(0.9).set_color(YELLOW_C)
        input2 = Tex(r"\texttt{Input2}", arg_separator="").scale(0.9).set_color(YELLOW_C)
        w, h = config.frame_width, config.frame_height
        y_text  =  h/2 - h/3 - 1
        y_image =  h/2 - 2*h/3 - 1


        row1, (r1_func, r1_in, r1_lpar, r1_rpar, r1_eq, r1_out) = build_row(
            y_text,
            input1,
            "1ea06586b18e8fce1b923eff26fd8252f617f0efd4e49820e8e9bee0614e5792"
        )

        row2, (r2_func, r2_in, r2_lpar, r2_rpar, r2_eq, r2_out) = build_row(
            y_image,
            input2,
            "1ea06586b18e8fce1b923eff26fd8252f617f0efd4e49820e8e9bee0614e5792"
        )

        self.play(Write(r1_func), Write(r1_lpar), Write(r1_in), Write(r1_rpar), Write(r1_eq))
        self.play(Write(r1_out))

        self.play(Write(r2_func), Write(r2_lpar), Write(r2_in), Write(r2_rpar), Write(r2_eq))
        self.play(Write(r2_out))

        self.wait(5)


        lhs_bits_r1 = VGroup(r1_func, r1_lpar, r1_rpar)
        lhs_bits_r2 = VGroup(r2_func, r2_lpar, r2_rpar)
        self.play(
            FadeOut(lhs_bits_r1, shift=DOWN*0.05),
            FadeOut(lhs_bits_r2, shift=DOWN*0.05),
            run_time=0.4
        )

        gap_top_right = r1_out.get_left()[0] - r1_eq.get_right()[0]   # top digest gap (right of '=')
        gap_bot_left  = r2_eq.get_left()[0] - r2_in.get_right()[0]    # bottom input gap (left of '=')

        # 2) build targets on the other row with SAME horizontal gaps
        text2_top_target = r2_in.copy().next_to(r1_eq, RIGHT, buff=gap_top_right)
        hash1_bot_target = r1_out.copy().next_to(r2_eq, LEFT,  buff=gap_bot_left)

        # 3) force EXACT Y to match the current text on each row
        text2_top_target.set_y(r1_in.get_y())   # top row target Y == current top text Y
        hash1_bot_target.set_y(r2_in.get_y())   # bottom row target Y == current bottom text Y

        noteq_r1 = MathTex(r"\neq").scale(0.9).move_to(r1_eq)


        # 4) animate the swap
        self.play(
            Transform(r1_eq, noteq_r1),
            ReplacementTransform(r2_in,  text2_top_target),
            ReplacementTransform(r1_out, hash1_bot_target),
            run_time=0.9, rate_func=rf.ease_in_out_cubic,
            
        )

        # (optional) keep references if used later
        r1_out = text2_top_target
        r2_in  = hash1_bot_target
        r1_eq = noteq_r1

        self.wait(10)

        keep = two256.copy().move_to(two256)
        self.add(keep)             # now 'keep' is a top-level mobject

        # fade EVERYTHING except the standalone copy
        others = Group(*[m for m in self.mobjects if m is not keep])
        self.play(FadeOut(others, shift=DOWN*0.05), run_time=0.6)

        # center + grow the kept copy
        self.play(
            keep.animate.move_to(ORIGIN).scale(2.0),
            run_time=0.9, rate_func=rf.ease_in_out_cubic,
        )
        self.wait(10)

        #self.play(FadeOut(keep, shift=DOWN*0.1), run_time=0.6)

        num1 = Text("115,792,089,237,316,195,423,570,985,008,687,907,853,269,984,665,640,564,039,457,584,007,913,129,639,936").scale(0.4)
        num2 = Text("1,000,000,000,000").scale(0.4)
        num3 = Text("13,407,807,929,942,597,099,574,024,998,205,846,127,479,365,820,592,393,377,723,561,443,721,764,030,073,546,976,801,874,298,166,903,427,690,031,858,186,486,050,853,753,882,811,946,569,946,433,649,006,084,096").scale(0.2)
        num4 = Text("1,000,000,000,000,000,000,000,000").scale(0.4)

        ROW_BUFF = 0.25
        SHIFT_UP = 0.5
        S = 0.5
        stack = VGroup()

        num1.move_to(ORIGIN)
        self.play(ReplacementTransform(keep, num1), run_time=0.8, rate_func=rf.ease_in_out_cubic)
        stack.add(num1)

        self.wait(5)
        self.play(stack.animate.shift(UP * SHIFT_UP), run_time=0.5, rate_func=rf.ease_in_out_cubic)


        num2.next_to(stack, DOWN, buff=ROW_BUFF)
        self.play(Write(num2))
        stack.add(num2)

        self.wait(5)
        self.play(stack.animate.shift(UP * SHIFT_UP), run_time=0.5, rate_func=rf.ease_in_out_cubic)

        num4.next_to(stack, DOWN, buff=ROW_BUFF)
        self.play(Write(num4))
        stack.add(num4)

        self.wait(5)
        self.play(stack.animate.shift(UP * SHIFT_UP), run_time=0.5, rate_func=rf.ease_in_out_cubic)

        self.play(stack.animate.scale(0.5), run_time=0.6)

        num3.next_to(stack, DOWN, buff=ROW_BUFF * S)
        self.play(Write(num3))
        stack.add(num3)


        self.wait(10)

        all = VGroup(*[num1, num2, num3, num4])
        self.play(FadeOut(all, shift=DOWN * 0.1), run_time=0.6)

        self.wait(5)

        






