# description
"""
/*
;|**********************************************************************;
;* Project           : Mark 6 simulator
;*
;* Program name      : mark_six.py
;*
;* Author            : SIO TOU LAI (laisiotou1997@gmail.com)
;*
;* Date created      : 14/07/2020
;*
;* Version           : Internal
;*
;* Copyright         : GNU GENERAL PUBLIC LICENSE Version 3
;*
;* Purpose           : Demonstrate 80 years of mark six experience. ;)
;*
;* Revision History  :
;*
;* Date        Author      Ref    Revision (Date in DDMMYYYY format)
;* 14072020    lst97       1      First release
;*
;* Known Issue       :
;*
;|**********************************************************************;
*/
"""

""" Rules [https://bet.hkjc.com/marksix/userinfo.aspx?lang=ch&file=prize_entitlement.asp]
[CHT] 若頭獎及/或二獎無人中獎，獎金將會撥入下一期攪珠的頭獎基金作「多寶」金額。
第一組獎金	45% x ﹝獎金基金減去第四、五、六及七組的總獎金及金多寶扣數*﹞÷ 中獎單位
第二組獎金	15% x ﹝獎金基金減去第四、五、六及七組的總獎金及金多寶扣數*﹞÷ 中獎單位
第三組獎金	40% x ﹝獎金基金減去第四、五、六及七組的總獎金及金多寶扣數*﹞÷ 中獎單位
*由二零零六年七月一日起，金多寶扣數定為獎金基金減去第四、五、六及七組總獎金後的百分之九。

頭獎         選中6個「攪出號碼」	                    獎金會因應該期獲中頭獎注數而有所不同，每期頭獎獎金基金訂為不少於港幣800萬元。
二獎	     選中5個「攪出號碼」+「特別號碼」	          獎金會因應該期獲中二獎注數而有所不同
三獎	     選中5個「攪出號碼」	                    獎金會因應該期獲中三獎注數而有所不同
四獎	     選中4個「攪出號碼」+「特別號碼」             固定獎金港幣9,600元
五獎	     選中4個「攪出號碼」	                    固定獎金港幣640元
六獎	     選中3個「攪出號碼」+「特別號碼」             固定獎金港幣320元
七獎	     選中3個「攪出號碼」	                    固定獎金港幣40元

[ENG]
1st Prize	Pick all the 6 Drawn Numbers	        Prize is determined by the total number of winning unit investments in the First Division Prize. The minimum First Division Prize Fund is set at HK$8 million
2nd Prize	Pick 5 Drawn Numbers + Extra Number	    Prize is determined by the total number of winning unit investments in the Second Division Prize
3rd Prize	Pick 5 Drawn Numbers	                Prize is determined by the total number of winning unit investments in the Third Division Prize
4th Prize	Pick 4 Drawn Numbers + Extra Number	    A fixed prize of $9,600
5th Prize	Pick 4 Drawn Numbers	                A fixed prize of $640
6th Prize	Pick 3 Drawn Numbers + Extra Number	    A fixed prize of $320
7th Prize	Pick 3 Drawn Numbers	                A fixed prize of $40

Mathsmatical chance: 1/139,838,160 = 0.0000007151123842%

Lab hit rate [58767953] %
0:18456212 31.405232
1:25124147 42.7514414
2:12223079 20.798885
3:2677564  4.5561634
4:274301   0.466752687
5:12474	   0.021225854
6:176      0.000299482
7:0        No data
"""

# header
import random
import re
regex = re
randint = random.randint

# global variable (constance)
MAX_LENGTH = 7
MIN_NUMBER = 1
MAX_NUMBER = 49

PRIZE_7TH = 40
PRIZE_6TH = 320
PRIZE_5TH = 640
PRIZE_4TH = 9600
PRIZE_3TH = 100000
PRIZE_2TH = 1000000
PRIZE_1TH = 26500000

TICKET_PRICE = 10

# declearation
class Game:
    dupList = __guessList = __resultList = draw = __sumtotal = __average = None
    __odd = 0
    __even = 0
    isSpecialHit = False
    
    def __init__(self, guessList, draw):
        self.__guessList = guessList
        self.draw = draw

    def __sortDuplicateList(self) -> list:
        """ Sort duplicateList, special number will not be sorted.

        Args:
            game (Game): Game class.

        Returns:
            list: Duplicate list.
        """
        maxIndex = len(self.dupList) - 1
        return (sorted(self.dupList[0: maxIndex]) + self.dupList[maxIndex:]) if (self.isSpecialHit and maxIndex != 0) else sorted(self.dupList)

    def __isRandomNumDuplicate(self, rnum: int) -> bool:
        return rnum in self.__resultList

    def __genResultList(self):
        """ Generate sorted list contain Mark 6 format number. (The 7th digit is special number)

        Returns:
            {`list`}: List that pushed with non duplicate number.
        """
        self.__resultList = list()
        while True:
            rnum = randint(MIN_NUMBER, MAX_NUMBER)
            if self.__isRandomNumDuplicate(rnum):
                continue # re-generate a number

            if len(self.__resultList) == MAX_LENGTH - 1:
                self.__resultList.sort()
                self.__resultList.append(rnum)
                break
            self.__resultList.append(rnum)

    def __cmpWin(self):
        """ Compare guessList with resultList. (This function will motify dupList & isSpecialHit).

        Args:
            game (Game): Game class.
        """
        index, self.dupList = 0, list()
        for guessNum in self.__guessList:
            if guessNum in self.__resultList:
                if index == MAX_LENGTH -1:
                    self.isSpecialHit = True
                    self.dupList = self.__sortDuplicateList()
                self.dupList.append(guessNum)
            index += 1

    def __finalizeGame(self):
        """ Assign other value in Game class

        Args:
            game (Game): Game class
        """
        self.__sumtotal = sum(self.__resultList)
        self.__average = round((self.__sumtotal / len(self.__resultList)), 0)
        
        for num in self.__resultList:
            if num % 2 == 0:
                self.__even += 1
            else:
                self.__odd += 1

    def __resetResult(self):
        """ Reset `resultList`, `isSpecialHit`, `dupList`, `odd`, `even` at Game

        Args:
            game (Game): Game class
        """
        del self.dupList, self.__resultList 
        self.isSpecialHit = False
        self.__odd = self.__even = 0

    def run(self):
        player = Player(self.__guessList)
        while True:
            self.__genResultList()
            self.__cmpWin()
            self.__finalizeGame()
            player.calcPrize(self)
            self.draw += 1

            if self.draw == 12000:
                return player
            self.__resetResult()

class Player:
    principal = 0
    prizeCount = [0, 0, 0, 0, 0, 0, 0, 0]
    __guessList = None

    def __init__(self, guessList: list):
        self.__guessList = tuple(guessList)

    def calcPrize(self, game:Game):
        """ Data that indicate how many prize player reach.
        - index[0]: No prize recive
        - index[1]: 1st prize recive
        - ...
        - index[7]: 7st prize recive

        Args:
            player (Player): Player class
            game (Game): Game class
        """
        numberHit = len(game.dupList)
        # can be simpify?
        if numberHit > 2 and game.isSpecialHit == False:
            #7, 5, 3, 1
            if numberHit == 3:
                self.principal += PRIZE_7TH
                self.prizeCount[7] += 1
            elif numberHit == 4:
                self.principal += PRIZE_5TH
                self.prizeCount[5] += 1
            elif numberHit == 5:
                self.principal += PRIZE_3TH
                self.prizeCount[3] += 1
            elif numberHit == 6:
                self.principal += PRIZE_1TH
                self.prizeCount[1] += 1
        elif numberHit > 2 and game.isSpecialHit == True:
            #1(hit all, almost impossible), 6, 4, 2
            if numberHit == 4:
                self.principal += PRIZE_6TH
                self.prizeCount[6] += 1
            elif numberHit == 5:
                self.principal += PRIZE_4TH
                self.prizeCount[4] += 1
            elif numberHit == 6:
                self.principal += PRIZE_2TH
                self.prizeCount[2] += 1
            elif numberHit == 7:
                self.principal += PRIZE_1TH
                self.prizeCount[1] += 1
        else:
            self.principal -= TICKET_PRICE
            self.prizeCount[0] += 1

    def printResult(self):
        print("\n* * * Guess List: " + str(self.__guessList) + " * * *")
        print("80 years of gambling: [%d]\n1st: %d\n2nd: %d\n3rd: %d\n4th: %d\n5th: %d\n6th: %d\n7th: %d\nNo-win %d\n"
        %(self.principal, self.prizeCount[1], self.prizeCount[2], self.prizeCount[3], self.prizeCount[4],
        self.prizeCount[5], self.prizeCount[6], self.prizeCount[7], self.prizeCount[0]))

# global function declearation
def isValidStrFormat(userStr: str) -> bool:
    """ Using a regex to check if the string is valid.

    Args:
        userStr (str): User string

    Returns:
        bool: `True` if valid else `False`
    """
    return regex.search("^\s*\d+(\s*,+\s*\d+)*\s*$", userStr)

def isGuessNumDuplicate(guessList):
    """Check if the user enter same number to the list

    Args:
        strList (list): [description]

    Returns:
        [type]: [description]
    """
    return not (len(guessList) == len(set(guessList))) # to be learn

def isValidGuessList(guessList: list) -> bool:
    """ Number(x) must 1 <= x <= 49, non-duplicate and 7 length long

    Args:
        strList (list): [description]

    Returns:
        bool: [description]
    """
    #check Length && duplicate
    if isGuessNumDuplicate(guessList) or len(guessList) != MAX_LENGTH:
        return False

    #check if each number in range
    for guessNum in guessList:
        if guessNum in range(MIN_NUMBER, MAX_NUMBER + 1):
            continue
        return False
    return True

def formatedGuessList(userStr:str) -> list:
    """ Convert userStr to a list that only contain non-duplicate and 1 <= x <= 49 and 7 length long

    Args:
        userStr (str): String to be checked

    Returns:
    - `list`: User guess number is valid, each number are saved in the list.
    - `False`: Invalid string.
    """
    if isValidStrFormat(userStr):
        userGuessList = [int(num) for num in userStr.replace(" ", "").split(",")] # cover string to int
        if isValidGuessList(userGuessList):
            return sorted(userGuessList[:MAX_LENGTH - 1]) + userGuessList[MAX_LENGTH - 1:]
    raise ValueError

# main
while True:
    userStr = input("Please enter 7 numbers seperate with \",\"\n")
    try:
        guessList = formatedGuessList(userStr)
        break
    except ValueError:
        print("Input is not valid, please try again.\n")

player = Game(guessList, 0).run()
player.printResult()

exit(0)
