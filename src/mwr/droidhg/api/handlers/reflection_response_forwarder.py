from mwr.cinnibar.api.builders import ReflectionResponseFactory

from mwr.droidhg import Sessions
from mwr.droidhg.api.protobuf_pb2 import Message
from mwr.droidhg.device import DeviceGoneAway

class ReflectionResponseForwarder:
    """
    ReflectionResponseForwarder is given all REFLECTION_RESPONSE messages
    received by a Server. It finds the Session, based on the session_id, and
    forwards the Message to the Console.
    """
    
    def __init__(self, connection):
        self.connection = connection
    
    def handle(self, message):
        """
        handle() is passed messages for the ReflectionResponseForwarder to
        forward.
        """

        if message.type != Message.REFLECTION_RESPONSE:
            raise Exception("is not a REFLECTION_RESPONSE")
        if not message.HasField('reflection_response'):
            raise Exception("does not contain a REFLECTION_RESPONSE")
        
        session = Sessions.get(message.reflection_response.session_id)

        if session is not None:
            session.console.write(message.SerializeToString())
        else:
            print "no session:", message.reflection_response.session_id
            