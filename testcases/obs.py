# import subprocess
# import time
# from utils import times
# # import cv2
#
# # 启动推流
# def push_obs(push_url, seconds=220):
#     ffmpeg_command = [
#         'ffmpeg', '-re', '-i', 'input.mp4', '-c:v', 'libx264', '-b:v', '1M', '-f', 'flv', push_url
#     ]
#
#     ffmpeg_process = subprocess.Popen(ffmpeg_command)
#
#     # 模拟网络不稳定
#     time.sleep(seconds)  # 正常推流10秒
#     # subprocess.call(['tc', 'qdisc', 'add', 'dev', 'eth0', 'root', 'netem', 'loss', '10%'])  # 丢包10%
#     # time.sleep(10)  # 继续推流10秒
#     # subprocess.call(['tc', 'qdisc', 'del', 'dev', 'eth0', 'root'])  # 恢复正常
#
#     # 结束推流
#     ffmpeg_process.terminate()
#
#
# def pull_obs(pull_url, duration=10):
#     output_file = times.current_time("%Y%m%d%H%M%S")
#     output_file = output_file+".mp4"
#
#     command = [
#         "ffmpeg",
#         "-i", pull_url,  # 输入直播流 URL
#         "-t", str(duration),  # 拉取时长（秒）
#         "-c", "copy",  # 直接复制流，不重新编码
#         output_file
#     ]
#     try:
#         subprocess.run(command, check=True, stderr=subprocess.PIPE)
#         print("直播流拉取成功")
#         return True
#     except subprocess.CalledProcessError as e:
#         print(f"直播流拉取失败：{e.stderr.decode()}")
#         return False
#
# # 检查拉取的视频文件是否正常
# # def check_video_file(video_file):
# #     """
# #     检查拉取的视频文件是否正常
# #     :param video_file: 视频文件路径
# #     """
# #     cap = cv2.VideoCapture(video_file)
# #     if not cap.isOpened():
# #         print("无法打开视频文件")
# #         return False
# #
# #     frame_count = 0
# #     while cap.isOpened():
# #         ret, frame = cap.read()
# #         if not ret:
# #             break
# #         frame_count += 1
# #
# #     cap.release()
# #     print(f"视频帧分析完成，总帧数：{frame_count}")
# #     return frame_count > 0  # 如果有帧，则认为视频正常
#
#
#
# def ping_test(server):
#     result = subprocess.run(['ping', '-c', '4', server], capture_output=True, text=True)
#     return result.stdout
#
# print(ping_test("https://wjm-pull.tv189.com/livegw/3be38072c8.flv"))
#
#
# if __name__ == '__main__':
#     # push_obs("rtmp://tywjmapi.tv189.com/livegw/055008b72d")
#     # pull_url = "https://wjm-pull.tv189.com/livegw/3be38072c8.flv"
#     pull_url = "https://wjm-pull.tv189.com/livegw/3be38072c8.flv"
#     # pull_obs(pull_url, duration=30)
#
#     ping_test("https://wjm-pull.tv189.com")