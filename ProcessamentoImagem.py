import cv2
import pytesseract


def load_image():
    img = cv2.imread("static\img\oletim.png")
    return img


def enhance_image(img):
    # crop
    y = 125
    x = 450
    h = 700
    w = 500
    crop = img[y:y + h, x:x + w]


    # Read input image, convert to grayscale
    img = crop
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold using Otsu's
    work_img = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]

    return work_img


def process_image_data():
    custom_config = r'--oem 3 --psm 6'
    pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\Tesseract.exe"
    img = load_image()
    img = enhance_image(img)
    data = pytesseract.image_to_string(img, config=custom_config)
    file = open('static\data\dados.csv', 'w')
    file.write(data)
    file.close()


def load_data():
    database = []
    archive= open('static\data\dados.csv','r')
    while True:
        line = archive.readline()  # lê uma linha de cada vez, passa para a proxima quando chamado novamente
        if line == '':  # quando o arquivo acabar retornara uma linha vazia
            break  # pare quando isso acontecer
        else:
            bd = line.rstrip(
                '\n')  # retira a quebra de linha gerada pelo metodo split ao final de cada linha da string linha
            bd = bd.split(
                ';')  # transforma bd em lista e quebra linha a cada ; tornando cada quebra um novo elemento na lista
            database.append(bd)  # append da lista bd dentro da lista dados
    archive.close()
    database = clear_data(database)

    return database


def clear_data(database):
    #  limpar dados vazios
    data = []
    c = len(database)-1
    while True:
        if database[c][0] == '':
            del database[c]
            c -= 1
        c -= 1
        if c == 0:
            break

    # capturar dados importantes
    if database[0][0] == 'CONFIRMADOS':
        data.append(database[1][0])
    for i in range(len(database)):
        if 'UNIVERSITARIO' in database[i][0]:
            data.append(database[i][0])
        elif '/' in database[i][0]:
            data.append(database[i][0])

    # limpar dados importantes
    data[0] = int(data[0])
    cut = data[1].rsplit('| 0 ').strip('%')
    data[1] = cut[1]

    #dic
    dados = {'confirmados': data[0], 'UTI': data[1]}
    return dados
