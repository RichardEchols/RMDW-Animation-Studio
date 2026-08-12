from manim import *

# ---- Visual language ----
BG = "#1C1C1C"
CRIMSON = "#B11E2F"
CYAN = "#58C4DD"
GREEN = "#83C167"
YELLOW = "#FFD93D"
WHITE = "#EAEAEA"
GREY = "#888888"
MONO = "Menlo"


class Scene1_OldWay(Scene):
    """The Traditional Studio — a team + expensive software."""
    def construct(self):
        self.camera.background_color = BG

        title = Text("The Traditional Studio", font_size=44, color=WHITE, weight=BOLD, font=MONO)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=1.5)
        self.wait(0.8)

        # The team of roles (the expensive part)
        roles = ["Writer", "Storyboard Artist", "Animator", "Editor", "Sound Designer"]
        role_mobs = VGroup()
        for i, r in enumerate(roles):
            m = Text(r, font_size=26, color=GREY, font=MONO)
            m.shift(LEFT * 3.2 + UP * (1.2 - i * 0.55))
            role_mobs.add(m)
        self.play(*[FadeIn(m, shift=RIGHT * 0.3) for m in role_mobs], run_time=1.5)
        self.wait(0.6)

        # The expensive software (the other expensive part)
        tools = ["After Effects", "Maya", "Cinema 4D"]
        tool_mobs = VGroup()
        for i, t in enumerate(tools):
            m = Text(t, font_size=24, color=CRIMSON, font=MONO)
            m.shift(RIGHT * 3.2 + UP * (1.2 - i * 0.55))
            tool_mobs.add(m)
        self.play(*[FadeIn(m, shift=LEFT * 0.3) for m in tool_mobs], run_time=1.2)
        self.wait(0.6)

        # The cost tag
        cost = Text("A team. Expensive software. Weeks per video.", font_size=28, color=YELLOW, font=MONO)
        cost.to_edge(DOWN, buff=0.8)
        self.play(Write(cost), run_time=1.5)
        self.wait(1.5)

        # Clean exit
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.wait(0.3)


class Scene2_NewWay(Scene):
    """The Solo Operator — one person, one model, a pipeline."""
    def construct(self):
        self.camera.background_color = BG

        title = Text("The Solo Operator", font_size=44, color=WHITE, weight=BOLD, font=MONO)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=1.5)
        self.wait(0.8)

        # One person
        person = Text("1 PERSON", font_size=30, color=CYAN, weight=BOLD, font=MONO)
        person.shift(LEFT * 3.0)
        self.play(FadeIn(person, scale=0.8), run_time=1.0)
        self.wait(0.5)

        # One model
        model = Text("1 LOCAL MODEL", font_size=30, color=CRIMSON, weight=BOLD, font=MONO)
        model.shift(LEFT * 3.0 + DOWN * 1.0)
        self.play(FadeIn(model, scale=0.8), run_time=1.0)
        self.wait(0.5)

        # Free tools
        free = Text("FREE OPEN TOOLS", font_size=30, color=GREEN, weight=BOLD, font=MONO)
        free.shift(LEFT * 3.0 + DOWN * 2.0)
        self.play(FadeIn(free, scale=0.8), run_time=1.0)
        self.wait(0.5)

        # The pipeline arrow
        pipeline = Text("Script \u2192 Storyboard \u2192 Animate \u2192 Render \u2192 Publish",
                        font_size=26, color=WHITE, font=MONO)
        pipeline.shift(RIGHT * 1.5)
        self.play(Write(pipeline), run_time=1.5)
        self.wait(0.8)

        # The message
        msg = Text("One person. One local model. A repeatable pipeline.",
                   font_size=28, color=YELLOW, font=MONO)
        msg.to_edge(DOWN, buff=0.8)
        self.play(Write(msg), run_time=1.5)
        self.wait(1.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.wait(0.3)


class Scene3_Pipeline(Scene):
    """The 5-stage pipeline, each lighting up in sequence."""
    def construct(self):
        self.camera.background_color = BG

        title = Text("The Pipeline", font_size=44, color=WHITE, weight=BOLD, font=MONO)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=1.2)
        self.wait(0.6)

        stages = [
            ("1. Script", "I write the story", CYAN),
            ("2. Storyboard", "I plan the scenes", CYAN),
            ("3. Animate", "Manim + Blender + p5.js", CRIMSON),
            ("4. Render", "I render the frames", GREEN),
            ("5. Publish", "I ship the video", GREEN),
        ]

        # Build the 5 stage boxes in a row
        boxes = VGroup()
        labels = VGroup()
        descs = VGroup()
        for i, (name, desc, color) in enumerate(stages):
            x = -4.2 + i * 2.1
            box = Rectangle(width=1.9, height=1.6, color=color, stroke_width=3)
            box.shift(RIGHT * x)
            label = Text(name, font_size=20, color=color, weight=BOLD, font=MONO)
            label.move_to(box.get_center() + UP * 0.4)
            d = Text(desc, font_size=14, color=GREY, font=MONO)
            d.move_to(box.get_center() + DOWN * 0.45)
            boxes.add(box)
            labels.add(label)
            descs.add(d)

        # Reveal all boxes dimly first, then light each one up
        self.play(*[Create(b) for b in boxes], run_time=1.5)
        self.wait(0.5)

        for i in range(len(stages)):
            self.play(
                labels[i].animate.set_opacity(1.0),
                descs[i].animate.set_opacity(1.0),
                boxes[i].animate.set_stroke_width(5),
                run_time=0.6
            )
            self.wait(0.6)

        # The message
        msg = Text("The AI is the team. The tools are the hands.",
                   font_size=30, color=YELLOW, weight=BOLD, font=MONO)
        msg.to_edge(DOWN, buff=0.8)
        self.play(Write(msg), run_time=1.5)
        self.wait(1.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.wait(0.3)


class Scene4_Punchline(Scene):
    """The punchline — you don't need a studio, you need a pipeline."""
    def construct(self):
        self.camera.background_color = BG

        line1 = Text("You don't need a studio.", font_size=40, color=WHITE, weight=BOLD, font=MONO)
        line2 = Text("You need a pipeline.", font_size=40, color=CRIMSON, weight=BOLD, font=MONO)
        group = VGroup(line1, line2).arrange(DOWN, buff=0.4)
        self.play(Write(line1), run_time=1.2)
        self.wait(0.5)
        self.play(Write(line2), run_time=1.2)
        self.wait(1.2)

        # Fade to the title card
        self.play(FadeOut(group), run_time=0.6)

        brand = Text("RMDW ANIMATION STUDIO", font_size=52, color=CRIMSON, weight=BOLD, font=MONO)
        sub = Text("One person. One local model. Your own hardware. Free tools.",
                   font_size=24, color=WHITE, font=MONO)
        sub2 = Text("Built by JAH 3.0 + Hermes", font_size=22, color=CYAN, font=MONO)
        sub3 = Text("github.com/RichardEchols/RMDW-Animation-Studio", font_size=18, color=GREY, font=MONO)
        card = VGroup(brand, sub, sub2, sub3).arrange(DOWN, buff=0.5)

        self.play(FadeIn(brand, scale=0.7), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(sub, shift=UP * 0.3), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(sub2, shift=UP * 0.3), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(sub3, shift=UP * 0.3), run_time=1.0)
        self.wait(2.5)
