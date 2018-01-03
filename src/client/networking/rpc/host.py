from client.networking.host import Host


class RPCHost(Host):
    def connect(self, server):
        '''make an RPC proxy from self'''
