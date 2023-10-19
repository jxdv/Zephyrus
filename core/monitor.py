class Monitor:
    def __init__(self, target, hash_alg, verbose, threads):
        self.target = target
        self.hash_alg = hash_alg
        self.verbose = verbose
        self.threads = threads
