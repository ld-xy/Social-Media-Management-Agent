class Memory:
    """
    记忆上下文管理
    """

    def __init__(self):
        self.memory = {}

    def __call__(self):
        pass

    def get(self, key):
        return self.memory.get(key)
