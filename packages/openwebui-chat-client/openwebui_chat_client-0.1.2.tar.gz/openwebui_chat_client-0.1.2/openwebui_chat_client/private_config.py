from openwebui_chat_client import OpenWebUIClient
import logging
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
BASE_URL = "http://localhost:3003"  # Replace with your OpenWebUI server URL
# Obtain your JWT token or API key for authentication from your account settings.
AUTH_TOKEN = "sk-26c968f00efd414a839ee725e3b082e8"
MODEL_ID = "gpt-4.1"
SINGLE_MODEL = "gpt-4.1"
MULTIMODAL_MODEL = "gemini-2.0-flash"  # 单模型对话使用的默认模型

# examples/basic_usage.py

# 确保这些模型在你的 Open WebUI 中都可用
PARALLEL_MODELS = ["gpt-4.1", "gemini-2.5-flash"]
# 多模态测试模型

# --- 为应用程序配置日志 ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def create_test_image(text: str, filename: str) -> str:
    """辅助函数，用于创建带文字的测试图片。"""
    try:
        img = Image.new("RGB", (500, 100), color=(20, 40, 80))
        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except IOError:
            font = ImageFont.load_default()
        d.text((10, 10), text, fill=(255, 255, 200), font=font)
        img.save(filename)
        logging.info(f"✅ Created test image: {filename}")
        return filename
    except ImportError:
        logging.warning("Pillow library not installed. Cannot create test image.")
        return None


def run_all_demos():
    """运行所有功能的演示。"""
    if AUTH_TOKEN == "YOUR_AUTH_TOKEN":
        logging.error("🛑 Please set your 'AUTH_TOKEN' in the script.")
        return

    # 使用一个默认模型初始化客户端，这个模型可以在 chat() 方法中被覆盖
    client = OpenWebUIClient(BASE_URL, AUTH_TOKEN, default_model_id=SINGLE_MODEL)

    # # --- 场景 1: 单模型对话 ---
    # print("\n" + "#" * 20 + " SCENE 1: Single-Model Chat " + "#" * 20)
    # response, _ = client.chat(
    #     question="What is the difference between a library and a framework?",
    #     chat_title="Tech Concepts: Library vs Framework",
    #     folder_name="Tech Discussions",
    #     model_id=SINGLE_MODEL,  # 可以显式指定模型
    # )
    # if response:
    #     print(f"\n🤖 [{SINGLE_MODEL}'s Response]:\n{response}\n")

    # # --- 场景 2: 多模型并行对话 (第一轮) ---
    # print("\n" + "#" * 20 + " SCENE 2: Multi-Model Parallel Chat (Round 1) " + "#" * 20)
    # parallel_responses = client.parallel_chat(
    #     question="In one sentence, what is the most exciting thing about space exploration?",
    #     chat_title="Space Exploration Insights",
    #     model_ids=PARALLEL_MODELS,
    #     folder_name="Science",
    # )
    # if parallel_responses:
    #     for model, content in parallel_responses.items():
    #         print(f"\n🤖 [{model}'s Response]:\n{content}\n")

    # # --- 场景 3: 继续多模型并行对话 (第二轮) ---
    # print("\n" + "#" * 20 + " SCENE 3: Multi-Model Parallel Chat (Round 2) " + "#" * 20)
    # # 客户端会自动找到 "Space Exploration Insights" 这个聊天并继续
    # parallel_responses_2 = client.parallel_chat(
    #     question="Based on your previous answer, name one specific mission that exemplifies this.",
    #     chat_title="Space Exploration Insights",
    #     model_ids=PARALLEL_MODELS,
    #     folder_name="Science",
    # )
    # if parallel_responses_2:
    #     for model, content in parallel_responses_2.items():
    #         print(f"\n🤖 [{model}'s Response]:\n{content}\n")

    # # --- 场景 4: 多模态对话 (使用单模型chat方法) ---
    # print("\n" + "#" * 20 + " SCENE 4: Multimodal Chat " + "#" * 20)
    # image_path = create_test_image("Welcome to the Future!", "multimodal_test.png")
    # if image_path:
    #     # 我们使用标准的 chat() 方法，但传入图片路径和多模态模型ID
    #     response, _ = client.chat(
    #         question="What message is written in this image?",
    #         chat_title="Multimodal Test",
    #         folder_name="Tech Demos",
    #         image_paths=[image_path],
    #         model_id=MULTIMODAL_MODEL,
    #     )
    #     if response:
    #         print(f"\n🤖 [{MULTIMODAL_MODEL}'s Response]:\n{response}\n")
    # else:
    #     logging.warning(
    #         "Skipping multimodal demo because test image could not be created."
    #     )
        
    # **************************************************************************
    # --- Scene 3: Multi-Model, Multimodal Parallel Chat ---
    # This is the ultimate test case.
    # **************************************************************************
    print("\n" + "#"*20 + " SCENE 3: Multi-Model & Multimodal Chat " + "#"*20)
    image_path = create_test_image("Project 'Phoenix' Status: GREEN", "multimodal_status.png")
    
    if image_path:
        # We use the parallel_chat() method with both text and an image.
        multimodal_responses = client.parallel_chat(
            question="Summarize the status update from this image. Be concise.",
            chat_title="Project Phoenix Status Report",
            folder_name="Project Updates",
            image_paths=[image_path],
            model_ids=PARALLEL_MODELS
        )
        if multimodal_responses:
            for model, content in multimodal_responses.items():
                print(f"\n🤖 [{model}'s Response]:\n{content}\n")
    else:
        logging.warning("Skipping multimodal demo because test image could not be created.")


    print("\n🎉 All demo scenarios completed. Please check your Open WebUI interface.")


if __name__ == "__main__":
    run_all_demos()
