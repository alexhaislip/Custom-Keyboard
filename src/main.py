import random
from docx import Document
from os import listdir
from os.path import isfile, join

class Custom_Keyboard:
    def __init__(self):
        mypath = "../text data/"
        docxfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        self.words = []
        
        for filename in docxfiles:
            document = Document(mypath+filename)
            for p in document.paragraphs:
                text = ""
                for char in p.text:
                    if char.isalpha():
                        text += char.lower()
                    else:
                        text += ' '
                    
                for word in text.split(' '):
                    if not word.isalpha():
                        continue
                    self.words.append(word)

        self.keyboards = [(self.get_score(self.qwerty), self.qwerty)]
        print("QWERTY cost = " + str(self.get_score(self.qwerty)))
        print()

    def get_score(self, keyboard):
        score = 0
        loc = dict()
        hand = dict()
        
        for i in range(3):
            for j in range(len(keyboard[i])):
                loc[keyboard[i][j]] = (i, j)

        hand[-5] = (1, 0)
        hand[-4] = (0, 1)
        hand[-3] = (0, 2)
        hand[-2] = (1, 3)
        hand[+2] = (1, 6)
        hand[+3] = (0, 7)
        hand[+4] = (0, 8)
        hand[+5] = (0, 9)
        
        for word in self.words:
            for char in word:
                x = loc[char][0]
                y = loc[char][1]
                score += self.cost[x][y] # keyboard pressing cost
                
                current = hand[self.finger[x][y]]
                distance = abs(x-current[0]) + abs(y-current[1])*2
                hand[self.finger[x][y]] = (x, y)
                score += distance # finger moving cost

        return score

    def genetic_algorithm(self):
        new_keyboards = []
        for score, keyboard in self.keyboards:
            new_keyboards.append((self.get_score(keyboard), keyboard))
            for generate_num in range(20):
                loc = dict()
                new_keyboard = []
                for i in range(3):
                    new_keyboard.append([])
                    for j in range(len(keyboard[i])):
                        loc[keyboard[i][j]] = (i, j)
                        new_keyboard[i].append(keyboard[i][j])

                K = 3
                for i in range(K):
                    x = chr(ord('a')+random.randint(0, 25))
                    y = chr(ord('a')+random.randint(0, 25))
                    loc[x], loc[y] = loc[y], loc[x]

                for key, value in loc.items():
                    new_keyboard[value[0]][value[1]] = key
                new_score = self.get_score(new_keyboard)
                new_keyboards.append((new_score, new_keyboard))

        limit = 10
        self.keyboards = []
        new_keyboards.sort()
        
        for keyboard in new_keyboards:
            if keyboard in self.keyboards:
                continue
            self.keyboards.append(keyboard)
            if len(self.keyboards) == limit:
                break

    def print_keyboard(self, keyboard):
        print("Total Cost = " + str(self.get_score(keyboard)))
        for i in range(3):
            if i == 1:
                print(' ',end='')
            elif i == 2:
                print('  ',end='')
            for j in range(len(keyboard[i])):
                print(keyboard[i][j]+"  ", end ='')
            print()
        print()

    # -5 = left hand little finger
    # 2  = right hand forefinger
    finger = [[-5, -4, -3, -2, -2, 2, 2, 3, 4, 5],
              [-5, -4, -3, -2, -2, 2, 2, 3, 4],
              [-5, -4, -2, -2, 2, 2, 2]]

    # The cost you need to press the keyboard
    # It is based on my personal experience
    # cost : 1 ~ 5 = easy ~ extreme
    cost = [[5, 2, 2, 3, 3, 3, 3, 2, 2, 5],
            [3, 2, 2, 1, 1, 1, 1, 2, 2],
            [5, 4, 3, 3, 3, 3, 3]]
    
    # qwerty keyboard
    qwerty = [['q','w','e','r','t','y','u','i','o','p'],
              ['a','s','d','f','g','h','j','k','l'],
              ['z','x','c','v','b','n','m']]

if __name__ == "__main__":
    model = Custom_Keyboard()
    for i in range(100):
        model.genetic_algorithm()
        print("Epoch = " + str(i))
        model.print_keyboard(model.keyboards[0][1])
