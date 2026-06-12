from manim import *
import random
import math

class NeonIntro(Scene):
    def construct(self):

        # ============================================================
        # CONFIGURATION
        # ============================================================
        NAME = "DAVE CHAPPELLE"
        TAGLINE = "LIVE TONIGHT"

        # Colour palette
        HOT_PINK     = "#FF2D78"
        CYAN         = "#00F5FF"
        ACID_YELLOW  = "#FFFF00"
        DEEP_PURPLE  = "#6600FF"
        WHITE        = "#FFFFFF"
        BLOOD_ORANGE = "#FF4500"

        self.camera.background_color = "#000000"

        # ============================================================
        # STAGE 1 — STATIC NOISE BURST (random pixel storm)
        # ============================================================
        noise_dots = VGroup()
        for _ in range(180):
            dot = Dot(
                point=[
                    random.uniform(-7, 7),
                    random.uniform(-4, 4),
                    0
                ],
                radius=random.uniform(0.01, 0.06),
                color=random.choice([HOT_PINK, CYAN, ACID_YELLOW, WHITE])
            )
            dot.set_opacity(random.uniform(0.3, 1.0))
            noise_dots.add(dot)

        self.add(noise_dots)
        self.wait(0.08)
        self.remove(noise_dots)
        self.wait(0.04)
        self.add(noise_dots)
        self.wait(0.06)
        self.remove(noise_dots)

        # ============================================================
        # STAGE 2 — SHOCKWAVE RING EXPANDS FROM CENTRE
        # ============================================================
        rings = VGroup()
        for i in range(4):
            ring = Circle(
                radius=0.1,
                color=[HOT_PINK, CYAN, ACID_YELLOW, DEEP_PURPLE][i],
                stroke_width=3 - i * 0.5
            )
            ring.set_opacity(0.9 - i * 0.15)
            rings.add(ring)

        self.play(
            *[
                AnimationGroup(
                    rings[i].animate.scale(30).set_opacity(0),
                )
                for i in range(4)
            ],
            lag_ratio=0.12,
            run_time=0.7,
            rate_func=rush_into
        )
        self.remove(rings)

        # ============================================================
        # STAGE 3 — GLITCH HORIZONTAL SLICES (VHS tear)
        # ============================================================
        glitch_bars = VGroup()
        for i in range(12):
            bar = Rectangle(
                width=random.uniform(2, 14),
                height=random.uniform(0.05, 0.25),
                fill_color=random.choice([HOT_PINK, CYAN, DEEP_PURPLE]),
                fill_opacity=random.uniform(0.4, 0.9),
                stroke_width=0
            )
            bar.move_to([
                random.uniform(-3, 3),
                random.uniform(-3.5, 3.5),
                0
            ])
            glitch_bars.add(bar)

        self.play(
            FadeIn(glitch_bars, run_time=0.06),
        )
        self.wait(0.05)
        self.play(
            FadeOut(glitch_bars, run_time=0.06),
        )

        # ============================================================
        # STAGE 4 — LETTERS FLY IN FROM ALL DIRECTIONS (staggered)
        # ============================================================
        # Build each letter separately so they can fly from different angles
        letters = VGroup()
        for char in NAME:
            if char == " ":
                # Spacer
                spacer = Text(" ", font="Impact", font_size=88, color=WHITE)
                letters.add(spacer)
            else:
                letter = Text(
                    char,
                    font="Impact",
                    font_size=88,
                    color=WHITE
                )
                letters.add(letter)

        # Arrange letters horizontally
        letters.arrange(RIGHT, buff=0.05)
        letters.move_to(ORIGIN)

        # Scale down if name is long
        if letters.width > 12:
            letters.scale(12 / letters.width)

        # Store final positions
        final_positions = [l.get_center().copy() for l in letters]

        # Launch directions — alternating chaos
        launch_vectors = []
        directions = [
            UP * 8 + LEFT * 6,
            DOWN * 7 + RIGHT * 5,
            LEFT * 10,
            RIGHT * 10,
            UP * 9 + RIGHT * 4,
            DOWN * 8 + LEFT * 3,
            UP * 6,
            DOWN * 9,
            LEFT * 8 + UP * 5,
            RIGHT * 7 + DOWN * 6,
            UP * 10 + RIGHT * 7,
            DOWN * 6 + LEFT * 8,
            LEFT * 9 + DOWN * 3,
            RIGHT * 8 + UP * 4,
        ]

        # Position letters at launch points
        for i, letter in enumerate(letters):
            if letter.text.strip():
                direction = directions[i % len(directions)]
                letter.move_to(final_positions[i] + direction)

        self.add(letters)

        # Animate each letter slamming to its final position
        anims = []
        for i, letter in enumerate(letters):
            if letter.text.strip():
                anims.append(
                    letter.animate(rate_func=rush_into).move_to(final_positions[i])
                )

        self.play(
            *anims,
            lag_ratio=0.06,
            run_time=0.9
        )

        # ============================================================
        # STAGE 5 — IMPACT FLASH (white screen slam)
        # ============================================================
        flash = Rectangle(
            width=20, height=12,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        )
        self.add(flash)
        self.wait(0.04)
        self.play(FadeOut(flash, run_time=0.15))

        # ============================================================
        # STAGE 6 — CHROMATIC ABERRATION (pink + cyan ghost copies)
        # ============================================================
        pink_ghost = letters.copy()
        pink_ghost.set_color(HOT_PINK)
        pink_ghost.set_opacity(0.6)
        pink_ghost.shift(LEFT * 0.08 + UP * 0.04)

        cyan_ghost = letters.copy()
        cyan_ghost.set_color(CYAN)
        cyan_ghost.set_opacity(0.6)
        cyan_ghost.shift(RIGHT * 0.08 + DOWN * 0.04)

        self.add(pink_ghost, cyan_ghost)
        self.wait(0.1)

        # Ghosts snap back
        self.play(
            pink_ghost.animate.shift(RIGHT * 0.08 + DOWN * 0.04).set_opacity(0),
            cyan_ghost.animate.shift(LEFT * 0.08 + UP * 0.04).set_opacity(0),
            run_time=0.2
        )
        self.remove(pink_ghost, cyan_ghost)

        # ============================================================
        # STAGE 7 — NEON COLOUR WAVE SWEEPS THROUGH LETTERS
        # ============================================================
        # Colour each letter with a wave of neon
        neon_colours = [HOT_PINK, CYAN, ACID_YELLOW, HOT_PINK, CYAN, DEEP_PURPLE,
                        ACID_YELLOW, HOT_PINK, CYAN, ACID_YELLOW, HOT_PINK, CYAN,
                        DEEP_PURPLE, ACID_YELLOW]

        colour_anims = []
        for i, letter in enumerate(letters):
            colour_anims.append(
                letter.animate.set_color(neon_colours[i % len(neon_colours)])
            )

        self.play(
            *colour_anims,
            lag_ratio=0.04,
            run_time=0.5
        )

        # Then snap back to white with a flash
        self.play(
            letters.animate.set_color(WHITE),
            run_time=0.15
        )

        # ============================================================
        # STAGE 8 — ELECTRIC STRIKE LINES (lightning bolts across name)
        # ============================================================
        bolts = VGroup()
        for _ in range(6):
            # Jagged lightning path
            start_x = random.uniform(-6, -2)
            end_x = random.uniform(2, 6)
            y_base = random.uniform(-0.5, 0.5)

            points = [np.array([start_x, y_base, 0])]
            x = start_x
            while x < end_x:
                x += random.uniform(0.3, 0.8)
                y = y_base + random.uniform(-0.4, 0.4)
                points.append(np.array([min(x, end_x), y, 0]))

            bolt = VMobject()
            bolt.set_points_as_corners(points)
            bolt.set_stroke(
                color=random.choice([CYAN, ACID_YELLOW, WHITE]),
                width=random.uniform(1, 3),
                opacity=random.uniform(0.7, 1.0)
            )
            bolts.add(bolt)

        self.play(
            ShowPassingFlash(bolts, time_width=0.4, run_time=0.5)
        )

        # ============================================================
        # STAGE 9 — SHOCKWAVE RINGS FROM NAME (second hit)
        # ============================================================
        impact_rings = VGroup()
        for i in range(5):
            r = Circle(
                radius=0.2,
                color=[CYAN, HOT_PINK, ACID_YELLOW, DEEP_PURPLE, WHITE][i],
                stroke_width=2
            )
            impact_rings.add(r)

        self.play(
            *[
                impact_rings[i].animate.scale(20 + i * 5).set_opacity(0)
                for i in range(5)
            ],
            lag_ratio=0.1,
            run_time=0.6,
            rate_func=rush_into
        )
        self.remove(impact_rings)

        # ============================================================
        # STAGE 10 — TAGLINE SLAMS IN FROM BELOW
        # ============================================================
        tagline_text = Text(
            TAGLINE,
            font="Impact",
            font_size=36,
            color=CYAN
        )
        tagline_text.next_to(letters, DOWN, buff=0.35)

        # Neon underline
        underline = Line(
            tagline_text.get_left() + LEFT * 0.2,
            tagline_text.get_right() + RIGHT * 0.2,
            color=HOT_PINK,
            stroke_width=3
        )
        underline.next_to(tagline_text, DOWN, buff=0.1)

        # Tagline starts off-screen below
        tagline_start = tagline_text.get_center() + DOWN * 5
        tagline_text.move_to(tagline_start)

        self.play(
            tagline_text.animate(rate_func=rush_into).next_to(letters, DOWN, buff=0.35),
            run_time=0.35
        )
        self.play(
            Create(underline, run_time=0.3)
        )

        # ============================================================
        # STAGE 11 — GLITCH FLICKER SEQUENCE (3 rapid stutters)
        # ============================================================
        everything = VGroup(letters, tagline_text, underline)

        for _ in range(3):
            # Shift everything slightly for glitch
            offset = np.array([random.uniform(-0.15, 0.15), random.uniform(-0.08, 0.08), 0])
            self.play(
                everything.animate.shift(offset),
                run_time=0.04,
                rate_func=linear
            )
            self.play(
                everything.animate.shift(-offset),
                run_time=0.04,
                rate_func=linear
            )

        # Final noise burst overlay during flicker
        final_noise = VGroup()
        for _ in range(60):
            dot = Dot(
                point=[random.uniform(-7, 7), random.uniform(-4, 4), 0],
                radius=random.uniform(0.02, 0.05),
                color=random.choice([HOT_PINK, CYAN, ACID_YELLOW])
            )
            dot.set_opacity(random.uniform(0.2, 0.7))
            final_noise.add(dot)

        self.add(final_noise)
        self.wait(0.05)
        self.remove(final_noise)

        # ============================================================
        # STAGE 12 — HOLD ON THE MONEY SHOT (2.5 seconds)
        # Then cinematic fade to black
        # ============================================================

        # Subtle slow pulse on the name — breathing neon
        self.play(
            letters.animate.scale(1.04).set_color(CYAN),
            run_time=0.4,
            rate_func=there_and_back
        )
        self.play(
            letters.animate.set_color(WHITE),
            run_time=0.2
        )

        # Hold
        self.wait(2.0)

        # Cinematic fade — everything out
        self.play(
            FadeOut(letters, run_time=0.6),
            FadeOut(tagline_text, run_time=0.6),
            FadeOut(underline, run_time=0.6),
        )

        # Final black flash
        end_flash = Rectangle(
            width=20, height=12,
            fill_color="#000000",
            fill_opacity=1,
            stroke_width=0
        )
        self.add(end_flash)
        self.wait(0.2)