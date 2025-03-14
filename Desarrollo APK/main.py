import os
import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock

# Configura el fondo de la ventana a blanco.
Window.clearcolor = (1, 1, 1, 1)

# --------------------------------------------------
# Funciones de persistencia usando un archivo JSON
# --------------------------------------------------
USUARIOS_FILE = "usuarios.json"

def cargar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        try:
            with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def guardar_usuario(username, password):
    usuarios = cargar_usuarios()
    usuarios[username] = password  # Nota: en producción se debe almacenar un hash de la contraseña.
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4)

# --------------------------------------------------
# Definición de las pantallas
# --------------------------------------------------
class SplashScreen(Screen):
    def on_enter(self):
        # Agenda la animación para que se inicie cuanto la pantalla ya tenga sus ids disponibles.
        Clock.schedule_once(self.start_animation, 0)

    def start_animation(self, dt):
        logo = self.ids.get("logo")
        if not logo:
            print("No se encontró el widget 'logo' en SplashScreen.")
            return
        # Animación: fade in de 2 segundos y luego fade out de 1 segundo.
        anim = Animation(opacity=1, duration=2) + Animation(opacity=0, duration=1)
        anim.bind(on_complete=self.on_animation_complete)
        anim.start(logo)

    def on_animation_complete(self, animation, widget):
        # Cambia a la pantalla de login al terminar la animación.
        self.manager.current = "login"

class LoginScreen(Screen):
    def iniciar_sesion(self):
        username = self.ids.get("username").text
        password = self.ids.get("password").text
        usuarios = cargar_usuarios()
        if username in usuarios and usuarios[username] == password:
            print("Inicio de sesión exitoso para:", username)
            # Aquí puedes redirigir a la pantalla principal de la aplicación.
        else:
            print("Credenciales incorrectas para:", username)

class RegisterScreen(Screen):
    def registrar_usuario(self):
        reg_username = self.ids.get("reg_username")
        reg_password = self.ids.get("reg_password")
        if reg_username is None or reg_password is None:
            print("Error: Los campos de registro no se encontraron.")
            return

        username = reg_username.text
        password = reg_password.text
        if username and password:
            guardar_usuario(username, password)
            print("Usuario registrado:", username)
            self.manager.current = "login"
        else:
            print("Debe ingresar un usuario y una contraseña válidos.")

class MyScreenManager(ScreenManager):
    pass

# --------------------------------------------------
# La App (No se sobreescribe build() para evitar doble carga)
# --------------------------------------------------
class DesarrolloAPKApp(App):
    # Al no sobreescribir build(), Kivy carga automáticamente "desarrolloapk.kv"
    pass

if __name__ == "__main__":
    DesarrolloAPKApp().run()
