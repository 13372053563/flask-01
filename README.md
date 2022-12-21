先创建虚拟环境，Python版本为3.8

然后下载requirements.txt
pip install -r requirement.txt

结晶检测的路径为：http://127.0.0.1:5000/detect_api/start_detect/?path=D:\project\python\Python-Web\flask-01\blue_prints\detect\inference\images\bus.jpg
其中path需要的是图片的绝对路径

detect_api.py中的# view_image(image_path=source, result=result)可以将预测的结果展示在图片中

对于种类还存在问题：CalciumCarbonate。文件在detect/utils/num2label.py