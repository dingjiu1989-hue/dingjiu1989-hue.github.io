---
title: "ACID vs BASE Transactions"
description: "Compare ACID and BASE transaction models, when to use each, and how modern databases balance consistency, availability, and partition tolerance."
date: 2026-05-11
board: database
url: https://dingjiu1989-hue.github.io/en/database/acid-vs-base.html
---

# ACID vs BASE Transactions

Consistency Models   
ACID and BASE represent opposing philosophies for database consistency. ACID guarantees strict consistency while BASE prioritizes availability.   
ACID Properties   
Atomicity, Consistency, Isolation, Durability:   

    
    
    -- ACID transaction example
    
    BEGIN TRANSACTION;
    
    UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
    
    UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
    
    COMMIT;
    
    

  
BASE Properties   
Basically Available, Soft state, Eventual consistency:   

    
    
    class EventualConsistentLedger:
    
        def __init__(self):
    
            self.pending = []
    
        
    
        def transfer(self, sender, recipient, amount):
    
            self.pending.append({
    
                "sender": sender, "recipient": recipient,
    
                "amount": amount, "timestamp": time.time()
    
            })
    
            return {"status": "accepted"}
    
        
    
        def reconcile(self):
    
            for tx in self.pending:
    
                self.apply_transaction(tx)
    
    

  
When to Relax ACID   
| Requirement | ACID | BASE | |-------------|------|------| | Consistency | Strong | Eventual | | Availability | Lower | Higher | | Latency | Higher | Lower | | Use case | Financial | Analytics |   
Conclusion   
Choose ACID where correctness is critical and BASE where scale matters. Modern databases increasingly blur the line. Understand your consistency requirements and choose accordingly.
