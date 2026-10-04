# Wawet Gateway — planned infrastructure host

Linux-class host (existing SBC or mini PC) for Reticulum interfaces, optional
LXMF services and self-hosted integrations. Candidate bearers: Ethernet/Wi-Fi IP,
RNode radio and later HaLow backhaul. RNS already provides network forwarding;
Wawet should add application policy and observability rather than a routing stack.

Plan interface health, event counts, duplicate/expired/rate-limit counters and
link latency. Later expose aggregate Prometheus metrics, opt-in MQTT/Home
Assistant bridges and local administration. Avoid location or identity metric
labels. Keep queues bounded and remove stale events before forwarding. Optional
Internet bridging must not become mandatory Hathorsoft infrastructure.
No daemon, container image, hosted service or management frontend is implemented
in this iteration. The local RNS spike validates only a narrow API path.
