import threading
import webbrowser
import os
import shutil
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

# 导入 Flask 应用模块，以便修改配置
import app as flask_app_module

class FundMonitorApp(App):
    def build(self):
        # 1. 设置数据存储路径（确保在安卓上有读写权限）
        # user_data_dir 是 Kivy 提供的可写目录
        self.setup_data_storage()

        # 2. 启动 Flask 服务线程
        self.flask_thread = threading.Thread(target=self.run_flask)
        self.flask_thread.daemon = True
        self.flask_thread.start()
        
        # 3. 延迟3秒打开浏览器
        Clock.schedule_once(self.open_browser, 3)
        
        return Label(text="FundMonitor Service Running...\nOpening Browser...", font_size='20sp', halign='center')

    def setup_data_storage(self):
        """配置持久化存储，防止数据丢失"""
        try:
            # 获取当前应用的私有数据目录
            data_dir = self.user_data_dir
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            # 目标配置文件路径
            target_config = os.path.join(data_dir, 'funds.json')
            
            # 如果目标不存在，尝试从打包资源中复制一份初始配置
            if not os.path.exists(target_config):
                # 假设原始 funds.json 在 main.py 同级目录
                source_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'funds.json')
                if os.path.exists(source_config):
                    shutil.copy(source_config, target_config)
            
            # 修改 Flask app 的配置文件路径指向可写目录
            flask_app_module.CONFIG_FILE = target_config
            print(f"Config file path set to: {target_config}")
            
        except Exception as e:
            print(f"Error setting up storage: {e}")

    def run_flask(self):
        # 在安卓上监听 0.0.0.0 端口 5000
        # 注意：debug=False, use_reloader=False 是必须的，否则在安卓上会报错
        flask_app_module.app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

    def open_browser(self, dt):
        # 打开本地浏览器访问
        webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    FundMonitorApp().run()
