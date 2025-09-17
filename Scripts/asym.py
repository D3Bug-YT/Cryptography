from manim import *
from manim import rate_functions as rf

class asym(Scene):
    def construct(self):
        title = Text("Symmetric Key Encryption").scale(0.84).set_color(GREEN_C)
        title.to_edge(UP)
        self.play(Write(title))

        self.wait(10)

        self.play(Transform(title, Text("Asymmetric Key Encryption").scale(0.84).set_color(BLUE_C).to_edge(UP)), run_time=1.5)

        self.wait(10)

        pub_key = Text("Public Key").scale(0.7).set_color(BLUE_E)
        priv_key = Text("Private Key").scale(0.7).set_color(BLUE_A)

        pub_key_text = Text(": Known to everyone").scale(0.7).set_color(WHITE)
        priv_key_text = Text(": Known only to the owner").scale(0.7).set_color(WHITE)

        pub_row = VGroup(pub_key, pub_key_text).arrange(RIGHT, buff=0.1)
        priv_row = VGroup(priv_key, priv_key_text).arrange(RIGHT, buff=0.1)

        self.play(Write(pub_row))
        self.play(Write(priv_row.next_to(pub_row, DOWN, buff=0.3)))

        self.wait(10)

        #self.play(FadeOut(pub_key_text, DOWN * 0.2), FadeOut(priv_key_text, DOWN * 0.2), run_time=0.6)
        self.play(
            FadeOut(pub_key_text, shift=0.2*DOWN),
            FadeOut(priv_key_text, shift=0.2*DOWN),
            run_time=0.6,
        )

        pub_key.set_color(BLUE_E)
        priv_key.set_color(BLUE_A)

        func = Tex(r"\text{Encrypt}", arg_separator="").scale(0.9).set_color(BLUE_C)
        lpar = Tex(r"\big(").scale(0.9)
        comma = Tex(r",").scale(0.9)
        space = Rectangle(width=0.25, height=0.001, stroke_width=0, fill_opacity=0)
        rpar = Tex(r"\big)").scale(0.9)
        eq = Tex("=").scale(0.9)
        plain_text = Text("Plain Text").scale(0.7).set_color(GREEN_B)
        cipher_text = Text("Cipher Text").scale(0.7).set_color(RED_A)

        func2 = Tex(r"\text{Decrypt}", arg_separator="").scale(0.9).set_color(BLUE_C)
        lpar2 = Tex(r"\big(").scale(0.9)
        comma2 = Tex(r",").scale(0.9)
        space2 = Rectangle(width=0.25, height=0.001, stroke_width=0, fill_opacity=0)
        rpar2 = Tex(r"\big)").scale(0.9)
        eq2 = Tex("=").scale(0.9)
        plain_text2 = Text("Plain Text").scale(0.7).set_color(GREEN_B)
        cipher_text2 = Text("Cipher Text").scale(0.7).set_color(RED_A)

        pub_key_target = pub_key.copy()
        priv_key_target = priv_key.copy()

        left_group = Group(func, lpar, pub_key_target, comma, space, plain_text, rpar, eq, cipher_text).arrange(RIGHT, buff=0.05, aligned_edge=ORIGIN)
        right_group = Group(func2, lpar2, priv_key_target, comma2, space2, cipher_text2, rpar2, eq2, plain_text2).arrange(RIGHT, buff=0.05, aligned_edge=ORIGIN)
        right_group.next_to(left_group, DOWN, buff=0.3)
        both_groups = Group(left_group, right_group).center()
        both_groups.next_to(title, DOWN, buff=0.75)


        pub_key.generate_target(); pub_key.target.move_to(pub_key_target)
        priv_key.generate_target(); priv_key.target.move_to(priv_key_target)

        args = Group(pub_key_target, plain_text)
        comma.align_to(args, DOWN)

        args2 = Group(priv_key_target, cipher_text2)
        comma2.align_to(args2, DOWN)

        #self.play(Write(func), Write(lpar), Write(comma), Write(rpar), Write(eq), MoveToTarget(pub_key, path_arc=-TAU/24), Write(plain_text), Write(cipher_text), run_time=0.9)
        #self.play(Write(func2), Write(lpar2), Write(comma2), Write(rpar2), Write(eq2), MoveToTarget(priv_key, path_arc=TAU/24), Write(cipher_text2), Write(plain_text2), run_time=0.9)
        self.play(
            # first equation pieces
            Write(func), Write(lpar), Write(comma), Write(rpar), Write(eq),
            MoveToTarget(pub_key, path_arc=-TAU/24),
            Write(plain_text), Write(cipher_text),

            # second equation pieces
            Write(func2), Write(lpar2), Write(comma2), Write(rpar2), Write(eq2),
            MoveToTarget(priv_key, path_arc=TAU/24),
            Write(cipher_text2), Write(plain_text2),

            run_time=0.9
        )

        self.wait(10)

        box = SurroundingRectangle(
            both_groups,
            buff=0.3,             # padding around the group
            color=WHITE,
            stroke_width=4,
            corner_radius=0.15,   # <-- rounded corners
        )

        self.play(Create(box), run_time=0.6)

        self.wait(10)



        enc_func   = func.copy()
        enc_lpar   = lpar.copy()
        enc_comma  = comma.copy()
        enc_space  = space.copy()
        enc_rpar   = rpar.copy()
        enc_eq     = eq.copy()
        enc_pt     = plain_text.copy()
        enc_ct     = cipher_text.copy()
        enc_pub    = pub_key.copy()
        enc_priv   = priv_key.copy()

        dec_func   = func2.copy()
        dec_lpar   = lpar2.copy()
        dec_comma  = comma2.copy()
        dec_space  = space2.copy()
        dec_rpar   = rpar2.copy()
        dec_eq     = eq2.copy()
        dec_pt     = plain_text2.copy()
        dec_ct     = cipher_text2.copy()
        dec_pub    = pub_key.copy()
        dec_priv   = priv_key.copy()

        enc_group = Group(enc_func, enc_lpar, enc_priv, enc_comma, enc_space, enc_pt, enc_rpar, enc_eq, enc_ct).arrange(RIGHT, buff=0.05, aligned_edge=ORIGIN)
        dec_group = Group(dec_func, dec_lpar, dec_pub, dec_comma, dec_space, dec_ct, dec_rpar, dec_eq, dec_pt).arrange(RIGHT, buff=0.05, aligned_edge=ORIGIN)
        
        both_groups2 = Group(enc_group, dec_group).arrange(DOWN, buff=0.3)
        both_groups2.next_to(box, DOWN, buff=0.75).align_to(both_groups, LEFT)

        enc_comma.align_to(VGroup(enc_priv, enc_pt), DOWN)
        dec_comma.align_to(VGroup(dec_pub,  dec_ct), DOWN)

        self.add(both_groups2)

        self.play(
            AnimationGroup(
                # Top line -> swapped Encrypt line (now with Private Key)
                TransformFromCopy(func,       enc_func),
                TransformFromCopy(lpar,       enc_lpar),
                TransformFromCopy(priv_key,   enc_priv),     # key swap: source = top Private Key
                TransformFromCopy(comma,      enc_comma),
                TransformFromCopy(space,      enc_space),
                TransformFromCopy(plain_text, enc_pt),
                TransformFromCopy(rpar,       enc_rpar),
                TransformFromCopy(eq,         enc_eq),
                TransformFromCopy(cipher_text,enc_ct),

                # Bottom line -> swapped Decrypt line (now with Public Key)
                TransformFromCopy(func2,        dec_func),
                TransformFromCopy(lpar2,        dec_lpar),
                TransformFromCopy(pub_key,      dec_pub),    # key swap: source = top Public Key
                TransformFromCopy(comma2,       dec_comma),
                TransformFromCopy(space2,       dec_space),
                TransformFromCopy(cipher_text2, dec_ct),
                TransformFromCopy(rpar2,        dec_rpar),
                TransformFromCopy(eq2,          dec_eq),
                TransformFromCopy(plain_text2,  dec_pt),

                lag_ratio=0.03
            ),
            run_time=1.2
        )

        # Box the lower (swapped) equations with rounded corners, same style
        box2 = SurroundingRectangle(
            both_groups2,
            buff=0.3,
            color=WHITE,
            stroke_width=4,
            corner_radius=0.15,
        )
        self.play(Create(box2), run_time=0.6)

        self.wait(10)

        keep = title

        self.play(
            AnimationGroup(
                *[FadeOut(m, shift=0.2*DOWN) for m in self.mobjects if m is not keep],
                lag_ratio=0.02,
            ),
            run_time=0.6,
        )

        me = Text("Alice").scale(0.84).set_color(BLUE_C)
        you = Text("Bob").scale(0.84).set_color(BLUE_C)

        names = Group(me, you).arrange(RIGHT, buff=4.0, aligned_edge=DOWN)
        names.next_to(title, DOWN, buff=0.6)
        names.set_x(0)

        self.play(Write(me), Write(you), run_time=1.0)


        self.wait(10)
        '''
        public_key = Text("Public Key").scale(0.6).set_color(BLUE_E)
        plain_txt =  Text("Plain Text").scale(0.6).set_color(GREEN_B)
        private_key = Text("Private Key").scale(0.6).set_color(BLUE_A)
        cipher_txt = Text("Cipher Text").scale(0.6).set_color(RED_A)

        me_items = Group(private_key, plain_txt).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        me_items.next_to(me, DOWN, buff=0.3)
        you_items = Group(public_key, cipher_txt).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        you_items.next_to(you, DOWN, buff=0.3)

        func3 = Tex(r"\text{Encrypt}", arg_separator="").scale(0.8).set_color(BLUE_C)
        lpar3 = Tex(r"\big(").scale(0.6)
        comma3 = Tex(r",").scale(0.6)
        space3 = Rectangle(width=0.25, height=0.001, stroke_width=0, fill_opacity=0)
        rpar3 = Tex(r"\big)").scale(0.6)
        eq3 = Tex("=").scale(0.6)
        plain_text3 = Text("Plain Text").scale(0.6).set_color(GREEN_B)
        cipher_text3 = Text("Cipher Text").scale(0.6).set_color(RED_A)

        private_target = private_key.copy()
        plain_target = plain_txt.copy()

        self.play(Write(public_key), Write(private_key), run_time=1.0)
        self.play(Write(plain_txt), run_time=1.0)
        self.add(private_target, plain_target)

        me_group = Group(func3, lpar3, private_target, comma3, space3, plain_target, rpar3, eq3, cipher_text3).arrange(RIGHT, buff=0.05, aligned_edge=ORIGIN)
        me_group.next_to(me_items, DOWN, buff=0.3).align_to(me_items, LEFT)

        private_target.generate_target(); private_key.target.move_to(private_target)
        plain_target.generate_target(); plain_txt.target.move_to(plain_target)

        args3 = Group(private_key.copy(), plain_text3)
        comma3.align_to(args3, DOWN)

        self.play(
            # first equation pieces
            Write(func3), Write(lpar3), Write(comma3), Write(rpar3), Write(eq3),
            MoveToTarget(private_target, path_arc=-TAU/24),
            MoveToTarget(plain_target, path_arc=-TAU/24), 
            Write(cipher_text3),
            run_time=0.9
        )

        '''
        public_key = Text("Alice's Public Key").scale(0.6).set_color(BLUE_E)
        plain_txt  = Text("Plain Text").scale(0.6).set_color(GREEN_B)
        plain_text5 = Text("Plain Text").scale(0.6).set_color(GREEN_B)
        private_key = Text("Alice's Private Key").scale(0.6).set_color(BLUE_A)
        cipher_txt = Text("Cipher Text").scale(0.6).set_color(RED_A)

        me_items = VGroup(private_key, plain_txt).arrange(DOWN, buff=0.15, aligned_edge=ORIGIN)
        me_items.next_to(me, DOWN, buff=0.3)

        you_items = VGroup(public_key, cipher_txt, plain_text5).arrange(DOWN, buff=0.15, aligned_edge=ORIGIN)
        you_items.next_to(you, DOWN, buff=0.3)

        # Draw the labels under Me/Everyone Else
        self.play(Write(public_key), Write(private_key), run_time=0.6)
        self.play(Write(plain_txt), run_time=0.6)

        # Equation tokens (Encrypt(private, plaintext) = ciphertext)
        func3 = Tex(r"\text{Encrypt}", arg_separator="").scale(0.8).set_color(BLUE_C)
        lpar3 = MathTex(r"\big(").scale(0.6)
        comma3 = MathTex(",").scale(0.6)
        space3 = Rectangle(width=0.15, height=0.001, stroke_width=0, fill_opacity=0)
        rpar3 = MathTex(r"\big)").scale(0.6)
        eq3   = MathTex("=").scale(0.6)
        plain_text3  = Text("Plain Text").scale(0.6).set_color(GREEN_B)
        cipher_text3 = Text("Cipher Text").scale(0.6).set_color(RED_A)

        # Invisible target slots (same font/size as originals)
        priv_slot  = private_key.copy().set_opacity(0)
        plain_slot = plain_txt.copy().set_opacity(0)

        # Build the equation line (targets included but invisible)
        me_group = VGroup(
            func3, lpar3, priv_slot, comma3, space3, plain_slot, rpar3, eq3, cipher_text3
        ).arrange(RIGHT, buff=0.05, aligned_edge=ORIGIN)
        me_group.next_to(title, DOWN, buff=3.5).align_to(title, ORIGIN)

        # Align comma baseline to args
        comma3.align_to(VGroup(priv_slot, plain_slot), DOWN)

        # Show all visible tokens of the equation (not the invisible slots)
        self.play(Write(func3), Write(lpar3), Write(comma3), Write(rpar3), Write(eq3), run_time=0.9)

        # --- MOVE EXPLICIT CLONES (originals stay put) ---
        moving_priv  = private_key.copy()
        moving_plain = plain_txt.copy()
        self.add(moving_priv, moving_plain)

        moving_priv.generate_target();  moving_priv.target.move_to(priv_slot)
        moving_plain.generate_target(); moving_plain.target.move_to(plain_slot)

        self.play(
            MoveToTarget(moving_priv,  path_arc=-TAU/24),
            MoveToTarget(moving_plain, path_arc=-TAU/24),
            run_time=0.9
        )

        self.play(Write(cipher_text3), run_time=0.6)

        # Once landed, remove invisible placeholders (we keep the landed clones)
        self.remove(priv_slot, plain_slot)

        self.wait(10)

        cipher_text4 = cipher_text3.copy()
        cipher_text4.generate_target(); cipher_text4.target.move_to(cipher_txt)
        self.play(MoveToTarget(cipher_text4, path_arc=TAU/24), run_time=0.9)
        #self.play(Add(cipher_txt))
        


        self.wait(10)



        func4 = Tex(r"\text{Decrypt}", arg_separator="").scale(0.8).set_color(BLUE_C)
        lpar4 = MathTex(r"\big(").scale(0.6)
        comma4 = MathTex(",").scale(0.6)
        space4 = Rectangle(width=0.15, height=0.001, stroke_width=0, fill_opacity=0)
        rpar4 = MathTex(r"\big)").scale(0.6)
        eq4   = MathTex("=").scale(0.6)
        plain_text4 = Text("Plain Text").scale(0.6).set_color(GREEN_B)

        # Invisible landing slots (keep originals on screen)
        pk_slot = public_key.copy().set_opacity(0)   # for Public Key clone
        ct_slot = cipher_txt.copy().set_opacity(0)   # for Cipher Text clone

        dec_group = VGroup(
            func4, lpar4, pk_slot, comma4, space4, ct_slot, rpar4, eq4, plain_text4
        ).arrange(RIGHT, buff=0.05, aligned_edge=ORIGIN)

        # Place this line under your previous equation line (me_group)
        dec_group.next_to(title, DOWN, buff=3.5).align_to(title, ORIGIN)

        # Tidy baseline for the comma
        comma4.align_to(VGroup(pk_slot, ct_slot), DOWN)

        self.play(FadeOut(me_group, shift=DOWN*0.2), FadeOut(moving_priv, shift=DOWN*0.2), FadeOut(moving_plain, shift=DOWN*0.2), run_time=0.6)

        self.wait(10)

        # Draw the visible tokens (not the invisible slots)
        self.play(
            Write(func4), Write(lpar4), Write(comma4), Write(rpar4), Write(eq4),
            run_time=0.9
        )

        # --- MOVE EXPLICIT CLONES (originals stay put) ---
        moving_pub = public_key.copy()
        moving_ct  = cipher_txt.copy()
        self.add(moving_pub, moving_ct)

        moving_pub.generate_target(); moving_pub.target.move_to(pk_slot)
        moving_ct.generate_target();  moving_ct.target.move_to(ct_slot)

        self.play(
            MoveToTarget(moving_pub, path_arc=-TAU/24),
            MoveToTarget(moving_ct,  path_arc=-TAU/24),
            run_time=0.9
        )

        # Reveal the result (= Plain Text)
        self.play(Write(plain_text4), run_time=0.6)

        # Cleanup placeholders (we keep the landed clones)
        self.remove(pk_slot, ct_slot)

        self.wait(10)

        plain_text6 = plain_text4.copy()
        plain_text6.generate_target(); plain_text6.target.move_to(plain_text5)
        self.play(MoveToTarget(plain_text6, path_arc=TAU/24), run_time=0.9)

        self.wait(10)



        # ----------------------------------------------------------------



        # 1) Fade everything except title, Me/You, and the two key labels
        keep = {title, me, you, public_key, private_key}
        to_fade = []
        for m in list(self.mobjects):
            # don't fade if m is a kept item or contains a kept item
            if any(k is m or (hasattr(m, "submobjects") and k in m.submobjects) for k in keep):
                continue
            to_fade.append(m)

        if to_fade:
            self.play(
                AnimationGroup(*[FadeOut(m, shift=0.2*DOWN) for m in to_fade], lag_ratio=0.03),
                run_time=0.6
            )

        self.wait(10)

        # 2) Write Plain Text under "Everyone Else"
        plain_you = Text("Plain Text").scale(0.6).set_color(GREEN_B)
        plain_you.next_to(public_key, DOWN, buff=0.15).align_to(public_key, ORIGIN)
        self.play(Write(plain_you), run_time=0.4)

        self.wait(10)

        # 3) Encrypt(public key, plaintext) = ciphertext
        E_func  = Tex(r"\text{Encrypt}").scale(0.8).set_color(BLUE_C)
        E_lpar  = MathTex(r"\big(").scale(0.6)
        E_comma = MathTex(",").scale(0.6)
        E_space = Rectangle(width=0.15, height=0.001, stroke_width=0, fill_opacity=0)
        E_rpar  = MathTex(r"\big)").scale(0.6)
        E_eq    = MathTex("=").scale(0.6)
        E_ct    = Text("Cipher Text").scale(0.6).set_color(RED_A)

        pk_slot = public_key.copy().set_opacity(0)
        pt_slot = plain_you.copy().set_opacity(0)

        enc_line = VGroup(
            E_func, E_lpar, pk_slot, E_comma, E_space, pt_slot, E_rpar, E_eq, E_ct
        ).arrange(RIGHT, buff=0.05, aligned_edge=ORIGIN)
        enc_line.next_to(title, DOWN, buff=3.5).set_x(0)
        E_comma.align_to(VGroup(pk_slot, pt_slot), DOWN)

        # draw visible tokens in the equation (leave slots invisible)
        self.play(Write(E_func), Write(E_lpar), Write(E_comma), Write(E_rpar), Write(E_eq), run_time=0.8)

        # move EXPLICIT CLONES from the You column into the encrypt line
        moving_pk  = public_key.copy()
        moving_pt  = plain_you.copy()
        self.add(moving_pk, moving_pt)
        moving_pk.generate_target(); moving_pk.target.move_to(pk_slot)
        moving_pt.generate_target(); moving_pt.target.move_to(pt_slot)
        self.play(
            MoveToTarget(moving_pk, path_arc=-TAU/24),
            MoveToTarget(moving_pt, path_arc=-TAU/24),
            run_time=0.9
        )

        self.wait(10)

        # reveal ciphertext in the equation
        self.play(Write(E_ct), run_time=0.4)

        # drop a COPY of the resulting ciphertext under "Me"
        cipher_me = E_ct.copy()
        self.add(cipher_me)
        cipher_me.generate_target()
        # position under Me: below Private Key (or adjust to taste)
        cipher_me.target.next_to(private_key, DOWN, buff=0.15).align_to(private_key, ORIGIN)
        self.play(MoveToTarget(cipher_me, path_arc=TAU/24), run_time=0.8)

        self.wait(10)

        # 4) Decrypt(private key, ciphertext) = plaintext
        D_func  = Tex(r"\text{Decrypt}").scale(0.8).set_color(BLUE_C)
        D_lpar  = MathTex(r"\big(").scale(0.6)
        D_comma = MathTex(",").scale(0.6)
        D_space = Rectangle(width=0.15, height=0.001, stroke_width=0, fill_opacity=0)
        D_rpar  = MathTex(r"\big)").scale(0.6)
        D_eq    = MathTex("=").scale(0.6)
        D_pt    = Text("Plain Text").scale(0.6).set_color(GREEN_B)

        sk_slot = private_key.copy().set_opacity(0)  # slot for Private Key
        ct_slot = cipher_me.copy().set_opacity(0)    # slot for Cipher Text (from Me)

        dec_line = VGroup(
            D_func, D_lpar, sk_slot, D_comma, D_space, ct_slot, D_rpar, D_eq, D_pt
        ).arrange(RIGHT, buff=0.05, aligned_edge=ORIGIN)
        dec_line.next_to(title, DOWN, buff=3.5).set_x(0)
        D_comma.align_to(VGroup(sk_slot, ct_slot), DOWN)

        self.play(FadeOut(enc_line, shift=DOWN*0.2), FadeOut(moving_pk, shift=DOWN*0.2), FadeOut(moving_pt, shift=DOWN*0.2), run_time=0.6)

        self.wait(10)

        self.play(Write(D_func), Write(D_lpar), Write(D_comma), Write(D_rpar), Write(D_eq), run_time=0.8)



        # move EXPLICIT CLONES from the Me column into the decrypt line
        moving_sk = private_key.copy()
        moving_ct = cipher_me.copy()
        self.add(moving_sk, moving_ct)
        moving_sk.generate_target(); moving_sk.target.move_to(sk_slot)
        moving_ct.generate_target(); moving_ct.target.move_to(ct_slot)
        self.play(
            MoveToTarget(moving_sk, path_arc=-TAU/24),
            MoveToTarget(moving_ct, path_arc=-TAU/24),
            run_time=0.9
        )

        self.wait(10)

        # reveal plaintext in the equation
        self.play(Write(D_pt), run_time=0.4)

        # drop a COPY of the resulting plaintext under "Me" (stack it below the cipher or next to it)
        plain_me = D_pt.copy()
        self.add(plain_me)
        plain_me.generate_target()
        plain_me.target.next_to(cipher_me, DOWN, buff=0.15).align_to(private_key, ORIGIN)
        self.play(MoveToTarget(plain_me, path_arc=TAU/24), run_time=0.8)

        self.wait(10)

        keep = {title}
        to_fade = []
        for m in list(self.mobjects):
            # don't fade if m is a kept item or contains a kept item
            if any(k is m or (hasattr(m, "submobjects") and k in m.submobjects) for k in keep):
                continue
            to_fade.append(m)

        if to_fade:
            self.play(
                AnimationGroup(*[FadeOut(m, shift=0.2*DOWN) for m in to_fade], lag_ratio=0.03),
                run_time=0.6
            )

        self.wait(10)
