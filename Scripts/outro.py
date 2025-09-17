from manim import *
from manim import rate_functions as rf

class outro(Scene):
    def construct(self):
        title = Text("Asymmetric Key Encryption").scale(0.84).set_color(BLUE_C)
        title.to_edge(UP)
        self.play(Write(title))

        me = Text("Alice").scale(0.84).set_color(BLUE_C)
        you = Text("Bob").scale(0.84).set_color(BLUE_C)

        names = VGroup(me, you).arrange(RIGHT, buff=5.0, aligned_edge=DOWN)
        names.next_to(title, DOWN, buff=0.5)
        names.set_x(0)

        pub_key = Text("Bob Public Key").scale(0.6).set_color(BLUE_E)
        pub_key.next_to(me, DOWN, buff=0.15).align_to(me, ORIGIN)
        priv_key = Text("Bob Private Key").scale(0.6).set_color(BLUE_A)
        priv_key.next_to(you, DOWN, buff=0.15).align_to(you, ORIGIN)

        self.play(Write(names))
        self.play(Write(pub_key), Write(priv_key))
        self.wait(10)

        plain_text = Text("Plain Text Sym Key: ").scale(0.6).set_color(GREEN_B)
        plain_text_content = Text("123").scale(0.6).set_color(GREEN_B)
        plain_text_group = VGroup(plain_text, plain_text_content).arrange(RIGHT, buff=0.1)
        plain_text_content.align_to(plain_text, DOWN)

        plain_text_group.next_to(pub_key, DOWN, buff=0.15).align_to(pub_key, ORIGIN)

        self.play(Write(plain_text_group))
        self.wait(10)

        E_func  = Tex(r"\text{Encrypt}").scale(0.8).set_color(BLUE_C)
        E_lpar  = MathTex(r"\big(").scale(0.6)
        E_comma = MathTex(",").scale(0.6)
        E_space = Rectangle(width=0.15, height=0.001, stroke_width=0, fill_opacity=0)
        E_rpar  = MathTex(r"\big)").scale(0.6)
        E_eq    = MathTex("=").scale(0.6)
        E_ct    = Text("Cipher Text: ").scale(0.6).set_color(RED_A)
        E_ct_content = Text("JpQ").scale(0.6).set_color(RED_A)



        pk_slot  = pub_key.copy().set_opacity(0)            # Bob Public Key
        msg_slot = plain_text_content.copy().set_opacity(0) # "123"


        # Assemble the equation line
        enc_line = VGroup(
            E_func, E_lpar, pk_slot, E_comma, E_space, msg_slot, E_rpar, E_eq, E_ct_content,
        ).arrange(RIGHT, buff=0.06, aligned_edge=ORIGIN)

        # Position the line under your plaintext label; align left for a tidy column vibe
        enc_line.next_to(title, DOWN, buff=3).align_to(title, ORIGIN)

        # Typography tweak: drop the comma baseline to match the args
        E_comma.align_to(VGroup(pk_slot, msg_slot), DOWN)

        # Draw only the visible tokens for now (keep slots invisible so the clones can land)
        self.play(Write(E_func), Write(E_lpar), Write(E_comma), Write(E_rpar), Write(E_eq), run_time=0.8)

        # --- Move explicit clones into the slots (originals stay where they are) ---
        moving_pk  = pub_key.copy()
        moving_msg = plain_text_content.copy()
        self.add(moving_pk, moving_msg)

        moving_pk.generate_target();  moving_pk.target.move_to(pk_slot)
        moving_msg.generate_target(); moving_msg.target.move_to(msg_slot)

        self.play(
            MoveToTarget(moving_pk,  path_arc=-TAU/24),
            MoveToTarget(moving_msg, path_arc=-TAU/24),
            run_time=0.9
        )

        # Reveal the ciphertext on the right side of the equation
        self.play(Write(E_ct_content), run_time=0.8)

        self.wait(10)

        # (optional) If you want a copy of the ciphertext to appear under Alice too:
        # ct_under_alice = E_ct.copy()
        # self.add(ct_under_alice)
        # ct_under_alice.generate_target()
        # ct_under_alice.target.next_to(pub_key, DOWN, buff=0.15).align_to(pub_key, LEFT)
        # self.play(MoveToTarget(ct_under_alice, path_arc=TAU/24), run_time=0.8)

        # Clean up (we keep landed clones, remove invisible placeholders)
        self.remove(pk_slot, msg_slot)

        E_ct_content_copy = E_ct_content.copy()
        E_ct_moving = E_ct_content.copy()
        self.add(E_ct_moving)

        ct_content = VGroup(E_ct, E_ct_content_copy).arrange(RIGHT, buff=0.1)


        ct_content.next_to(priv_key, DOWN, buff=0.15).align_to(priv_key, ORIGIN)
        self.play(Write(E_ct), run_time=0.8)

        E_ct_moving.generate_target();  E_ct_moving.target.move_to(E_ct_content_copy)

        self.play(MoveToTarget(E_ct_moving, path_arc=TAU/24), run_time=0.8)

        self.wait(10)

        self.play(FadeOut(enc_line, shift=0.2*DOWN), FadeOut(moving_pk, shift=0.2*DOWN), FadeOut(moving_msg, shift=0.2*DOWN), run_time=0.6)

        self.wait(10)


        D_func  = Tex(r"\text{Decrypt}").scale(0.8).set_color(BLUE_C)
        D_lpar  = MathTex(r"\big(").scale(0.6)
        D_comma = MathTex(",").scale(0.6)
        D_space = Rectangle(width=0.15, height=0.001, stroke_width=0, fill_opacity=0)
        D_rpar  = MathTex(r"\big)").scale(0.6)
        D_eq    = MathTex("=").scale(0.6)
        D_pt_content = Text("123").scale(0.6).set_color(GREEN_B)

        sk_slot = priv_key.copy().set_opacity(0)
        ct_under_bob_source = E_ct_moving
        ct_slot = ct_under_bob_source.copy().set_opacity(0)

        dec_line = VGroup(
            D_func, D_lpar, sk_slot, D_comma, D_space, ct_slot, D_rpar, D_eq, D_pt_content
        ).arrange(RIGHT, buff=0.06, aligned_edge=ORIGIN)
        dec_line.next_to(title, DOWN, buff=3).align_to(title, ORIGIN)

        D_comma.align_to(VGroup(sk_slot, ct_slot), DOWN)

        self.play(Write(D_func), Write(D_lpar), Write(D_comma), Write(D_rpar), Write(D_eq), run_time=0.8)

        moving_sk = priv_key.copy()
        moving_ct = ct_under_bob_source.copy()
        self.add(moving_sk, moving_ct)

        moving_sk.generate_target(); moving_sk.target.move_to(sk_slot)
        moving_ct.generate_target(); moving_ct.target.move_to(ct_slot)

        self.play(
            MoveToTarget(moving_sk, path_arc=-TAU/24),
            MoveToTarget(moving_ct, path_arc=-TAU/24),
            run_time=0.9
        )

        self.play(Write(D_pt_content), run_time=0.5)

        pt_label_under_bob = Text("Plain Text Sym Key: ").scale(0.6).set_color(GREEN_B)
        pt_value_slot      = D_pt_content.copy().set_opacity(0)  # invisible landing spot

        pt_row = VGroup(pt_label_under_bob, pt_value_slot).arrange(RIGHT, buff=0.1)
        # Place it just below the "Cipher Text: JpQ" row you built earlier
        pt_row.next_to(ct_content, DOWN, buff=0.15)

        # Write the label, then fly a COPY of the equation's plaintext value into place
        self.play(Write(pt_label_under_bob), run_time=0.6)

        pt_value_moving = D_pt_content.copy()
        self.add(pt_value_moving)
        pt_value_moving.generate_target(); pt_value_moving.target.move_to(pt_value_slot)

        self.play(MoveToTarget(pt_value_moving, path_arc=TAU/24), run_time=0.8)

        # Clean placeholders (keep landed clones)
        self.remove(sk_slot, ct_slot, pt_value_slot)

        self.wait(10)

        self.play(FadeOut(dec_line, shift=0.2*DOWN), FadeOut(moving_sk, shift=0.2*DOWN), FadeOut(moving_ct, shift=0.2*DOWN), run_time=0.6)

        self.wait(10)

        sym_title = Text("Symmetric Key Encryption").scale(0.84).set_color(GREEN_C)
        sym_title.next_to(title, DOWN, buff=3).align_to(title, ORIGIN)
        self.play(Write(sym_title), run_time=0.8)

        self.wait(10)

        plain_text_msg = Text("Plain Text Msg: ").scale(0.6).set_color(GREEN_B)
        plain_text_msg_content = Text("HELLO").scale(0.6).set_color(GREEN_B)
        plain_text_msg_group = VGroup(plain_text_msg, plain_text_msg_content).arrange(RIGHT, buff=0.1)
        plain_text_msg_group.next_to(pub_key, DOWN, buff=2.5).align_to(pub_key, ORIGIN)

        self.play(Write(plain_text_msg_group), run_time=0.8)

        self.wait(10)

        SE_func  = Tex(r"\text{Encrypt}").scale(0.8).set_color(GREEN_C)
        SE_lpar  = MathTex(r"\big(").scale(0.6)
        SE_comma = MathTex(",").scale(0.6)
        SE_space = Rectangle(width=0.15, height=0.001, stroke_width=0, fill_opacity=0)
        SE_rpar  = MathTex(r"\big)").scale(0.6)
        SE_eq    = MathTex("=").scale(0.6)
        SE_ct_content = Text("X7ka$").scale(0.6).set_color(RED_A)   # placeholder ciphertext text

        # Invisible landing slots (so originals stay put up in the columns)
        # Use the *landed clone* from earlier for the symmetric key value (123):
        symkey_slot = plain_text_content.copy().set_opacity(0)          # 123
        msg_slot    = plain_text_msg_content.copy().set_opacity(0)   # HELLO

        # Assemble the symmetric equation line
        sym_enc_line = VGroup(
            SE_func, SE_lpar, symkey_slot, SE_comma, SE_space, msg_slot, SE_rpar, SE_eq, SE_ct_content
        ).arrange(RIGHT, buff=0.06, aligned_edge=ORIGIN)

        # Place ~1.5 units below the symmetric title and center it under the title
        sym_enc_line.next_to(sym_title, DOWN, buff=1.75)
        sym_enc_line.set_x(sym_title.get_center()[0])

        # Baseline tweak so the comma sits nicely with its args
        SE_comma.align_to(VGroup(symkey_slot, msg_slot), DOWN)

        # Draw the visible tokens first (keep slots invisible so clones can land)
        self.play(Write(SE_func), Write(SE_lpar), Write(SE_comma), Write(SE_rpar), Write(SE_eq), run_time=0.8)

        # --- Move EXPLICIT CLONES into the slots (originals stay put) ---
        moving_symkey = plain_text_content.copy()          # copy of "123" under Bob
        moving_msg2   = plain_text_msg_content.copy()   # copy of "HELLO" under Bob
        self.add(moving_symkey, moving_msg2)

        moving_symkey.generate_target(); moving_symkey.target.move_to(symkey_slot)
        moving_msg2.generate_target();   moving_msg2.target.move_to(msg_slot)

        self.play(
            MoveToTarget(moving_symkey, path_arc=-TAU/24),
            MoveToTarget(moving_msg2,   path_arc=-TAU/24),
            run_time=0.9
        )

        # Reveal the ciphertext result on the right
        self.play(Write(SE_ct_content), run_time=0.5)

        # (optional) If you want to keep only the landed clones and not the invisible slots:
        self.remove(symkey_slot, msg_slot)

        self.wait(10)

        SE_ct_label_under = Text("Cipher Text: ").scale(0.6).set_color(RED_A)
        SE_ct_value_slot  = SE_ct_content.copy().set_opacity(0)

        sym_ct_row = VGroup(SE_ct_label_under, SE_ct_value_slot).arrange(RIGHT, buff=0.1)

        # Place it under the symmetric equation line, centered on Bob's column
        sym_ct_row.next_to(priv_key, DOWN, buff=2.5)
        sym_ct_row.set_x(you.get_center()[0])  # center under "Bob"

        # Write the label first
        self.play(Write(SE_ct_label_under), run_time=0.5)

        # Fly a COPY of the equation's ciphertext into the slot (original stays in the equation)
        moving_ct_copy = SE_ct_content.copy()
        self.add(moving_ct_copy)
        moving_ct_copy.generate_target(); moving_ct_copy.target.move_to(SE_ct_value_slot)

        self.play(MoveToTarget(moving_ct_copy, path_arc=TAU/24), run_time=0.8)

        # Keep the landed clone; remove the invisible placeholder
        self.remove(SE_ct_value_slot)

        self.wait(10)

        self.play(FadeOut(sym_enc_line, shift=0.2*DOWN), FadeOut(moving_symkey, shift=0.2*DOWN), FadeOut(moving_msg2, shift=0.2*DOWN), run_time=0.6)

        self.wait(10)

        SD_func  = Tex(r"\text{Decrypt}").scale(0.8).set_color(GREEN_C)
        SD_lpar  = MathTex(r"\big(").scale(0.6)
        SD_comma = MathTex(",").scale(0.6)
        SD_space = Rectangle(width=0.15, height=0.001, stroke_width=0, fill_opacity=0)
        SD_rpar  = MathTex(r"\big)").scale(0.6)
        SD_eq    = MathTex("=").scale(0.6)
        SD_pt_content = Text("HELLO").scale(0.6).set_color(GREEN_B)

        # Invisible slots (keep originals in the column)
        # 'pt_value_moving' should be the symmetric key "123" that now lives under Bob
        # 'moving_ct_copy' is the ciphertext you just dropped under Bob
        symkey_slot_2 = pt_value_moving.copy().set_opacity(0)
        ct_slot_2     = moving_ct_copy.copy().set_opacity(0)

        sym_dec_line = VGroup(
            SD_func, SD_lpar, symkey_slot_2, SD_comma, SD_space, ct_slot_2, SD_rpar, SD_eq, SD_pt_content
        ).arrange(RIGHT, buff=0.06, aligned_edge=ORIGIN)

        # Put it exactly where the symmetric encrypt line was
        sym_dec_line.next_to(sym_title, DOWN, buff=1.75)
        sym_dec_line.set_x(sym_title.get_center()[0])

        # Nice comma baseline
        SD_comma.align_to(VGroup(symkey_slot_2, ct_slot_2), DOWN)

        # Draw visible tokens
        self.play(Write(SD_func), Write(SD_lpar), Write(SD_comma), Write(SD_rpar), Write(SD_eq), run_time=0.8)

        # Move EXPLICIT CLONES from Bob's column into the equation
        moving_symkey_2 = pt_value_moving.copy()
        moving_ct_2     = moving_ct_copy.copy()
        self.add(moving_symkey_2, moving_ct_2)

        moving_symkey_2.generate_target(); moving_symkey_2.target.move_to(symkey_slot_2)
        moving_ct_2.generate_target();     moving_ct_2.target.move_to(ct_slot_2)

        self.play(
            MoveToTarget(moving_symkey_2, path_arc=-TAU/24),
            MoveToTarget(moving_ct_2,     path_arc=-TAU/24),
            run_time=0.9
        )

        # Reveal plaintext result in the equation
        self.play(Write(SD_pt_content), run_time=0.5)

        # --- "Plain Text Msg: HELLO" row under Bob's column (under the Cipher Text row) ---

        pt_msg_label_under_bob = Text("Plain Text Msg: ").scale(0.6).set_color(GREEN_B)
        pt_msg_value_slot      = SD_pt_content.copy().set_opacity(0)

        pt_msg_row = VGroup(pt_msg_label_under_bob, pt_msg_value_slot).arrange(RIGHT, buff=0.1)

        # Place it right under your Cipher Text row under Bob
        # (assuming 'sym_ct_row' is the row you built: ["Cipher Text: ", <value>])
        pt_msg_row.next_to(sym_ct_row, DOWN, buff=0.12)
        # Center the row in Bob's column (use 'you' as the column anchor)
        pt_msg_row.set_x(you.get_center()[0])

        # Write label, then fly a COPY of the result into the slot
        self.play(Write(pt_msg_label_under_bob), run_time=0.4)

        pt_msg_value_moving = SD_pt_content.copy()
        self.add(pt_msg_value_moving)
        pt_msg_value_moving.generate_target(); pt_msg_value_moving.target.move_to(pt_msg_value_slot)

        self.play(MoveToTarget(pt_msg_value_moving, path_arc=TAU/24), run_time=0.8)

        # Clean placeholders; keep landed clones
        self.remove(symkey_slot_2, ct_slot_2, pt_msg_value_slot)

        self.wait(10)

        to_fade = Group(*list(self.mobjects))  # snapshot the current mobjects
        self.play(FadeOut(to_fade, shift=0.25*DOWN, scale=0.95), run_time=0.8)

        self.wait(5)

