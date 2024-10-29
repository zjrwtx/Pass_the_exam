# 不挂科AI后端

## 项目简介

不挂科AI后端是一个基于FastAPI框架构建的Web应用程序，旨在为用户提供一系列智能化的服务，包括视频转PPT、PPT转PDF、PDF和PPT内容解析、考试重点大纲生成、出题、思维导图生成等功能。该后端服务使用了多种Python库，如FastAPI、PyPDF2、python-pptx、sqlalchemy、pydantic、passlib、python-jose、python-dotenv、requests、pymysql、scikit-image、opencv-python、imutils和img2pdf等。

## 功能

- 视频转PPT
- PPT转PDF
- PDF和PPT内容解析
- 考试重点大纲生成
- 出题
- 思维导图生成

## 环境配置

在开始使用本应用之前，您需要确保您的环境中安装了以下依赖项：

- fastapi
- PyPDF2
- python-pptx
- sqlalchemy
- pydantic
- passlib
- python-jose
- python-dotenv
- requests
- pymysql
- scikit-image
- opencv-python
- imutils
- img2pdf
- python-multipart

您可以通过以下命令安装这些依赖项：

```bash
pip install -r requirements.txt
```

## 运行应用

要运行该应用，请使用以下命令：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API端点

以下是该项目提供的API端点列表：

- /upload/：上传视频文件，并将其转换为PPT。
- /mindmap：上传PDF或PPTX文件，并生成思维导图。
- /topics：上传PDF或PPTX文件，并生成考试重点大纲。
- /examkeypoints：上传PDF或PPTX文件，并生成期末考试试卷。
- /check_user：检查用户名是否已存在。

## 贡献

如果您想为该项目做出贡献，请遵循以下步骤：

1. Fork该项目。
2. 创建一个新的分支。
3. 提交您的更改。
4. 发起一个Pull Request。

## 许可证

该项目采用MIT许可证。有关详细信息，请查看LICENSE文件。

## 联系方式

如果您有任何问题或建议，请通过以下方式联系我们：

- 邮箱：[3038880699@qq.com](mailto:3038880699@qq.com)
- GitHub：[zjrwtx](https://github.com/zjrwtx)

感谢您的关注和使用！
