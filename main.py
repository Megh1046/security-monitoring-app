import os
import threading
import time
import webbrowser
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window

try:
    import monitor
except ImportError:
    # Handle the case where monitor.py might be missing locally
    pass

# Set Kivy background to match dashboard
Window.clearcolor = (0.05, 0.05, 0.05, 1)

# Monkey-patch monitor subprocess call so it works on Android locally
original_popen = monitor.subprocess.Popen
def patch_popen(cmd, *args, **kwargs):
    # If it's the specific command `adb logcat ...`
    if cmd and cmd[0] == 'adb' and len(cmd) > 1 and cmd[1] == 'logcat':
        # Drop the 'adb' wrapper. On Android, the app runs 'logcat' directly!
        new_cmd = ['logcat'] + cmd[2:]
        return original_popen(new_cmd, *args, **kwargs)
    return original_popen(cmd, *args, **kwargs)

class SecurityMonitorApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.label = Label(
            text="Security Monitor\n⚙️ Background Service Starting...", 
            halign='center',
            color=(0.8, 0.8, 0.8, 1),
            font_size='20sp'
        )
        self.btn = Button(
            text="Open Web Dashboard", 
            on_press=self.open_dashboard, 
            disabled=True,
            background_color=(0, 0.9, 1, 1),
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.label)
        layout.add_widget(self.btn)
        
        # Patch the Popen utility for Android
        monitor.subprocess.Popen = patch_popen
        
        # Run Flask and matching loop in background
        t = threading.Thread(target=self.run_monitor, daemon=True)
        t.start()
        
        return layout

    def run_monitor(self):
        # Callback to update UI from the monitor thread
        def update_status(text):
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.set_label(text))

        update_status("Starting Monitoring Service...")
        time.sleep(1)
        
        # Execute the main monitoring loop with a status callback
        try:
            monitor.monitor(
                device=None, 
                batch_file=None, 
                rules_path='rules.json', 
                web=True, 
                port=5000, 
                status_callback=update_status
            )
        except Exception as e:
            update_status(f"Critical Error: {str(e)}")

    def set_label(self, text):
        self.label.text = f"Security Monitor\n{text}"
        if "Error" in text:
            self.label.color = (1, 0, 0, 1) # Red
        elif "Active" in text or "Running" in text:
            self.label.color = (0, 1, 0.5, 1) # Green
            self.btn.disabled = False
        else:
            self.label.color = (0.8, 0.8, 0.8, 1)

    def open_dashboard(self, instance):
        # Try both 127.0.0.1 and 0.0.0.0 for compatibility
        webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    SecurityMonitorApp().run()
