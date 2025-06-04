import threading
import time
import random
import uuid

class Lock:
    def __init__(self, item_id):
        self.item_id = item_id
        self.lock_value = False
        self.transaction = None
        self.queue = []

    def acquire(self, transaction):
        if not self.lock_value:
            self.lock_value = True
            self.transaction = transaction
            print(f"[LOCK] {transaction.tid} obteve o bloqueio em {self.item_id}")
            return True
        else:
            if transaction.timestamp < self.transaction.timestamp:  # wait-die
                print(f"[WAIT] {transaction.tid} esperando por {self.item_id}")
                self.queue.append(transaction)
                return False
            else:
                print(f"[KILL] {transaction.tid} morto por wait-die (esperava por {self.item_id})")
                transaction.abort_due_to_deadlock()
                return False

    def release(self, transaction):
        if self.transaction == transaction:
            self.lock_value = False
            self.transaction = None
            print(f"[UNLOCK] {transaction.tid} liberou {self.item_id}")
            if self.queue:
                next_transaction = self.queue.pop(0)
                self.acquire(next_transaction)

class Transaction(threading.Thread):
    def __init__(self, tid, timestamp, lock_x, lock_y):
        super().__init__()
        self.tid = tid
        self.timestamp = timestamp
        self.lock_x = lock_x
        self.lock_y = lock_y
        self.aborted = False

    def run(self):
        print(f"[START] Transação {self.tid} iniciou")
        while True:
            if self.try_run():
                break
            time.sleep(random.uniform(0.5, 1.5))

    def try_run(self):
        try:
            time.sleep(random.uniform(0.1, 1))
            if not self.lock_x.acquire(self):
                return False
            time.sleep(random.uniform(0.1, 1))
            if not self.lock_y.acquire(self):
                self.lock_x.release(self)
                return False

            time.sleep(random.uniform(0.1, 1))
            self.lock_x.release(self)
            time.sleep(random.uniform(0.1, 1))
            self.lock_y.release(self)
            print(f"[COMMIT] Transação {self.tid} finalizou com sucesso")
            return True
        except DeadlockException:
            return False

    def abort_due_to_deadlock(self):
        print(f"[ABORT] Transação {self.tid} abortada devido a deadlock")
        raise DeadlockException()

class DeadlockException(Exception):
    pass

def main():
    lock_x = Lock("X")
    lock_y = Lock("Y")
    transactions = []

    for i in range(5):
        tid = f"T{i+1}"
        timestamp = time.time() + random.random()  # Simula timestamps únicos
        t = Transaction(tid, timestamp, lock_x, lock_y)
        transactions.append(t)

    for t in transactions:
        t.start()

    for t in transactions:
        t.join()

    print("[FIM] Todas as transações foram concluídas.")

if __name__ == "__main__":
    main()