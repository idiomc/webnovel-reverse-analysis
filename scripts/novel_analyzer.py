#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Novel Reverse Analyzer — Webnovel DNA Extractor
Usage: python novel_analyzer.py <novel.txt> [--encoding auto|utf-8|gbk]
"""

import sys
import os
import re
import json
import argparse
from collections import Counter, defaultdict


def detect_encoding(filepath):
    """Auto-detect file encoding."""
    for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030']:
        try:
            with open(filepath, 'r', encoding=enc, errors='ignore') as f:
                sample = f.read(5000)
                if len(sample) > 100 and len(re.findall(r'[\u4e00-\u9fff]', sample)) > 50:
                    return enc
        except:
            continue
    return 'utf-8'


def analyze_novel(filepath, encoding='auto'):
    if encoding == 'auto':
        encoding = detect_encoding(filepath)
    
    with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
        text = f.read()
    
    total_chars = len(text)
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    
    # Chapter detection
    chapter_pattern = re.compile(r'\n\s*第([一二三四五六七八九十百千零\d]+)章\s+(.*?)(?:\n|\r)')
    chapters = chapter_pattern.findall(text)
    chapter_count = len(chapters)
    
    # Volume detection
    volume_pattern = re.compile(r'第([一二三四五六七八九十百千]+)卷\s+(.+?)(?:\n|\r)')
    volumes = volume_pattern.findall(text)
    
    # Chapter length distribution
    raw_splits = re.split(r'(\n\s*第[一二三四五六七八九十百千零\d]+章\s+.+?\n)', text)
    chapter_data = []
    for i in range(1, len(raw_splits), 2):
        if i+1 < len(raw_splits):
            content = raw_splits[i+1]
            chapter_data.append({
                'title': raw_splits[i].strip(),
                'chars': len(re.findall(r'[\u4e00-\u9fff]', content))
            })
    
    chapter_lengths = [c['chars'] for c in chapter_data]
    avg_chapter = sum(chapter_lengths) / len(chapter_lengths) if chapter_lengths else 0
    
    # Character extraction
    name_candidates = re.findall(r'([\u4e00-\u9fff]{2,4})(?:说|道|问|答|喊|叫|看|望|盯|想|觉得|感觉|知道|明白|记得|忘记|点头|摇头|站|坐|走|跑|躺|蹲|趴|笑|哭|怒|皱眉|瞪|瞅|瞧|瞥)', text)
    stop_words = {'自己', '什么', '怎么', '没有', '知道', '看着', '觉得', '感觉', '明白', '以为', '认为', '心想', '喃喃', '说道', '大声', '小声', '轻声', '冷笑', '苦笑', '微笑', '嘿嘿', '哈哈', '忽然', '突然', '缓缓', '慢慢', '猛地', '用力', '死死', '紧紧', '连忙', '赶紧', '转身', '抬头', '低头', '回头看', '转过头', '摇摇头', '点点头', '伸出手', '收回', '放下', '拿起', '掏出'}
    filtered = [(name, count) for name, count in Counter(name_candidates).most_common(100) if name not in stop_words and len(name) >= 2]
    top_names = filtered[:50]
    
    # Protagonist = most frequent + appears in first chapter
    first_chapter = text[:5000]
    protagonist = top_names[0][0] if top_names else "Unknown"
    
    # Supporting tiers
    core = [n for n, c in top_names if c > 2000]
    major = [n for n, c in top_names if 500 <= c <= 2000]
    minor = [n for n, c in top_names if 100 <= c < 500]
    cameo = [n for n, c in top_names if c < 100]
    
    # Style DNA
    sentences = re.split(r'[。！？；\n]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    short_sentences = [s for s in sentences if 5 <= len(s) <= 25]
    short_rate = len(short_sentences) / len(sentences) if sentences else 0
    
    body_reactions = {
        '瞳孔': text.count('瞳孔'), '头皮发麻': text.count('头皮发麻'), '头皮': text.count('头皮'),
        '发抖': text.count('发抖'), '颤抖': text.count('颤抖'), '哆嗦': text.count('哆嗦'),
        '冷汗': text.count('冷汗'), '冒汗': text.count('冒汗'), '恶心': text.count('恶心'),
        '呕吐': text.count('呕吐'), '窒息': text.count('窒息'), '心跳': text.count('心跳'),
        '呼吸急促': text.count('呼吸急促'), '呼吸': text.count('呼吸'), '抽搐': text.count('抽搐'),
        '僵硬': text.count('僵硬'), '发麻': text.count('发麻'), '刺痛': text.count('刺痛'),
        '汗毛': text.count('汗毛'), '鸡皮疙瘩': text.count('鸡皮疙瘩'), '青筋': text.count('青筋'),
        '血丝': text.count('血丝'), '胃': text.count('胃'), '肠子': text.count('肠子'),
        '肚子': text.count('肚子'), '头疼': text.count('头疼'), '头疼欲裂': text.count('头疼欲裂'),
    }
    
    vulgar = {'屁': text.count('屁'), '艹': text.count('艹'), '他妈': text.count('他妈'), '老子': text.count('老子'), '杂种': text.count('杂种'), '狗娘': text.count('狗娘'), '废物': text.count('废物'), '蠢': text.count('蠢'), '傻': text.count('傻'), '疯': text.count('疯'), '癫': text.count('癫'), '神经病': text.count('神经病')}
    
    emotion = {'恐惧': text.count('恐惧'), '害怕': text.count('害怕'), '绝望': text.count('绝望'), '痛苦': text.count('痛苦'), '迷惘': text.count('迷惘'), '迷茫': text.count('迷茫'), '困惑': text.count('困惑'), '憎恨': text.count('憎恨'), '愤怒': text.count('愤怒'), '悲伤': text.count('悲伤'), '希望': text.count('希望'), '开心': text.count('开心'), '高兴': text.count('高兴'), '笑': text.count('笑'), '哭': text.count('哭')}
    
    narrative = {'不知道': text.count('不知道'), '分不清': text.count('分不清'), '假的': text.count('假的'), '真的': text.count('真的'), '幻觉': text.count('幻觉'), '清醒': text.count('清醒'), '陷入': text.count('陷入'), '回过神来': text.count('回过神来'), '猛地': text.count('猛地'), '忽然': text.count('忽然'), '刹那间': text.count('刹那间'), '下一刻': text.count('下一刻')}
    
    horror = {'血': text.count('血'), '肉': text.count('肉'), '骨头': text.count('骨头'), '腐烂': text.count('腐烂'), '尸体': text.count('尸体'), '死': text.count('死'), '杀': text.count('杀'), '吃': text.count('吃'), '啃': text.count('啃'), '嚼': text.count('嚼'), '咬': text.count('咬'), '吞': text.count('吞'), '撕裂': text.count('撕裂'), '碾碎': text.count('碾碎'), '捣烂': text.count('捣烂'), '蠕动': text.count('蠕动'), '黏糊': text.count('黏糊'), '脓': text.count('脓'), '蛆': text.count('蛆'), '虫子': text.count('虫子')}
    
    # Power system detection
    cultivation = {'筑基': text.count('筑基'), '金丹': text.count('金丹'), '元婴': text.count('元婴'), '化神': text.count('化神'), '飞升': text.count('飞升'), '成仙': text.count('成仙')}
    sequence = {'序列': text.count('序列'), '途径': text.count('途径'), '魔药': text.count('魔药'), '扮演法': text.count('扮演法'), '非凡特性': text.count('非凡特性')}
    
    power_type = 'none'
    if sum(cultivation.values()) > 10:
        power_type = 'cultivation'
    elif sum(sequence.values()) > 10:
        power_type = 'sequence'
    elif sum(horror.values()) > 1000:
        power_type = 'custom'
    
    # ESP detection
    esp = []
    modern_keywords = text.count('医院') + text.count('学校') + text.count('医生') + text.count('警察') + text.count('精神病')
    if modern_keywords > 500:
        esp.append({"element": "现代世界元素", "uniqueness": 4, "copy_risk": "adaptable"})
    
    if sum(cultivation.values()) == 0 and sum(sequence.values()) == 0 and chinese_chars > 1000000:
        esp.append({"element": "无传统境界体系", "uniqueness": 5, "copy_risk": "forbidden"})
    
    if text.count('分不清') > 30:
        esp.append({"element": "认知崩塌机制", "uniqueness": 5, "copy_risk": "forbidden"})
    
    # Build report
    report = {
        'metadata': {
            'total_chars': total_chars,
            'chinese_chars': chinese_chars,
            'estimated_word_count': round(chinese_chars * 1.15),
            'chapter_count': chapter_count,
            'volume_count': len(volumes),
            'encoding': encoding,
            'file_size_mb': round(os.path.getsize(filepath) / 1024 / 1024, 2)
        },
        'structure': {
            'avg_chapter_chars': round(avg_chapter, 0),
            'min_chapter': min(chapter_lengths) if chapter_lengths else 0,
            'max_chapter': max(chapter_lengths) if chapter_lengths else 0,
            'chapter_count': len(chapter_data)
        },
        'characters': {
            'protagonist': {'name': protagonist, 'mentions': top_names[0][1] if top_names else 0},
            'top_30_names': top_names[:30],
            'supporting_tiers': {'core': core, 'major': major, 'minor': minor, 'cameo': cameo}
        },
        'setting': {
            'power_system': {'type': power_type, 'cultivation': cultivation, 'sequence': sequence},
            'weird_entities': {'body_horror': {k: v for k, v in horror.items() if v > 50 and k in ['蠕动', '腐烂', '脓', '蛆']}, 'cognitive': {k: v for k, v in narrative.items() if v > 50}}
        },
        'style_dna': {
            'short_sentence_rate': round(short_rate, 4),
            'total_sentences': len(sentences),
            'short_sentences': len(short_sentences),
            'body_reactions': body_reactions,
            'vulgar_language': vulgar,
            'emotion_words': emotion,
            'narrative_patterns': narrative,
            'horror_elements': horror
        }
    }
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Novel Reverse Analyzer')
    parser.add_argument('filepath', help='Path to novel text file')
    parser.add_argument('--encoding', default='auto', help='File encoding (auto/utf-8/gbk)')
    parser.add_argument('--output', default='.', help='Output directory')
    args = parser.parse_args()
    
    if not os.path.exists(args.filepath):
        print(f"Error: File not found: {args.filepath}")
        sys.exit(1)
    
    report = analyze_novel(args.filepath, args.encoding)
    
    basename = os.path.splitext(os.path.basename(args.filepath))[0]
    json_path = os.path.join(args.output, f"{basename}_analysis.json")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"Analysis complete: {json_path}")
    print(f"Chapters: {report['structure']['chapter_count']}")
    print(f"Chinese chars: {report['metadata']['chinese_chars']}")
    print(f"Short sentence rate: {report['style_dna']['short_sentence_rate']:.2%}")
    print(f"Protagonist: {report['characters']['protagonist']['name']} ({report['characters']['protagonist']['mentions']} mentions)")


if __name__ == '__main__':
    main()
