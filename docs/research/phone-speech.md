# Phone speech and location research

**FACT:** Android exposes `isOnDeviceRecognitionAvailable` and
`createOnDeviceSpeechRecognizer`; availability must be checked. Apple exposes
`supportsOnDeviceRecognition` and a request's `requiresOnDeviceRecognition`.
These APIs do not guarantee offline recognition for every device or language.
Sources: [Android SpeechRecognizer](https://developer.android.com/reference/android/speech/SpeechRecognizer),
[Apple recognizer capability](https://developer.apple.com/documentation/speech/sfspeechrecognizer/supportsondevicerecognition)
and [Apple offline request](https://developer.apple.com/documentation/speech/sfspeechrecognitionrequest/requiresondevicerecognition).

**DESIGN DECISION:** phone microphone and compute for optional extra detail;
no baseline device microphone, speech processor or network transcription service.
Do not silently upload audio if an offline request fails. Keep raw audio off
the road network; even recognised free text is outside experimental v1.

Experiment matrix: Android/iOS versions, installed language models, offline
startup, airplane-mode operation, locked/background phone, BLE disconnect,
noise/accent sensitivity, permission denial, battery cost and end-to-end latency.
Report failures without blocking the physical button's basic event path. Keep
voice configuration and reviewing transcription stationary-only.

Location experiment: phone GNSS with BLE should transmit position, timestamp,
accuracy and explicit validity, not last-known coordinates masquerading as a
fresh fix. Measure background restrictions on both platforms before relying on
phone location. The current simulator has perfect known location and time;
real stale-fix policy belongs in the device requirements.
