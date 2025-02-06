import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import RenderContext, Mesh
from kivy.graphics.transformation import Matrix
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.input.motionevent import MotionEvent
from kivy.uix.boxlayout import BoxLayout
import math

kivy.require('2.1.0')  # Kivy version

# مختصات مکعب
vertices = [
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
]

# خطوط مکعب
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

class Cube3D(Widget):
    def __init__(self, **kwargs):
        super(Cube3D, self).__init__(**kwargs)
        self.size = Window.size
        self.pos = (0, 0)
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.touch_pos = None
        self.render_context = RenderContext()
        self.canvas.add(self.render_context)

    def draw_cube(self):
        with self.render_context:
            self.canvas.clear()
            glEnable(GL_DEPTH_TEST)

            # ماتریس چرخش برای نمایش سه‌بعدی
            rotation_matrix = Matrix().rotate(self.angle_x, 1, 0, 0)
            rotation_matrix.rotate(self.angle_y, 0, 1, 0)
            rotation_matrix.rotate(self.angle_z, 0, 0, 1)

            # ایجاد متریال برای مکعب
            mesh = Mesh(vertices=vertices, indices=edges, mode='lines')
            mesh.transform = rotation_matrix

    def on_touch_move(self, touch):
        # حرکت صفحه لمسی را برای تغییر زاویه مکعب بررسی می‌کنیم
        if self.touch_pos:
            dx = touch.x - self.touch_pos[0]
            dy = touch.y - self.touch_pos[1]

            # بر اساس حرکت انگشت‌ها مکعب را بچرخانید
            self.angle_x += dy * 0.1
            self.angle_y += dx * 0.1
        self.touch_pos = (touch.x, touch.y)

    def on_touch_up(self, touch):
        self.touch_pos = None

    def on_touch_down(self, touch):
        self.touch_pos = (touch.x, touch.y)

    def update(self, dt):
        self.draw_cube()

class CubeApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        cube = Cube3D()
        layout.add_widget(cube)
        cube.update(1/60.0)  # تنظیم فریم ریت بازی
        return layout

if __name__ == '__main__':
    CubeApp().run()