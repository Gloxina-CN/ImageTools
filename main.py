# coding=utf-8
# 图像信息读取使用 Pillow
# Pillow Docs 地址: https://pillow.readthedocs.io/en/stable/reference


import os
import time
import yaml
import uuid
import shutil
import warnings
from PIL import Image


# 用于检查路径是否合法的库，还没用上
# from pathvalidate import is_valid_filepath


# 忽略潜在的由 Pillow.Image 产生的 Corrupt EXIF data 错误
warnings.filterwarnings("ignore", category=UserWarning, module='PIL.TiffImagePlugin')


# 配置文件检查函数
# 使用 pathvalidate 验证路径是否为合法路径
# 如果是非法路径，则返回错误信息，并返回默认路径
# 。。。还没写
'''
def VerifyPath(path, config_item, default_path):
    if not is_valid_filepath(path):
        print(f'警告: 配置文件中的 "{config_item}" 无效，程序将使用默认值 "{default_path}"')
        path = default_path
    return path
'''


# 功能选择函数
def function_select():

    # 获取用户输入的功能代码
    def get_function_code():
        print(f'\n请选择功能:\n1# 图像分类\n2# 图像转换\n3# 图像批量重命名\n4# 退出...\n')
        while True:
            try:
                function_select = int(input(f'请输入编号(1,2,3,4): '))
                if function_select in {1, 2, 3, 4}:
                    function_execute(function_select)
                    break
                else:
                    print(f'编号不存在，请重新输入。')
            except ValueError:
                print(f'输入无效，请输入数字编号。')


    # 对功能选择函数进行响应
    def function_execute(function_select):
        if function_select == 1:
            image_classifier()
        elif function_select == 2:
            image_converter()
        elif function_select == 3:
            image_rename()
        elif function_select == 4:
            program_exit('0x00')


    get_function_code()


# 图像分类操作函数
def image_classifier():

    # 模式选择
    def classifier_mode_select():

        print(f'\n请选择模式:\n1# 使用配置文件定义的模式\n2# AspectRatio\n3# Threshold\n4# FileSuffix\n5# 返回...\n')
        while True:
            try:
                mode_select = int(input(f'请输入编号(1,2,3,4,5): '))
                if mode_select in {1, 2, 3, 4, 5}:
                    classifier_mode_execute(mode_select)
                    break
                else:
                    print(f'编号不存在，请重新输入。')
            except ValueError:
                print(f'输入无效，请输入数字编号。')


    # 对模式选择进行响应
    def classifier_mode_execute(mode_select):

        if mode_select == 1:
            mode = config.get('Mode', '').strip('"')
            print(f'模式: {mode}')
            if mode == 'AspectRatio':
                aspect_ratio()
            elif mode == 'Threshold':
                threshold()
            elif mode == 'FileSuffix':
                file_suffix()
            else:
                program_exit('0x01')
        elif mode_select == 2:
            mode = 'AspectRatio'
            print(f'模式: {mode}')
            aspect_ratio()
        elif mode_select == 3:
            mode = 'Threshold'
            print(f'模式: {mode}')
            threshold()
        elif mode_select == 4:
            mode = 'FileSuffix'
            print(f'模式: {mode}')
            file_suffix()
        elif mode_select == 5:
            function_select()


    # 当模式为 AspectRatio 时，执行下面的函数
    def aspect_ratio():

        # 判断配置文件状态，没做合法性检测
        source_path = (config.get('AspectRatioSourceFolder', '').strip('"'))
        if source_path == '':
            print(f'警告: 配置文件中 "AspectRatioSourceFolder" 的值为空，程序将使用默认值 "./AspectRatio/Source"')
            source_path = './AspectRatio/Source'
        else:
                print(f'读取到配置 "AspectRatioSourceFolder" 的值为 "{source_path}"')
        

        landscape_path = config.get("LandscapeFolder", '').strip('"')
        if landscape_path == '':
            print(f'警告: 配置文件中 "LandscapeFolder" 的值为空，程序将使用默认值 "./AspectRatio/Landscape"')
            landscape_path = './AspectRatio/Landscape'
        else:
                print(f'读取到配置 "LandscapeFolder" 的值为 "{landscape_path}"')


        portrait_path = config.get('PortraitFolder', '').strip('"')
        if portrait_path =='':
            print(f'警告: 配置文件中 "PortraitFolder" 的值为空，程序将使用默认值 "./AspectRatio/Portrait"')
            portrait_path = './AspectRatio/Portrait'
        else:
            print(f'读取到配置 "Portrait" 的值为 "{portrait_path}"')


        other_path = config.get('OtherFolder', '').strip('"')
        if other_path == '':
            print(f'警告: 配置文件中 "OtherFolder" 的值为空，程序将使用默认值 "./AspectRatio/Other"')
            other_path = './AspectRatio/Other'
        else:
            print(f'读取到配置 "OtherFolder" 的值为 "{other_path}"')


        w2h_threshold_str = config.get('W2H_Threshold', '').strip('"')
        if w2h_threshold_str == '':
            print(f'警告: 配置文件中 "W2H_Threshold" 的值为空，程序将使用默认值 "1.2"')
            w2h_threshold = 1.2
        else:
            try:
                w2h_threshold = float(w2h_threshold_str)
                print(f'读取到配置 "W2H_Threshold" 的值为 "{w2h_threshold}"')
            except ValueError:
                print(f'警告: 配置文件中 "W2H_Threshold" 的值无效，程序将使用默认值 "1.2"')
                w2h_threshold = 1.2

        # 暂停三秒，查看配置文件读取信(bao)息(cuo)
        time.sleep(3)

        os.makedirs(source_path, exist_ok=True)
        os.makedirs(landscape_path, exist_ok=True)
        os.makedirs(portrait_path, exist_ok=True)
        os.makedirs(other_path, exist_ok=True)

        # 遍历 Source 文件夹下的所有图片
        for filename in os.listdir(source_path):
            time.sleep(0.05)
            try:
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp')):
                    file_path = os.path.join(source_path, filename)
                    with Image.open(file_path) as img:
                        width, height = img.size

                    # 判断图像属于三种分类中的哪种
                    # 三种分类: 横向 纵向 其他
                    if width / height >= w2h_threshold:
                        target = landscape_path
                    elif height / width >= w2h_threshold:
                        target = portrait_path
                    else:
                        target = other_path

                    shutil.move(file_path, os.path.join(target, filename))
                    print(f'已处理: {filename} => {target}')
            
            except (IOError, OSError) as error:
                print(f'{filename} 不是常见的图像格式，程序可能无法识别，跳过此文件: {error}')

        input('分类完成，按 Enter 继续...')
        function_select()


    # 当模式为 Threshold 时，执行下面的函数
    def threshold():

        # Threshold 模式中的纵向模式
        def threshold_portrait():

            # 读取配置文件
            source_path = config.get('ThresholdSourceFolder', '').strip('"')
            if source_path == '':
                print(f'警告: 配置文件中 "ThresholdSourceFolder" 的值为空，程序将使用默认值 "./Threshold/Source"')
                source_path = './Threshold/Source'
            else:
                print(f'读取到配置 "ThresholdSourceFolder" 的值为 "{source_path}"')


            target_path = config.get('TargetFolder', '').strip('"')
            if target_path == '':
                print(f'警告: 配置文件中 "TargetFolder" 的值为空，程序将使用默认值 "./Threshold/Target"')
                target_path = './Threshold/Target'
            else:
                print(f'读取到配置 "TargetFolder" 的值为 "{target_path}"')


            portrait_minwidth_str = config.get('PortraitMinWidth', '').strip('"')
            if portrait_minwidth_str == '':
                print(f'警告: 配置文件中 "PortraitMinWidth" 的值为空，程序将使用默认值 "1080"')
                portrait_minwidth = int(1080)
            else:
                try:
                    portrait_minwidth = int(portrait_minwidth_str)
                    print(f'读取到配置 "PortraitMinWidth" 的值为 "{portrait_minwidth}"')
                except ValueError:
                    print(f'警告: 配置文件中 "PortraitMinWidth" 的值无效，程序将使用默认值 "1080"')
                    portrait_minwidth = int(1080)
            

            portrait_minheight_str = config.get('PortraitMinHeight', '').strip('"')
            if portrait_minheight_str == '':
                print(f'警告: 配置文件中 "PortraitMinHeight" 的值为空，程序将使用默认值 "2400"')
                portrait_minwidth = int(2400)
            else:
                try:
                    portrait_minheight = int(portrait_minheight_str)
                    print(f'读取到配置 "PortraitMinHeight" 的值为 "{portrait_minheight}"')
                except ValueError:
                    print(f'警告: 配置文件中 "PortraitMinHeight" 的值无效，程序将使用默认值 "2400"')
                    portrait_minwidth = int(2400)

            
            # 暂停三秒，查看配置文件读取信(bao)息(cuo)
            time.sleep(3)

            os.makedirs(source_path, exist_ok=True)
            os.makedirs(target_path, exist_ok=True)

            for filename in os.listdir(source_path):
                time.sleep(0.05)
                try:
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp')):
                        file_path = os.path.join(source_path, filename)
                        with Image.open(file_path) as img:
                            width, height = img.size

                        # 判断图像是否满足配置文件中设置的阈值
                        # 如果位达到任意一个最低阈值，则移动到目标文件夹
                        if portrait_minwidth is None and portrait_minheight is None:
                            program_exit('0x01')
                        elif (portrait_minwidth is None or width <= portrait_minwidth) or (portrait_minheight is None or height <= portrait_minheight):
                            shutil.move(file_path, os.path.join(target_path, filename))
                            print(f'已处理: {filename} => {target_path}')

                except (IOError, OSError) as error:
                    print(f'{filename} 不是常见的图像格式，程序可能无法识别，跳过此文件: {error}')

            input('分类完成，按 Enter 继续...')
            function_select()


        # Threshold 模式中的横向模式
        def threshold_landscape():

            # 读取配置文件
            source_path = config.get('ThresholdSourceFolder', '').strip('"')
            if source_path == '':
                print(f'警告: 配置文件中 "ThresholdSourceFolder" 的值为空，程序将使用默认值 "./Threshold/Source"')
                source_path = './Threshold/Source'
            else:
                print(f'读取到配置 "ThresholdSourceFolder" 的值为 "{source_path}"')
            

            target_path = config.get('TargetFolder', '').strip('"')
            if target_path == '':
                print(f'警告: 配置文件中 "TargetFolder" 的值为空，程序将使用默认值 "./Threshold/Target"')
                target_path = './Threshold/Target'
            else:
                print(f'读取到配置 "TargetFolder" 的值为 "{target_path}"')


            landscape_minwidth_str = config.get('LandscapeMinWidth', '').strip('"')
            if landscape_minwidth_str == '':
                print(f'警告: 配置文件中 "LandscapeMinWidth" 的值为空，程序将使用默认值 "2560"')
                landscape_minwidth = int(2560)
            else:
                try:
                    landscape_minwidth = int(landscape_minwidth_str)
                    print(f'读取到配置 "LandscapeMinWidth" 的值为 "{landscape_minwidth}"')
                except ValueError:
                    print(f'警告: 配置文件中 "LandscapeMinWidth" 的值无效，程序将使用默认值 "2560"')
                    landscape_minwidth = int(2560)


            landscape_minheight_str = config.get('LandscapeMinHeight', '').strip('"')
            if landscape_minheight_str == '':
                print(f'警告: 配置文件中 "LandscapeMinHeight" 的值为空，程序将使用默认值 "1440"')
                landscape_minheight = int(1440)
            else:
                try:
                    landscape_minheight = int(landscape_minheight_str)
                    print(f'读取到配置 "LandscapeMinHeight" 的值为 "{landscape_minheight}"')
                except ValueError:
                    print(f'警告: 配置文件中 "LandscapeMinHeight" 的值无效，程序将使用默认值 "1440"')
                    landscape_minheight = int(1440)

            
            # 暂停三秒，查看配置文件读取信(bao)息(cuo)
            time.sleep(3)

            os.makedirs(source_path, exist_ok=True)
            os.makedirs(target_path, exist_ok=True)

            for filename in os.listdir(source_path):
                time.sleep(0.05)
                try:
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp')):
                        file_path = os.path.join(source_path, filename)
                        with Image.open(file_path) as img:
                            width, height = img.size

                        # 判断图像是否满足配置文件中设置的阈值
                        # 如果位达到任意一个最低阈值，则移动到目标文件夹
                        if landscape_minwidth is None and landscape_minheight is None:
                            program_exit('0x01')
                        elif (landscape_minwidth is None or width <= landscape_minwidth) or (landscape_minheight is None or height <= landscape_minheight):
                            shutil.move(file_path, os.path.join(target_path, filename))
                            print(f'已处理: {filename} => {target_path}')

                except (IOError, OSError) as error:
                    print(f'{filename} 不是常见的图像格式，程序可能无法识别，跳过此文件: {error}')

            input('分类完成，按 Enter 继续...')
            function_select()


        # Threshold 模式中的模式选择
        print('\n请选择 Threshold 的模式:\n1# 纵向模式\n2# 横向模式\n3# 返回...')
        while True:
            try:
                threshold_mode_select = int(input('请输入编号(1,2,3): '))
                if threshold_mode_select in {1, 2, 3}:
                    if threshold_mode_select == 1:
                        print(f'模式: Threshold, Portrait')
                        time.sleep(2)
                        print(f'开始执行任务...')
                        threshold_portrait()
                    elif threshold_mode_select == 2:
                        print(f'模式: Threshold, Landscape')
                        time.sleep(2)
                        print(f'开始执行任务...')
                        threshold_landscape()
                    elif threshold_mode_select == 3:
                        classifier_mode_select()
                    else:
                        program_exit('0x02')
                else:
                    print(f'编号不存在，请重新输入。')
            except ValueError:
                print(f'输入无效，请输入数字编号。')


    # 当模式为 FileSuffix 时，执行下面的函数
    def file_suffix():
        
        # 读取配置文件
        source_path = config.get('FileSuffixSourceFolder', '').strip('"')
        if source_path == '':
            print(f'警告: 配置文件中 "FileSuffixSourceFolder" 的值为空，程序将使用默认值 "./data/FileSuffix/Source"')
            source_path = './data/FileSuffix/Source'
        else:
            print(f'读取到配置 "FileSuffixSourceFolder" 的值为 "{source_path}"')


        png_target = config.get('PNGTarget', '').strip('"')
        if png_target == '':
            print(f'警告: 配置文件中 "PNGTarget" 的值为空，程序将使用默认值 "./data/FileSuffix/PNG"')
            png_target = './data/FileSuffix/PNG'
        else:
            print(f'读取到配置 "PNGTarget" 的值为 "{png_target}"')
            

        jpeg_target = config.get('JPEGTarget', '').strip('"')
        if jpeg_target == '':
            print(f'警告: 配置文件中 "JPEGTarget" 的值为空，程序将使用默认值 "./data/FileSuffix/JPEG"')
            jpeg_target = './data/FileSuffix/JPEG'
        else:
            print(f'读取到配置 "JPEGTarget" 的值为 "{jpeg_target}"')
            

        webp_target = config.get('WebPTarget', '').strip('"')
        if webp_target == '':
            print(f'警告: 配置文件中 "WebPTarget" 的值为空，程序将使用默认值 "./data/FileSuffix/WebP"')
            webp_target = './data/FileSuffix/WebP'
        else:
            print(f'读取到配置 "WebPTarget" 的值为 "{webp_target}"')
            

        bmp_target = config.get('BMPTarget', '').strip('"')
        if bmp_target == '':
            print(f'警告: 配置文件中 "BMPTarget" 的值为空，程序将使用默认值 "./data/FileSuffix/BMP"')
            bmp_target = './data/FileSuffix/BMP'
        else:
            print(f'读取到配置 "BMPTarget" 的值为 "{bmp_target}"')

        # 暂停三秒，查看配置文件读取信(bao)息(cuo)
        time.sleep(3)

        os.makedirs(source_path, exist_ok=True)
        os.makedirs(png_target, exist_ok=True)
        os.makedirs(jpeg_target, exist_ok=True)
        os.makedirs(webp_target, exist_ok=True)
        os.makedirs(bmp_target, exist_ok=True)

        for filename in os.listdir(source_path):
            try:
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp')):

                    if filename.lower().endswith(('.png')):
                        file_path = os.path.join(source_path, filename)
                        shutil.move(file_path, os.path.join(png_target, filename))
                        print(f'已处理: {filename} => {png_target}')

                    elif filename.lower().endswith(('.jpg', '.jpeg')):
                        file_path = os.path.join(source_path, filename)
                        shutil.move(file_path, os.path.join(jpeg_target, filename))
                        print(f'已处理: {filename} => {jpeg_target}')

                    elif filename.lower().endswith(('.webp')):
                        file_path = os.path.join(source_path, filename)
                        shutil.move(file_path, os.path.join(webp_target, filename))
                        print(f'已处理: {filename} => {webp_target}')

                    elif filename.lower().endswith(('.bmp')):
                        file_path = os.path.join(source_path, filename)
                        shutil.move(file_path, os.path.join(bmp_target, filename))
                        print(f'已处理: {filename} => {bmp_target}')

            except (IOError, OSError) as error:
                print(f'{filename} 不是常见的图像格式，程序可能无法识别，跳过此文件: {error}')

        input('分类完成，按 Enter 继续...')
        function_select()
        

    # 加载功能 Classifier 的配置文件 => variable = config
    config_path = './config/classifier.yaml'
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)


    classifier_mode_select()


# 图像格式转换操作函数
def image_converter():

    # 格式选择
    def converter_format_select():

        # 获取源文件格式选择
        def source_format_select():
            print(f'\n请选择源文件格式:\n1# PNG\n2# JP(E)G\n3# WebP\n4# BMP\n5# 返回...\n')
            while True:
                try:
                    source_format_num = int(input(f'请输入编号(1,2,3,4,5):'))
                    if source_format_num in {1, 2, 3, 4, 5}:
                        if source_format_num == 5:
                            function_select()
                        else:
                            target_format_select(source_format_num)
                            break
                    else:
                        print(f'编号不存在，请重新输入。')
                except ValueError:
                    print(f'输入无效，请输入数字编号。')


        # 获取目标格式文件选择
        def target_format_select(source_format_num):
            print(f'\n请选择目标文件格式:\n1# PNG\n2# JPG\n3# WebP\n4# BMP\n5# 返回...\n')
            while True:
                try:
                    target_format_num = int(input(f'请输入编号(1,2,3,4,5):'))
                    if target_format_num in {1, 2, 3, 4, 5}:
                        if target_format_num == 5:
                            source_format_select()
                        else:
                            format_execute(source_format_num, target_format_num)
                            break
                    else:
                        print(f'编号不存在，请重新输入。')
                except ValueError:
                    print(f'输入无效，请输入数字编号。')


        # 对格式选择进行响应
        def format_execute(source_format, target_format):

            # 防止源文件和目标文件格式相同
            if source_format == target_format:
                print(f'警告：源文件格式不能与目标文件格式相同，请重新选择...')
                source_format_select()
            else:
                print('占位')



        source_format_select()


    # 加载功能 Converter 的配置文件
    config_path = './config/converter.yaml'
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)


    p2j_quality = int(config.get('P2J_Quality', '').strip('"'))
    if p2j_quality == '':
        print(f'警告: 配置文件中 "P2J_Quality" 的值为空，程序将使用默认值 "80"')
        p2j_quality = int('80')
    else:
        print(f'读取到配置 "BMPTarget" 的值为 "{p2j_quality}"')


    p2w_quality = int(config.get('P2W_Quality', '').strip('"'))
    if p2w_quality == '':
        print(f'警告: 配置文件中 "P2W_Quality" 的值为空，程序将使用默认值 "80"')
        p2w_quality = int('80')
    else:
        print(f'读取到配置 "BMPTarget" 的值为 "{p2w_quality}"')


    converter_format_select()


# 图像重命名操作函数
def image_rename():


    # 加载功能 Rename 的配置文件
    config_path = './config/rename.yaml'
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)


    source_path = config.get('RenameSourceFolder', '').strip('"')
    if source_path == '':
        print(f'警告: 配置文件中 "RenameSourceFolder" 的值为空，程序将使用默认值 "./data/Rename/Source"')
        source_path = './data/Rename/Source'
    else:
        print(f'读取到配置 "RenameSourceFolder" 的值为 "{source_path}"')


    target_path = config.get('RenameTargetFolder', '').strip('"')
    if target_path == '':
        print(f'警告: 配置文件中 "RenameTargetFolder" 的值为空，程序将使用默认值 "./data/Rename/Renamed"')
        target_path = './data/Rename/Renamed'
    else:
        print(f'读取到配置 "RenameTargetFolder" 的值为 "{target_path}"')


    # 暂停三秒，查看配置文件读取信(bao)息(cuo)
    time.sleep(3)


    os.makedirs(source_path, exist_ok=True)
    os.makedirs(target_path, exist_ok=True)


    # 遍历 Source 文件夹下的所有图片
    for filename in os.listdir(source_path):
        time.sleep(0.05)
        try:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp')):
                new_filename = str(uuid.uuid4()).replace('-', '') + os.path.splitext(filename)[1]
                source_file = os.path.join(source_path, filename)
                target_file = os.path.join(target_path, new_filename)

                shutil.move(source_file, target_file)

                print(f'已处理: {filename} => {new_filename}')
        
        except (IOError, OSError) as error:
            print(f'{filename} 不是常见的图像格式，程序可能无法识别，跳过此文件: {error}')

        
    input('重命名完成，按 Enter 继续...')
    function_select()


# 程序终止函数
def program_exit(exitcode):
    
    if exitcode == '0x00':
        print('侦测到停止命令，程序正常结束')
    elif exitcode == '0x01':
        print('程序无法正确读取配置文件，可能是配置文件错误')
    elif exitcode == '0x02':
        print('程序因未知原因中断')
    else:
        program_exit('0x02')

    input('程序终止，按 Enter 退出...')
    exit()


# 侦测强行中断操作，如果按下 ^C，将事件直接传递到 program_exit() 函数
try:
    function_select()
except KeyboardInterrupt:
    print('侦测到 ^C 输入，强制中止程序...')
    program_exit('0x00')