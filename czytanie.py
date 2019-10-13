import wx
import random
import os, sys
from playsound import playsound


class Question:
    def __init__(self, game, soundfile):
        self.file = soundfile
        self.txt = os.path.split(self.file)[-1][:-4]
        self.sound = 'bing'
        self.answered = False
        self.game = game
        self.tries = 0

    def __str__(self):
        a = 'a' if self.answered else ' '
        return f'[ {"  " if self.answered else self.txt}{a}]'

    def __repr__(self):
        return f'Question: {self.txt}'

    def play(self):
        print(self.file)
        playsound(self.file)


class Game:
    def __init__(self, level=1):
        self.level = level
        files = list(os.path.join(root, file)
                     for root, d, files in os.walk(os.path.join('resources', 'sounds'))
                     if files and (not level or int(os.path.split(root)[1]) < level)
                     for file in files)
        self.questions = dict((((i, j), Question(self, random.choice(files))) for i in range(4) for j in range(3)))
        self.set_new_question()
        self.play_current_question()
        self.active = True
        self.wrong_answers = 0

    def play_current_question(self):
        self.current_question.play()

    def set_new_question(self):
        questions = list(filter(lambda x: not x.answered, self.questions.values()))
        if questions:
            self.current_question = random.choice(questions)
        else:
            self.current_question = None
            self.active = False

    def print(self):
        for j in range(3):
            for i in range(4):
                print(self.questions[(i, j)], end='')
            print()

    def answer(self, question):
        self.current_question.tries += 1
        if question.txt == self.current_question.txt:
            question.answered = True
            self.set_new_question()
        else:
            self.wrong_answers += 1
        if self.active:
            self.play_current_question()


class Cover(wx.Panel):
    def __init__(self, *args, **kw):
        if 'pos' in kw: kw['pos'] = (kw['pos'][0] * 200, kw['pos'][1] * 200)
        super(Cover, self).__init__(*args, **kw)
        self.SetSize((200, 200))
        self.text = wx.StaticText(self, label='', style=wx.ALIGN_CENTRE, size=(200, 200), pos=(0, 0))
        vbox = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.DEFAULT)
        self.text.SetFont(font)
        vbox.Add(self.text, flag=wx.ALL, border=50)
        self.SetSizer(vbox)
        self.text.Bind(wx.EVT_LEFT_DOWN, self.turn_off)

    def turn_off(self, arg):
        self.question.game.answer(self.question)
        if self.question.answered:
            self.SetBackgroundColour(None)
            self.text.Hide()
        master = self.GetParent().GetParent()
        for cover in master.covers.values():
            cover.activeChanged()

        game = self.question.game
        if not game.active:
            if game.wrong_answers < 3:
                master.initUI(Game(game.level + 1))
            if game.wrong_answers > 5:
                master.initUI(Game(max(1, game.level - 1)))


    def set_question(self, question: Question):
        self.question = question
        self.SetBackgroundColour(wx.Colour(120, 120, 120))
        if random.randint(0, 5):
            self.text.SetLabel('\n' + question.txt)
        elif random.randint(0, 1):
            self.text.SetLabel('\n' + question.txt.upper())
        else:
            self.text.SetLabel('\n' + question.txt[0].upper() + question.txt[1:])
        self.text.Show()

        self.text.SetForegroundColour(wx.BLACK)

    def activeChanged(self):
        if self.question.tries > 2:
            self.text.SetForegroundColour(wx.GREEN)


class ReadingPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(ReadingFrame, self).__init__(*args, **kwargs)


class ReadingFrame(wx.Frame):

    def __init__(self, game):
        super(ReadingFrame, self).__init__(None)
        self.image = None

        self.buildUI()
        self.initUI(game)

    def setImage(self):
        if self.image: self.RemoveChild(self.image)
        r, d, files = next(os.walk(os.path.join('resources', 'images')))
        file = random.choice(files)
        img = open(os.path.join('resources', 'images', file), 'r+b')
        image = wx.Image(img, wx.BITMAP_TYPE_PNG)
        ratio = min(1, max(image.Height / 600, image.Width / 800))
        image.Rescale(image.Width / ratio, image.Height / ratio, wx.IMAGE_QUALITY_HIGH)
        self.image.SetBitmap(image.ConvertToBitmap())

    def buildUI(self):
        self.pnl = wx.Panel(self)
        self.image = wx.StaticBitmap(self.pnl)
        coverGen = (((i, j), Cover(self.pnl, pos=(i, j))) for i in range(4) for j in range(3))
        self.covers = dict(coverGen)

        self.SetSize((800, 600))
        self.SetTitle('Czytanie')
        self.Centre()

    def initUI(self, game: Game):
        self.setImage()
        for i in game.questions:
            self.covers[i].set_question(game.questions[i])


app = wx.App()
ReadingFrame(Game()).Show()
app.MainLoop()
