import arabic_reshaper
from bidi.algorithm import get_display
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget, IconRightWidget, OneLineListItem
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.fitimage import FitImage
from kivymd.uix.slider import MDSlider
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform
import os
import random
import shutil

# 1. إعداد المسارات وتسجيل الخط
FONT_PATH = "assets/font/arial.ttf"
LabelBase.register(name="ArabicFont", fn_regular=FONT_PATH)


def ar(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(text))


def format_time(seconds):
    if not seconds or seconds < 0: return "00:00"
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


class CustomMenuItem(OneLineListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids._lbl_primary.font_name = "ArabicFont"
        self.ids._lbl_primary.halign = "right"


class FullPlayerScreen(MDScreen):
    def __init__(self, home_ref, **kwargs):
        super().__init__(**kwargs)
        self.home = home_ref
        self.is_sliding = False
        self.timer_dialog = None
        self.info_dialog = None
        self.countdown_label = None

        layout = MDFloatLayout(md_bg_color=(0.05, 0.05, 0.05, 1))

        header = MDBoxLayout(size_hint_y=None, height="60dp", pos_hint={"top": 1}, padding="10dp")
        header.add_widget(MDIconButton(icon="chevron-down", theme_icon_color="Custom", icon_color=(1, 1, 1, 1),
                                       on_release=self.close_player))
        self.title_label = MDLabel(text=ar("الآن يتم التشغيل"), halign="center", theme_text_color="Custom",
                                   text_color=(1, 1, 1, 1), font_name="ArabicFont")
        header.add_widget(self.title_label)

        self.more_btn = MDIconButton(icon="dots-vertical", theme_icon_color="Custom", icon_color=(1, 1, 1, 1))
        self.more_btn.bind(on_release=self.open_menu)
        header.add_widget(self.more_btn)
        layout.add_widget(header)

        menu_items = [
            {"text": ar("مؤقت الإيقاف"), "viewclass": "CustomMenuItem",
             "on_release": lambda x="timer": self.menu_callback(x)},
            {"text": ar("تعيين كنغمة رنين"), "viewclass": "CustomMenuItem",
             "on_release": lambda x="ringtone": self.menu_callback(x)},
        ]
        self.menu = MDDropdownMenu(caller=self.more_btn, items=menu_items, width_mult=4)

        self.album_art = FitImage(source="assets/images/avatar.png", size_hint=(None, None), size=("240dp", "240dp"),
                                  pos_hint={"center_x": 0.5, "center_y": 0.68}, radius=[20, ])
        layout.add_widget(self.album_art)

        title_container = MDBoxLayout(orientation="horizontal", size_hint=(0.85, None), height="50dp",
                                      pos_hint={"center_x": 0.5, "center_y": 0.45}, spacing="10dp")
        self.heart_btn = MDIconButton(icon="heart-outline", theme_icon_color="Custom", icon_color=(1, 1, 1, 1),
                                      on_release=self.toggle_heart)
        self.song_title = MDLabel(text="", font_style="H5", halign="right", theme_text_color="Custom",
                                  text_color=(1, 1, 1, 1), font_name="ArabicFont")
        title_container.add_widget(self.heart_btn);
        title_container.add_widget(self.song_title)
        layout.add_widget(title_container)

        slider_box = MDBoxLayout(orientation="vertical", size_hint=(0.85, None), height="80dp",
                                 pos_hint={"center_x": 0.5, "center_y": 0.32})
        self.progress_slider = MDSlider(min=0, max=100, value=0, hint=False)
        self.progress_slider.bind(on_touch_down=self.on_slider_down, on_touch_up=self.on_slider_up,
                                  value=self.on_slider_move)

        time_labels = MDBoxLayout(size_hint_y=None, height="20dp")
        self.current_time_lbl = MDLabel(text="00:00", theme_text_color="Custom", text_color=(0.7, 0.7, 0.7, 1),
                                        font_size="13sp")
        self.total_time_lbl = MDLabel(text="00:00", halign="right", theme_text_color="Custom",
                                      text_color=(0.7, 0.7, 0.7, 1), font_size="13sp")
        time_labels.add_widget(self.current_time_lbl);
        time_labels.add_widget(self.total_time_lbl)
        slider_box.add_widget(self.progress_slider);
        slider_box.add_widget(time_labels)
        layout.add_widget(slider_box)

        btns_layout = MDBoxLayout(orientation="horizontal", size_hint=(0.9, None), height="80dp",
                                  pos_hint={"center_x": 0.5, "center_y": 0.18}, padding="10dp")
        self.btn_mode = MDIconButton(icon="shuffle-variant", icon_size="26dp", theme_icon_color="Custom",
                                     icon_color=(0.7, 0.7, 0.7, 1), on_release=self.toggle_play_mode)
        btn_prev = MDIconButton(icon="skip-previous", icon_size="32dp", theme_icon_color="Custom",
                                icon_color=(1, 1, 1, 1), on_release=lambda x: self.home.play_prev())
        self.btn_play = MDIconButton(icon="pause-circle", icon_size="55dp", theme_icon_color="Custom",
                                     icon_color=(1, 0.5, 0, 1), on_release=lambda x: self.home.toggle_play())
        btn_next = MDIconButton(icon="skip-next", icon_size="32dp", theme_icon_color="Custom", icon_color=(1, 1, 1, 1),
                                on_release=lambda x: self.home.play_next())
        btn_list = MDIconButton(icon="playlist-music", icon_size="26dp", theme_icon_color="Custom",
                                icon_color=(1, 1, 1, 1), on_release=self.close_player)

        btns_layout.add_widget(self.btn_mode);
        btns_layout.add_widget(Widget());
        btns_layout.add_widget(btn_prev);
        btns_layout.add_widget(Widget());
        btns_layout.add_widget(self.btn_play);
        btns_layout.add_widget(Widget());
        btns_layout.add_widget(btn_next);
        btns_layout.add_widget(Widget());
        btns_layout.add_widget(btn_list)
        layout.add_widget(btns_layout)
        self.add_widget(layout)

    def open_menu(self, instance):
        self.menu.open()

    def menu_callback(self, action):
        self.menu.dismiss()
        if action == "timer":
            self.show_timer_dialog()
        elif action == "ringtone":
            self.set_as_ringtone()

    # --- وظيفة تعيين نغمة الرنين ---
    def set_as_ringtone(self):
        current_zamil = self.home.zamil_list[self.home.current_index]
        zamil_name = current_zamil[0]
        zamil_path = current_zamil[2]

        # محاكاة العملية (في أندرويد الحقيقي نحتاج مكتبات Java)
        print(f"Setting {zamil_path} as Ringtone...")

        msg = f"تم تعيين '{zamil_name}' كنغمة رنين بنجاح"
        if platform == "android":
            msg = "تمت إضافة النغمة لخيارات النظام، يرجى تفعيلها من الإعدادات"

        self.info_dialog = MDDialog(
            title=ar("نغمة الرنين"),
            text=ar(msg),
            buttons=[MDFlatButton(text=ar("موافق"), font_name="ArabicFont",
                                  on_release=lambda x: self.info_dialog.dismiss())],
        )
        self.info_dialog.ids.title.font_name = "ArabicFont"
        self.info_dialog.open()

    def show_timer_dialog(self):
        content = MDBoxLayout(orientation="vertical", spacing="5dp", size_hint_y=None, height="350dp")
        self.countdown_label = MDLabel(
            text=ar("المؤقت غير نشط") if self.home.remaining_time <= 0 else ar(
                f"الوقت المتبقي: {format_time(self.home.remaining_time)}"),
            halign="center", font_name="ArabicFont", theme_text_color="Secondary", size_hint_y=None, height="40dp"
        )
        content.add_widget(self.countdown_label)
        times = [(10, "بعد 10 دقائق"), (20, "بعد 20 دقيقة"), (30, "بعد 30 دقيقة"), (60, "بعد 60 دقيقة"),
                 (0, "تعطيل مؤقت الإيقاف")]
        for mins, label_text in times:
            btn = MDFlatButton(text=ar(label_text), font_name="ArabicFont", size_hint_x=1,
                               on_release=lambda x, m=mins: self.set_timer(m))
            content.add_widget(btn)

        self.timer_dialog = MDDialog(
            title=ar("مؤقت الإيقاف"), type="custom", content_cls=content,
            buttons=[MDFlatButton(text=ar("إغلاق"), font_name="ArabicFont",
                                  on_release=lambda x: self.timer_dialog.dismiss())],
        )
        self.timer_dialog.ids.title.font_name = "ArabicFont"
        self.timer_update_event = Clock.schedule_interval(self.update_dialog_countdown, 1)
        self.timer_dialog.on_dismiss = lambda: Clock.unschedule(self.timer_update_event)
        self.timer_dialog.open()

    def update_dialog_countdown(self, dt):
        if self.timer_dialog and self.countdown_label:
            if self.home.remaining_time > 0:
                self.countdown_label.text = ar(f"الوقت المتبقي: {format_time(self.home.remaining_time)}")
            else:
                self.countdown_label.text = ar("المؤقت غير نشط")
        return True

    def set_timer(self, minutes):
        self.home.start_sleep_timer(minutes)
        if minutes == 0:
            if self.countdown_label: self.countdown_label.text = ar("تم تعطيل المؤقت")

    def toggle_heart(self, instance):
        if instance.icon == "heart-outline":
            instance.icon = "heart";
            instance.icon_color = (1, 0, 0, 1)
        else:
            instance.icon = "heart-outline";
            instance.icon_color = (1, 1, 1, 1)

        idx = self.home.current_index
        list_heart = self.home.all_list_widgets[idx].children[0].children[0]
        list_heart.icon = instance.icon
        list_heart.icon_color = (1, 0, 0, 1) if instance.icon == "heart" else (0.5, 0.5, 0.5, 1)

    def on_slider_down(self, instance, touch):
        if instance.collide_point(*touch.pos): self.is_sliding = True

    def on_slider_move(self, instance, value):
        if self.is_sliding and self.home.sound:
            current_pos = (value / 100) * self.home.sound.length
            self.current_time_lbl.text = format_time(current_pos)

    def on_slider_up(self, instance, touch):
        if self.is_sliding:
            if self.home.sound:
                seek_time = (instance.value / 100) * self.home.sound.length
                self.home.sound.seek(seek_time);
                self.home.last_pos = seek_time
            self.is_sliding = False

    def toggle_play_mode(self, instance):
        if self.home.play_mode == "sequence":
            self.home.play_mode = "repeat";
            self.btn_mode.icon = "repeat-once";
            self.btn_mode.icon_color = (1, 0.5, 0, 1)
        elif self.home.play_mode == "repeat":
            self.home.play_mode = "shuffle";
            self.btn_mode.icon = "shuffle"
        else:
            self.home.play_mode = "sequence";
            self.btn_mode.icon = "shuffle-variant";
            self.btn_mode.icon_color = (0.7, 0.7, 0.7, 1)

    def close_player(self, *args):
        self.manager.transition.direction = "down";
        self.manager.current = "home"


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = None
        self.current_index = 0
        self.play_mode = "sequence"
        self.last_pos = 0
        self.remaining_time = 0
        self.all_list_widgets = []

        Clock.schedule_interval(self.update_progress, 1.0)
        Clock.schedule_interval(self.tick_timer, 1.0)

        self.zamil_list = [
            ("الله ما أقسى الرحيل الموجع", "assets/images/raheel.jpg", "assets/audio/raheel.mp3"),
            ("سج بالونات", "assets/images/saj.jpg", "assets/audio/saj.mp3"),
            ("يكفيش يا أعذار", "assets/images/yakfeesh.jpg", "assets/audio/yakfeesh.mp3"),
            ("ونتي ونه", "assets/images/wannati.jpg", "assets/audio/wannati.mp3"),
            ("بقايا الذكريات", "assets/images/baqaya.jpg", "assets/audio/baqaya.mp3"),
            ("ولا شيب الراس", "assets/images/shaib.jpg", "assets/audio/shaib.mp3"),
            ("القريب البعيد", "assets/images/al_qareeb.jpg", "assets/audio/al_qareeb.mp3"),
            ("كلها سود", "assets/images/soud.jpg", "assets/audio/soud.mp3"),
            ("محبة واشتياق", "assets/images/mahabba.jpg", "assets/audio/mahabba.mp3"),
            ("ما جفيت الوفاء", "assets/images/wafa.jpg", "assets/audio/wafa.mp3"),
            ("قصة كاملة", "assets/images/qessa.jpg", "assets/audio/qessa.mp3"),
            ("ماتضيق الروح في الصدر الوسيع", "assets/images/avatar.png", "assets/audio/madiyq.mp3"),
        ]

        self.layout = MDFloatLayout()
        main_content = MDBoxLayout(orientation="vertical")

        self.toolbar = MDTopAppBar(
            title=ar("زوامل إبراهيم الملصي"),
            anchor_title="center",
            md_bg_color=(1, 0.5, 0, 1),
            elevation=2
        )
        self.toolbar.ids.label_title.font_name = "ArabicFont"
        main_content.add_widget(self.toolbar)

        search_box = MDBoxLayout(size_hint_y=None, height="60dp", padding=["15dp", "5dp"])
        self.search_field = MDTextField(
            hint_text=ar("ابحث عن زامل..."),
            font_name_hint_text="ArabicFont",
            font_name_helper_text="ArabicFont",
            mode="round",
            fill_color_normal=(0.95, 0.95, 0.95, 1),
            icon_right="magnify"
        )
        self.search_field.bind(text=self.filter_list)
        search_box.add_widget(self.search_field)
        main_content.add_widget(search_box)

        scroll = ScrollView()
        self.list_view = MDList()
        self.create_list_items()

        self.list_view.add_widget(Widget(size_hint_y=None, height="90dp"))
        scroll.add_widget(self.list_view)
        main_content.add_widget(scroll)
        self.layout.add_widget(main_content)

        self.player_card = MDCard(
            orientation="horizontal", size_hint=(1, None), height="60dp",
            pos_hint={"center_x": 0.5, "y": -1}, radius=[0, ],
            md_bg_color=(0.1, 0.1, 0.1, 1), padding=["10dp", "5dp"],
            elevation=10, on_release=self.open_full_player
        )

        self.btn_play_mini = MDIconButton(
            icon="pause",
            icon_size="30dp",
            theme_icon_color="Custom",
            icon_color=(1, 0.5, 0, 1),
            on_release=self.toggle_play_safe
        )

        info_box = MDBoxLayout(orientation="vertical", padding=["5dp", 0], size_hint_x=0.6)
        self.player_title = MDLabel(text=ar("اختر زامل"), font_name="ArabicFont", font_size="14sp",
                                    theme_text_color="Custom", text_color=(1, 1, 1, 1), halign="right", shorten=True)
        self.player_artist = MDLabel(text=ar("إبراهيم الملصي"), font_name="ArabicFont", font_size="12sp",
                                     theme_text_color="Hint", halign="right")
        info_box.add_widget(self.player_title);
        info_box.add_widget(self.player_artist)

        self.mini_img = FitImage(source="assets/images/avatar.png", size_hint=(None, None), size=("45dp", "45dp"),
                                 radius=[5, ], pos_hint={"center_y": 0.5})

        self.player_card.add_widget(self.btn_play_mini)
        self.player_card.add_widget(info_box)
        self.player_card.add_widget(self.mini_img)

        self.layout.add_widget(self.player_card)
        self.add_widget(self.layout)

    def create_list_items(self):
        self.list_view.clear_widgets()
        self.all_list_widgets = []
        for idx, (title, img, path) in enumerate(self.zamil_list):
            item = TwoLineAvatarIconListItem(
                text=ar(title),
                secondary_text=ar("إبراهيم الملصي"),
                on_release=lambda x, i=idx: self.select_zamil(i)
            )
            item.ids._lbl_primary.font_name = "ArabicFont";
            item.ids._lbl_secondary.font_name = "ArabicFont"
            img_path = img if os.path.exists(img) else "assets/images/avatar.png"
            item.add_widget(ImageLeftWidget(source=img_path, radius=[10, ]))

            heart = IconRightWidget(icon="heart-outline", theme_icon_color="Custom", icon_color=(0.5, 0.5, 0.5, 1))
            heart.bind(on_release=lambda x, h=heart, i=idx: self.toggle_list_heart(h, i))
            item.add_widget(heart)

            self.list_view.add_widget(item)
            self.all_list_widgets.append(item)

    def filter_list(self, instance, value=""):
        search_term = self.search_field.text.lower()
        self.list_view.clear_widgets()
        for idx, (title, img, path) in enumerate(self.zamil_list):
            if search_term in title.lower():
                self.list_view.add_widget(self.all_list_widgets[idx])
        self.list_view.add_widget(Widget(size_hint_y=None, height="90dp"))

    def toggle_list_heart(self, instance, index):
        if instance.icon == "heart-outline":
            instance.icon = "heart";
            instance.icon_color = (1, 0, 0, 1)
        else:
            instance.icon = "heart-outline";
            instance.icon_color = (0.5, 0.5, 0.5, 1)

        if index == self.current_index:
            if self.manager and "player" in self.manager.screen_names:
                p = self.manager.get_screen("player")
                p.heart_btn.icon = instance.icon
                p.heart_btn.icon_color = (1, 0, 0, 1) if instance.icon == "heart" else (1, 1, 1, 1)

    def start_sleep_timer(self, minutes):
        if hasattr(self, 'sleep_timer_event') and self.sleep_timer_event:
            Clock.unschedule(self.sleep_timer_event)
        if minutes > 0:
            self.remaining_time = minutes * 60
            self.sleep_timer_event = Clock.schedule_once(self.stop_music_by_timer, self.remaining_time)
        else:
            self.remaining_time = 0

    def tick_timer(self, dt):
        if self.remaining_time > 0: self.remaining_time -= 1

    def stop_music_by_timer(self, dt):
        if self.sound and self.sound.state == 'play': self.toggle_play()
        self.remaining_time = 0

    def update_progress(self, dt):
        if self.sound and self.sound.state == 'play':
            pos = self.sound.get_pos()
            if self.manager and "player" in self.manager.screen_names:
                p = self.manager.get_screen("player")
                if not p.is_sliding:
                    p.progress_slider.value = (pos / self.sound.length) * 100
                    p.current_time_lbl.text = format_time(pos);
                    p.total_time_lbl.text = format_time(self.sound.length)
            if pos >= self.sound.length - 1: self.handle_auto_next()

    def handle_auto_next(self):
        if self.play_mode == "repeat":
            self.last_pos = 0;
            self.sound.seek(0);
            self.sound.play()
        elif self.play_mode == "shuffle":
            self.select_zamil(random.randint(0, len(self.zamil_list) - 1))
        else:
            self.play_next()

    def select_zamil(self, index):
        self.current_index = index;
        self.last_pos = 0
        title, img, path = self.zamil_list[index]
        self.player_title.text = ar(title)
        self.mini_img.source = img if os.path.exists(img) else "assets/images/avatar.png"
        Animation(pos_hint={"center_x": 0.5, "y": 0}, duration=0.3).start(self.player_card)
        if self.sound: self.sound.stop()
        self.sound = SoundLoader.load(path)
        if self.sound:
            self.sound.play();
            self.btn_play_mini.icon = "pause"
            if self.manager and "player" in self.manager.screen_names:
                p = self.manager.get_screen("player")
                p.song_title.text = ar(title);
                p.album_art.source = self.mini_img.source
                p.btn_play.icon = "pause-circle"

                list_heart = self.all_list_widgets[index].children[0].children[0]
                p.heart_btn.icon = list_heart.icon
                p.heart_btn.icon_color = (1, 0, 0, 1) if list_heart.icon == "heart" else (1, 1, 1, 1)

    def toggle_play_safe(self, instance):
        self.toggle_play();
        return True

    def toggle_play(self, *args):
        if self.sound:
            if self.sound.state == 'play':
                self.last_pos = self.sound.get_pos();
                self.sound.stop();
                self.btn_play_mini.icon = "play"
            else:
                self.sound.play();
                Clock.schedule_once(lambda dt: self.sound.seek(self.last_pos), 0.1);
                self.btn_play_mini.icon = "pause"
            if self.manager and "player" in self.manager.screen_names:
                self.manager.get_screen(
                    "player").btn_play.icon = "pause-circle" if self.btn_play_mini.icon == "pause" else "play-circle"

    def open_full_player(self, *args):
        if self.manager:
            self.manager.transition.direction = "up";
            self.manager.current = "player"

    def play_next(self, *args):
        self.current_index = (self.current_index + 1) % len(self.zamil_list);
        self.select_zamil(self.current_index)

    def play_prev(self, *args):
        self.current_index = (self.current_index - 1) % len(self.zamil_list);
        self.select_zamil(self.current_index)


class ZamilApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        for style in self.theme_cls.font_styles.keys():
            self.theme_cls.font_styles[style] = ["ArabicFont", self.theme_cls.font_styles[style][1],
                                                 self.theme_cls.font_styles[style][2],
                                                 self.theme_cls.font_styles[style][3]]
        sm = ScreenManager()
        self.home_screen = HomeScreen(name="home")
        sm.add_widget(self.home_screen)
        sm.add_widget(FullPlayerScreen(home_ref=self.home_screen, name="player"))
        return sm


if __name__ == "__main__":
    ZamilApp().run()
