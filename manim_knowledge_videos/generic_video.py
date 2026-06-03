from __future__ import annotations

import json
import os
from pathlib import Path

from manim import *


TOPIC_PATH = Path(os.environ["TOPIC_JSON"]).resolve()
TOPIC = json.loads(TOPIC_PATH.read_text(encoding="utf-8"))
ROOT = TOPIC_PATH.parent.parent
RUN_DIR = Path(os.environ.get("RUN_DIR", ROOT / "outputs" / TOPIC["slug"])).resolve()

FONT = "PingFang SC"
PAPER = "#F7F7F2"
INK = "#222222"
MUTED = "#666A73"
TEAL = "#2A9D8F"
CORAL = "#E76F51"
AMBER = "#E9C46A"
BLUE = "#457B9D"
VIOLET = "#7C5CFF"
COLORS = [TEAL, CORAL, BLUE, AMBER, VIOLET]


class GenericKnowledgeVideo(Scene):
    def construct(self):
        self.camera.background_color = PAPER
        self.title_text = Text(TOPIC["title"], font=FONT, font_size=38, color=INK)
        self.title_text.to_edge(UP, buff=0.32)
        self.add(self.title_text)
        self.current_subtitle = None
        for index, segment in enumerate(TOPIC["segments"]):
            self.play_segment(index, segment)

    def play_segment(self, index, segment):
        audio = RUN_DIR / "audio" / f"seg_{index + 1:02d}.wav"
        if audio.exists():
            self.add_sound(str(audio))
        self.set_subtitle(segment["subtitle"])
        getattr(self, f"visual_{segment['visual']['type']}")(segment)

    def set_subtitle(self, text):
        if self.current_subtitle:
            self.remove(self.current_subtitle)
        label = Text(text, font=FONT, font_size=27, color=INK, line_spacing=0.85)
        label.set(width=11.9)
        box = RoundedRectangle(
            corner_radius=0.12,
            width=12.55,
            height=max(0.72, label.height + 0.32),
            fill_color=WHITE,
            fill_opacity=0.92,
            stroke_color="#D5D8DE",
            stroke_width=1.2,
        )
        group = VGroup(box, label)
        label.move_to(box.get_center())
        group.to_edge(DOWN, buff=0.22)
        self.current_subtitle = group
        self.add(group)
        self.bring_to_front(group)

    def clear_stage(self):
        keep = {self.title_text, self.current_subtitle}
        moving = [mob for mob in list(self.mobjects) if mob not in keep]
        if moving:
            self.play(*[FadeOut(mob) for mob in moving], run_time=0.12)
        self.bring_to_front(self.current_subtitle)

    def hold(self, segment, used_time):
        self.wait(max(0.45, segment["duration"] - used_time))

    def token(self, text, color=BLUE, width=None):
        width = width or max(1.2, min(2.6, 0.35 * len(text) + 0.9))
        box = RoundedRectangle(
            corner_radius=0.15,
            width=width,
            height=0.62,
            fill_color=color,
            fill_opacity=0.16,
            stroke_color=color,
            stroke_width=2,
        )
        label = Text(text, font=FONT, font_size=25, color=INK)
        label.set(max_width=width - 0.22)
        return VGroup(box, label)

    def card(self, title, body, color=TEAL, width=3.25, height=1.75):
        rect = RoundedRectangle(
            corner_radius=0.12,
            width=width,
            height=height,
            fill_color=color,
            fill_opacity=0.13,
            stroke_color=color,
            stroke_width=2,
        )
        t = Text(title, font=FONT, font_size=30, color=color)
        b = Text(body, font=FONT, font_size=22, color=INK, line_spacing=0.82)
        b.set(width=width - 0.38)
        return VGroup(rect, VGroup(t, b).arrange(DOWN, buff=0.22).move_to(rect.get_center()))

    def visual_title(self, segment):
        v = segment["visual"]
        q = Text(v["headline"], font=FONT, font_size=46, color=INK).move_to(UP * 0.65)
        sub = Text(v.get("subhead", ""), font=FONT, font_size=30, color=TEAL)
        sub.set(width=10.8).next_to(q, DOWN, buff=0.48)
        self.play(Write(q), run_time=1.0)
        if v.get("subhead"):
            self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.8)
        self.hold(segment, 1.8)
        self.clear_stage()

    def visual_compare(self, segment):
        items = segment["visual"]["items"]
        cards = VGroup(*[self.card(i["title"], i["body"], COLORS[n]) for n, i in enumerate(items)])
        cards.arrange(RIGHT, buff=0.55).move_to(UP * 0.35)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.25) for c in cards], lag_ratio=0.18), run_time=1.4)
        self.hold(segment, 1.4)
        self.clear_stage()

    def visual_pipeline(self, segment):
        steps = segment["visual"]["steps"]
        nodes = VGroup(*[self.token(s, COLORS[i % len(COLORS)]) for i, s in enumerate(steps)])
        nodes.arrange(RIGHT, buff=0.45).move_to(UP * 0.3)
        arrows = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), color=MUTED, buff=0.15) for i in range(len(nodes) - 1)])
        caption = Text(segment["visual"].get("caption", ""), font=FONT, font_size=30, color=INK).next_to(nodes, DOWN, buff=0.65)
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.18) for n in nodes], lag_ratio=0.16), run_time=1.2)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=1.0)
        if segment["visual"].get("caption"):
            self.play(FadeIn(caption), run_time=0.7)
        self.hold(segment, 2.9)
        self.clear_stage()

    def visual_tokens(self, segment):
        labels = segment["visual"]["tokens"]
        tokens = VGroup(*[self.token(t, COLORS[i % len(COLORS)]) for i, t in enumerate(labels)])
        tokens.arrange(RIGHT, buff=0.26).move_to(UP * 0.65)
        focus_idx = segment["visual"].get("focus", 0)
        note = Text(segment["visual"].get("note", ""), font=FONT, font_size=31, color=INK)
        note.set(width=10.5).next_to(tokens, DOWN, buff=0.7)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tokens], lag_ratio=0.12), run_time=1.2)
        self.play(Indicate(tokens[focus_idx], color=COLORS[focus_idx % len(COLORS)]), FadeIn(note), run_time=1.0)
        self.hold(segment, 2.2)
        self.clear_stage()

    def visual_cache(self, segment):
        v = segment["visual"]
        before = VGroup(*[self.token(t, BLUE, 1.25) for t in v["before"]]).arrange(RIGHT, buff=0.15).move_to(UP * 1.15)
        cache = VGroup(*[self.token(t, TEAL, 1.25) for t in v["cache"]]).arrange(RIGHT, buff=0.15).move_to(ORIGIN)
        new = self.token(v["new"], CORAL, 1.35).move_to(DOWN * 1.05 + LEFT * 1.1)
        arrow = Arrow(new.get_top(), cache[-1].get_bottom(), color=CORAL, buff=0.2)
        label = Text(v.get("caption", ""), font=FONT, font_size=29, color=INK).move_to(DOWN * 1.65)
        self.play(FadeIn(before), run_time=0.7)
        self.play(TransformFromCopy(before, cache), run_time=1.0)
        self.play(FadeIn(new), GrowArrow(arrow), FadeIn(label), run_time=1.1)
        self.hold(segment, 2.8)
        self.clear_stage()

    def visual_loop(self, segment):
        labels = segment["visual"]["steps"]
        positions = [UP * 1.1, RIGHT * 3 + DOWN * 0.1, DOWN * 1.35, LEFT * 3 + DOWN * 0.1]
        nodes = VGroup(*[self.token(labels[i], COLORS[i], 2.05).move_to(positions[i]) for i in range(len(labels))])
        arrows = VGroup(*[Arrow(nodes[i].get_center(), nodes[(i + 1) % len(nodes)].get_center(), color=MUTED, buff=0.65) for i in range(len(nodes))])
        center = Text(segment["visual"].get("center", ""), font=FONT, font_size=31, color=INK).move_to(ORIGIN)
        self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.16), FadeIn(center), run_time=1.4)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=1.2)
        self.hold(segment, 2.6)
        self.clear_stage()

    def visual_bars(self, segment):
        items = segment["visual"]["items"]
        rows = VGroup()
        max_value = max(i["value"] for i in items)
        for idx, item in enumerate(items):
            name = Text(item["label"], font=FONT, font_size=25, color=INK)
            bar = Rectangle(width=5.5 * item["value"] / max_value, height=0.38, fill_color=COLORS[idx], fill_opacity=0.72, stroke_width=0)
            value = Text(item.get("text", str(item["value"])), font=FONT, font_size=23, color=INK)
            rows.add(VGroup(name, bar, value).arrange(RIGHT, buff=0.28, aligned_edge=LEFT))
        rows.arrange(DOWN, buff=0.27, aligned_edge=LEFT).move_to(UP * 0.4)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.12), run_time=1.4)
        self.hold(segment, 1.4)
        self.clear_stage()

    def visual_formula(self, segment):
        v = segment["visual"]
        formula = Text(v["formula"], font=FONT, font_size=34, color=INK)
        formula.set(width=11.2).move_to(UP * 1.0)
        cards = VGroup(*[self.card(i["title"], i["body"], COLORS[n], width=3.15, height=1.55) for n, i in enumerate(v["items"])])
        cards.scale(0.86).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.35)
        self.play(Write(formula), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.14), run_time=1.3)
        self.hold(segment, 2.5)
        self.clear_stage()

    def visual_trace(self, segment):
        items = segment["visual"]["items"]
        rows = VGroup()
        for idx, item in enumerate(items):
            left = self.token(item["label"], COLORS[idx % len(COLORS)], width=2.15)
            right = Text(item["text"], font=FONT, font_size=25, color=INK)
            right.set(max_width=7.6)
            rows.add(VGroup(left, right).arrange(RIGHT, buff=0.38))
        rows.arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(UP * 0.25)
        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.18) for row in rows], lag_ratio=0.16), run_time=1.6)
        self.hold(segment, 1.6)
        self.clear_stage()

    def visual_summary(self, segment):
        points = VGroup()
        for idx, text in enumerate(segment["visual"]["points"], start=1):
            item = Text(f"{idx}. {text}", font=FONT, font_size=28, color=COLORS[(idx - 1) % len(COLORS)], line_spacing=0.88)
            item.set(max_width=10.6)
            points.add(item)
        points.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to(UP * 0.3)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in points], lag_ratio=0.16), run_time=1.5)
        self.hold(segment, 1.5)
