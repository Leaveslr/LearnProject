from __future__ import annotations

from pathlib import Path

import numpy as np
from manim import *

from content import SEGMENTS


ROOT = Path(__file__).resolve().parent
FONT = "PingFang SC"
INK = "#222222"
MUTED = "#666A73"
PAPER = "#F7F7F2"
TEAL = "#2A9D8F"
CORAL = "#E76F51"
AMBER = "#E9C46A"
BLUE = "#457B9D"
VIOLET = "#7C5CFF"


class TransformerAttentionForBeginners(Scene):
    def construct(self):
        self.camera.background_color = PAPER
        self.title_text = Text("Transformer Attention 机制", font=FONT, font_size=38, color=INK)
        self.title_text.to_edge(UP, buff=0.32)
        self.add(self.title_text)
        self.current_subtitle = None

        self.segment(0, self.opening)
        self.segment(1, self.context_example)
        self.segment(2, self.naive_problem)
        self.segment(3, self.core_intuition)
        self.segment(4, self.qkv_roles)
        self.segment(5, self.matching_scores)
        self.segment(6, self.softmax_weights)
        self.segment(7, self.pass_values)
        self.segment(8, self.contextual_embedding)
        self.segment(9, self.formula_scene)
        self.segment(10, self.multi_head)
        self.segment(11, self.mask_scene)
        self.segment(12, self.summary_scene)

    def segment(self, idx, builder):
        audio = ROOT / "assets" / "audio" / f"seg_{SEGMENTS[idx]['id']}.wav"
        if audio.exists():
            self.add_sound(str(audio))
        self.set_subtitle(SEGMENTS[idx]["subtitle"])
        builder(float(SEGMENTS[idx]["duration"]))

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
        self.play(
            *[FadeOut(mob) for mob in list(self.mobjects) if mob not in keep],
            run_time=0.35,
        )
        self.bring_to_front(self.current_subtitle)

    def token(self, text, color=BLUE, width=1.45):
        box = RoundedRectangle(
            corner_radius=0.15,
            width=width,
            height=0.62,
            fill_color=color,
            fill_opacity=0.16,
            stroke_color=color,
            stroke_width=2,
        )
        label = Text(text, font=FONT, font_size=26, color=INK)
        return VGroup(box, label)

    def opening(self, duration):
        question = Text("词语如何读懂上下文？", font=FONT, font_size=48, color=INK)
        question.move_to(UP * 0.7)
        answer = Text("Attention = 给每个词一套“参考别人”的机制", font=FONT, font_size=31, color=TEAL)
        answer.next_to(question, DOWN, buff=0.5)
        self.play(Write(question), run_time=1.0)
        self.play(FadeIn(answer, shift=UP * 0.2), run_time=1.0)
        self.wait(duration - 2.0)
        self.clear_stage()

    def context_example(self, duration):
        words = ["苹果", "手机", "很", "快"]
        tokens = VGroup(*[self.token(w, color=[CORAL, TEAL, AMBER, BLUE][i]) for i, w in enumerate(words)])
        tokens.arrange(RIGHT, buff=0.28).move_to(UP * 1.2)
        lone = self.token("苹果", color=CORAL, width=1.7).move_to(DOWN * 0.4 + LEFT * 2.3)
        fruit = Text("水果？", font=FONT, font_size=30, color=CORAL).next_to(lone, DOWN, buff=0.35)
        brand = Text("品牌？", font=FONT, font_size=30, color=TEAL).next_to(lone, RIGHT, buff=1.3)
        arrow = Arrow(lone.get_right(), brand.get_left(), color=TEAL, buff=0.15)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tokens], lag_ratio=0.12), run_time=1.2)
        self.play(FadeIn(lone), FadeIn(fruit), run_time=0.8)
        self.play(GrowArrow(arrow), FadeIn(brand), Indicate(tokens[1], color=TEAL), run_time=1.3)
        self.wait(duration - 3.3)
        self.clear_stage()

    def naive_problem(self, duration):
        left = self.token("只看自己", color=CORAL, width=2.2).move_to(LEFT * 3 + UP * 0.6)
        right = self.token("参考上下文", color=TEAL, width=2.5).move_to(RIGHT * 2.7 + UP * 0.6)
        bad = Text("意思模糊", font=FONT, font_size=31, color=CORAL).next_to(left, DOWN, buff=0.5)
        good = Text("意思被校准", font=FONT, font_size=31, color=TEAL).next_to(right, DOWN, buff=0.5)
        bridge = Arrow(left.get_right(), right.get_left(), color=AMBER, buff=0.2)
        self.play(FadeIn(left), FadeIn(bad), run_time=0.9)
        self.play(GrowArrow(bridge), FadeIn(right), FadeIn(good), run_time=1.1)
        self.wait(duration - 2.0)
        self.clear_stage()

    def core_intuition(self, duration):
        center = self.token("苹果", color=CORAL, width=1.7).move_to(ORIGIN)
        words = VGroup(
            self.token("我", BLUE, 1.15),
            self.token("手机", TEAL, 1.45),
            self.token("很", AMBER, 1.15),
            self.token("快", VIOLET, 1.15),
        )
        positions = [LEFT * 3 + UP, RIGHT * 3 + UP, LEFT * 3 + DOWN * 0.7, RIGHT * 3 + DOWN * 0.7]
        for mob, pos in zip(words, positions):
            mob.move_to(pos)
        arrows = VGroup(*[Arrow(center.get_center(), mob.get_center(), color=BLUE, buff=0.45) for mob in words])
        caption = Text("每个词都在问：谁能帮我？", font=FONT, font_size=34, color=INK).to_edge(UP, buff=1.15)
        self.play(FadeIn(center), FadeIn(caption), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(w) for w in words], lag_ratio=0.12), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08), run_time=1.2)
        self.wait(duration - 3.0)
        self.clear_stage()

    def qkv_roles(self, duration):
        cards = VGroup(
            self.role_card("Query", "我想找什么线索", CORAL),
            self.role_card("Key", "我能提供什么线索", TEAL),
            self.role_card("Value", "真正传递的信息", BLUE),
        ).arrange(RIGHT, buff=0.45).move_to(UP * 0.45)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.25) for card in cards], lag_ratio=0.18), run_time=1.6)
        formula = Text("先匹配 Q 和 K，再按权重混合 V", font=FONT, font_size=31, color=INK)
        formula.next_to(cards, DOWN, buff=0.65)
        self.play(FadeIn(formula), run_time=0.8)
        self.wait(duration - 2.4)
        self.clear_stage()

    def role_card(self, title, body, color):
        rect = RoundedRectangle(
            corner_radius=0.12,
            width=3.35,
            height=2.0,
            fill_color=color,
            fill_opacity=0.14,
            stroke_color=color,
            stroke_width=2,
        )
        t = Text(title, font=FONT, font_size=34, color=color)
        b = Text(body, font=FONT, font_size=24, color=INK)
        b.set(width=2.8)
        return VGroup(rect, VGroup(t, b).arrange(DOWN, buff=0.25).move_to(rect.get_center()))

    def matching_scores(self, duration):
        query = self.role_card("Query: 苹果", "我该怎么理解？", CORAL).scale(0.8).move_to(LEFT * 3.2 + UP * 0.7)
        keys = VGroup(
            self.token("苹果", CORAL, 1.45),
            self.token("手机", TEAL, 1.45),
            self.token("很", AMBER, 1.15),
            self.token("快", BLUE, 1.15),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 2.9 + UP * 0.2)
        scores = VGroup(
            Text("0.25", font=FONT, font_size=25, color=MUTED),
            Text("0.70", font=FONT, font_size=34, color=TEAL),
            Text("0.05", font=FONT, font_size=25, color=MUTED),
            Text("0.15", font=FONT, font_size=25, color=MUTED),
        )
        for s, k in zip(scores, keys):
            s.next_to(k, LEFT, buff=0.45)
        arrows = VGroup(*[Arrow(query.get_right(), k.get_left(), color=TEAL if i == 1 else "#B8BEC8", buff=0.2) for i, k in enumerate(keys)])
        self.play(FadeIn(query), FadeIn(keys), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08), FadeIn(scores), run_time=1.5)
        self.play(Indicate(keys[1], color=TEAL), Indicate(scores[1], color=TEAL), run_time=1.0)
        self.wait(duration - 3.5)
        self.clear_stage()

    def softmax_weights(self, duration):
        labels = ["苹果", "手机", "很", "快"]
        values = [0.18, 0.62, 0.08, 0.12]
        bars = VGroup()
        for label, val, color in zip(labels, values, [CORAL, TEAL, AMBER, BLUE]):
            name = Text(label, font=FONT, font_size=25, color=INK)
            bar = Rectangle(width=5.2 * val, height=0.38, fill_color=color, fill_opacity=0.75, stroke_width=0)
            num = Text(f"{val:.2f}", font=FONT, font_size=23, color=INK)
            row = VGroup(name, bar, num).arrange(RIGHT, buff=0.28, aligned_edge=LEFT)
            bars.add(row)
        bars.arrange(DOWN, buff=0.26, aligned_edge=LEFT).move_to(UP * 0.45)
        total = Text("Softmax 后：权重加起来 = 1", font=FONT, font_size=31, color=TEAL).next_to(bars, DOWN, buff=0.55)
        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.2) for row in bars], lag_ratio=0.12), run_time=1.4)
        self.play(FadeIn(total), run_time=0.8)
        self.wait(duration - 2.2)
        self.clear_stage()

    def pass_values(self, duration):
        apple = self.token("苹果", CORAL, 1.55).move_to(LEFT * 3.4 + UP * 0.6)
        phone_value = self.role_card("Value: 手机", "品牌 / 设备 / 科技", TEAL).scale(0.78).move_to(RIGHT * 2.7 + UP * 0.6)
        mix = Text("0.62 x Value(手机)", font=FONT, font_size=34, color=TEAL).move_to(DOWN * 0.65)
        arrow1 = Arrow(phone_value.get_left(), apple.get_right(), color=TEAL, buff=0.25)
        self.play(FadeIn(apple), FadeIn(phone_value), run_time=1.0)
        self.play(GrowArrow(arrow1), FadeIn(mix), run_time=1.3)
        glow = SurroundingRectangle(apple, color=TEAL, buff=0.12)
        self.play(Create(glow), run_time=0.7)
        self.wait(duration - 3.0)
        self.clear_stage()

    def contextual_embedding(self, duration):
        before = self.token("苹果", CORAL, 1.55).move_to(LEFT * 3 + UP * 0.4)
        after = self.token("苹果手机语境", TEAL, 3.0).move_to(RIGHT * 2.6 + UP * 0.4)
        arrow = Arrow(before.get_right(), after.get_left(), color=AMBER, buff=0.25)
        delta = Text("表示更新", font=FONT, font_size=27, color=AMBER).next_to(arrow, UP, buff=0.15)
        note = Text("Attention 输出的是“更新后的表示”", font=FONT, font_size=32, color=INK).move_to(DOWN * 0.75)
        self.play(FadeIn(before), run_time=0.7)
        self.play(GrowArrow(arrow), FadeIn(delta), TransformFromCopy(before, after), run_time=1.4)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(duration - 2.9)
        self.clear_stage()

    def formula_scene(self, duration):
        formula = Text(
            "Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V",
            font=FONT,
            font_size=33,
            color=INK,
        ).move_to(UP * 0.95)
        steps = VGroup(
            self.role_card("1. 匹配", "QK^T：谁和谁相关", CORAL),
            self.role_card("2. 归一化", "softmax：变成权重", AMBER),
            self.role_card("3. 求和", "乘 V：传递信息", TEAL),
        ).scale(0.72).arrange(RIGHT, buff=0.25).move_to(DOWN * 0.45)
        self.play(Write(formula), run_time=1.3)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in steps], lag_ratio=0.15), run_time=1.6)
        self.wait(duration - 2.9)
        self.clear_stage()

    def multi_head(self, duration):
        center = self.token("同一句话", BLUE, 2.0).move_to(ORIGIN)
        heads = VGroup(
            self.role_card("Head 1", "品牌关系", TEAL),
            self.role_card("Head 2", "修饰关系", CORAL),
            self.role_card("Head 3", "位置关系", VIOLET),
        ).scale(0.68).arrange(RIGHT, buff=0.32).to_edge(UP, buff=1.2)
        arrows = VGroup(*[Arrow(center.get_top(), h.get_bottom(), color=[TEAL, CORAL, VIOLET][i], buff=0.18) for i, h in enumerate(heads)])
        out = Text("多个角度同时看上下文", font=FONT, font_size=33, color=INK).move_to(DOWN * 1.3)
        self.play(FadeIn(center), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.2) for h in heads], lag_ratio=0.12), run_time=1.1)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), FadeIn(out), run_time=1.4)
        self.wait(duration - 3.1)
        self.clear_stage()

    def mask_scene(self, duration):
        grid = VGroup()
        n = 5
        cell_size = 0.58
        for r in range(n):
            for c in range(n):
                allowed = c <= r
                cell = Square(
                    side_length=cell_size,
                    fill_color=TEAL if allowed else CORAL,
                    fill_opacity=0.75 if allowed else 0.18,
                    stroke_color=WHITE,
                    stroke_width=1.5,
                )
                cell.move_to(np.array([(c - 2) * cell_size, (2 - r) * cell_size, 0]))
                grid.add(cell)
        grid.move_to(UP * 0.25)
        past = Text("能看：过去和当前", font=FONT, font_size=29, color=TEAL).next_to(grid, LEFT, buff=0.65)
        future = Text("挡住：未来", font=FONT, font_size=29, color=CORAL).next_to(grid, RIGHT, buff=0.65)
        self.play(FadeIn(grid, scale=0.96), FadeIn(past), FadeIn(future), run_time=1.4)
        self.wait(duration - 1.4)
        self.clear_stage()

    def summary_scene(self, duration):
        points = VGroup(
            Text("1. Attention：找相关词", font=FONT, font_size=34, color=TEAL),
            Text("2. Value：把有用信息传过去", font=FONT, font_size=34, color=CORAL),
            Text("3. Multi-Head：从多个角度理解", font=FONT, font_size=34, color=BLUE),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(UP * 0.35)
        closing = Text("公式只是这三个动作的压缩写法", font=FONT, font_size=31, color=INK).next_to(points, DOWN, buff=0.6)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in points], lag_ratio=0.16), run_time=1.5)
        self.play(FadeIn(closing), run_time=0.8)
        self.wait(duration - 2.3)
