class purchase_order_vm:
    def __init__(self, poid, title, status, created_by, purchasereq, foruser):
        self.poid = poid
        self.title = title
        self.status = status
        self.created_by = created_by
        self.purchasereq = purchasereq
        self.foruser = foruser