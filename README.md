# DeepSeek R1 联网搜索

DeepSeek R1联网搜索演示，基于streamlit+python

## 功能特点

- 支持搜索框输入问题
- 调用DeepSeek API处理请求
- 流式实时输出答案
- 支持多轮交互对话
- 美观的用户界面

## 安装步骤

1. 克隆代码仓库：

```bash
git clone https://github.com/sencloud/deepseek_r1_online_search.git
cd deepseek_r1_online_search
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 配置API密钥：

复制`.env.example`文件为`.env`并填入您的DeepSeek API密钥：

```bash
cp .env.example .env
```

然后编辑`.env`文件：

```
# Deepseek API配置
DEEPSEEK_API_KEY=your_api_key_here
```

## 运行应用

启动Streamlit应用：

```bash
streamlit run app.py
```

应用将在本地启动，默认访问地址为：http://localhost:8501

## 使用说明

1. 在输入框中输入您的问题
2. 点击"发送"按钮提交问题
3. 系统会实时流式输出DeepSeek的回答
4. 继续输入问题进行多轮对话

## 项目结构

- `app.py`: Streamlit应用主文件
- `deepseek_client.py`: DeepSeek API客户端
- `config.py`: 配置文件
- `.env`: 环境变量配置文件
- `requirements.txt`: 项目依赖

## 其他
如果你喜欢我的项目，可以给我买杯咖啡：
<img src="https://github.com/user-attachments/assets/e75ef971-ff56-41e5-88b9-317595d22f81" alt="image" width="300" height="300">

## 许可证

MIT License