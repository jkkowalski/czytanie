import wx
import random

# http://zetcode.com/wxpython/widgets/

#img = wx.Bitmap('resources/obrazek.png')


# with open("resources/obrazek.png") as f:

class Cover(wx.Panel):
    def __init__(self, *args, **kw):
        if 'pos' in kw: kw['pos'] = (kw['pos'][0]*200, kw['pos'][1]*200)
        super(Cover, self).__init__(*args, **kw)
        self.SetSize((200,200))
        self.SetBackgroundColour(wx.Colour(120,120,120))
        st1 = wx.StaticText(self, label='ME', style=wx.ALIGN_CENTRE, size=(200,200), pos=(0,0))
        st1.SetForegroundColour(wx.BLACK)
        vbox = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.DEFAULT)
        st1.SetFont(font)
        vbox.Add(st1, flag=wx.ALL, border=15)
        self.SetSizer(vbox)
        st1.Bind(wx.EVT_LEFT_DOWN, self.turnOff)

    def turnOff(self, arg):
        self.SetBackgroundColour(None)

class ReadingFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(ReadingFrame, self).__init__(None)

        self.InitUI()

    def InitUI(self):
        pnl = wx.Panel(self)
        closeButton = wx.Button(pnl, label='Close', pos=(20, 20))
        img = open('resources/obrazek.png', 'r+b')
        wxImg = wx.Image(img, wx.BITMAP_TYPE_PNG)
        ratio = min(1, max(wxImg.Height/300, wxImg.Width/400))
        wxImg.Rescale(wxImg.Width/ratio, wxImg.Height/ratio, wx.IMAGE_QUALITY_HIGH)
        wx.StaticBitmap(pnl).SetBitmap(wxImg.ConvertToBitmap())
        coverGen = (((i, j), Cover(pnl, pos=(i,j))) for i in range(4) for j in range(3))
        self.covers=dict(coverGen)

        self.SetSize((800, 600))
        self.SetTitle('wx.Button')
        self.Centre()


class Question:
    def __init__(self):
        self.txt = 'ME'
        self.sound = 'bing'
        self.answered = False
        self.active = False

    def __str__(self):
        return f'Question: {self.txt}'

    def __repr__(self):
        return self.__str__()

    def play(self):
        print(f'Sound {self.sound} for {self.txt}')

class Game:
    def __init__(self):
        self.questions = dict((((i,j), Question()) for i in range(4) for j in range(3)))
        self.get_question()

    def play_current_question(self):
        self.questions[self.current_question].play()

    def get_question(self):
        self.current_question = random.choice(list(filter(lambda x: not self.questions[x].answered, self.questions)))
        self.questions[self.current_question].active = True
        self.play_current_question()


app = wx.App()
ReadingFrame(Game()).Show()
app.MainLoop()
