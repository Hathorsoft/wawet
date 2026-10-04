# Optional amateur-radio and long-distance track

**FACT:** Ofcom publishes the UK amateur licence and guidance, including rules
on use and encryption. Refer to [the current guidance](https://www.ofcom.org.uk/siteassets/resources/documents/manage-your-licence/amateur/amateur_radio_licence_guidance_for_licensees.pdf)
and [licensing page](https://www.ofcom.org.uk/spectrum/radio-equipment/amateur-radio).
No encrypted consumer carriage has been approved for Wawet.

**DESIGN DECISION:** normal Drive owners must never require an amateur licence.
Keep these experiments separate from the default consumer network. Do not
bridge encrypted Wawet traffic onto amateur bands without a verified lawful
basis for that exact use and country. A gateway cannot erase bearer restrictions.

Research candidates: serial KISS/TNC, packet radio VHF/UHF, HF digital modes,
[Modem73](https://reticulum.network/manual/programs.html), link asymmetry and
long-distance gateways. Data Slayer videos are experiment ideas, not regulatory
authority or evidence of Wawet performance. No modem project is endorsed without
examining actual code, licence and measurements.

Gate: map operator privileges, permitted content, encryption, identification,
bandwidth and commercial-message restrictions from the licence, then choose a
legal test payload and link. Measure latency/error rate and store-and-forward
expiry across two regions. If the consumer use is incompatible, use another
bearer rather than weakening consumer privacy or imposing operator licences.
