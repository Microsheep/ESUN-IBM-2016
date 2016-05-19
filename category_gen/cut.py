import sys
import jieba

""" set unicode """
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

""" setup jeiba """
jieba.set_dictionary('dict.txt.big')
content = open("store.txt", 'r', encoding="utf-8").readlines()
output = open("store_cut.txt", "w", encoding="utf-8")
def numnum(x):
    return x.count("1")+x.count("2")+x.count("3")+x.count("4")+x.count("5")+x.count("6")+x.count("7")+x.count("8")+x.count("9")+x.count("0")

def killsym(x):
    syms=["_","-","(",")","$","\n","+","=","*","@","~","#","%","|","^","&","<",">","[","]","{","}",",",".",":",";","\\","/","?","!","\'","\"","§","＜","�","ｘ","︽","≡","↘","●","]","ㄅ","◇","◆","【","】","♥","㊣","＊","．","『","』","╭","※","。","？","★","◤","◢","《","•","》","☆","（","）","、","：","！","❤","～","｜","│","‧","╮","╯","の","「","」","█","▌","♪","’","〞","〕","〔","│","／","１","２","３","４","５","６","７","８","９","０","ａ","ｂ","ｃ","ｄ","ｅ","ｆ","ｇ","ｈ","ｉ","ｊ","ｋ","ｌ","ｍ","ｎ","ｏ","ｐ","ｑ","ｒ","ｓ","ｔ","ｕ","ｖ","ｗ","ｘ","ｙ","ｚ","Ａ","Ｂ","Ｃ","Ｄ","Ｅ","Ｆ","Ｇ","Ｈ","Ｉ","Ｊ","Ｋ","Ｌ","Ｍ","Ｎ","Ｏ","Ｐ","Ｑ","Ｒ","Ｓ","Ｔ","Ｕ","Ｖ","Ｗ","Ｘ","Ｙ","Ｚ"]
    for sym in syms:
        x = x.replace(sym," ")
    return x

for line in content:
    sp = line.split(",")
    gp = sp[0]
    line = "".join(sp[1:])
    ans=""
    words = jieba.cut(killsym(str(line).split("－")[0]), cut_all=False)
    for word in words:
        tmp = word.strip('\n').strip(' ').split("－")[0]
        if tmp!='' and not tmp.isnumeric() and numnum(tmp)<3 :
            ans=ans+tmp+" "
    output.write(gp + "," + ans + "\n")

