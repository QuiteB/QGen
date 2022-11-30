import json
from cryptography.fernet import Fernet
from tkinter.filedialog import askopenfilename
import os
    # resultant dictionary
filename = askopenfilename()
c = 0
dictq = []
dicto = []
answer = []
with open(filename) as fh:
    for line in fh:
        sno = ["question", "options", "answers"]
        desc = line.strip()
        if not desc.startswith(".") and c != 0:
            if c1 == 1:
                c1 = 2
                dictq.append(desc)
            elif c1 >= 2:
                while c1 == 2:
                    answer.append(desc)
                    break
                dico.append(desc)
                c1 += 1
        else:
            c += 1
            c1 = 1
            if c > 1:
                dicto.append(dico)
            dico = []
            continue
    dict2 = dict(zip(sno, [dictq, dicto, answer]))

qstr = json.dumps(dict2, indent=1)
#encrypted = self.encrpt(qstr)
#return encrypted

key = b'CjqCzW0CZfmaMYuizKRmizo4GMkx3ane4dnnpiEo4eE='
data = qstr
fernet = Fernet(key)
encrypted = fernet.encrypt(bytes(data, 'utf-8'))
with open('Quiz.json', 'wb') as f:
    f.write(encrypted)
