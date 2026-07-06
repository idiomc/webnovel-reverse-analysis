---
name: webnovel-reverse-analysis
description: Reverse-analyze existing web novels to extract their structural DNA — character matrices, setting systems, style fingerprints, emotional engines, and unique selling points. Use when the user wants to deeply parse, deconstruct, or fuse existing novels. Triggers on: "解析小说", "逆向分析", "提取DNA", "小说融合", "分析笔风", "解构设定", "全文扫描", "提取人物图谱", "分析情感引擎", "novel reverse analysis", "extract novel DNA", "parse webnovel".
---

# Webnovel Reverse Analysis

Reverse-engineer existing web novels to extract their composable DNA for fusion, imitation, or competitive analysis.

## When to Use

- User sends a novel file and says "读一下", "分析一下", "提取DNA"
- User wants to fuse multiple novels into a new one
- User wants to understand why a novel works (structure, pacing, characters)
- User wants to avoid copying exclusive selling points
- User wants to create a "style fingerprint" of an author

## Workflow

### Phase 1: Ingestion

1. **Copy file to workspace** — Never operate on temp files directly
2. **Detect encoding** — Try UTF-8 first, then GBK/GB2312/GB18030
3. **Validate integrity** — Check total chars vs expected. If <50% of file size in chars, encoding is wrong
4. **Split chapters** — Match patterns: `第[一二三四五六七八九十百千零\d]+章`, `Chapter \d+`, `第\d+章`

### Phase 2: Structural Anatomy

| Dimension | Tool | Output |
|-----------|------|--------|
| Chapter count | Regex split | Integer |
| Avg chapter length | Chinese chars / chapters | Integer |
| Length distribution | Min/max/percentiles | JSON |
| Volume structure | `第X卷` markers | List |
| Pacing sample | Early 5 + Mid 5 + Late 5 chapters | JSON |

### Phase 3: Character Matrix

1. **Extract name candidates** — Regex: `([\u4e00-\u9fff]{2,4})(?:说|道|看|想|觉得|知道|点头|摇头|站|坐|走|笑|哭|怒|喊|问|答)`
2. **Filter stop words** — Remove: 自己, 什么, 怎么, 知道, 看着, 觉得, 忽然, 猛地, 连忙, 转身, 回头, etc.
3. **Top-N names** — Counter.most_common(50)
4. **Protagonist detection** — Highest frequency + first-chapter appearance
5. **Supporting cast** — Frequency tiers: >2000 (core), 500-2000 (major), 100-500 (minor), <100 (cameo)
6. **Relationship inference** — Co-occurrence within 50-char window

### Phase 4: Setting System

Scan for categorized keywords:

**Cultivation/Power System**
- Traditional: 筑基, 金丹, 元婴, 化神, 飞升
- Alternative: 序列, 途径, 魔药, 扮演法, 非凡特性
- Custom: Any repeated 2-4 char terms near 功法/修炼/升级

**Weird/Eldritch Entities**
- Body horror: 黑太岁, 蠕动, 寄生, 腐烂, 脓, 蛆
- Cognitive: 幻觉, 分不清, 认知, 污染, 侵蚀
- Named entities: Proper nouns appearing >50 times

**World Levels**
- Surface world keywords
- Hidden world keywords
- Divine/high-dimensional keywords

### Phase 5: Style DNA

| Metric | How to Measure | Threshold |
|--------|---------------|-----------|
| Short sentence rate | Split by [。！？；\n], count 5-25 chars | >30% = high |
| Body reaction frequency | Count 瞳孔, 头皮, 冷汗, 颤抖, 胃,  etc. | >200 = high |
| Vulgar language density | Count 屁, 艹, 他妈, 老子, 杂种 | >50 = coarse |
| Dialogue density | Count quotation marks / total sentences | >20% = dialogue-heavy |
| Sudden-action adverbs | 猛地, 忽然, 下一刻, 刹那间 | >500 = pulse pacing |
| Cognitive uncertainty | 不知道, 分不清, 幻觉, 假的 | >1000 = uncertainty-driven |

### Phase 6: Emotional Engine

**Core emotion ratio** (per 1000 Chinese chars):
- Hope: 希望, 期待, 相信, 坚持
- Despair: 绝望, 痛苦, 死, 杀
- Fear: 恐惧, 害怕, 头皮发麻, 冷汗
- Absurdity: 笑, 疯, 癫, 傻

**Narrative tension pattern**:
- "不知道" frequency = information asymmetry driver
- "分不清" frequency = cognitive collapse driver
- "真的/假的" ratio = reality-uncertainty index

### Phase 7: Exclusive Selling Points (ESPs)

Identify elements with **high uniqueness** (not found in generic novels):

| Check | Method |
|-------|--------|
| Dual-world? | Count modern keywords (医院, 学校, 医生, 警察) |
| No-cultivation? | Count 筑基/金丹/元婴 = 0? |
| Organization-growth? | Count named organization mentions vs individual |
| Passive-protagonist? | Protagonist is victim of system, not driver |
| Anti-ascension? | 成仙/飞升/成神 frequency < 10 |
| Body-horror-as-daily? | 吃/肉/血/蠕动 in mundane contexts |

### Phase 8: Collision Report (for Fusion)

When user wants to fuse multiple novels:

1. **Extract ESPs from each novel**
2. **Mark collision zones** — Any ESP appearing in >1 source = collision risk
3. **Mark forbidden clones** — Elements with ★★★★★ uniqueness = NEVER copy
4. **Mark fusion-ready elements** — Elements with ★★☆☆☆ uniqueness = free to use
5. **Generate hybrid formula** — Pick one structural DNA from each source, ensuring no collision

## Output Format

All analysis MUST be saved as:
- `{novel_name}_深度解析_数据.json` — Raw data
- `{novel_name}_深度解析报告.md` — Human-readable report

## Anti-AI Detection Rules

When generating analysis reports, AVOID:
1. "不是…而是…" constructions
2. Excessive parallelism (不是A，不是B，而是C)
3. Overuse of 破折号
4. Abstract summarization without concrete data
5. "从某种意义上说" / "从某种角度来看"
6. Three-paragraph structure (introduction → analysis → conclusion)
7. AI-typical words:  delve,  indeed,  it is worth noting,  undoubtedly

Prefer: Short sentences, data-first, concrete examples, raw counts.
