from .comfy_ui_api import ComfyUIAPI
import json
import requests 
import time
from .utils.logger import logger
import os   
import pkg_resources

class MimicMotionComfyUI:
    @staticmethod
    def get_workflow_path(filename):
        return pkg_resources.resource_filename('shuke_ai', os.path.join('workflows', filename))

    @staticmethod
    def generate_mimicmotion(url: str, image_path: str, video_path: str, output_path: str):
        logger.info(f"开始生成MimicMotion: url={url}, image={image_path}, video={video_path}, output={output_path}")
        
        api = ComfyUIAPI(url)
        logger.info("开始上传图片...")
        image_result = api.upload_image(image_path)
        logger.info(f"图片上传成功: {image_result}")
        
        logger.info("开始上传视频...")
        video_result = api.upload_video(video_path)
        logger.info(f"视频上传成功: {video_result}")

        logger.info("加载工作流文件...")
        with open(MimicMotionComfyUI.get_workflow_path("mimicmotion.json"), "r") as f:
            workflow = json.load(f)
        logger.info("工作流文件加载成功")

        logger.info("修改工作流配置...")
        workflow["1616"]["inputs"]["image"] = image_result["name"]
        workflow["60"]["inputs"]["video"] = video_result["name"]
        logger.info("工作流配置修改完成")

        payload = {
            "prompt": workflow,
            "client_id": "mimicmotion"
        }
        
        logger.info("发送工作流请求...")
        response = api.session.post(f'{api.server_url}/prompt', json=payload)
        response.raise_for_status()
        prompt_id = response.json()["prompt_id"]
        logger.info(f"工作流请求发送成功, prompt_id: {prompt_id}")

        # 轮询检查执行结果
        logger.info("开始轮询检查执行结果...")
        while True:
            history = api.get_history(prompt_id)
            if prompt_id in history:
                execution_result = history[prompt_id]
                if "error" in execution_result:
                    logger.error("工作流执行出错")
                    logger.error(f"错误信息: {execution_result['error']}")
                    
                    if "node_errors" in execution_result:
                        for node_id, error in execution_result["node_errors"].items():
                            logger.error(f"节点 {node_id} 错误: {error}")
                    if "executed" in execution_result:
                        logger.info(f"已执行的节点: {execution_result['executed']}")
                    raise Exception(f"工作流执行失败: {execution_result['error']}")
                else:
                    logger.info("工作流执行成功")
                    logger.info(f"执行结果: {execution_result}")
                    # 下载生成的视频
                    logger.info("开始下载生成的视频...")
                    filename = execution_result["outputs"]["1148"]["gifs"][0]["filename"]
                    try:
                        video_content = api.download_video(filename)
                        output_file = os.path.join(output_path, filename)
                        with open(output_file, "wb") as f:
                            f.write(video_content)
                        logger.info(f"视频下载成功: {output_file}")
                        return output_file
                    except Exception as e:
                        logger.error(f"视频下载失败: {str(e)}")
                        raise
                break
            time.sleep(1)

if __name__ == "__main__":
    api = ComfyUIAPI("https://t8jz3wsh9kiy1vfe-80.container.x-gpu.com/")
    
    try:
        # 上传图片和视频
        image_result = api.upload_image("/Users/chaiyapeng/Downloads/1747648066007.jpg")
        logger.info(f"图片上传结果: {image_result}")
        
        video_result = api.upload_video("/Users/chaiyapeng/Downloads/with_audio.mp4")
        logger.info(f"视频上传结果: {video_result}")

        # 加载并修改工作流
        with open(MimicMotionComfyUI.get_workflow_path("mimicmotion.json"), "r") as f:
            workflow = json.load(f)
            workflow["1616"]["inputs"]["image"] = image_result["name"]
            workflow["60"]["inputs"]["video"] = video_result["name"]

            payload = {
                "prompt": workflow,
                "client_id": "mimicmotion"
            }
            
            # 发送工作流请求
            response = api.session.post(f'{api.server_url}/prompt', json=payload)
            response.raise_for_status()
            prompt_id = response.json()["prompt_id"]
            logger.info(f"工作流提交成功,prompt_id: {prompt_id}")

            # 轮询检查执行结果
            logger.info("开始轮询检查执行结果...")
            retry_count = 0
            while True:
                retry_count += 1
                logger.info(f"第{retry_count}次轮询检查...")
                history = api.get_history(prompt_id)
                if prompt_id in history:
                    execution_result = history[prompt_id]
                    if "error" in execution_result:
                        logger.error("工作流执行出错")
                        logger.error(f"错误信息: {execution_result['error']}")
                        
                        if "node_errors" in execution_result:
                            for node_id, error in execution_result["node_errors"].items():
                                logger.error(f"节点 {node_id} 错误: {error}")
                        if "executed" in execution_result:
                            logger.info(f"已执行的节点: {execution_result['executed']}")
                    else:
                        logger.info("工作流执行成功")
                        logger.info(f"执行结果: {execution_result}")
                        # 下载生成的视频
                        filename = execution_result["outputs"]["1148"]["gifs"][0]["filename"]
                        try:
                            video_content = api.download_video(filename)
                            with open("output.mp4", "wb") as f:
                                f.write(video_content)
                            logger.info("视频下载成功: output.mp4")
                        except Exception as e:
                            logger.error(f"视频下载失败: {str(e)}")
                            raise
                    break
                logger.info("未获取到执行结果,1秒后重试...")
                time.sleep(1)
                
    except Exception as e:
        logger.error(f"程序执行异常: {str(e)}")