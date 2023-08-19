import re
from kivy.uix.dropdown import DropDown
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from functools import partial
from pytube import YouTube

Window.size = (500, 600)


class MyApp(MDApp):

    def getLinkInfo(self, event, layout):
        self.link = self.linkinput.text
        self.checklink = re.match('^https://www.youtube.com/.*', self.link)
        self.yt = YouTube(self.link)

        if self.checklink:
            print('Valid Link')
            self.errorLabel.text = ''
            self.errorLabel.pos_hint = {'center_x': 0.5, 'center_y': 20}
            try:
                self.title = str(self.yt.title)
                self.views = str(self.yt.views)
                self.length = str(self.yt.length)

                self.titleLabel.text = self.title
                self.titleLabel.pos_hint = {'center_x': 0.5, 'center_y': 0.4}
                self.viewsLabel.text = 'Views: ' + self.views
                self.viewsLabel.pos_hint = {'center_x': 0.5, 'center_y': 0.35}
                self.lengthLabel.text = 'Length: ' + self.length
                self.lengthLabel.pos_hint = {'center_x': 0.5, 'center_y': 0.30}

                self.downloadbutton.text = 'Download'
                self.downloadbutton.pos_hint = {'center_x': 0.5, 'center_y': 0.15}
                self.downloadbutton.size_hint = (.3, .1)

                self.video = self.yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
                print(self.video)

                self.dropDown = DropDown()
                for video in self.video:
                    btn = Button(text=video.resolution, size_hint_y=None, height=30)
                    btn.bind(on_release=lambda btn: self.dropDown.select(btn.text))
                    self.dropDown.add_widget(btn)

                self.main_btn = Button(text='144p', size_hint=(None, None), pos=(360, 65), height=50)
                self.main_btn.bind(on_release=self.dropDown.open)
                self.dropDown.bind(on_select=lambda instance, x: setattr(self.main_btn, 'text', x))
                layout.add_widget(self.main_btn)

                print('Title: ' + self.title)
                print('Views: ' + self.views)
                print('Length: ' + self.length)
            except:
                # self.errorLabel.text = 'Check Network '
                self.errorLabel.pos_hint = {'center_x': 0.5, 'center_y': 0.45}
        else:
            self.errorLabel.text = 'Invalid or Empty Link'
            self.errorLabel.pos_hint = {'center_x': 0.5, 'center_y': 0.45}
            print('Invalid Link')

    def download(self, event, layout):
        self.ys = self.yt.streams.filter(file_extension='mp4').filter(res=self.main_btn.text).first()

        print('Downloading..')
        self.ys.download(r'C:\eoati\Music')
        print('Download Complete')

    def build(self):
        layout = MDRelativeLayout(md_bg_color=[0.9, 0.9, 0.9])  # Light gray background

        self.img = Image(source='youtube.png', size_hint=(.5, .5),
                         pos_hint={'center_x': 0.5, 'center_y': 0.90})
        layout.add_widget(self.img)

        self.youtubelink = Label(text='Please enter link to download',
                                 pos_hint={'center_x': 0.5, 'center_y': 0.75},
                                 size_hint=(1, 1), font_size=20, color=(0, 0, 0))  # Black text
        layout.add_widget(self.youtubelink)

        self.linkinput = TextInput(text='', pos_hint={'center_x': 0.5, 'center_y': 0.65},
                                   size_hint=(1, None), height=48, font_size=29,
                                   foreground_color=(0, 0, 0), font_name='Arial')  # Black text
        layout.add_widget(self.linkinput)

        self.linkbutton = Button(text='Get Link', pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                 size_hint=(.2, .1), font_name='Arial', font_size=24,
                                 background_color=[0, 1, 0])
        self.linkbutton.bind(on_press=partial(self.getLinkInfo, layout))
        layout.add_widget(self.linkbutton)

        self.titleLabel = Label(text='', pos_hint={'center_x': 0.5, 'center_y': 0.25},
                                size_hint=(1, 1), font_size=20, color=(0, 0, 0))  # Black text
        self.viewsLabel = Label(text='', pos_hint={'center_x': 0.5, 'center_y': 0.2},
                                size_hint=(1, 1), font_size=20, color=(0, 0, 0))  # Black text
        self.lengthLabel = Label(text='', pos_hint={'center_x': 0.5, 'center_y': 0.15},
                                 size_hint=(1, 1), font_size=20, color=(0, 0, 0))  # Black text
        layout.add_widget(self.titleLabel)
        layout.add_widget(self.viewsLabel)
        layout.add_widget(self.lengthLabel)

        self.downloadbutton = Button(pos_hint={'center_x': 0.5, 'center_y': 2.0},
                                     size_hint=(.2, .1), size=(75, 75), font_name='Arial',
                                     bold=True, font_size=24, background_color=[0, 1, 0])
        self.downloadbutton.bind(on_press=partial(self.download, layout))
        layout.add_widget(self.downloadbutton)

        self.errorLabel = Label(text='', pos_hint={'center_x': 0.5, 'center_y': 20},
                                size_hint=(1, 1), font_size=20, color=(1, 0, 0))
        layout.add_widget(self.errorLabel)
        return layout


if __name__ == '__main__':
    MyApp().run()
