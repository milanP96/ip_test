class JobSerializer:
    """Prepare SQLAlchemy object for Flask jsonify function"""

    def __init__(self, sqlalchemy_obj):
        self.id = sqlalchemy_obj.id
        self.ips = sqlalchemy_obj.ips
        self.status = sqlalchemy_obj.status
        self.value = sqlalchemy_obj.value
        self.search_expression = sqlalchemy_obj.search_expression
        self.ips_resolved = sqlalchemy_obj.ips_resolved
        self.ips_matched = sqlalchemy_obj.ips_matched
        self.ips_received = sqlalchemy_obj.ips_received

    def serialize(self):
        return {
            "id": self.id,
            "ips": self.ips,
            "status": self.status,
            "value": self.value,
            "search_expression": self.search_expression,
            "ips_resolved": self.ips_resolved,
            "ips_matched": self.ips_matched,
            "ips_received": self.ips_received
        }
