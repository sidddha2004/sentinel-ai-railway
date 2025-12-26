"""
Sentinel AI - Railway Demo Backend
Lightweight fraud detection system for Railway deployment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
import time
import random
from pathlib import Path

app = FastAPI(title="Sentinel AI - Demo Mode")

# CORS - Allow your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import lightweight database
from lightweight_db import DemoDatabase

# Initialize demo database
db = DemoDatabase()

# ============================================================================
# REQUEST MODELS
# ============================================================================

class TransactionRequest(BaseModel):
    description: str
    amount: float
    bank: str = "Bank A"
    user_id: str = "admin"
    is_fraud: int = 0

class SearchRequest(BaseModel):
    query: str
    bank_filter: str = "All"
    min_amount: float = 0
    user_id: str = "admin"

class BroadcastRequest(BaseModel):
    source_bank: str
    description: str

# ============================================================================
# CORE ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "system": "Sentinel AI - Demo Mode",
        "version": "2.0-railway",
        "mode": "demo",
        "note": "Lightweight version for Railway deployment"
    }

@app.post("/secure-ingest")
async def ingest_transaction(txn: TransactionRequest):
    """Add new transaction"""
    success = db.add_transaction(
        description=txn.description,
        amount=txn.amount,
        bank=txn.bank,
        user_id=txn.user_id,
        is_fraud=txn.is_fraud
    )
    
    if success:
        return {
            "status": "stored",
            "id": f"demo_{int(time.time() * 1000)}",
            "message": f"Transaction stored in {txn.bank}"
        }
    else:
        raise HTTPException(status_code=500, detail="Storage failed")

@app.post("/secure-search")
async def search_transactions(search: SearchRequest):
    """Search transactions with filtering"""
    results = db.search_transactions(
        query=search.query,
        bank_filter=search.bank_filter,
        min_amount=search.min_amount,
        user_id=search.user_id
    )
    
    return {
        "results": results,
        "count": len(results),
        "query": search.query
    }

@app.delete("/secure-delete/{txn_id}")
async def delete_transaction(txn_id: str):
    """Delete transaction (admin only)"""
    success = db.delete_transaction(txn_id)
    
    if success:
        return {"status": "deleted", "id": txn_id}
    else:
        raise HTTPException(status_code=404, detail="Transaction not found")

# ============================================================================
# FEDERATED LEARNING ENDPOINTS (SIMPLIFIED)
# ============================================================================

@app.post("/secure-broadcast")
async def broadcast_threat(req: BroadcastRequest):
    """Simulate threat broadcast across network"""
    
    print(f"\n📡 Broadcasting threat from {req.source_bank}")
    print(f"Pattern: {req.description}")
    
    # Simulate network scan
    time.sleep(1)
    
    # Mock impact statistics
    impact = db.simulate_broadcast(req.source_bank, req.description)
    
    total = sum(impact.values())
    
    return {
        "status": "Broadcast Complete",
        "source_bank": req.source_bank,
        "threat_pattern": req.description,
        "impact_report": impact,
        "total_protected": total,
        "message": f"Protected {total} transactions across the network"
    }

@app.post("/federated-round")
async def trigger_federated_round():
    """Simulate federated learning round"""
    time.sleep(1.5)
    
    new_accuracy = round(random.uniform(0.90, 0.98), 3)
    round_id = f"FL-{random.randint(1000, 9999)}"
    
    return {
        "status": "Updated",
        "round_id": round_id,
        "new_accuracy": new_accuracy,
        "participants": ["Bank A", "Bank B", "Bank C"],
        "message": "Global model updated successfully"
    }

@app.post("/secure-train")
async def train_index():
    """Simulate index optimization"""
    time.sleep(1)
    return {
        "status": "Trained",
        "message": "Indexes optimized successfully"
    }

# ============================================================================
# SYSTEM INFO ENDPOINTS
# ============================================================================

@app.get("/network-stats")
async def get_network_stats():
    """Get network statistics"""
    return {
        "network": {
            "Bank A": {"normal_patterns": 45, "known_threats": 12},
            "Bank B": {"normal_patterns": 38, "known_threats": 9},
            "Bank C": {"normal_patterns": 52, "known_threats": 15}
        },
        "total_banks": 3,
        "architecture": "Demo Mode - In-Memory"
    }

@app.get("/system-health")
async def system_health():
    """System health check"""
    return {
        "status": "healthy",
        "mode": "demo",
        "indexes": {
            "secure_history": "active (in-memory)",
            "known_threats": "active (in-memory)"
        },
        "features": {
            "demo_mode": "enabled",
            "real_time_updates": "polling",
            "ml_detection": "basic"
        }
    }

@app.get("/streaming-stats")
async def get_streaming_stats():
    """Get real-time statistics (for polling)"""
    stats = db.get_stats()
    
    return {
        "recent_transactions": stats["total"],
        "legitimate": stats["legitimate"],
        "threats": stats["threats"],
        "by_bank": stats["by_bank"],
        "time_window": "demo dataset",
        "timestamp": time.time()
    }

# ============================================================================
# RAG ENDPOINTS (MOCK RESPONSES)
# ============================================================================

@app.post("/rag-analysis")
async def generate_fraud_analysis(search: SearchRequest):
    """Generate mock AI fraud analysis"""
    
    # Simulate processing time
    time.sleep(1.5)
    
    # Get relevant transactions
    results = db.search_transactions(
        query=search.query,
        bank_filter=search.bank_filter,
        min_amount=search.min_amount,
        user_id=search.user_id
    )
    
    # Generate mock analysis
    threat_count = sum(1 for r in results if "BLOCKED" in r.get("risk_level", ""))
    
    analysis = f"""**Fraud Intelligence Report**

**Query Analysis:** "{search.query or 'general patterns'}"
**Bank Scope:** {search.bank_filter}
**Transactions Analyzed:** {len(results)}

**Risk Assessment:**
- High Risk Transactions: {threat_count}
- Medium Risk: {len(results) - threat_count}
- Primary Threat Vectors: Card testing, unauthorized transfers

**AI Insights:**
The analyzed pattern shows {'elevated' if threat_count > 0 else 'normal'} threat activity. 
{f'Detected {threat_count} transactions matching known fraud signatures.' if threat_count > 0 else 'No immediate threats detected in current dataset.'}

**Recommendations:**
- Continue monitoring for unusual patterns
- Enable real-time alerts for high-risk transactions
- Review transactions over $5000 manually

*Note: This is a demo analysis. Production system uses Gemini AI for deeper insights.*
"""
    
    return {
        "status": "success",
        "report": {
            "analysis": analysis,
            "retrieved_count": len(results)
        }
    }

@app.post("/quick-threat-check")
async def quick_threat_check(txn: TransactionRequest):
    """Quick threat assessment for single transaction"""
    
    # Simulate AI processing
    time.sleep(1)
    
    # Simple rule-based assessment
    risk_score = 0
    factors = []
    
    if txn.amount > 5000:
        risk_score += 30
        factors.append("Large amount ($5000+)")
    
    if txn.amount < 5:
        risk_score += 40
        factors.append("Micro-transaction (potential card testing)")
    
    desc_lower = txn.description.lower()
    suspicious_terms = ['unauthorized', 'stolen', 'fraud', 'test', 'verify']
    
    for term in suspicious_terms:
        if term in desc_lower:
            risk_score += 20
            factors.append(f"Suspicious keyword: '{term}'")
    
    # Generate assessment
    if risk_score > 50:
        verdict = "🚫 **HIGH RISK - BLOCK RECOMMENDED**"
        action = "This transaction should be blocked and investigated."
    elif risk_score > 25:
        verdict = "⚠️ **MEDIUM RISK - REVIEW REQUIRED**"
        action = "Flag for manual review before processing."
    else:
        verdict = "✅ **LOW RISK - APPROVE**"
        action = "Transaction appears legitimate. Safe to process."
    
    assessment = f"""{verdict}

**Transaction Details:**
- Description: {txn.description}
- Amount: ${txn.amount}
- Bank: {txn.bank}

**Risk Score:** {risk_score}/100

**Risk Factors Detected:**
{chr(10).join(f"- {f}" for f in factors) if factors else "- No significant risk factors"}

**Recommendation:**
{action}

*Note: Demo mode using rule-based detection. Production uses ML models.*
"""
    
    return {
        "status": "success",
        "assessment": assessment
    }

# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Load demo data on startup"""
    print("\n" + "="*70)
    print("🚀 SENTINEL AI - RAILWAY DEMO MODE")
    print("="*70)
    print("✅ FastAPI initialized")
    print("✅ Demo database loaded")
    print("✅ 200 sample transactions ready")
    print("✅ Mock AI analysis enabled")
    print("="*70)
    print("\n💡 This is a demo version optimized for Railway deployment")
    print("   Full features: CyborgDB, Kafka, Real ML models")
    print("="*70 + "\n")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)