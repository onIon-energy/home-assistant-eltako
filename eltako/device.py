"""Representation of an Eltako device."""
from eltakobus.message import ESP2Message, EltakoWrappedRPS, EltakoWrapped1BS, EltakoWrapped4BS, RPSMessage, Regular4BSMessage, Regular1BSMessage
from eltakobus.error import ParseError

from homeassistant.helpers.dispatcher import async_dispatcher_connect, dispatcher_send
from homeassistant.helpers.entity import Entity

from .const import SIGNAL_RECEIVE_MESSAGE, SIGNAL_SEND_MESSAGE, LOGGER


class EltakoEntity(Entity):
    """Parent class for all entities associated with the Eltako component."""
    _attr_has_entity_name = True

    def __init__(self, gateway, dev_id, dev_name="Device"):
        """Initialize the device."""
        self.gateway = gateway
        self.dev_id = dev_id
        self.dev_name = dev_name

    async def async_added_to_hass(self):
        """Register callbacks."""
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL_RECEIVE_MESSAGE, self._message_received_callback
            )
        )

    def _message_received_callback(self, msg):
        """Handle incoming messages."""
        
        # Eltako wrapped RPS
        try:
            msg = EltakoWrappedRPS.parse(msg.serialize())
        except ParseError:
            pass
        else:
            if msg.address == self.dev_id.plain_address():
                self.value_changed(msg)
            return
        
        # Eltako wrapped 1BS
        try:
            msg = EltakoWrapped1BS.parse(msg.serialize())
        except ParseError:
            pass
        else:
            if msg.address == self.dev_id.plain_address():
                self.value_changed(msg)
            return

        # Eltako wrapped 4BS
        try:
            msg = EltakoWrapped4BS.parse(msg.serialize())
        except ParseError:
            pass
        else:
            if msg.address == self.dev_id.plain_address():
                self.value_changed(msg)
            return
    
        # RPS
        try:
            msg = RPSMessage.parse(msg.serialize())
        except ParseError:
            pass
        else:
            if msg.address == self.dev_id.plain_address():
                self.value_changed(msg)
            return

        # 1BS
        try:
            msg = Regular1BSMessage.parse(msg.serialize())
        except ParseError:
            pass
        else:
            if msg.address == self.dev_id.plain_address():
                self.value_changed(msg)
            return

        # 4BS
        try:
            msg = Regular4BSMessage.parse(msg.serialize())
        except ParseError:
            pass
        else:
            if msg.address == self.dev_id.plain_address():
                self.value_changed(msg)
            return

    def value_changed(self, msg):
        """Update the internal state of the device when a message arrives."""
    
    def send_message(self, msg):
        dispatcher_send(self.hass, SIGNAL_SEND_MESSAGE, msg)
