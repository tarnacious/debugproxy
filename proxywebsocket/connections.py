from tornado.websocket import WebSocketHandler
import logging

logger = logging.getLogger(__name__)

class Connections(object):

    def __init__(self) -> None:
        self.connections = dict() # type: Dict[str, List[WebSocketHandler]]
        self.status()


    def add_connection(self, id: str, connection: WebSocketHandler) -> None:
        logger.debug("Connections: Adding {}".format(id));
        connections = self.connections.get(id, [])
        connections.append(connection)
        self.connections[id] = connections
        self.status()


    def remove_connection(self, id: str, connection: WebSocketHandler) -> None:
        logger.debug("Connections: Removing {}".format(id));
        if id in self.connections:
            connections = self.connections[id]
            connections = list(filter(lambda c: c != connection,
                                      connections))
            if len(connections) > 0:
                self.connections[id] = connections
            else:
                del self.connections[id]
        self.status()


    def broadcast(self, id: str, message: bytes) -> None:
        logger.debug("Connections: Broadcasting {}".format(id));
        if id in self.connections:
            connections = self.connections[id]
            for connection in connections:
                try:
                    connection.write_message(message)
                except Exception:
                    logger.error("Connections: Error sending message to: ".format(id))
        else:
            logger.error("Connections: Client not connected {}".format(id))
        self.status()


    def status(self) -> None:
        for id, connections in self.connections.items():
            logger.debug("{}: {} connections".format(id, len(connections)))
