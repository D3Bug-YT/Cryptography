from manim import *
from manim import rate_functions as rf

class encrypt_intro(Scene):
    def construct(self):
        title = Text(
            "Encryption", 
            t2c={"Encry": BLUE_C, "ption": GREEN_C}
        ).scale(0.84)

        title.to_edge(UP)
        self.play(Write(title), run_time=1.5)

        self.wait(10)



        key_img = ImageMobject("Other_ss/key.png").set(height=0.6).set_color(GREEN_C)
        enc_img = ImageMobject("Other_ss/encrypted-data.png").set(height=0.6).set_color(GREEN_C)
        txt_img = ImageMobject("Other_ss/text-format.png").set(height=0.6).set_color(GREEN_C)

        key_text = Text("Key").scale(0.6).set_color(BLUE_C)
        enc_text = Text("Cipher Text").scale(0.6).set_color(BLUE_C)
        txt_text = Text("Plain Text").scale(0.6).set_color(BLUE_C)

        key_desc = Text("—  A secret/random value that enables encryption/decryption.").scale(0.6)
        enc_desc = Text("—  The scrambled output after encryption.").scale(0.6)
        txt_desc = Text("—  The original, readable data").scale(0.6)

        row1 = Group(key_text, key_img, key_desc).arrange(RIGHT, buff=0.2)
        row2 = Group(txt_text, txt_img, txt_desc).arrange(RIGHT, buff=0.2)
        row3 = Group(enc_text, enc_img, enc_desc).arrange(RIGHT, buff=0.2)

        col = Group(row1, row2, row3).arrange(DOWN, buff=0.5)

        for row in [row1, row2, row3]:
            row.align_to(row1, LEFT)

        col.to_edge(LEFT, buff=1.0)


        self.play(Write(key_text), FadeIn(key_img, shift=RIGHT*0.2), Write(key_desc), run_time=1)
        self.wait(10)
        self.play(Write(txt_text), FadeIn(txt_img, shift=RIGHT*0.2), Write(txt_desc), run_time=1)
        self.wait(10)
        self.play(Write(enc_text), FadeIn(enc_img, shift=RIGHT*0.2), Write(enc_desc), run_time=1)
        self.wait(10)

        self.play(FadeOut(col, shift=DOWN*0.2), run_time=1)

        self.play(Transform(title, Text("Symmetric Key Encryption").scale(0.84).set_color(GREEN_C).to_edge(UP)), run_time=1.5)

        self.wait(10)
        key_img.set_color(WHITE).scale(0.5)
        txt_img.set_color(WHITE).scale(0.5)

        key_text.set_color(WHITE).scale(0.6)
        txt_text.set_color(WHITE).scale(0.6)

        key_pair = Group(key_img, key_text).arrange(RIGHT, buff=0.1, aligned_edge=ORIGIN)
        txt_pair = Group(txt_img, txt_text).arrange(RIGHT, buff=0.1, aligned_edge=ORIGIN)

        top_row = Group(key_pair, txt_pair).arrange(RIGHT, buff=2.5, aligned_edge=ORIGIN)

        top_row.next_to(title, DOWN, buff=0.6)
        top_row.set_x(0)

        self.play(
            FadeIn(key_pair, shift=DOWN*0.15),
            FadeIn(txt_pair, shift=DOWN*0.15),
            run_time=1.0
        )
            

        self.wait(10)




        enc_img.set_color(WHITE).scale(0.5)
        enc_text.set_color(WHITE).scale(0.6)
        enc_group = Group(enc_img, enc_text).arrange(RIGHT, buff=0.1, aligned_edge=ORIGIN)


        func = Tex(r"\text{Encrypt}", arg_separator="").scale(0.9).set_color(GREEN_C)
        lpar = Tex(r"\big(").scale(0.9)
        comma = Tex(r",").scale(0.9)
        space = Rectangle(width=0.25, height=0.001, stroke_width=0, fill_opacity=0)
        rpar = Tex(r"\big)").scale(0.9)
        eq = Tex("=").scale(0.9)

        key_pair_target = key_pair.copy()
        txt_pair_target = txt_pair.copy()


        left_group = Group(func, lpar, key_pair_target, comma, space, txt_pair_target, rpar, eq, enc_group).arrange(RIGHT, buff=0.05, aligned_edge=ORIGIN)
        
        args = Group(key_pair_target, txt_pair_target)
        comma.align_to(args, DOWN) 

        key_pair.generate_target(); key_pair.target.move_to(key_pair_target)
        txt_pair.generate_target(); txt_pair.target.move_to(txt_pair_target)


        self.wait(10)


        self.play(Write(func), Write(lpar), Write(comma), Write(rpar), Write(eq), MoveToTarget(key_pair, path_arc=-TAU/24), MoveToTarget(txt_pair, path_arc= TAU/24), Write(enc_text), FadeIn(enc_img, shift=DOWN*0.2), run_time=0.9)



        self.wait(10)

        encrypt_expr = Group(func, lpar, key_pair, comma, txt_pair, rpar, eq, enc_group)
        self.play(encrypt_expr.animate.shift(UP * 1.2), run_time=0.6)

        self.wait(10)

        func1 = Tex(r"\text{Decrypt}", arg_separator="").scale(0.9).set_color(GREEN_C)
        lpar1 = Tex(r"\big(").scale(0.9)
        comma1 = Tex(r",").scale(0.9)
        space1 = Rectangle(width=0.25, height=0.001, stroke_width=0, fill_opacity=0)
        rpar1 = Tex(r"\big)").scale(0.9)
        eq1 = Tex("=").scale(0.9)

        key_pair_target = key_pair.copy()
        txt_pair_target = txt_pair.copy()
        enc_group_target = enc_group.copy()

        left_group2 = Group(func1, lpar1, key_pair_target, comma1, space1, enc_group_target, rpar1, eq1, txt_pair_target).arrange(RIGHT, buff=0.05, aligned_edge=ORIGIN)

        args = Group(key_pair_target, txt_pair_target)
        comma1.align_to(args, DOWN)

        key_clone = key_pair.copy()
        enc_clone = enc_group.copy()
        txt_clone = txt_pair.copy()
        self.add(key_clone, enc_clone, txt_clone)

        key_clone.generate_target(); key_clone.target.move_to(key_pair_target)
        enc_clone.generate_target(); enc_clone.target.move_to(enc_group_target)
        txt_clone.generate_target(); txt_clone.target.move_to(txt_pair_target)

        self.play(Write(func1), Write(lpar1), Write(comma1), Write(rpar1), Write(eq1), run_time=0.8)
        self.play(
            MoveToTarget(key_clone, path_arc=-TAU/24),
            MoveToTarget(enc_clone, path_arc= TAU/24),
            MoveToTarget(txt_clone, path_arc= TAU/24),
            run_time=0.9
        )

        self.wait(10)

        me = Text("Alice").scale(0.84).set_color(GREEN_C)
        you = Text("Bob").scale(0.84).set_color(GREEN_C)

        names = VGroup(me, you).arrange(RIGHT, buff=5.0, aligned_edge=DOWN)
        names.next_to(title, DOWN, buff=0.6)
        names.set_x(0)


        keep = title

        # fade all other top-level mobjects
        others = Group(*[m for m in self.mobjects if m is not keep])
        self.play(FadeOut(others), run_time=0.8)
        self.wait(2)


        self.play(Write(me), Write(you), run_time=1.0)

        self.wait(10)

        message = Text("Plain Text: Hello").scale(0.5)
        message.next_to(me, DOWN, buff=0.3)

        self.play(Write(message), run_time=1.0)

        self.wait(10)

        key = Text("Key: 123").scale(0.5)
        key.next_to(message, DOWN, buff=0.3)

        self.play(Write(key), run_time=1.0)

        key_slot = Text("123").scale(0.5).set_color(WHITE)
        pt_slot = Text("Hello").scale(0.5).set_color(WHITE)
        enc_slot = Text("Xj3$p").scale(0.5).set_color(WHITE)

        self.wait(10)

        func2 = Tex(r"\text{Encrypt}", arg_separator="").scale(0.6).set_color(GREEN_C)
        lpar2 = Tex(r"\big(").scale(0.5)
        comma2 = Tex(r",").scale(0.5)
        space2 = Rectangle(width=0.1, height=0.001, stroke_width=0, fill_opacity=0)
        rpar2 = Tex(r"\big)").scale(0.5)
        eq2 = Tex("=").scale(0.5)

        eq_small = VGroup(func2, lpar2, key_slot, comma2, space2, pt_slot, rpar2, eq2, enc_slot).arrange(RIGHT, buff=0.06, aligned_edge=ORIGIN)

        eq_small.next_to(key, DOWN, buff=0.25)

        comma2.align_to(VGroup(key_slot, pt_slot), DOWN)

        self.play(
            Write(func2), Write(lpar2), Write(comma2), Write(rpar2), Write(eq2),
            run_time=0.9
        )

        hello_chars  = VGroup(*message[-5:]).copy()
        digits_chars = VGroup(*key[-3:]).copy()
        self.add(hello_chars, digits_chars)

        self.play(
            ReplacementTransform(digits_chars, key_slot),   # 123 → key_slot
            ReplacementTransform(hello_chars, pt_slot),     # Hello → pt_slot
            run_time=0.9
        )

        self.play(Write(enc_slot), run_time=0.9)

        self.wait(10)

        cipher_label = Text("Cipher Text:").scale(0.5).set_color(WHITE)
        ct_slot = Text("Xj3$p").scale(0.5).set_color(WHITE).set_opacity(0)
        row_ct = VGroup(cipher_label, ct_slot).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        row_ct.next_to(you, DOWN, buff=0.3)
        row_ct.set_x(you.get_x())

        self.play(Write(cipher_label), run_time=0.4)

        enc_copy = enc_slot.copy()
        self.add(enc_copy)

        value_target = enc_slot.copy()
        value_target.next_to(cipher_label, RIGHT, buff=0.1).align_to(cipher_label, DOWN)

        enc_copy.generate_target()
        enc_copy.target.move_to(value_target)

        self.play(MoveToTarget(enc_copy, path_arc=-TAU/24), run_time=0.6)

        self.wait(10)

        you_key = Text("Key: 123").scale(0.5).set_color(WHITE)
        you_key.next_to(VGroup(cipher_label, enc_copy), DOWN, buff=0.3)

        self.play(Write(you_key), run_time=0.6)

        self.wait(10)


        func3  = Tex(r"\text{Decrypt}", arg_separator="").scale(0.6).set_color(GREEN_C)
        lpar3  = Tex(r"\big(").scale(0.5)
        comma3 = Tex(r",").scale(0.5)
        rpar3  = Tex(r"\big)").scale(0.5)
        space3 = Rectangle(width=0.1, height=0.001, stroke_width=0, fill_opacity=0)
        eq3    = Tex("=").scale(0.5)

        key_slot2 = Text("123").scale(0.5).set_color(WHITE)
        ct_slot2  = Text("Xj3$p").scale(0.5).set_color(WHITE)
        pt_out2   = Text("Hello").scale(0.5).set_color(WHITE)

        eq_dec = VGroup(func3, lpar3, key_slot2, comma3, space3, ct_slot2, rpar3, eq3, pt_out2).arrange(RIGHT, buff=0.06, aligned_edge=ORIGIN)

        eq_dec.next_to(you_key, DOWN, buff=0.25)
        eq_dec.set_x(you.get_x())

        comma3.align_to(VGroup(key_slot2, ct_slot2), DOWN)

        self.play(
            Write(func3), Write(lpar3), Write(comma3), Write(rpar3), Write(eq3),
            run_time=0.9
        )

        digits_chars2 = VGroup(*you_key[-3:]).copy()

        ct_chars2 = enc_copy.copy()

        self.add(digits_chars2, ct_chars2)

        self.play(
            ReplacementTransform(digits_chars2, key_slot2),  # 123 → key_slot2
            ReplacementTransform(ct_chars2,  ct_slot2),      # Xj3$p → ct_slot2
            run_time=0.9
        )

        self.play(Write(pt_out2), run_time=0.7)

        self.wait(10)

        others = Group(*[m for m in self.mobjects if m is not keep])
        self.play(FadeOut(others), run_time=0.8)
        self.wait(10)

        







