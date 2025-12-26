"""
Lightweight In-Memory Database for Railway Demo
No external dependencies - just Python stdlib
"""

import json
import time
import random
from pathlib import Path
from typing import List, Dict, Optional


class DemoDatabase:
    """In-memory fraud detection database"""
    
    def __init__(self):
        """Initialize with pre-loaded demo data"""
        self.transactions = []
        self.transaction_counter = 0
        
        # Load demo data
        self._load_demo_data()
        
        print(f"✅ Loaded {len(self.transactions)} demo transactions")
    
    def _load_demo_data(self):
        """Load transactions from demo_data.json"""
        demo_file = Path("demo_data.json")
        
        if demo_file.exists():
            with open(demo_file, 'r') as f:
                self.transactions = json.load(f)
        else:
            # Generate demo data if file doesn't exist
            self.transactions = self._generate_demo_data()
            
            # Save for next time
            with open("demo_data.json", 'w') as f:
                json.dump(self.transactions, f, indent=2)
    
    def _generate_demo_data(self) -> List[Dict]:
        """Generate 200 realistic demo transactions"""
        print("📦 Generating demo dataset...")
        
        banks = ["Bank A", "Bank B", "Bank C"]
        users = ["Alice", "Bob", "Charlie", "admin"]
        
        # Legitimate transaction templates
        legitimate = [
            ("Coffee at Starbucks", 4.50),
            ("Grocery shopping at Walmart", 87.32),
            ("Gas station fill-up", 45.00),
            ("Online shopping Amazon", 156.78),
            ("Restaurant dinner", 67.90),
            ("Movie tickets", 28.00),
            ("Gym membership", 49.99),
            ("Phone bill payment", 85.00),
            ("Electric utility", 120.50),
            ("Rent payment", 1500.00),
            ("Car insurance", 275.00),
            ("Netflix subscription", 15.99),
            ("Spotify premium", 9.99),
            ("Pharmacy prescription", 34.50),
            ("Pet store supplies", 56.80),
        ]
        
        # Fraud patterns
        fraud = [
            ("Unauthorized card testing", 1.00),
            ("Suspicious offshore transfer", 9500.00),
            ("Stolen card purchase", 2500.00),
            ("Card verification attempt", 0.50),
            ("Unusual foreign transaction", 7800.00),
            ("Multiple small charges", 2.99),
            ("High-risk merchant", 5600.00),
            ("Suspicious ATM withdrawal", 3000.00),
        ]
        
        data = []
        
        # Generate 170 legitimate + 30 fraud (85/15 split)
        for i in range(170):
            desc, amt = random.choice(legitimate)
            data.append({
                "id": f"demo_{i}",
                "description": desc,
                "amount": amt,
                "bank": random.choice(banks),
                "user_id": random.choice(users),
                "is_fraud": 0,
                "timestamp": time.time() - random.randint(0, 86400),  # Last 24h
                "risk_level": "✅ LOW RISK (Verified Pattern)",
                "index_source": "secure_history"
            })
        
        for i in range(30):
            desc, amt = random.choice(fraud)
            data.append({
                "id": f"demo_threat_{i}",
                "description": desc,
                "amount": amt,
                "bank": random.choice(banks),
                "user_id": "system",
                "is_fraud": 1,
                "timestamp": time.time() - random.randint(0, 86400),
                "risk_level": "🚫 BLOCKED (Known Threat Pattern)",
                "index_source": "known_threats"
            })
        
        # Shuffle
        random.shuffle(data)
        
        return data
    
    def add_transaction(
        self,
        description: str,
        amount: float,
        bank: str,
        user_id: str,
        is_fraud: int = 0
    ) -> bool:
        """Add new transaction"""
        try:
            # Generate risk level
            if is_fraud == 1:
                risk_level = "🚫 BLOCKED (Known Threat Pattern)"
                index_source = "known_threats"
            elif amount < 5:
                risk_level = "⚠️ MEDIUM RISK (Unusual Pattern)"
                index_source = "secure_history"
            else:
                risk_level = "✅ LOW RISK (Verified Pattern)"
                index_source = "secure_history"
            
            txn = {
                "id": f"user_{int(time.time() * 1000)}",
                "description": description,
                "amount": amount,
                "bank": bank,
                "user_id": user_id,
                "is_fraud": is_fraud,
                "timestamp": time.time(),
                "risk_level": risk_level,
                "index_source": index_source
            }
            
            self.transactions.insert(0, txn)  # Add to front
            self.transaction_counter += 1
            
            return True
        except Exception as e:
            print(f"❌ Add failed: {e}")
            return False
    
    def search_transactions(
        self,
        query: str,
        bank_filter: str = "All",
        min_amount: float = 0,
        user_id: str = "admin"
    ) -> List[Dict]:
        """Search transactions with filters"""
        
        # Determine user's bank
        user_bank_map = {
            'Alice': 'Bank A',
            'Bob': 'Bank B',
            'Charlie': 'Bank C'
        }
        
        # For non-admin users, filter by their bank only
        if user_id != "admin" and user_id in user_bank_map:
            bank_filter = user_bank_map[user_id]
        
        results = []
        
        for txn in self.transactions:
            # Bank filter
            if bank_filter != "All" and txn["bank"] != bank_filter:
                continue
            
            # Amount filter
            if txn["amount"] < min_amount:
                continue
            
            # Text search (simple contains)
            if query and query.lower() not in txn["description"].lower():
                continue
            
            # For non-admin, hide threats from other banks
            if user_id != "admin":
                if txn.get("index_source") == "known_threats":
                    continue
            
            # Format for frontend
            results.append({
                "id": txn["id"],
                "score": 0.5,  # Mock similarity score
                "risk_level": txn["risk_level"],
                "metadata": {
                    "description": txn["description"],
                    "amount": txn["amount"],
                    "bank": txn["bank"],
                    "user_id": txn.get("user_id", "system"),
                    "timestamp": txn["timestamp"]
                },
                "index_source": txn.get("index_source", "secure_history")
            })
        
        # Sort by timestamp (newest first)
        results.sort(key=lambda x: x["metadata"]["timestamp"], reverse=True)
        
        return results[:30]  # Return top 30
    
    def delete_transaction(self, txn_id: str) -> bool:
        """Delete transaction by ID"""
        try:
            self.transactions = [t for t in self.transactions if t["id"] != txn_id]
            return True
        except:
            return False
    
    def simulate_broadcast(self, source_bank: str, threat_description: str) -> Dict[str, int]:
        """Simulate threat broadcast"""
        
        # Mock finding similar patterns in other banks
        impact = {
            "Bank A": random.randint(2, 8),
            "Bank B": random.randint(2, 8),
            "Bank C": random.randint(2, 8)
        }
        
        # Remove source bank
        if source_bank in impact:
            del impact[source_bank]
        
        return impact
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        
        total = len(self.transactions)
        threats = sum(1 for t in self.transactions if t["is_fraud"] == 1)
        legitimate = total - threats
        
        by_bank = {
            "Bank A": sum(1 for t in self.transactions if t["bank"] == "Bank A"),
            "Bank B": sum(1 for t in self.transactions if t["bank"] == "Bank B"),
            "Bank C": sum(1 for t in self.transactions if t["bank"] == "Bank C")
        }
        
        return {
            "total": total,
            "threats": threats,
            "legitimate": legitimate,
            "by_bank": by_bank
        }