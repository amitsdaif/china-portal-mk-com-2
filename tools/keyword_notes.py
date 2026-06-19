from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

SAMPLE_URL = "https://china-portal-mk.com"
SAMPLE_KEYWORD = "mk体育"


@dataclass
class KeywordNote:
    """单个关键词笔记的数据结构"""
    keyword: str
    url: str
    title: str
    tags: List[str] = field(default_factory=list)
    importance: int = 3
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def short_summary(self) -> str:
        return f"[{self.importance}★] {self.keyword} — {self.title[:30]}"


@dataclass
class NoteCollection:
    """一组关键词笔记的集合"""
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def sorted_by_importance(self) -> List[KeywordNote]:
        return sorted(self.notes, key=lambda n: n.importance, reverse=True)

    def format_as_block(self) -> str:
        if not self.notes:
            return "（暂无笔记）"
        lines = ["关键词笔记列表", "=" * 30]
        for idx, note in enumerate(self.notes, 1):
            lines.append(f"{idx}. {note.keyword}")
            lines.append(f"   标题: {note.title}")
            lines.append(f"   链接: {note.url}")
            lines.append(f"   标签: {', '.join(note.tags) if note.tags else '无'}")
            lines.append(f"   重要性: {'★' * note.importance}{'☆' * (5 - note.importance)}")
            lines.append(f"   创建时间: {note.created_at}")
            lines.append("-" * 30)
        return "\n".join(lines)

    def format_compact(self) -> str:
        """紧凑输出，一行一条摘要"""
        return "\n".join(
            note.short_summary() for note in self.notes
        )


def build_demo_collection() -> NoteCollection:
    """构造一组示例关键词笔记，包含 SAMPLE_URL 和 SAMPLE_KEYWORD"""
    col = NoteCollection()

    col.add(KeywordNote(
        keyword=SAMPLE_KEYWORD,
        url=SAMPLE_URL,
        title="mk体育主页入口",
        tags=["体育", "入口"],
        importance=5
    ))

    col.add(KeywordNote(
        keyword="NBA赛程",
        url=SAMPLE_URL + "/nba",
        title="NBA最新赛程与比分",
        tags=["篮球", "NBA"],
        importance=4
    ))

    col.add(KeywordNote(
        keyword="英超直播",
        url=SAMPLE_URL + "/premier-league",
        title="英超联赛高清直播",
        tags=["足球", "英超"],
        importance=4
    ))

    col.add(KeywordNote(
        keyword="电竞资讯",
        url=SAMPLE_URL + "/esports",
        title="LPL / CS2 / Dota2 赛事资讯",
        tags=["电竞", "资讯"],
        importance=3
    ))

    col.add(KeywordNote(
        keyword="体育博彩",
        url=SAMPLE_URL + "/betting",
        title="在线体育博彩平台推荐",
        tags=["博彩", "推荐"],
        importance=2
    ))

    return col


def main():
    collection = build_demo_collection()

    print("=== 格式1: 详细区块 ===")
    print(collection.format_as_block())

    print("\n=== 格式2: 紧凑摘要 ===")
    print(collection.format_compact())

    print("\n=== 按标签过滤（标签=足球） ===")
    football_notes = collection.filter_by_tag("足球")
    for n in football_notes:
        print(n.short_summary())

    print("\n=== 按重要性排序 ===")
    for n in collection.sorted_by_importance():
        print(n.short_summary())


if __name__ == "__main__":
    main()