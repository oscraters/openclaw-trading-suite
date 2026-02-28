from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from openclaw_trading_suite.adapters import AdapterRegistry, AdapterType
from openclaw_trading_suite.db import SQLiteStore


@dataclass(frozen=True)
class OvernightResearchConfig:
    report_dir: Path
    report_date: str
    autonomy_level: str
    market_symbols: list[str]
    research_topics: list[str]
    strategy_focus: list[str]


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _build_report(
    cfg: OvernightResearchConfig,
    market_sections: list[str],
    topic_sections: list[str],
    hypothesis_sections: list[str],
) -> str:
    return "\n".join(
        [
            f"# While You Were Sleeping Report ({cfg.report_date})",
            "",
            f"- Autonomy Mode: `{cfg.autonomy_level}`",
            f"- Generated At (UTC): `{_utc_now()}`",
            "",
            "## Overnight Actions",
            "- Ran market condition checks on configured symbols.",
            "- Pulled lightweight international topic headlines.",
            "- Generated strategy-linked hypothesis ideas for review/testing.",
            "",
            "## Market Conditions",
            *market_sections,
            "",
            "## International Sentiment and News",
            *topic_sections,
            "",
            "## New/Updated Hypothesis Ideas",
            *hypothesis_sections,
            "",
            "## Suggested Next Session Priorities",
            "1. Validate top 1-2 hypotheses in paper mode before promotion.",
            "2. Re-check risk budgets for strategies impacted by overnight volatility.",
            "3. Queue challenger retrain if drift persists for two consecutive sessions.",
        ]
    )


def run_overnight_research(
    cfg: OvernightResearchConfig,
    adapters: AdapterRegistry,
    store: SQLiteStore,
) -> Path:
    market_data = adapters.get(AdapterType.MARKET_DATA, adapters.list_names(AdapterType.MARKET_DATA)[0])
    news = adapters.get(AdapterType.NEWS, adapters.list_names(AdapterType.NEWS)[0])

    market_sections: list[str] = []
    for symbol in cfg.market_symbols:
        quote = market_data.get_latest_quote(symbol)
        market_sections.append(
            f"- `{symbol}` last `{quote.get('last')}` (bid `{quote.get('bid')}` / ask `{quote.get('ask')}`)."
        )

    topic_sections: list[str] = []
    for topic in cfg.research_topics:
        headlines = news.get_headlines(topic, limit=3)
        topic_sections.append(f"### {topic}")
        for item in headlines:
            topic_sections.append(f"- {item.get('headline')} [{item.get('sentiment', 'unknown')}]")

    hypothesis_sections = [
        f"- Focus `{focus}`: test a swing setup with strict invalidation and regime tag updates."
        for focus in cfg.strategy_focus
    ]

    report_body = _build_report(cfg, market_sections, topic_sections, hypothesis_sections)

    cfg.report_dir.mkdir(parents=True, exist_ok=True)
    report_path = cfg.report_dir / f"while-you-were-sleeping-{cfg.report_date}.md"
    report_path.write_text(report_body, encoding="utf-8")

    store.insert_overnight_report(
        report_id=str(uuid4()),
        report_date=cfg.report_date,
        autonomy_level=cfg.autonomy_level,
        summary_md=report_body,
        created_at=_utc_now(),
    )
    return report_path

