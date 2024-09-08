import img2pdf
from pathlib import Path
import re


#数字がない文字列は前に持ってきている。
#逆にしたいときは代2引数にfloat('inf')を指定
#https://note.nkmk.me/python-sort-num-str/
def extract_num(s, ret=0):
    p = re.compile(r'(\d+)')    
    search = p.search(s)
    if search:
        return int(search.groups()[-1])
        print(search.groups())
    else:
        return ret


#単処理
def ImageToPdf(outputpath, imagepath):
    '''
    outputpath: pathlib.Path()
    imagepath: pathlib.Path()
    '''
    lists = list(imagepath.glob("**/*"))#単フォルダ内を検索
    #jpg,pngファイルだけpdfに結合
    #Pathlib.WindowsPath()をstring型に変換しないとエラー
    #jpegにも対応
    imgpath_list = [str(i) for i in lists if i.match("*.jpg") or i.match("*.webp") or i.match("*.jpeg")]

    #https://note.nkmk.me/python-sort-num-str/
    #0埋めされていない番号順に対応
    imgpath_list.sort(key=lambda s: extract_num(s))

    #pdfを作成
    with open(outputpath,"wb") as f:
        f.write(img2pdf.convert(imgpath_list))
    print(outputpath.name + " :Done")

#複数フォルダをループ処理する
while True:
    #作業フォルダ
    base_path = input("PDFに変換したいファルダが入った親フォルダをd&Pしてください")
    base_path = base_path.strip(" \' ")
    #作業フォルダ内のディレクトリだけを抽出する
    glob = Path(base_path).glob("*")
    imagefolderlist = list([item for item in list(glob) if item.is_dir()])
    #outputpathに指定ディレクトリと同名を指定する
    outputpathlist = list([item.with_name(item.name + ".pdf") for item in imagefolderlist])
    #ループ処理を行う
    for outputpath,imagepath in zip(outputpathlist,imagefolderlist):
        try:
            ImageToPdf(outputpath,imagepath)
        except:
            import traceback
            traceback.print_exc()