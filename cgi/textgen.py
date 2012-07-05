#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Image, ImageDraw, ImageFont,logging

class	TextAutoSize():
    def __init__(self,text,width,height,font,fontStartSize=25,linePadding=0,backgroundColor=(255,255,255,0),textColor=(0,0,0,255),nbsp='_'):
        self.fontStartSize=fontStartSize
        self.linePadding=linePadding
        self.backgroundColor=backgroundColor
        self.textColor=textColor
        self.imageWidth=width
        self.imageHeight=height
        self.font=font
        self.minTextSize=8
        self.nbsp=nbsp
        self.text=text
        self.textLayout=None

    def tryTextSize(self,size):

        font = ImageFont.truetype(self.font, size)
        words = self.text.split()
        currentText = Text(font,linePadding = self.linePadding)

        #calculate lines content and it's positions
        currentLine = ''
        testText = TextLine()

        for word in words:
            testText.text = testText.text + word

            if testText.widthForFont(font) > self.imageWidth:

                testText=TextLine()
                testText.text += word

                currentText.appendLine(currentLine.strip())
                currentLine = word

                #Если встречается слишком длинное слово - размер шрифта нужно понизить
                if testText.widthForFont(font)>self.imageWidth:
                    return None

                #Если весь текст при выбранном шрифте не влезает по высоте - размер шрифта нужно понизить
                if (testText.heightForFont(font) + currentText.height) > self.imageHeight:
                    return None

            else:
                currentLine += ' ' + word

            testText.text += ' '





        currentText.appendLine(currentLine.strip())
        self.textLayout = currentText
        return size
		
    def chooseTextSize(self):
        cur_size=self.fontStartSize
        text_size=None

        while text_size==None:
            text_size=self.tryTextSize(cur_size)
            cur_size=cur_size-1
            if cur_size<self.minTextSize:
                break
        return text_size
		
    def drawOptimalText(self,centerAling=True,textOffsetPercent=0):

        optimal_size=self.chooseTextSize()

        if optimal_size is None:
            return None


        image = Image.new("RGBA", (self.imageWidth,self.imageHeight),self.backgroundColor)
        canvas = ImageDraw.Draw(image)

        #Центрировать блок текста по вертикали и горизонтали
        topMargin = (self.imageHeight-self.textLayout.height+self.textLayout.height/len(self.textLayout.lines)*textOffsetPercent)/2
        leftMargin = (self.imageWidth-self.textLayout.width)/2

        #Выровнять текст по центру
        if centerAling:
            leftMargin=0
            self.textLayout.alignCenterInWidth(self.imageWidth)

        for line in self.textLayout.lines:
            canvas.text((line.left+leftMargin,line.top+topMargin), line.text.replace(self.nbsp,' '),font=self.textLayout.font,fill=self.textColor)
        del canvas

        return image
        
class TextLine:
    def __init__(self,text='',left=0,top=0):
        self._text=text
        self.top=top
        self.left=left

    def alignCenterInWidthWithFont(self,width,font):
        self.left=(width-self.widthForFont(font))/2

    def widthForFont(self,font):
        return font.getsize(self.text)[0]

    def heightForFont(self,font):
        return font.getsize(self.text)[1]

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self,value):
        self._text=value

	
class Text:
    def __init__(self,font,linePadding=0):
        self.lines=[] #List of Text Objects
        self.font=font #ImageFont Object
        self.linePadding=linePadding

    def appendLine(self,text):
        lineTop=self.height+self.linePadding
        self.lines.append(TextLine(text,0,lineTop))

    @property
    def width(self):
        result=0

        for line in self.lines:
            lineWidth=line.widthForFont(self.font)
            if lineWidth>result:
                result=lineWidth

        return result

    @property
    def height(self):
        characterHeight=self.font.getsize('A')[1]
        height=(characterHeight+self.linePadding)*len(self.lines)-self.linePadding
        return height

    def alignCenterInWidth(self,width):
        for line in self.lines:
            line.alignCenterInWidthWithFont(width,self.font)



		

