# 短视频脚本：Q/K/V 到底怎么理解？

## 选题

本期讲：用“提问、匹配、取内容”理解 Attention。

## 开头 0-5 秒

```text
别一上来背 Attention 公式，先搞懂 Q、K、V 分别在干嘛。
```

## 第一段 5-25 秒

```text
Q 是当前 token 想找什么，K 是其他 token 怎么被匹配，V 是其他 token 真正提供什么内容。
```

画面：Q 问，K 匹配，V 回答。

## 第二段 25-70 秒

```text
Attention 的过程是：Q 和 K 算相关性，除以根号 d 稳定数值，再 softmax 成权重，最后用权重加权 V。
所以它的本质是先匹配，再取内容。
```

画面：QK -> scale -> softmax -> weighted V。

## 第三段 70-100 秒

```text
Decoder 里还要加 causal mask，保证当前位置只能看历史，不能偷看未来。
训练时完整序列已知，可以并行算；推理时才逐 token 生成。
```

## 结尾

```text
一句话记住：Attention 不是玄学，就是动态从上下文取信息。
```

