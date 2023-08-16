import time, re, math, os; from PIL import Image, ImageDraw; from typing import List


class AJ:
    def __init__(self):

        self.art = open('ART.txt', 'w', encoding='utf-8')
        self.art.write(f"gif = [")

        self.wid = int(input('Enter Width : '))
        self.hei = int(input('Enter Height : '))

        self.ARTS = []

        self.GifToPng()

        self.art.write(']')

        self.RunArt()


    def GifToPng(self):

        im = Image.open('img.gif')

        if not (os.path.exists('./OutPut')):
            os.mkdir('./OutPut')

        for i in range(im.n_frames):

            print(f'{i} / {im.n_frames}', end = '\r')

            im.seek(im.n_frames // im.n_frames * i)

            im.save(f'./OutPut/img-{i}.png')

            self.content = ''

            self.start(f'./OutPut/img-{i}.png')

        
    def start(self, img):

        self.img = Image.open(img, 'r').convert('RGBA')

        width, height = self.img.size

        self.ReSize(width, height)


    def ReSize(self, width, height):

        if width > self.wid:
            scale = width / self.wid
            
            width = self.wid
            height = math.floor(height / scale)

        if height > self.hei:
            scale = height / self.hei

            height = self.hei

            width = math.floor(width / scale)


        self.CreateCanva(width, height)

    
    def CreateCanva(self, width, height):

        canvas = Image.new("RGBA", (width, height))

        context = ImageDraw.Draw(canvas)

        canvas.paste(self.img.resize((width, height)), (0, 0))

        image_data = canvas.crop((0, 0, width, height)).tobytes()

        canvas.save('ghdfijk.png')

        self.Pixels(list(image_data), width)

    
    def Pixels(self, pixel_data, width):

        n = len(pixel_data)

        ii = 0

        

        while ii < n:

            try:

                top = pixel_data[ii : ii + 4]
                bottom = pixel_data[(ii + width * 4) : (ii + 4 + width * 4)]

                if ((top[0] == bottom[0] and top[1] == bottom[1] and top[2] == bottom[2] and not self.CheckTransparent(top) and not self.CheckTransparent(bottom)) or (self.CheckTransparent(top) and self.CheckTransparent(bottom))):
                    
                    self.content += f"\x1b[{self.RGBWork(top)}m "

                else:

                    if (self.CheckTransparent(bottom) and not self.CheckTransparent(top)):

                        self.content += f"\x1b[{self.RGBWork(bottom)};{self.RGBWork(top, True)}m▀"

                    else:

                        self.content += f"\x1b[{self.RGBWork(bottom, True)};{self.RGBWork(top)}m▄"

                ii += 4


                if self.EndOfLine(ii, width):
                
                    ii += 4 * width

                    self.content += '\x1b[m\n'

                while re.search(r'(\x1b\[[0-9;]+m)([▄▀ ]+)\1', self.content):
                    self.content = re.sub(r'(\x1b\[[0-9;]+m)([▄▀ ]+)\1', r'\1\2', self.content)

            except:
                break

        self.ARTS.append(self.content)

        con = re.sub('\\x1b', '\\\\033', self.content)

        self.art.write(f"'''\n{con}''',\n")

    

    def EndOfLine(self, i: int, image_width: int) -> bool:

        return (i > 0 and (i // 4) % image_width == 0)
    

    def CheckTransparent(self, rgba: List[int]) -> bool:
        _, _, _, a = rgba
        return a < 13
    

    def RGBWork(self, top, foreground=False):

        r = top[0]
        g = top[1]
        b = top[2]

        if self.CheckTransparent(top):
            return '39' if foreground else '49'
        
        if True:
            return f"{38 if foreground else 48};2;{r or 0};{g or 0};{b or 0}"
        
    
    def RunArt(self):

        clr = '\x1b[1A\x1b[2K'

        while True:

            for i in self.ARTS:

                print(f'{clr * 100}{i}\n\n\n\n\t\t\t\t\tPress CTRL + C To Exit\n\n\n\n\t\t\t\t\tBy Sami / zvhk')

                time.sleep(0.05)
        
AJ()