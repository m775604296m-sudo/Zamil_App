import arabic_reshaper
from bidi.algorithm import get_display
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivy.graphics import Color, Ellipse
from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivymd.uix.label import MDIcon


def ar(text):
    if not text: return ""
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text


class CircularAvatarWithBorder(RelativeLayout):
    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = ("170dp", "170dp")
        self.pos_hint = {"center_x": 0.5}
        with self.canvas:
            Color(1, 0.84, 0, 1)
            self.bg_circle = Ellipse(pos=(0, 0), size=self.size)

        self.add_widget(FitImage(
            source=source,
            size_hint=(None, None),
            size=self.size,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            radius=[85, ]
        ))


class SplashScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        app = MDApp.get_running_app()
        app.theme_cls.font_styles.update({
            "H5": ["ArabicFont", 22, False, 0.15],
            "Body1": ["ArabicFont", 16, False, 0.15],
        })

        main_layout = MDBoxLayout(orientation="vertical", padding=("20dp", "15dp", "20dp", "20dp"), spacing="10dp")

        # 1. الصورة الشخصية
        main_layout.add_widget(CircularAvatarWithBorder(source="assets/images/avatar.png"))

        # 2. العنوان الرئيسي
        main_layout.add_widget(MDLabel(
            text=ar("زوامل إبراهيم الملصي"),
            halign="center",
            font_name="ArabicFont",
            font_style="H5",
            bold=True,
            size_hint_y=None,
            height="40dp",
            text_color=(1, 1, 1, 1),
            theme_text_color="Custom"
        ))

        # 3. السبينر
        spinner_layout = MDBoxLayout(size_hint=(None, None), size=("30dp", "30dp"), pos_hint={"center_x": 0.5},
                                     spacing="5dp")
        spinner_layout.add_widget(MDSpinner(active=True, color=(1, 0.84, 0, 1), line_width="1.5dp"))
        main_layout.add_widget(spinner_layout)

        # 4. نص جاري البحث
        main_layout.add_widget(MDLabel(
            text=ar("...جاري البحث عن الزوامل"),
            halign="center",
            font_name="ArabicFont",
            theme_text_color="Hint",
            font_size="13sp",
            size_hint_y=None,
            height="20dp"
        ))

        # 5. كارد معلومات التواصل (المربع الأصفر)
        contact_card = MDCard(
            orientation="vertical",
            padding=("10dp", "2dp", "10dp", "10dp"),  # تقليل الـ padding العلوي جداً (2dp) لرفع المحتوى
            size_hint=(0.85, None),
            height="165dp",  # تقليل الارتفاع الكلي ليناسب المحتوى المرفوع
            pos_hint={"center_x": 0.5},
            line_color=(1, 0.84, 0, 1),
            radius=[12, ],
            style="outlined",
            md_bg_color=(0, 0, 0, 0.6),
            elevation=2
        )

        card_content = MDBoxLayout(orientation="vertical", spacing="0dp")

        # عنوان الكارد (تصميم وبرمجة)
        card_content.add_widget(MDLabel(
            text=ar("تصميم وبرمجة: محمد الصلبة"),
            halign="center",
            font_name="ArabicFont",
            theme_text_color="Custom",
            text_color=(1, 0.84, 0, 1),
            bold=True,
            font_size="15sp",
            size_hint_y=None,
            height="85dp"  # تقليل الارتفاع لتقريب العناصر
        ))

        # --- قسم معلومات التواصل ---
        info_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height="85dp")

        # إزاحة لليسار ليبقى النص داخل الحدود
        info_layout.add_widget(Widget(size_hint_x=0.12))

        lines_container = MDBoxLayout(orientation="vertical", spacing="8dp")  # تقليل المسافات بين الأسطر

        ICON_SIZE = ("18dp", "18dp")
        ICON_COLOR = (1, 0.84, 0, 1)
        TEXT_COLOR = (1, 1, 1, 0.7)
        LABEL_WIDTH = "175dp"

        # 1. البريد
        email_line = MDBoxLayout(orientation="horizontal", spacing="10dp", size_hint_y=None, height="20dp")
        email_line.add_widget(MDIcon(icon="email-outline", size_hint=(None, None), size=ICON_SIZE, color=ICON_COLOR,
                                     pos_hint={"center_y": 0.5}))
        email_line.add_widget(
            MDLabel(text="m775604296@gmail.com", font_size="12sp", theme_text_color="Custom", text_color=TEXT_COLOR,
                    size_hint_x=None, width=LABEL_WIDTH, halign="left"))
        lines_container.add_widget(email_line)

        # 2. الهاتف
        phone_line = MDBoxLayout(orientation="horizontal", spacing="10dp", size_hint_y=None, height="20dp")
        phone_line.add_widget(FitImage(source="assets/images/pho.png", size_hint=(None, None), size=ICON_SIZE,
                                       pos_hint={"center_y": 0.5}))
        phone_line.add_widget(
            MDLabel(text="+967 775604296", font_size="12sp", theme_text_color="Custom", text_color=TEXT_COLOR,
                    size_hint_x=None, width=LABEL_WIDTH, halign="left"))
        lines_container.add_widget(phone_line)

        # 3. إنستقرام
        insta_line = MDBoxLayout(orientation="horizontal", spacing="10dp", size_hint_y=None, height="20dp")
        insta_line.add_widget(FitImage(source="assets/images/ins.png", size_hint=(None, None), size=ICON_SIZE,
                                       pos_hint={"center_y": 0.5}))
        insta_line.add_widget(
            MDLabel(text="mohammed_alslbh_711", font_size="12sp", theme_text_color="Custom", text_color=TEXT_COLOR,
                    size_hint_x=None, width=LABEL_WIDTH, halign="left"))
        lines_container.add_widget(insta_line)

        info_layout.add_widget(lines_container)
        card_content.add_widget(info_layout)

        contact_card.add_widget(card_content)
        main_layout.add_widget(contact_card)

        self.add_widget(main_layout)
