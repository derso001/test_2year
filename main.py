from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        title = Label(
            text="Ласкаво просимо!",
            font_size='24sp',
            size_hint=(1, 0.2),
            color=(1, 1, 1, 1),
        )
        layout.add_widget(title)
        for i in range(1, 5):
            btn = Button(
                text=f"Перейти на екран {i} (питання)",
                size_hint=(1, 0.2),
                background_color=(0.2, 0.6, 0.8, 1),
                color=(1, 1, 1, 1),
                font_size='18sp',
            )
            btn.bind(on_press=lambda x, i=i: setattr(self.manager, 'current', f'screen{i}'))
            layout.add_widget(btn)
        self.add_widget(layout)


class QuestionScreen(Screen):
    def __init__(self, screen_number, question, options, correct_option, **kwargs):
        super().__init__(**kwargs)
        self.correct_option = correct_option
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        question_label = Label(
            text=question,
            font_size='18sp',
            size_hint=(1, 0.4),
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle",
            text_size=(self.width, None),
        )
        question_label.bind(size=self.update_text_size)
        layout.add_widget(question_label)

        for i, option in enumerate(options, 1):
            btn = Button(
                text=f"{i}. {option}",
                size_hint=(1, 0.15),
                background_color=(0.3, 0.5, 0.9, 1),
                color=(1, 1, 1, 1),
                font_size='16sp',
            )
            btn.bind(on_press=self.check_answer)
            layout.add_widget(btn)

        back_btn = Button(
            text="На головний екран",
            size_hint=(1, 0.15),
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def update_text_size(self, instance, value):
        instance.text_size = (instance.width * 0.9, None)

    def check_answer(self, instance):
        if instance.text.endswith(self.correct_option):
            instance.background_color = (0.2, 0.8, 0.2, 1)
            instance.text = "Правильно!"
        else:
            instance.background_color = (0.8, 0.2, 0.2, 1)
            instance.text = "Неправильно!"


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))

        questions = [
            {
                "question": "Що таке Kivy?",
                "options": ["Бібліотека для створення графіки", "Бібліотека для створення GUI", "Мова програмування", "Редактор коду"],
                "correct": "Бібліотека для створення GUI"
            },
            {
                "question": "Який клас використовується для управління екранами?",
                "options": ["ScreenManager", "ScreenHandler", "WindowManager", "LayoutManager"],
                "correct": "ScreenManager"
            },
            {
                "question": "Який віджет використовується для кнопки?",
                "options": ["Label", "Button", "Input", "BoxLayout"],
                "correct": "Button"
            },
            {
                "question": "Який параметр відповідає за розміри віджета?",
                "options": ["size_hint", "pos_hint", "size", "position"],
                "correct": "size_hint"
            }
        ]

        for i, q in enumerate(questions, 1):
            sm.add_widget(QuestionScreen(screen_number=i, question=q['question'], options=q['options'], correct_option=q['correct'], name=f'screen{i}'))

        return sm


MyApp().run()