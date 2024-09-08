import os
from PIL import Image

def convert_webp_to_jpeg(input_folder):
    jpeg_images = []
    
    # フォルダ内のすべてのファイルを確認
    for filename in os.listdir(input_folder):
        # スペースをアンダースコアに置き換えたファイル名を生成
        new_filename = filename.replace(' ', '_')
        old_file_path = os.path.join(input_folder, filename)
        new_file_path = os.path.join(input_folder, new_filename)
        
        # WebPファイルの場合、JPEGに変換
        if filename.lower().endswith('.webp'):
            jpeg_path = os.path.splitext(new_file_path)[0] + '.jpg'
            with Image.open(old_file_path) as img:
                rgb_img = img.convert('RGB')
                rgb_img.save(jpeg_path, 'JPEG')
                jpeg_images.append(jpeg_path)
        elif filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            # JPEGファイルそのまま追加
            jpeg_images.append(old_file_path)
        elif filename.lower().endswith('.png') or filename.lower().endswith('.gif'):
            # その他の画像形式も追加
            jpeg_images.append(old_file_path)
        
    
    return jpeg_images

def create_pdf_from_images(images, output_pdf_path):
    # 画像をPDFに変換
    if images:
        with Image.open(images[0]) as img:
            img_list = [Image.open(image) for image in images[1:]]
            img.save(output_pdf_path, save_all=True, append_images=img_list)

def main(folder_path):
    if not os.path.isdir(folder_path):
        raise ValueError("指定されたパスはフォルダではありません。")
    
    # フォルダの名前をPDFのファイル名にする
    folder_name = os.path.basename(os.path.normpath(folder_path))
    output_pdf_path = os.path.join(folder_path, f"{folder_name}.pdf")
    
    # 画像を変換およびリストに追加
    images = convert_webp_to_jpeg(folder_path)
    
    # JPEG画像からPDFを作成
    create_pdf_from_images(images, output_pdf_path)
    
    print(f"PDFファイルが作成されました: {output_pdf_path}")

if __name__ == "__main__":
    folder_path = input("フォルダのパスを入力してください: ").strip()
    main(folder_path)
