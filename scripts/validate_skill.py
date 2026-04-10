#!/usr/bin/env python3
"""
.validate_skill.py — 验证生成的 .skill 文件结构完整性和格式正确性

用法:
    python validate_skill.py <skill_file_path>

验证项:
    1. 文件存在且可读
    2. YAML frontmatter 完整性
    3. 必须章节是否存在
    4. 伦理声明是否存在
    5. 各章节内容是否为空（警告级）
"""

import sys
import re
import os


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """解析 YAML frontmatter，返回 (metadata_dict, body_content)"""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter_str = match.group(1)
    body = match.group(2)

    # 简易 YAML 解析（不依赖第三方库）
    metadata = {}
    for line in frontmatter_str.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if value.startswith('[') and value.endswith(']'):
                # 简易数组解析
                value = [v.strip().strip('"').strip("'") for v in value[1:-1].split(',')]
            metadata[key] = value

    return metadata, body


def validate_skill(file_path: str) -> dict:
    """验证 .skill 文件，返回验证结果"""
    result = {
        'passed': True,
        'errors': [],
        'warnings': [],
        'info': []
    }

    # 1. 文件存在性
    if not os.path.exists(file_path):
        result['errors'].append(f'文件不存在: {file_path}')
        result['passed'] = False
        return result

    if not file_path.endswith('.skill') and not file_path.endswith('.md'):
        result['warnings'].append('文件扩展名不是 .skill 或 .md，可能影响兼容性')

    # 2. 读取内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        result['errors'].append(f'文件读取失败: {e}')
        result['passed'] = False
        return result

    if not content.strip():
        result['errors'].append('文件内容为空')
        result['passed'] = False
        return result

    # 3. Frontmatter 验证
    metadata, body = parse_frontmatter(content)

    if not metadata:
        result['errors'].append('缺少 YAML frontmatter（--- 之间的元数据区域）')
        result['passed'] = False
    else:
        required_meta = ['name', 'version', 'generated_at']
        for key in required_meta:
            if key not in metadata:
                result['errors'].append(f'Frontmatter 缺少必需字段: {key}')
                result['passed'] = False
            elif not metadata[key]:
                result['errors'].append(f'Frontmatter 字段 {key} 值为空')
                result['passed'] = False

        if 'source_platforms' not in metadata:
            result['warnings'].append('Frontmatter 缺少建议字段: source_platforms')

    # 4. 必须章节验证
    required_sections = [
        '声明',
        '角色设定',
        '写作规则',
        '结构模板',
        '词汇库',
        'Few-shot',
        '使用说明',
        '置信度报告'
    ]

    for section in required_sections:
        # 匹配 ## 或 ### 开头的标题
        pattern = rf'^##\s+.*{re.escape(section)}'
        if not re.search(pattern, body, re.MULTILINE | re.IGNORECASE):
            result['errors'].append(f'缺少必须章节: {section}')
            result['passed'] = False

    # 5. 伦理声明验证
    ethics_keywords = ['仅供学习研究参考', '不得用于冒充']
    ethics_found = any(kw in body for kw in ethics_keywords)
    if not ethics_found:
        result['errors'].append('缺少伦理声明（需包含"仅供学习研究参考"和"不得用于冒充"相关表述）')
        result['passed'] = False

    # 6. 内容非空验证（警告级）
    section_pattern = r'^##\s+(.+)$'
    sections = re.findall(section_pattern, body, re.MULTILINE)
    for section_title in sections:
        # 找到该标题后的内容直到下一个同级或更高级标题
        section_pattern_content = rf'^##\s+{re.escape(section_title)}\s*\n(.*?)(?=^##\s|\Z)'
        match = re.search(section_pattern_content, body, re.MULTILINE | re.DOTALL)
        if match:
            section_content = match.group(1).strip()
            if not section_content or section_content == '{' and '}' in section_content:
                # 检查是否全是模板占位符
                if '{' in section_content and '}' in section_content:
                    result['warnings'].append(f'章节 "{section_title}" 内容可能未填写（包含模板占位符）')

    # 7. 信息统计
    result['info'].append(f'文件大小: {os.path.getsize(file_path)} bytes')
    result['info'].append(f'元数据字段数: {len(metadata)}')
    result['info'].append(f'章节数: {len(sections)}')
    result['info'].append(f'Frontmatter name: {metadata.get("name", "未设置")}')

    return result


def main():
    if len(sys.argv) < 2:
        print('用法: python validate_skill.py <skill_file_path>')
        sys.exit(1)

    file_path = sys.argv[1]
    result = validate_skill(file_path)

    print(f'验证文件: {file_path}')
    print(f'结果: {"✅ 通过" if result["passed"] else "❌ 未通过"}')
    print()

    if result['errors']:
        print('❌ 错误:')
        for err in result['errors']:
            print(f'   - {err}')
        print()

    if result['warnings']:
        print('⚠️  警告:')
        for warn in result['warnings']:
            print(f'   - {warn}')
        print()

    if result['info']:
        print('ℹ️  信息:')
        for info in result['info']:
            print(f'   - {info}')
        print()

    sys.exit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
