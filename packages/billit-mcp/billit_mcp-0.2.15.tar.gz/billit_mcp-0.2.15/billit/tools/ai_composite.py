"""AI-enhanced composite tools."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from difflib import SequenceMatcher
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

from ..client import BillitAPIClient

router = APIRouter()


def get_client() -> BillitAPIClient:
    """Instantiate the Billit API client."""

    return BillitAPIClient()


def _similarity(a: str, b: str) -> float:
    """Compute a similarity ratio between two strings."""

    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


@router.get("/ai/suggest-payment-reconciliation")
async def suggest_payment_reconciliation(
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Match outstanding invoices with bank transactions by reference and amount."""

    invoices_resp = await client.request(
        "GET",
        "/orders",
        params={"$filter": "ToPay gt 0", "$top": 500},
    )
    tx_resp = await client.request(
        "GET",
        "/financialTransaction",
        params={"$top": 500},
    )
    invoices = invoices_resp.get("data", []) or []
    transactions = tx_resp.get("data", []) or []
    matches: List[Dict[str, Any]] = []
    for inv in invoices:
        ref = inv.get("PaymentReference")
        amount = float(inv.get("ToPay", 0))
        for tx in transactions:
            if ref and ref == tx.get("PaymentReference"):
                matches.append(
                    {
                        "order_id": inv.get("OrderID"),
                        "transaction_id": tx.get("FinancialTransactionID"),
                        "amount": amount,
                    }
                )
                break
            tx_amount = float(tx.get("Amount", 0))
            if amount and abs(amount - tx_amount) < 0.01:
                matches.append(
                    {
                        "order_id": inv.get("OrderID"),
                        "transaction_id": tx.get("FinancialTransactionID"),
                        "amount": amount,
                    }
                )
                break
    return {"success": True, "data": matches, "error": None, "error_code": None}


@router.get("/ai/invoice-summary")
async def generate_invoice_summary(
    start_date: str,
    end_date: str,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Return the number and total of sales invoices between two dates."""

    params = {
        "$filter": (
            f"OrderDirection eq 'Income' and OrderDate ge {start_date} "
            f"and OrderDate le {end_date}"
        ),
        "$top": 500,
    }
    resp = await client.request("GET", "/orders", params=params)
    invoices = resp.get("data", []) or []
    total = sum(float(i.get("TotalIncl", 0)) for i in invoices)
    return {
        "success": True,
        "data": {"count": len(invoices), "total_incl": total},
        "error": None,
        "error_code": None,
    }


@router.get("/ai/expense-summary")
async def generate_expense_summary(
    start_date: str,
    end_date: str,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Return the number and total of purchase invoices between two dates."""

    params = {
        "$filter": (
            f"OrderDirection eq 'Cost' and OrderDate ge {start_date} "
            f"and OrderDate le {end_date}"
        ),
        "$top": 500,
    }
    resp = await client.request("GET", "/orders", params=params)
    invoices = resp.get("data", []) or []
    total = sum(float(i.get("TotalIncl", 0)) for i in invoices)
    return {
        "success": True,
        "data": {"count": len(invoices), "total_incl": total},
        "error": None,
        "error_code": None,
    }


@router.get("/ai/cashflow")
async def get_cashflow_overview(
    period: str, client: BillitAPIClient = Depends(get_client)
) -> dict[str, Any]:
    """Summarize cash inflow and outflow for the given YYYY-MM period."""

    start = f"{period}-01"
    year, month = [int(p) for p in period.split("-")]
    if month == 12:
        end_date = f"{year + 1}-01-01"
    else:
        end_date = f"{year}-{month + 1:02d}-01"

    income_resp = await client.request(
        "GET",
        "/orders",
        params={
            "$filter": (
                f"OrderDirection eq 'Income' and OrderDate ge {start} "
                f"and OrderDate lt {end_date}"
            ),
            "$top": 500,
        },
    )
    cost_resp = await client.request(
        "GET",
        "/orders",
        params={
            "$filter": (
                f"OrderDirection eq 'Cost' and OrderDate ge {start} "
                f"and OrderDate lt {end_date}"
            ),
            "$top": 500,
        },
    )
    income_orders = income_resp.get("data", []) or []
    cost_orders = cost_resp.get("data", []) or []
    income_total = sum(float(o.get("TotalIncl", 0)) for o in income_orders)
    cost_total = sum(float(o.get("TotalIncl", 0)) for o in cost_orders)
    return {
        "success": True,
        "data": {
            "income": income_total,
            "expense": cost_total,
            "net": income_total - cost_total,
        },
        "error": None,
        "error_code": None,
    }


@router.post("/ai/categorize-expense/{invoice_id}")
async def categorize_expense_invoice(
    invoice_id: int, client: BillitAPIClient = Depends(get_client)
) -> dict[str, Any]:
    """Suggest a simple category for an expense invoice based on keywords."""

    resp = await client.request("GET", f"/orders/{invoice_id}")
    order = resp.get("data", {}) or {}
    lines = order.get("OrderLines", []) or []
    text = " ".join(l.get("Description", "") for l in lines).lower()
    if any(k in text for k in ["fuel", "gas", "petrol", "diesel"]):
        category = "Transport"
    elif any(k in text for k in ["office", "paper", "stationery"]):
        category = "Office"
    else:
        category = "General"
    return {
        "success": True,
        "data": {"invoice_id": invoice_id, "category": category},
        "error": None,
        "error_code": None,
    }


@router.get("/ai/overdue-invoices")
async def list_overdue_invoices(
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Return all overdue sales invoices."""

    resp = await client.request(
        "GET",
        "/orders",
        params={
            "$filter": "Overdue eq true and OrderDirection eq 'Income'",
            "$top": 500,
        },
    )
    data = resp.get("data", []) or []
    overdue_ids = [o.get("OrderID") for o in data]
    return {
        "success": True,
        "data": overdue_ids,
        "error": None,
        "error_code": None,
    }


@router.get("/ai/supplier-spend/{supplier_id}")
async def get_supplier_spend_summary(
    supplier_id: int,
    period: str,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Return total spend with a supplier for the given period."""

    start = f"{period}-01"
    year, month = [int(p) for p in period.split("-")]
    if month == 12:
        end_date = f"{year + 1}-01-01"
    else:
        end_date = f"{year}-{month + 1:02d}-01"
    params = {
        "$filter": (
            f"OrderDirection eq 'Cost' and Party/PartyID eq {supplier_id} "
            f"and OrderDate ge {start} and OrderDate lt {end_date}"
        ),
        "$top": 500,
    }
    resp = await client.request("GET", "/orders", params=params)
    orders = resp.get("data", []) or []
    total = sum(float(o.get("TotalIncl", 0)) for o in orders)
    return {
        "success": True,
        "data": {"supplier_id": supplier_id, "total_incl": total},
        "error": None,
        "error_code": None,
    }


@router.get("/ai/customer-revenue/{customer_id}")
async def get_customer_revenue_summary(
    customer_id: int,
    period: str,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Return total revenue from a customer for the given period."""

    start = f"{period}-01"
    year, month = [int(p) for p in period.split("-")]
    if month == 12:
        end_date = f"{year + 1}-01-01"
    else:
        end_date = f"{year}-{month + 1:02d}-01"
    params = {
        "$filter": (
            f"OrderDirection eq 'Income' and Party/PartyID eq {customer_id} "
            f"and OrderDate ge {start} and OrderDate lt {end_date}"
        ),
        "$top": 500,
    }
    resp = await client.request("GET", "/orders", params=params)
    orders = resp.get("data", []) or []
    total = sum(float(o.get("TotalIncl", 0)) for o in orders)
    return {
        "success": True,
        "data": {"customer_id": customer_id, "total_incl": total},
        "error": None,
        "error_code": None,
    }


@router.get("/ai/duplicate-contacts")
async def find_duplicate_contacts(
    similarity_threshold: float = 0.9,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Find contacts with similar names using a naive ratio check."""

    resp = await client.request("GET", "/party", params={"$top": 500})
    parties = resp.get("data", []) or []
    duplicates: List[Dict[str, Any]] = []
    names = [(p.get("PartyID"), p.get("Name", "")) for p in parties]
    for i, (id_a, name_a) in enumerate(names):
        for id_b, name_b in names[i + 1 :]:
            if not name_a or not name_b:
                continue
            ratio = _similarity(name_a, name_b)
            if ratio >= similarity_threshold:
                duplicates.append(
                    {"party_a": id_a, "party_b": id_b, "similarity": ratio}
                )
    return {"success": True, "data": duplicates, "error": None, "error_code": None}


@router.post("/ai/normalize-address/{party_id}")
async def normalize_contact_address(
    party_id: int, client: BillitAPIClient = Depends(get_client)
) -> dict[str, Any]:
    """Normalize address fields of a contact in a very naive way."""

    resp = await client.request("GET", f"/party/{party_id}")
    party = resp.get("data", {}) or {}
    addresses = party.get("Addresses", []) or []
    normalized = []
    for addr in addresses:
        normalized.append(
            {k: str(v).title() if isinstance(v, str) else v for k, v in addr.items()}
        )
    await client.request(
        "PATCH",
        f"/party/{party_id}",
        json={"Addresses": normalized},
    )
    return {
        "success": True,
        "data": {"party_id": party_id, "normalized": True},
        "error": None,
        "error_code": None,
    }


@router.post("/ai/create-invoice-from-text")
async def create_invoice_from_text(
    data: dict[str, Any], client: BillitAPIClient = Depends(get_client)
) -> dict[str, Any]:
    """Create a very simple sales invoice using provided free text."""
    
    text_description = data.get("text_description", "")
    invoice = {
        "OrderDirection": "Income",
        "OrderType": "Invoice",
        "Customer": {"Name": "Text Import"},
        "OrderLines": [
            {
                "Description": text_description,
                "Quantity": 1,
                "UnitPriceExcl": 0.0,
            }
        ],
    }
    resp = await client.request("POST", "/orders", json=invoice)
    return resp


@router.get("/ai/smart-search")
async def smart_search(
    query: str,
    entity_type: str = "all",
    max_results: int = 10,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Intelligent search across orders, parties, and products with semantic matching.
    
    Args:
        query: Natural language search query (e.g., "BDS winter split January 2025")
        entity_type: "orders", "parties", "products", or "all" 
        max_results: Maximum number of results to return
    """
    
    query_lower = query.lower()
    results = []
    
    # Parse common patterns from query
    amount_keywords = []
    date_keywords = []
    name_keywords = []
    content_keywords = []
    
    # Extract potential amounts
    import re
    amount_matches = re.findall(r'[€$£]\s*(\d{1,3}(?:,?\d{3})*(?:\.\d{2})?)', query)
    if amount_matches:
        amount_keywords = [float(amt.replace(',', '')) for amt in amount_matches]
    
    # Extract potential dates  
    date_patterns = [
        r'(\d{4})',  # Year
        r'(january|february|march|april|may|june|july|august|september|october|november|december)',
        r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)',
        r'(winter|spring|summer|fall|autumn)',
        r'(split)',
    ]
    for pattern in date_patterns:
        matches = re.findall(pattern, query_lower)
        date_keywords.extend(matches)
    
    # Extract company/name keywords
    name_patterns = ['bds', 'esport', 'surge', 'vitality', 'fnatic', 'riot']
    for pattern in name_patterns:
        if pattern in query_lower:
            name_keywords.append(pattern)
    
    # Content keywords
    content_patterns = ['split', 'bonus', 'promotion', 'consulting', 'parus', 'winter', 'summer']
    for pattern in content_patterns:
        if pattern in query_lower:
            content_keywords.append(pattern)
    
    # Search orders if requested
    if entity_type in ["orders", "all"]:
        order_params = {"$top": 200}  # Get more for better matching
        orders_resp = await client.request("GET", "/orders", params=order_params)
        orders = orders_resp.get("data", []) or []
        
        for order in orders:
            score = 0.0
            matches = []
            
            # Check customer name
            customer_name = (order.get("CounterParty", {}) or {}).get("DisplayName", "")
            if customer_name:
                for keyword in name_keywords:
                    if keyword in customer_name.lower():
                        score += 3.0
                        matches.append(f"Customer: {customer_name}")
            
            # Check reference and descriptions
            reference = order.get("Reference", "")
            if reference:
                for keyword in content_keywords:
                    if keyword in reference.lower():
                        score += 2.0
                        matches.append(f"Reference: {reference}")
            
            # Check order lines
            order_lines = order.get("OrderLines", []) or []
            for line in order_lines:
                description = line.get("Description", "")
                if description:
                    for keyword in content_keywords:
                        if keyword in description.lower():
                            score += 2.0
                            matches.append(f"Description: {description}")
            
            # Check amounts
            total = order.get("TotalIncl", 0)
            for amount in amount_keywords:
                if abs(float(total) - amount) < amount * 0.1:  # Within 10%
                    score += 2.0
                    matches.append(f"Amount: €{total}")
            
            # Check dates
            order_date = order.get("OrderDate", "")
            if order_date:
                for date_keyword in date_keywords:
                    if date_keyword in order_date.lower():
                        score += 1.5
                        matches.append(f"Date: {order_date}")
            
            # Add basic relevance for any text similarity
            searchable_text = f"{customer_name} {reference} " + " ".join(
                line.get("Description", "") for line in order_lines
            )
            similarity = _similarity(query_lower, searchable_text.lower())
            score += similarity * 1.0
            
            if score > 0.5:  # Minimum relevance threshold
                results.append({
                    "type": "order",
                    "score": score,
                    "data": order,
                    "matches": matches,
                    "summary": f"Invoice #{order.get('OrderNumber', 'N/A')} - {customer_name} - €{total}"
                })
    
    # Search parties if requested  
    if entity_type in ["parties", "all"]:
        parties_resp = await client.request("GET", "/party", params={"$top": 200})
        parties = parties_resp.get("data", []) or []
        
        for party in parties:
            score = 0.0
            matches = []
            
            name = party.get("Name", "")
            display_name = party.get("DisplayName", "")
            
            # Check name matching
            for keyword in name_keywords:
                if keyword in name.lower() or keyword in display_name.lower():
                    score += 3.0
                    matches.append(f"Name: {name}")
            
            # Text similarity
            searchable_text = f"{name} {display_name}"
            similarity = _similarity(query_lower, searchable_text.lower())
            score += similarity * 2.0
            
            if score > 0.5:
                results.append({
                    "type": "party", 
                    "score": score,
                    "data": party,
                    "matches": matches,
                    "summary": f"{party.get('PartyType', 'Party')} - {display_name or name}"
                })
    
    # Sort by relevance score
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Limit results
    results = results[:max_results]
    
    return {
        "success": True,
        "data": {
            "query": query,
            "results": results,
            "total_found": len(results),
            "parsed_keywords": {
                "amounts": amount_keywords,
                "dates": date_keywords, 
                "names": name_keywords,
                "content": content_keywords
            }
        },
        "error": None,
        "error_code": None,
    }
