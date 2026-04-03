from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
# استيراد الشاشات
from splash_screen import SplashScreen
from home_screen import HomeScreen, FullPlayerScreen

Window.size = (360, 640)


class ZamilApp(MDApp):
    def build(self):
        # تصحيح مسار الخط بناءً على مجلدات جهازك
        LabelBase.register(name="ArabicFont", fn_regular="assets/font/arial.ttf")

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        self.sm = ScreenManager()

        # إضافة الشاشات بترتيبها الصحيح
        self.sm.add_widget(SplashScreen(name="splash"))

        # إنشاء الشاشة الرئيسية
        self.home_screen = HomeScreen(name="home")
        self.sm.add_widget(self.home_screen)

        # إضافة شاشة المشغل (player) لحل خطأ الانتقال
        self.sm.add_widget(FullPlayerScreen(home_ref=self.home_screen, name="player"))

        # الانتقال بعد 7 ثوانٍ
        Clock.schedule_once(self.switch_to_home, 7)

        return self.sm

    def switch_to_home(self, dt):
        self.sm.current = "home"


if __name__ == "__main__":
    ZamilApp().run()
