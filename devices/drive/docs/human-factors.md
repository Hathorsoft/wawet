# Driver safety and human factors

Status: research plan, not a claim of safety or legal compliance. GOV.UK notes
restrictions on handheld devices and that hands-free use still requires proper
control and an unobstructed view. [Official guidance](https://www.gov.uk/using-mobile-phones-when-driving-the-law).

**DESIGN DECISION:** common reporting should be one simple tactile action.
Pairing, remapping, updates, transcription review and diagnostics are stationary-
only operations. A phone map is optional and should not become the ordinary
report path. The device is advisory, not an emergency service or navigation
instruction generator.

Do not freeze the example categories into six buttons. Begin with mockups of
three and four differentiated inputs; compare size, spacing, texture/shape,
reach and glove use. Test sight-independent differentiation and accidental
activation during bumps, cleaning or passenger interaction. Labels/colour alone
are insufficient for accessibility. International categories require language
and legal review before a camera/police button is selected.

Compare short press and guarded/long press: accidental prevention trades off
interaction duration. Double press may increase cognitive load. A local undo
can cancel unsent reports, but cannot revoke bytes already received. Network
withdrawal/negative reports require explicit protocol authority and are not
implemented. Do not advertise a universal cancellation feature.

Compare subtle LED acknowledgement, optional low-volume sound and haptic
feedback. Avoid glare, startling audio and repetitive alert storms. Users should
be able to adjust feedback while stationary. A no-fix acknowledgement must be
distinct from “report sent”; “sent” must be distinct from delivered or confirmed.

Mounting tests must check view obstruction, reach, cable strain, theft/removal,
impact risk, antenna orientation, heat and adhesive reliability. Use a modular
mount interface so no untested permanent mounting choice drives PCB layout.

Study gate: stationary usability first, then supervised closed-course testing
with an appropriate safety protocol; no public-road distraction experiments in
this iteration. Record task time, eyes-off-road duration, misclassification,
missed acknowledgement, accidental activation and subjective workload, including
participants with accessibility needs. Set quantitative acceptance thresholds
with qualified human-factors input before claiming the design is safe.
