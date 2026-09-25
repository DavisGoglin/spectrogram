# JP Pitch Accent Analyzer

> **⚠️ Made with an LLM.** This project was written by large
> language model.
> I don't have the audio background to verify anything it wrote, it just looks roughly accurate.

A single-page web app for practising **Japanese pitch accent**. It
tracks the fundamental frequency of your microphone in real time and
scrolls it right-to-left as a pitch contour, optionally over a spectrogram.
You can load a reference audio file, compare its pitch against yours, and
record/replay your own attempts.

Hosted here: https://davisgoglin.github.io/spectrogram/

---

## Features

- **Real-time pitch tracking** from the microphone, scrolling right-to-left.
- **Reference file overlay** — load an audio file, see its pitch contour drawn
  over your live mic, with looping and speed controls.
- **Record / replay / download** — toggle or hold record modes with instant playback and download.
- **Optional spectrogram** behind the contour.
- **Whole-window drag & drop** for loading audio.
- **Settings persist** across refreshes (but audio doesn't).
- **Pitch method selector**: Praat-style autocorrelation + Viterbi (default),
  YIN, plain autocorrelation, or **None** (spectrogram only — pitch tracking off.

---

## Quick start

The microphone (`getUserMedia`) only works in a **secure context**: `https://`
or `http://localhost`. Opening the file directly (`file://`) will not work
reliably.

### Option A — same machine (simplest)

```bash
cd spectrogram
python3 -m http.server 8000 --bind 127.0.0.1
# then open http://localhost:8000
```

### Option B — from another device (phone, laptop) over HTTPS

`serve.py` serves the folder over HTTPS with a self-signed certificate
(generated with `openssl`; no third-party packages needed).

```bash
cd spectrogram
python3 serve.py
# prints e.g. https://localhost:8443 and https://<lan-ip>:8443
# accept the certificate warning once, then allow the mic
```
---

## Hotkeys

| Key        | Action                                              |
| ---------- | --------------------------------------------------- |
| `V` (hold) | Push-to-talk: record while held, play back on release |
| `R`        | Toggle recording                                    |
| `P`        | Replay the last recording                           |
| `S`        | Pause / resume scrolling                            |
| `H`        | Show / hide the control panel                       |
| `Esc`      | Reopen the panel                                    |


---

## Recording notes

- Recordings are analysed with the currently selected pitch method and drawn as
  a separate trace while they play back.
- **Clips are not persisted** across reloads — download the WAV if you want to
  keep one.
- By default the reference file is paused while recording so it doesn't bleed
  through your speakers into the take. Turn that off (with headphones) if you
  want to record along with the reference.

---

## Credits / inspiration

- Layout and the scrolling-spectrogram idea are inspired by
  [borismus/spectrogram](https://github.com/borismus/spectrogram). This is an
  independent implementation focused on pitch (F0) tracking rather than a
  general spectrogram.
- Pitch method follows the spirit of Praat's autocorrelation pitch analysis
  (Boersma) and YIN (de Cheveigné & Kawahara, 2002).

## License

MIT assuming there isn't any copied code in here from incompatible licenses
