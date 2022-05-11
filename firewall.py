from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__(self, connection):
    # Keep track of the connection
    self.connection = connection

    # This binds the PacketIn event listener
    connection.addListeners(self)

  def do_final(self, packet, packet_in, switch_id):
    """ Handles accepting/dropping packets given network rules
    - packet: parsed packet
    - packet_in: actual ofp_packet_in message
    - switch_id: the id of the switch that received the packet
    """
    d_ip_port = {'10.2.2.10': 1, '10.2.2.11': 2}
    h_ip_port = {'10.1.1.10': 8, '10.1.1.11': 9, '10.1.1.12': 10, '10.1.1.13': 11}

    ip_packet = packet.find('ipv4')

    timeout = (30, 50)

    if ip_packet is not None:
      src = ip_packet.srcip
      dst = ip_packet.dstip
      if switch_id == 1:
        if src in h_ip_port.keys():
          if dst in d_ip_port.keys():
            self.accept(packet, packet_in, timeout, 2)
          elif dst == '10.3.3.1':
            self.accept(packet, packet_in, timeout, 1)
        elif dst in h_ip_port.keys():
          self.accept(packet, packet_in, timeout, h_ip_port[str(dst)])
      elif switch_id == 2:
        if src in h_ip_port.keys() and dst == '10.3.3.1':
          self.accept(packet, packet_in, timeout, 2)
        elif dst in h_ip_port.keys() and src == '10.3.3.1':
          self.accept(packet, packet_in, timeout, 1)
      elif switch_id == 3:
        if src in d_ip_port.keys() and dst in h_ip_port.keys():
          self.accept(packet, packet_in, timeout, 3)
        elif dst in d_ip_port.keys():
          self.accept(packet, packet_in, timeout, d_ip_port[str(dst)])
      elif switch_id == 4: 
        if src in h_ip_port.keys() and dst == '10.3.3.1':
          self.accept(packet, packet_in, timeout, 1)
        elif dst in h_ip_port.keys() and src == '10.3.3.1':
          self.accept(packet, packet_in, timeout, 2)
      else:
        self.drop(packet, packet_in, timeout)
    else:
      self.accept(packet, packet_in, timeout, of.OFPP_FLOOD)

  def accept(self, packet, packet_in, timeout, out_port):
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = timeout[0]
    msg.hard_timeout = timeout[1]
    msg.buffer_id = packet_in.buffer_id
    msg.actions.append(of.ofp_action_output(port=out_port))
    msg.data = packet_in
    self.connection.send(msg)

  def drop(self, packet, packet_in, timeout):
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = timeout[0]
    msg.hard_timeout = timeout[1] 
    msg.buffer_id = packet_in.buffer_id 
    msg.actions = []
    self.connection.send(msg)

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
