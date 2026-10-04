# Reticulum architecture research

## FACT — upstream roles

Reticulum uses destinations and identities, announces to distribute destination
information, and transport nodes for forwarding across interfaces. Its manual
covers path requests and constrained networks. Interface configuration includes
RNode, serial/KISS and IP interfaces. RNode is a radio interface; the Python
stack runs on a host. LXMF adds messaging with optional propagation nodes;
propagation is not a universal geographic road-event broadcast service.

Sources inspected: [understanding](https://reticulum.network/manual/understanding.html),
[interfaces](https://reticulum.network/manual/interfaces.html),
[hardware](https://reticulum.network/manual/hardware.html),
[LXMF](https://github.com/markqvist/LXMF),
[Destination source](https://github.com/markqvist/Reticulum/blob/master/RNS/Destination.py)
and [Packet source](https://github.com/markqvist/Reticulum/blob/master/RNS/Packet.py).
RNS **1.5.5** was installed and its API/source inspected locally.

## DESIGN DECISION — application boundary

Wawet owns event semantics and relevance; it does not implement general routing,
key exchange or a replacement mesh stack. `EventTransport` hides the backend.
The optional spike uses independently written API glue, not vendored upstream
source. Original code remains under its own licence; dependencies do not inherit
that licence. See [licensing](../../LICENSING.md) for current restrictions.

## EXPERIMENTAL RESULT

See [the recorded spike](reticulum-spike.md): two processes and independent
configuration directories exchange the exact event over loopback TCP. This
uses PLAIN destinations, not encrypted SINGLE destinations or identity discovery.
No routed, mobile or radio result has been established.

## OPEN QUESTIONS and next experiments

- For fleeting peers, measure time to discovery, first usable delivery and
  bytes spent on announces/path requests compared with contact duration.
- Compare direct local dissemination with routed delivery. Test whether
  identity churn affects path-cache utility and location privacy.
- Add two isolated hosts with SINGLE destinations, announce/recall, real
  authentication and retransmission deadlines; exercise link churn and expiry.
- Compare LXMF propagation against a bounded application event queue. Never
  renew stale reports simply because a propagation node retained them.
- Test 38-byte payload plus authenticated envelope and RNS overhead at legal
  radio settings. Measure airtime, queue saturation and loss, not just payload.
- Determine the minimum host role needed beside an RNode modem; no evidence
  yet establishes a cheap MCU running the required full endpoint behaviour.
- Resolve the current upstream licence's compatibility with the project's
  genuinely open-source ecosystem ambition before bundling RNS commercially.

Do not select a production Reticulum adapter merely because local PLAIN packets
work. Acceptance requires destination lifecycle, error reporting, callback
serialisation, bounded queues, authentication semantics, expiry and shutdown.
