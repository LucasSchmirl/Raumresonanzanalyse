# This is the `Raumresonanzanalyse` Project
created by Lucas Schmirl on: 30.05.2025, last edit: 30.05.2025

<br>

Contact me: [E-Mail](mailto:info.hellgineer@gmail.com?subject=User%20Question&body=I%20like%20your%20code%20man,%20keep%20it%20up.)


Check out my Homepage: [Hellgineer](https://hellgineer.com)

---

# Erklärung

Dieses Projekt führt eine Raumresonanzanalyse durch, indem es einen linearen Chirp-Ton von 40 Hz bis 300 Hz über Lautsprecher abspielt und gleichzeitig mit dem Mikrofon die Raumantwort aufnimmt.  
Anschließend wird das aufgenommene Signal in kurzen Fenstern analysiert, um die Frequenz mit der höchsten Resonanz (RMS-Amplitude) zu ermitteln.  

Der Benutzer wird danach gefragt, ob er diese vermutete Eigenfrequenz für 5 Sekunden anhören möchte.
Die Ergebnisse werden als Plot gespeichert und angezeigt.
Das Skript eignet sich gut, um die tiefen Resonanzfrequenzen eines Raumes schnell zu identifizieren.


## 1. Install dependencies
```bash
pip3 install -r requirements.txt
```

## 2. Run analysis
```bash
python3 resonance_analysis.py
```

## 3. Use for scientific purposes or to annoy your roommates/colleagues.
---

