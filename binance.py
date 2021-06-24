#!/usr/bin/python3

from datetime import datetime
import os
import re
import requests
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, Gdk, GLib


COINS = [
    'BTC/USDT',
    'ETH/USDT',
    'TRX/USDT',
    # 'XMR/USDT', # how to create : Binance coin name XMRUSDT to XMR/USDT
]

APP_ID = "Binance Prices"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ICON = os.path.join(BASE_DIR, 'coin.png')

class EntryWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Get Coins Price From Binance")
        self.window_is_hidden = False
        self.set_property('resizable', False)  
        self.deactive_coins = set()
        self.get_screen_size()
        self.set_border_width(10)
        self.set_size_request(100, 50)
        self.set_skip_taskbar_hint(True)
        self.interval = 60
        self.proxies = {'https': None}           
        self.statusIcon = Gtk.StatusIcon()
        self.statusIcon.connect("activate", self.onIconClick)
        self.statusIcon.set_from_file(ICON)
        self.label_price = Gtk.Label(label="\n")
        self.main_view()
        self.update()

    def main_view(self):
        self.box_outer = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(self.box_outer)

        # Time Buttons
        hbox = Gtk.Box(spacing=6)
        hbox.set_halign(1)
        hbox = Gtk.Box(spacing=6)
        hbox.set_halign(1)
        label = Gtk.Label(label="Result Time   ",)
        hbox.pack_start(label, False, False, 0)
        button1 = Gtk.RadioButton.new_with_label_from_widget(None, "1")
        button1.connect("toggled", self.on_button_toggled)
        hbox.pack_start(button1, False, False, 0)
        button2 = Gtk.RadioButton.new_with_mnemonic_from_widget(button1, "5")
        button2.connect("toggled", self.on_button_toggled,)
        hbox.pack_start(button2, False, False, 0)
        button3 = Gtk.RadioButton.new_with_mnemonic_from_widget(button1, "10")
        button3.connect("toggled", self.on_button_toggled,)
        hbox.pack_start(button3, False, False, 0)
        button4 = Gtk.RadioButton.new_with_mnemonic_from_widget(button1, "30")
        button4.connect("toggled", self.on_button_toggled,)
        hbox.pack_start(button4, False, False, 0)
        button5 = Gtk.RadioButton.new_with_mnemonic_from_widget(button1, "60")
        button5.connect("toggled", self.on_button_toggled,)
        hbox.pack_start(button5, False, False, 0)
        self.box_outer.pack_start(hbox, False, False, 0)

        # Http Proxy
        hbox = Gtk.Box(spacing=6)
        hbox.set_halign(1)
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text(
            "Type your Http Proxy and press enter".title())
        self.entry.connect("activate", self.on_http_proxy,)
        self.entry.set_width_chars(35)
        hbox.pack_start(self.entry, False, False, 0)
        self.box_outer.pack_start(hbox, False, False, 0)

        # Progress Bar
        self.progressbar = Gtk.ProgressBar()
        self.box_outer.pack_start(self.progressbar, False, False, 5)

        # Coin Section
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.box_outer.pack_start(listbox, False, False, 5)
        box_inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        box_inner.set_halign(3)
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row_2 = Gtk.ListBoxRow()
        hbox_2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        count = 0
        for coin in COINS:
            self.check_editable = Gtk.CheckButton(label=coin)
            self.check_editable.connect("toggled", self.on_editable_toggled)
            if count < 3:
                hbox.pack_start(self.check_editable, False, True, 0)
            else:
                hbox_2.pack_start(self.check_editable, False, True, 0)
                self.deactive_coins.add(coin)
            self.check_editable.set_active(True)
            count += 1
        row.add(hbox)
        box_inner.add(row)
        row_2.add(hbox_2)
        box_inner.add(row_2)
        listbox.add(box_inner)
        self.box_outer.pack_start(self.label_price, False, False, 0)

    def get_screen_size(self):
        display = Gdk.Display.get_default()
        x, y = (display.get_monitor(0).get_geometry().width,
                display.get_monitor(0).get_geometry().height)
        self.move(x * 0.75, 50)

    def req_binance(self):
        api_url = "https://api3.binance.com/api/v3/ticker/price"
        try:
            req = requests.get(
                api_url,
                proxies=self.proxies,
            )
            if req.status_code == 200:
                result = req.json()
        except requests.exceptions.ConnectionError:
            result = None
        return result

    def update(self, req=True):
        child = None
        label = f"<span foreground='lime' font_desc='Sans Normal 16 green'>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{29*'-'}\n"
        for chd in self.box_outer:
            if chd == self.label_price:
                child = chd
        if req:
            result = self.req_binance()
            active_coins = [c for c in COINS if c not in self.deactive_coins]
            if result:
                unmask = dict((i.replace("/", ''), i) for i in active_coins)
                sort_result = list(coin for coin in result if coin['symbol'] in [
                                   i.replace("/", '') for i in active_coins])
                count = 0
                for coin in sort_result:
                    label += f"{unmask[coin['symbol']]} : {float(coin['price'])} $\n"
                    count += 1
            else:
                self.interval = 3600
                label += "** No Internet Connection !! **\n"
            label += '</span>'
            child.set_markup(label)
            child.set_justify(Gtk.Justification.FILL)
            child.set_line_wrap(True)
            self.resize(100, len(active_coins) * 5)
        GLib.timeout_add(self.interval, self.update_progressbar)
        return GLib.SOURCE_CONTINUE

    def update_progressbar(self):
        if self.progressbar.get_fraction() == 1.0:
            self.progressbar.set_fraction(0.0)
            return False, self.update(req=False)
        fraction = self.progressbar.get_fraction() + 0.001
        self.progressbar.set_fraction(fraction)
        if fraction > 1:
            self.progressbar.set_fraction(0.0)
            return False, self.update()
        return True

    def on_button_toggled(self, button):
        if button.get_active():
            self.interval = int(button.get_label()) * 60
            self.progressbar.set_fraction(1.0)

    def on_http_proxy(self, entry):
        entry = entry.get_text()
        REGEX = r"(http|https)://([\w\-\.]+)(:(\d{2,5}))?"
        if re.match(REGEX, entry):
            self.proxies["https"] = entry
            self.update()

    def on_editable_toggled(self, button):
        if not button.get_active():
            self.deactive_coins.add(button.get_label())
        elif button.get_active() and button.get_label() in self.deactive_coins:
            self.deactive_coins.remove(button.get_label())

    def onIconClick(self, *args):
        self.deiconify()
        self.present()

if __name__ == "__main__":
    win = EntryWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
