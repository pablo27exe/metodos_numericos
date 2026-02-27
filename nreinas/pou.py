import sounddevice as sd
import numpy as np
import wave
import os
from scipy.io.wavfile import write
import time

class PouSoundRecorder:
    def __init__(self):
        self.sounds = {}
        self.available_colors = ['rojo', 'verde', 'azul', 'amarillo']
        self.sample_rate = 44100
        self.duration = 2  # duración de cada grabación en segundos
        self.recordings_dir = "pou_recordings"
        
        # Crear directorio para grabaciones si no existe
        if not os.path.exists(self.recordings_dir):
            os.makedirs(self.recordings_dir)
    
    def wait_for_user_start(self):
        """Espera a que el usuario indique que quiere comenzar a grabar"""
        print("\n⏸️  Presiona ENTER cuando quieras COMENZAR a grabar...")
        print("(El programa grabará durante 2 segundos después de presionar ENTER)")
        input()
        print("🎤 ¡Grabando! Haz el sonido ahora...")
    
    def record_sound(self, duration=None):
        """Graba un sonido con la duración especificada"""
        if duration is None:
            duration = self.duration
        
        # Esperar a que el usuario indique que quiere comenzar
        self.wait_for_user_start()
        
        # Grabar audio
        recording = sd.rec(int(duration * self.sample_rate), 
                          samplerate=self.sample_rate, 
                          channels=1, 
                          dtype='int16')
        sd.wait()  # Esperar hasta que termine la grabación
        
        print("✅ Grabación completada")
        return recording
    
    def save_sound(self, recording, color):
        """Guarda el sonido en un archivo WAV"""
        filename = f"{self.recordings_dir}/pou_{color}.wav"
        write(filename, self.sample_rate, recording)
        return filename
    
    def ask_for_color(self):
        """Pregunta al usuario a qué color corresponde el sonido grabado"""
        print("\n🎨 ¿A qué color de Pou corresponde este sonido?")
        print("Colores disponibles:", ", ".join(self.available_colors))
        
        while True:
            color = input("Color: ").strip().lower()
            
            if color in self.available_colors:
                if color in self.sounds:
                    overwrite = input(f"⚠️  Ya existe un sonido para Pou {color}. ¿Sobrescribir? (s/n): ").strip().lower()
                    if overwrite != 's':
                        continue
                return color
            else:
                print("❌ Color no válido. Usa: rojo, verde, azul o amarillo")
    
    def record_single_sound(self):
        """Graba un solo sonido y pregunta por su color"""
        print(f"\n{'='*40}")
        print("GRABAR NUEVO SONIDO")
        print(f"{'='*40}")
        
        # Mostrar colores que ya tienen sonido
        if self.sounds:
            print("Colores ya grabados:", ", ".join(self.sounds.keys()))
        
        # Grabar el sonido (espera a que el usuario inicie)
        recording = self.record_sound()
        
        # Preguntar el color
        color = self.ask_for_color()
        
        # Guardar el sonido
        filename = self.save_sound(recording, color)
        self.sounds[color] = filename
        
        print(f"✅ Sonido guardado para Pou {color}: {filename}")
        return color
    
    def record_all_sounds(self):
        """Graba los sonidos para los 4 colores de Pou"""
        print("🎮 CONFIGURACIÓN DE SONIDOS POU")
        print("=" * 50)
        print("Para cada Pou, espera a que suene en el juego y")
        print("presiona ENTER para grabar su sonido.")
        print("=" * 50)
        
        sounds_to_record = 4
        
        for i in range(sounds_to_record):
            print(f"\n📝 Sonido {i+1} de {sounds_to_record}")
            print("Prepara el sonido del Pou...")
            
            # Grabar y asignar color
            color = self.record_single_sound()
        
        print("\n🎉 ¡Todos los sonidos han sido configurados!")
        self.show_summary()
    
    def show_summary(self):
        """Muestra un resumen de los sonidos grabados"""
        print("\n📊 RESUMEN DE SONIDOS GRABADOS:")
        print("-" * 35)
        for color, filename in self.sounds.items():
            file_exists = "✅" if os.path.exists(filename) else "❌"
            print(f"{file_exists} Pou {color:8} -> {filename}")
    
    def listen_and_identify(self, listen_duration=5):
        """Escucha y trata de identificar los sonidos en tiempo real"""
        if len(self.sounds) < 4:
            print("❌ Debes grabar los 4 sonidos primero")
            return
        
        print(f"\n🎧 Modo escucha activado ({listen_duration} segundos)...")
        print("Escuchando sonidos de Pou...")
        print("Los sonidos detectados se mostrarán por consola")
        
        detected_sequence = []
        start_time = time.time()
        
        def audio_callback(indata, frames, time_info, status):
            if status:
                print(f"Error de audio: {status}")
            
            # Detección simple de sonido
            audio_level = np.max(np.abs(indata))
            if audio_level > 0.1:  # Umbral ajustable
                current_time = time.time() - start_time
                print(f"🔊 Sonido detectado! Tiempo: {current_time:.1f}s")
        
        try:
            with sd.InputStream(callback=audio_callback,
                              channels=1,
                              samplerate=self.sample_rate,
                              blocksize=int(self.sample_rate * 0.1)):
                print("Escuchando... Presiona Ctrl+C para detener")
                time.sleep(listen_duration)
                
        except KeyboardInterrupt:
            print("\n⏹️ Escucha detenida por el usuario")
        
        return detected_sequence
    
    def simulate_game_sequence(self):
        """Simula una secuencia de juego y muestra los colores"""
        if len(self.sounds) < 4:
            print("❌ Necesitas grabar los 4 sonidos primero")
            return
        
        colors = list(self.sounds.keys())
        sequence_length = int(input("Longitud de la secuencia (ej: 5): ") or "5")
        
        print(f"\n🎮 SIMULANDO SECUENCIA DE JUEGO ({sequence_length} sonidos)")
        print("La secuencia se mostrará automáticamente:")
        
        sequence = []
        for i in range(sequence_length):
            color = np.random.choice(colors)
            sequence.append(color)
            print(f"Sonido {i+1}: 🔊 [Pou {color}]")
            time.sleep(1.5)  # Pausa entre sonidos
        
        print(f"\n🎯 Secuencia completa: {' → '.join(sequence)}")
    
    def test_individual_recording(self):
        """Prueba la grabación de un sonido específico"""
        print("\n🧪 PRUEBA DE GRABACIÓN INDIVIDUAL")
        print("Presiona ENTER cuando quieras grabar un sonido de prueba")
        
        recording = self.record_sound()
        print("✅ Grabación de prueba completada")
        
        # Reproducir el sonido grabado para verificar
        play = input("¿Quieres reproducir el sonido grabado? (s/n): ").strip().lower()
        if play == 's':
            print("🔊 Reproduciendo...")
            sd.play(recording, self.sample_rate)
            sd.wait()
            print("✅ Reproducción completada")

def main():
    recorder = PouSoundRecorder()
    
    while True:
        print("\n" + "=" * 50)
        print("           GRABADOR DE SONIDOS POU")
        print("=" * 50)
        print("1. ▶️  Grabar todos los sonidos (4 Pous)")
        print("2. 🎤 Grabar un solo sonido")
        print("3. 📊 Ver sonidos grabados")
        print("4. 🎧 Modo escucha (detección)")
        print("5. 🎮 Simular secuencia de juego")
        print("6. 🔄 Probar grabación individual")
        print("7. ❌ Salir")
        
        choice = input("\nSelecciona una opción (1-7): ").strip()
        
        if choice == '1':
            recorder.record_all_sounds()
        elif choice == '2':
            recorder.record_single_sound()
        elif choice == '3':
            recorder.show_summary()
        elif choice == '4':
            duration = int(input("Duración de escucha (segundos): ") or "10")
            recorder.listen_and_identify(duration)
        elif choice == '5':
            recorder.simulate_game_sequence()
        elif choice == '6':
            recorder.test_individual_recording()
        elif choice == '7':
            print("¡Hasta luego! 🎮")
            break
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    # Verificar dependencias
    print("🔧 Verificando dependencias...")
    try:
        import sounddevice
        import scipy
        print("✅ Todas las dependencias están instaladas")
    except ImportError as e:
        print(f"❌ Faltan dependencias: {e}")
        print("Instala con: pip install sounddevice scipy numpy")
        exit(1)
    
    main()