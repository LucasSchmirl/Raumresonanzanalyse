import numpy as np
import sounddevice as sd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
from scipy.signal import chirp

# Einstellungen
start_freq = 40
end_freq = 300
duration = 10.0       # Gesamtdauer Sweep in Sekunden
volume = 0.5
sample_rate = 44100

os.makedirs("plots", exist_ok=True)

# Chirp-Signal: 40 bis 300 Hz
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
wave = chirp(t, f0=start_freq, f1=end_freq, t1=duration, method='linear')

# Fade-in/out 50ms
fade_duration = 0.05
fade_samples = int(sample_rate * fade_duration)
envelope = np.ones_like(wave)
envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
wave *= envelope

print("🔊 Starte Chirp-Sweep...")

recording = sd.playrec(volume * wave, samplerate=sample_rate, channels=1, dtype='float64', blocking=True)
sd.wait()
print("✅ Aufnahme abgeschlossen")

recording = recording.flatten()

# Parameter für Fensteranalyse
window_size = int(sample_rate * 0.05)  # 50 ms Fenster
step_size = int(window_size / 2)       # 50% Überlappung

# Zeitfenster für Analyse
num_windows = (len(recording) - window_size) // step_size + 1

rms_values = []
freqs = []

for i in range(num_windows):
    start = i * step_size
    end = start + window_size
    segment = recording[start:end]
    
    # RMS der Aufnahme im Fenster
    rms = np.sqrt(np.mean(segment**2))
    rms_values.append(rms)
    
    # Frequenz in diesem Fenster aus linearer Sweep-Zeit Frequenz Beziehung
    time_pos = (start + window_size / 2) / sample_rate
    freq = start_freq + (end_freq - start_freq) * (time_pos / duration)
    freqs.append(freq)

# Glätten der RMS-Werte mit gleitendem Mittelwert
def smooth(x, w=5):
    return np.convolve(x, np.ones(w)/w, mode='same')

rms_smooth = smooth(rms_values, w=7)

# Finde Resonanzfrequenz (höchster RMS-Wert)
max_index = np.argmax(rms_smooth)
resonance_freq = freqs[max_index]
print(f"🔔 Vermutete Eigenfrequenz dieses Raumes: {resonance_freq:.1f} Hz")

# Nachfrage, ob abgespielt werden soll
antwort = input(f"Möchtest du die Frequenz {resonance_freq:.1f} Hz für 5 Sekunden abspielen? (j/n): ").strip().lower()

if antwort == 'j':
    print(f"🔊 Spiele {resonance_freq:.1f} Hz für 5 Sekunden ab...")
    t_play = np.linspace(0, 5, int(sample_rate * 5), endpoint=False)
    sine_wave = 0.5 * np.sin(2 * np.pi * resonance_freq * t_play)
    
    # Fade-in/out 50ms
    fade_samples = int(sample_rate * 0.05)
    envelope = np.ones_like(sine_wave)
    envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
    envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
    sine_wave *= envelope
    
    sd.play(sine_wave, samplerate=sample_rate)
    sd.wait()
    print("✅ Abspielen beendet.")
else:
    print("Abspielen übersprungen.")

# Plot
plt.figure(figsize=(15, 10))
plt.plot(freqs, rms_smooth, marker='o')
plt.title("Raumresonanzanalyse (Chirp Sweep, 40–300 Hz)")
plt.xlabel("Frequenz (Hz)")
plt.ylabel("RMS-Amplitude (Aufnahme)")
plt.xlim(start_freq, end_freq)
plt.xticks(np.arange(start_freq, end_freq + 10, 10))
plt.grid(True)
plt.tight_layout()

plt.savefig("plots/resonanzanalyse__40_bis_300Hz.png")
plt.show()