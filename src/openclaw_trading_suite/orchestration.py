from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from openclaw_trading_suite.adapters import AdapterRegistry, AdapterType
from openclaw_trading_suite.autonomy import Decision, DecisionInput, evaluate_decision
from openclaw_trading_suite.db import SQLiteStore


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(frozen=True)
class ExecutionRequest:
    autonomy_input: DecisionInput
    strategy_id: str
    hypothesis_id: str
    symbol: str
    side: str
    qty: float
    order_type: str = "market"
    limit_price: float | None = None
    venue_adapter_name: str = "mock-execution"
    risk_profile: dict | None = None


def evaluate_and_execute(
    req: ExecutionRequest,
    adapters: AdapterRegistry,
    store: SQLiteStore,
) -> dict:
    decision_out = evaluate_decision(req.autonomy_input)
    risk_decision_id = str(uuid4())
    store.insert_risk_decision(
        risk_decision_id=risk_decision_id,
        hypothesis_id=req.hypothesis_id,
        risk_profile=req.risk_profile or {},
        position_size=req.qty,
        approval_mode=req.autonomy_input.autonomy_level.value,
        approved=decision_out.decision == Decision.APPROVE,
        decision_reason=decision_out.reason,
        created_at=_utc_now(),
    )

    if decision_out.decision != Decision.APPROVE:
        return {
            "executed": False,
            "decision": decision_out.decision.value,
            "reason": decision_out.reason,
        }

    adapter = adapters.get(AdapterType.EXECUTION, req.venue_adapter_name)
    order_id = str(uuid4())
    order_payload = {
        "symbol": req.symbol,
        "side": req.side,
        "qty": req.qty,
        "type": req.order_type,
        "limit_price": req.limit_price,
    }
    execution = adapter.place_order(order_payload)

    store.insert_order(
        order_id=order_id,
        hypothesis_id=req.hypothesis_id,
        venue=req.venue_adapter_name,
        symbol=req.symbol,
        side=req.side,
        order_type=req.order_type,
        qty=req.qty,
        limit_price=req.limit_price,
        status=execution.get("status", "unknown"),
        created_at=_utc_now(),
    )

    fill_id = str(uuid4())
    store.insert_fill(
        fill_id=fill_id,
        order_id=order_id,
        fill_time=_utc_now(),
        fill_price=float(execution.get("avg_fill_price", req.limit_price or 0.0)),
        fill_qty=float(execution.get("qty", req.qty)),
        fee=float(execution.get("fee", 0.0)),
    )
    return {
        "executed": True,
        "decision": decision_out.decision.value,
        "order_id": order_id,
        "fill_id": fill_id,
    }

