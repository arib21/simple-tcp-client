# KivyMD Imports
from kivy.core import text
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.bottomsheet import MDListBottomSheet
# Kivy Imports
from kivy.lang import Builder
from kivy.utils import platform
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import LabelBase
# Generic Imports
import webbrowser
import socket

if platform == "android":
    from android.permissions import request_permissions
    from android.permissions import Permission

class save_config_name(BoxLayout): pass

class main(MDApp):
    def on_start(self):
        if platform == "android":
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])

    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Dark"
        buildedKV = Builder.load_file("main.kv")
        return buildedKV

    def open_github(self):
        webbrowser.open("https://github.com/arib21/simple-tcp-client")

    def connect(self, server_ip, server_port, disconnect_btn):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((server_ip.text, int(server_port.text)))
            Snackbar(
                text=f"Successfully connected to {server_ip.text}:{server_port.text}!",
                font_size="12sp"
            ).open()
            disconnect_btn.disabled = False
        except socket.gaierror as error:
            error_dialog = Snackbar(
                text="Please, enter a valid IP Address and Port Number",
                font_size="12sp"
            )
            error_dialog.open()
        except socket.error as error:
            error_dialog = Snackbar(
                text=f"Coudn't connect to {server_ip.text}."
            )
            error_dialog.open()
        except:
            error_dialog = Snackbar(
                text="Please, enter a valid IP Address and Port Number",
                font_size="12sp"
            )
            error_dialog.open()

    def disconnect(self, server_ip, server_port, disconnect_btn):
        try:
            client.close()
            disconnect_btn.disabled = True
            Snackbar(
                text="Successfully disconnected..."
            ).open()

        except:
            Snackbar(
                text="Couldn't disconnect..."
            ).open()
    
    def save_config(self, server_ip, server_port):
        if server_ip == "" or server_port == "":
            Snackbar(
                    text="Please enter an IP Address & Port"
            ).open()
        else:
            with open("configs.txt", "a") as config_file:
                config_file.write(f"{server_ip}:{server_port}\n")
                Snackbar(
                    text="Successfully saved..."
                ).open()

    def import_load_to_box(self, *args):
        ip_port = args[0]
        ip_port = ip_port.split(":")
        self.root.ids.server_ip.text = ip_port[0]
        self.root.ids.server_port.text = ip_port[1]

    def import_config(self, server_ip, server_port):
        with open("tcp_client_config.txt", "r") as config_file:
            bottom_sheet = MDListBottomSheet()
            bottom_sheet.radius = 10
            bottom_sheet.radius_from = "top"
            configs = config_file.readlines()
            for i in configs:
                i = i.removesuffix("\n")
                bottom_sheet.add_item(f"{i}", lambda x, y=i: self.import_load_to_box(f"{y}"))
            bottom_sheet.open()

    def action_button_sorter(self, instance):
        if instance.icon == "import":
            self.import_config(self.root.ids.server_ip.text, self.root.ids.server_port.text)
        if instance.icon == "content-save":
            self.save_config(self.root.ids.server_ip.text, self.root.ids.server_port.text)

if __name__ == "__main__":
    main().run()
