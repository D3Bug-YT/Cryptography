from manim import *
from manim import rate_functions as rf

class HashingStart(Scene):
    def construct(self):
        # --- Title (same end-state look) ---
        t_hash = Text("Hashing").scale(0.84).set_color(YELLOW_C)
        t_hash.to_edge(UP)
        self.add(t_hash)
        self.wait(0.6)

        # Frame geometry (only need y-positions now)
        w, h = config.frame_width, config.frame_height
        y_text  =  h/2 - h/3           # 1/3 down
        y_image =  h/2 - 2*h/3         # 2/3 down

        # ---------- helpers ----------
        CHUNK = 16

        def make_hash_block(hex_str, chunk=CHUNK, scale=0.9):
            chunks = [hex_str[i:i+chunk] for i in range(0, len(hex_str), chunk)]
            stack_tex = r"\shortstack[l]{" + r"\\ ".join([rf"\texttt{{{c}}}" for c in chunks]) + "}"
            return Tex(stack_tex).scale(scale)

        def build_row(y, left_input_mobj, digest_hex):
            # pieces (note: parens are separate and bigger for nicer look)
            func      = Tex(r"\text{HashAlgorithm}", arg_separator="").scale(0.9)
            lpar      = Tex(r"\big(").scale(0.9)
            rpar      = Tex(r"\big)").scale(0.9)
            eq        = Tex("=").scale(0.9)
            right_blk = make_hash_block(digest_hex)

            # If the input is an image, size & align the parens to it
            if isinstance(left_input_mobj, ImageMobject):
                target_h = left_input_mobj.height * 1.15  # slight margin around the image
                for p in (lpar, rpar):
                    p.stretch_to_fit_height(target_h)
                    p.match_y(left_input_mobj)
                # tiny upward nudge to compensate for PNG padding (tweak if needed)
                left_input_mobj.shift(UP * 0.1)
            else:
                # For text inputs, keep parens baseline-aligned with the text
                VGroup(lpar, rpar).match_y(left_input_mobj)

            # Arrange: [HashAlgorithm] [ ( ] [input] [ ) ]  =  [stacked digest]
            left_group = Group(func, lpar, left_input_mobj, rpar).arrange(RIGHT, buff=0.05, aligned_edge=ORIGIN)
            row = Group(left_group, eq, right_blk).arrange(RIGHT, buff=0.35)

            # Anchor the '=' at x = 0, and place the row so '=' is at y
            row.shift(RIGHT * (0 - eq.get_center()[0]))
            row.shift(UP * (y - eq.get_center()[1]))

            # return in the order you'll animate: func → input → ( → ) → = → digest
            return row, (func, left_input_mobj, lpar, rpar, eq, right_blk)
        # ---------- /helpers ----------

   
        # --- Row 1: HashAlgorithm("Hello") = digest ---
        hello_arg = Tex(r"\texttt{``Hello''}", arg_separator="").scale(0.9).set_color(YELLOW_C)
        row1, (r1_func, r1_in, r1_lpar, r1_rpar, r1_eq, r1_out) = build_row(
            y_text,
            hello_arg,
            "185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969"
        )



        # --- Row 2: HashAlgorithm(book image) = digest ---
        book_img = ImageMobject("Other_ss/gta5.jpg").set(height=0.6)
        row2, (r2_func, r2_in, r2_lpar, r2_rpar, r2_eq, r2_out) = build_row(
            y_image,
            book_img,
            "909cb81127c5e1944b16dc5944ade59facb822c7a3f250d1f0256293bfd3c055"
        )

        book_final_pos = r2_in.get_center()

        r2_in.set_y(r1_in.get_center()[1])
        r2_in.set_x(r1_in.get_center()[0] + 3)


        self.play(Write(r1_in))
        self.wait(0.1)
        self.play(FadeIn(r2_in, shift=UP*0.1))

        self.wait(15)

        self.play(r2_in.animate.move_to(book_final_pos), run_time=0.8, rate_func=rf.ease_in_out_cubic)

        # animate row 1 like an equation writing across
        self.play(Write(r1_func), Write(r1_lpar), Write(r1_rpar), Write(r1_eq))
        #self.play(Write(r1_lpar))
        #self.play(Write(r1_rpar))
        #self.play(Write(r1_eq))
        self.play(Write(r1_out))


        # animate row 2
        self.play(Write(r2_func), Write(r2_lpar), Write(r2_rpar), Write(r2_eq))
        #self.play(Write(r2_lpar))
        #self.play(Write(r2_rpar))
        #self.play(Write(r2_eq))
        self.play(Write(r2_out))

        self.wait(10)

        brace = Brace(r1_out, direction=RIGHT, buff=0.15)
        label = Text("Hash or Digest", weight=MEDIUM).scale(0.5)
        label.next_to(brace, RIGHT, buff=0.2)
        self.play(FadeIn(brace), run_time=0.5)
        self.play(FadeIn(label, shift=RIGHT*0.1), run_time=0.4)

        self.wait(10)

        brace2 = Brace(r2_out, direction=RIGHT, buff=0.15)
        label2 = Text("256 bits AKA\n32 bytes", weight=MEDIUM).scale(0.5)
        label2.next_to(brace2, RIGHT, buff=0.2)
        self.play(FadeIn(brace2), run_time=0.5)
        self.play(FadeIn(label2, shift=RIGHT*0.1), run_time=0.4)

        self.wait(10)

        row2_all = Group(r2_func, r2_lpar, r2_in, r2_rpar, r2_eq, r2_out)
        both_braces_and_labels = Group(brace, label, brace2, label2)

        self.play(
            FadeOut(row2_all, shift=DOWN*0.1),
            FadeOut(both_braces_and_labels, shift=DOWN*0.1),
            run_time=0.6,
        )

        row1_all = Group(r1_func, r1_lpar, r1_in, r1_rpar, r1_eq, r1_out)
        target_y = 0.0
        dy = target_y - r1_eq.get_center()[1]
        self.play(row1_all.animate.shift(UP * dy), run_time=0.8, rate_func=rf.ease_in_out_cubic)

        self.wait(10)



        hello_new = Tex(r"\texttt{``hello''}", arg_separator="").scale(0.9).set_color(YELLOW_C)
        hello_new.match_height(r1_in).move_to(r1_in)

        self.play(FadeTransform(r1_in, hello_new, run_time=0.6))
        r1_in = hello_new

        self.bring_to_front(r1_in)


        row1_hex_str = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


        digest_lower = make_hash_block(row1_hex_str)
        digest_lower.move_to(r1_out)
        self.play(ReplacementTransform(r1_out, digest_lower, run_time=0.6))
        r1_out = digest_lower

        self.wait(10)

        hello_new2 = Tex(r"\texttt{``hello!''}", arg_separator="").scale(0.9).set_color(YELLOW_C)
        hello_new2.match_height(r1_in).move_to(r1_in)

        self.play(FadeTransform(r1_in, hello_new2, run_time=0.6))
        r1_in = hello_new2

        self.bring_to_front(r1_in)


        row1_hex_str_2 = "ce06092fb948d9ffac7d1a376e404b26b7575bcc11ee05a4615fef4fec3a308b"


        digest_lower_2 = make_hash_block(row1_hex_str_2)
        digest_lower_2.move_to(r1_out)
        self.play(ReplacementTransform(r1_out, digest_lower_2, run_time=0.6))
        r1_out = digest_lower_2

        self.wait(10)


        lhs_group = VGroup(r1_func, r1_lpar, r1_in, r1_rpar, r1_eq)
        self.play(FadeOut(lhs_group, shift=DOWN*0.1), run_time=0.5)

        h_Hello = "185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969"
        h_hello = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        h_hello_bng = "ce06092fb948d9ffac7d1a376e404b26b7575bcc11ee05a4615fef4fec3a308b"

        left_hash  = make_hash_block(h_Hello,     chunk=CHUNK, scale=0.9)
        mid_hash   = make_hash_block(h_hello,     chunk=CHUNK, scale=0.9)
        right_hash = make_hash_block(h_hello_bng, chunk=CHUNK, scale=0.9)

        for m in (left_hash, mid_hash, right_hash):
            m.move_to(r1_out)  

        self.play(
        AnimationGroup(
            ReplacementTransform(r1_out.copy(), left_hash),
            ReplacementTransform(r1_out.copy(), right_hash),
            ReplacementTransform(r1_out,        mid_hash),
            lag_ratio=0.0,
        ),
        run_time=0.8
        )   

        y_line = mid_hash.get_center()[1]
        triple = VGroup(left_hash, mid_hash, right_hash)
        self.play(
            triple.animate
                .arrange(RIGHT, buff=1)       # even horizontal spacing; tweak buff if needed
                .move_to([0, y_line, 0]),       # keep the same y, center on x
            run_time=0.8,
            rate_func=rf.ease_in_out_cubic
        ) 


        self.wait(10)

        def brace_with_label_below(target_mobj, tex_label, label_scale=0.55, brace_buff=0.15):
            """Brace under target with label under the brace."""
            br = Brace(target_mobj, direction=DOWN, buff=brace_buff)  # brace sits below, opening upward
            lbl = Tex(tex_label, arg_separator="").scale(label_scale)
            lbl.next_to(br, DOWN, buff=0.12)
            return br, lbl

        left_label_tex  = r"\texttt{``Hello''}"
        mid_label_tex   = r"\texttt{``hello''}"
        right_label_tex = r"\texttt{``hello!''}"

        brace_L, label_L = brace_with_label_below(left_hash,  left_label_tex)
        brace_M, label_M = brace_with_label_below(mid_hash,   mid_label_tex)
        brace_R, label_R = brace_with_label_below(right_hash, right_label_tex)

        label_L.set_color(YELLOW_C)
        label_M.set_color(YELLOW_C)
        label_R.set_color(YELLOW_C)

        # Animate braces first (labels are not added yet, so they won't pop in early)
        self.play(FadeIn(brace_L), FadeIn(brace_M), FadeIn(brace_R), run_time=0.5)

        # Now animate labels in
        self.play(
            FadeIn(label_L, shift=DOWN*0.1),
            FadeIn(label_M, shift=DOWN*0.1),
            FadeIn(label_R, shift=DOWN*0.1),
            run_time=0.4
        )

        # Only now ensure they’re on top if layering matters
        self.bring_to_front(brace_L, brace_M, brace_R, label_L, label_M, label_R)

        self.wait(10)

        def build_row_reversed(y, left_digest_hex, right_input_mobj, chunk=CHUNK, scale=0.9):
            """Build:  [ digest ]  =  [ HashAlgorithm( input ) ]  with '=' anchored at x=0, row at y."""
            # Left: stacked digest block
            left_blk = make_hash_block(left_digest_hex, chunk=chunk, scale=scale)

            # Right: HashAlgorithm( input )
            func = Tex(r"\text{HashAlgorithm}", arg_separator="").scale(0.9)
            lpar = Tex(r"\big(").scale(0.9)
            rpar = Tex(r"\big)").scale(0.9)

            # Align parens to the input baseline
            if isinstance(right_input_mobj, ImageMobject):
                VGroup(lpar, rpar).match_y(right_input_mobj)
            else:
                VGroup(lpar, rpar).match_y(right_input_mobj)

            right_group = Group(func, lpar, right_input_mobj, rpar).arrange(RIGHT, buff=0.05)

            eq = Tex("=").scale(0.9)
            row = Group(left_blk, eq, right_group).arrange(RIGHT, buff=0.35)

            # Anchor '=' at x=0 and place row so '=' is at y
            row.shift(RIGHT * (0 - eq.get_center()[0]))
            row.shift(UP * (y - eq.get_center()[1]))

            # Return parts so we can animate them nicely
            return row, (left_blk, eq, func, lpar, right_input_mobj, rpar)
        
        cluster = VGroup(
            left_hash, mid_hash, right_hash,
            brace_L, brace_M, brace_R,
            label_L, label_M, label_R
        )
        self.play(FadeOut(cluster, shift=DOWN*0.1), run_time=0.6)

        # --- 2) Draw reversed equation:  [ digest ] = [ HashAlgorithm( ? ) ] ---
        # Use the "hello" digest you used earlier (or pick any)
        rev_digest_hex = "87a797a48cba94ee585ee2c0d7d6f4cce4dd12f77192a4d0bc562938d6fb62b1"  # SHA-256("hello")

        q_input = Tex(r"\texttt{?}", arg_separator="").scale(0.9).set_color(YELLOW_C)

        # Put the row at y = 0 (middle). Change to another y if you prefer.
        row_rev, (rev_left, rev_eq, rev_func, rev_lpar, rev_in, rev_rpar) = build_row_reversed(
            y=0.0,
            left_digest_hex=rev_digest_hex,
            right_input_mobj=q_input,
            chunk=CHUNK,
            scale=0.9
        )

        # Animate it in (digest first, then '=', then the RHS pieces)
        self.play(Write(rev_left), run_time=0.5)
        self.play(Write(rev_eq), run_time=0.3)
        self.play(Write(rev_func), Write(rev_lpar), Write(rev_in), Write(rev_rpar), run_time=0.9)

        self.wait(10)


        rev_group = VGroup(rev_left, rev_eq, rev_func, rev_lpar, rev_in, rev_rpar)
        self.play(FadeOut(rev_group, shift=DOWN*0.1), run_time=0.5)


        bullets = BulletedList(
            "Takes arbitrary-sized input",
            "Produces fixed-size output",
            "Deterministic",
            "One-way",
        ).scale(0.6).set_color(YELLOW_C)
        bullets.move_to(ORIGIN)

        durations = [0.7, 0.7, 0.7, 0.7]
        gaps      = [3, 3, 3, 3] 

        for item, d, g in zip(bullets, durations, gaps):
            self.play(Write(item), run_time=d)
            if g > 0:
                self.wait(g)
        
        
        self.wait(10)
        self.play(FadeOut(bullets, shift=UP*0.05), run_time=0.35)




        card = RoundedRectangle(
            corner_radius=0.28,
            width=11,
            height=5,
            color=WHITE,
            stroke_width=2,
            fill_color=GRAY,
            fill_opacity=0.15  # no fill; change to 0.05 for a light fill
        ).move_to(ORIGIN)

        self.play(Create(card), run_time=0.5)

        title = Text("User Database", weight=BOLD).scale(0.7)
        title.next_to(card.get_top(), DOWN, buff=0.28)
        self.play(Write(title), run_time=0.4)

        underline = Line(ORIGIN, RIGHT).set_width(card.width)
        underline.next_to(title, DOWN, buff=0.12)
        self.play(Create(underline), run_time=0.35)



        # Compute the drawable vertical span (between underline and card bottom)
        y_top = underline.get_bottom()[1]
        y_bot = card.get_bottom()[1]

        # Evenly space 3 vertical lines across the interior width
        x_left  = card.get_left()[0]
        x_right = card.get_right()[0]
        width   = x_right - x_left


        g_left, g_mid, g_right = 1, 2, 5
        g_sum = g_left + g_mid + g_right

        x1 = x_left + width * (g_left / g_sum)
        x2 = x_left + width * ((g_left + g_mid) / g_sum)

        vlines = VGroup(
            Line([x1, y_bot, 0], [x1, y_top, 0], color=WHITE, stroke_width=1.5),
            Line([x2, y_bot, 0], [x2, y_top, 0], color=WHITE, stroke_width=1.5),
        )
        self.play(Create(vlines), run_time=0.5)


        y_top = underline.get_bottom()[1]
        y_bot = card.get_bottom()[1]

        x_left  = card.get_left()[0]
        x_right = card.get_right()[0]

        ys = [y_top + (i/7) * (y_bot - y_top) for i in (1, 2, 3, 4, 5, 6)]

        
        hlines = VGroup(*[
            Line([x_left, y, 0], [x_right, y, 0], color=WHITE, stroke_width=1.5)
            for y in ys
        ])

        self.play(Create(hlines), run_time=0.5)



        x_edges = [card.get_left()[0]] + [ln.get_x() for ln in vlines] + [card.get_right()[0]]
        x_edges = sorted(x_edges)  # left -> right

        # Y edges: top region (under the underline), each horizontal line y, bottom wall
        y_edges = [underline.get_bottom()[1]] + [ln.get_y() for ln in hlines] + [card.get_bottom()[1]]
        y_edges = sorted(y_edges, reverse=True)  # top -> bottom

        def cell_center(r, c):
            """Row r (0=top), Col c (0=left) -> center point."""
            x = 0.5 * (x_edges[c] + x_edges[c+1])
            y = 0.5 * (y_edges[r] + y_edges[r+1])
            return np.array([x, y, 0.0])

        def add_cell_text(r, c, s, scale=0.45, color=WHITE, align_left=False, xpad=0.12, weight=NORMAL):
            """Add text into a cell. If align_left, stick to cell's left edge with padding."""
            m = Text(s, weight=weight).scale(scale).set_color(color)
            if align_left:
                y = 0.5 * (y_edges[r] + y_edges[r+1])
                x = x_edges[c] + xpad
                m.move_to([x, y, 0], aligned_edge=LEFT)
            else:
                m.move_to(cell_center(r, c))
            self.play(FadeIn(m, shift=UP*0.05), run_time=0.2)
            return m

        # --- Example: headers & a few rows ---
        # Rows count = len(y_edges) - 1 ; Cols count = len(x_edges) - 1
        # With your setup: 3 columns (ID, username, password) and 7 rows

        # Header row (top row = 0)
        hdr_id  = add_cell_text(0, 0, "ID",        scale=0.5, weight=BOLD)
        hdr_usr = add_cell_text(0, 1, "Username",  scale=0.5, align_left=True, weight=BOLD)
        hdr_pwd = add_cell_text(0, 2, "Password",  scale=0.5, align_left=True, weight=BOLD)

        # Row 1
        r1_id  = add_cell_text(1, 0, "1")
        r1_usr = add_cell_text(1, 1, "alice",     align_left=True)
        r1_pwd = add_cell_text(1, 2, "A1iceP455word",  align_left=True)

        # Row 2
        r2_id  = add_cell_text(2, 0, "2")
        r2_usr = add_cell_text(2, 1, "bob",       align_left=True)
        r2_pwd = add_cell_text(2, 2, "B0bS5cr5t",  align_left=True)

        # Middle ellipsis row (roughly middle row index)
        mid_r = (len(y_edges) - 1) // 2
        add_cell_text(mid_r, 0, "…")
        add_cell_text(mid_r, 1, "…", align_left=True)
        add_cell_text(mid_r, 2, "…", align_left=True)

        add_cell_text(mid_r + 1, 0, "…")
        add_cell_text(mid_r + 1, 1, "…", align_left=True)
        add_cell_text(mid_r + 1, 2, "…", align_left=True)

        add_cell_text(mid_r + 2, 0, "…")
        add_cell_text(mid_r + 2, 1, "…", align_left=True)
        add_cell_text(mid_r + 2, 2, "…", align_left=True)

        # Bottom row 'n'
        last_r = (len(y_edges) - 1) - 1
        add_cell_text(last_r, 0, "n")
        add_cell_text(last_r, 1, "user_n",  align_left=True)
        #add_cell_text(last_r, 2, "password", align_left=True)
        pwd_n = add_cell_text(last_r, 2, "password", align_left=True)

        self.wait(10)

        def replace_with_hash(old_mobj, hex_str, col_index, scale=0.45, color=WHITE, xpad=0.12):
            # Build new monospace text
            new = Text(hex_str).scale(scale).set_color(color)

            # Fit within this column's cell width (avoid overflow)
            cell_left  = x_edges[col_index]
            cell_right = x_edges[col_index + 1]
            max_width  = (cell_right - cell_left) - 2 * xpad
            if new.width > max_width:
                new.scale(max_width / new.width)

            # Left-align to the same position as the old text
            new.move_to(old_mobj, aligned_edge=LEFT)

            # Animate the replacement
            self.play(ReplacementTransform(old_mobj, new), run_time=0.6)
            return new
        
        hash_r1 = "ba272df88d0404aafb2446e8a6d7ceb96255b68a90ca6c617373eae78a6ded6c"
        hash_r2 = "e7ecc5b582e3763330b3d46b9c39d08aa0682ff876ff8de4255e313edb04cfd6" 
        hash_rn = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8" 

        # Replace the password cells (column index 2)
        r1_pwd = replace_with_hash(r1_pwd, hash_r1, col_index=2)
        r2_pwd = replace_with_hash(r2_pwd, hash_r2, col_index=2)
        # bottom row 'n'
        pwd_n  = replace_with_hash(pwd_n, hash_rn, col_index=2)

        self.wait(10)


        keep = t_hash

        # fade all other top-level mobjects
        others = Group(*[m for m in self.mobjects if m is not keep])
        self.play(FadeOut(others, shift=DOWN*0.1), run_time=0.8)
        self.wait(2)
