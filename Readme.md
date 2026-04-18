🤖 Robot Omni Navigation Project

Dự án này được phát triển trên nền tảng hệ điều hành Ubuntu 24.04 tập trung vào việc xây dựng hệ thống điều hướng (Navigation) cho robot di động đa hướng (Omni-directional Robot) hoạt động trong môi trường mô phỏng Gazebo, chạy trên nền tảng ROS 2 Jazzy. Dự án tích hợp các thuật toán hiện đại như MPPI và SmacPlanner để tối ưu hóa khả năng di chuyển trong môi trường hẹp.
Dự án sử dụng world mô phỏng là môi trường trong bệnh viện (hospital world).

📂 Cấu trúc dự án (Workspace Structure)

Cấu trúc thực tế trong thư mục ros2_ws/src/robot_omni:

    config/: Chứa các file tham số cấu hình hệ thống.

        nav2_params.yaml: Cấu hình chính cho Nav2 (Planner, Controller, MPPI).

        ekf.yaml: Cấu hình bộ lọc Kalman (EKF) để kết hợp dữ liệu Odom và IMU.

        bridge_config.yaml: Cấu hình kết nối dữ liệu giữa ROS 2 và Gazebo.

    launch/: Chứa các kịch bản khởi chạy hệ thống tự động.

        localization_launch.py: Khởi chạy AMCL và Map Server.

        gazebo_control.launch.py: Khởi động môi trường mô phỏng vật lý.
        
        robot_patrol.py: Công cụ nhập số phòng, robot sẽ tự tính toán đường đi và di chuyển đến tọa độ đã định nghĩa.

        slam.py: Công cụ hỗ trợ tạo bản đồ mới.

    urdf/ & meshes/: Chứa file mô tả vật lý, khớp nối và mô hình 3D của robot Omni.

    rviz/: Lưu trữ các file cấu hình giao diện quan sát trực quan (localization.rviz).

    worlds/: Môi trường mô phỏng (bệnh viện, văn phòng).

🚀 Hướng dẫn vận hành nhanh
⚠️ Lưu ý quan trọng (Prerequisites)

Trước khi chạy, bạn cần cập nhật đường dẫn tuyệt đối trong file omni_base.urdf. Hãy thay đổi tất cả các đường dẫn chứa /home/tamtue/ros2_ws/ thành đường dẫn thực tế trên máy của bạn.
1. Build dự án

Mở terminal tại thư mục gốc ros2_ws:
Bash

cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash

2. Khởi chạy mô phỏng và Điều hướng

Sử dụng file launch tổng hợp để kích hoạt robot trong môi trường Gazebo:
Bash

ros2 launch robot_omni localization_launch.py 

3. Điều khiển Robot theo phòng (Patrol Mode)

Mở một terminal mới để chạy script nhập số phòng. Robot sẽ tự động di chuyển đến tọa độ đích đã định nghĩa:
Bash

python3 ~/ros2_ws/src/robot_omni/launch/robot_patrol.py

4. Kích hoạt vật thể chuyển động (Dynamic Obstacles)
Trước tiên bạn cần copy file move.sh vào thư mục bất kỳ (vd ~/ros2_ws)
Nếu muốn kiểm tra khả năng tránh vật cản động, hãy chạy script dưới với một terminal mới:
Bash

cd ~/ros2_ws
chmod a+x move.sh
./move.sh

🛠 Công nghệ sử dụng

    Middleware: ROS 2 Jazzy Jalisco.

    Controller: MPPI Controller (Model Predictive Path Integral) - Tối ưu hóa quỹ đạo thời gian thực, giúp xe Omni di chuyển mượt mà.

    Planner: SmacPlanner2D - Sử dụng thuật toán A* tối ưu cho mạng lưới chi phí.

    Localization: AMCL (Adaptive Monte Carlo Localization).

    Simulator: Gazebo Harmonic.

📝 Nhật ký tối ưu hóa (Tuning Log)

Trong quá trình thực hiện dự án, các thông số sau đã được tinh chỉnh để đạt hiệu suất tốt nhất:

    Cải thiện bám đường: Tăng PathAlignCritic lên 20-25 để robot bám khít đường đỏ khi cua gấp.

    Xử lý không gian hẹp: Điều chỉnh inflation_radius xuống 0.55m và tăng cost_scaling_factor lên 10.0 để thu gọn vùng chi phí màu tím, giúp robot đi qua cửa hẹp dễ dàng.

    Lỗi tiệm cận đích: Hạ thấp threshold_to_consider trong GoalCritic để loại bỏ hiện tượng robot bị khựng/do dự khi gần sát vị trí đích.
    
    
    Các nguồn tham khảo:
    	Navigation servers: https://docs.nav2.org/configuration/index.html
    	Behavior Tree:
	https://www.behaviortree.dev/docs/category/tutorials-basic
	https://docs.nav2.org/behavior_trees/index.html

	Groot tutorial: https://docs.nav2.org/tutorials/docs/groot2.html
	ROS2 Navigation:
	https://docs.nav2.org/
	https://roboticsbackend.com/ros2-nav2-tutorial/
	https://www.behaviortree.dev/
	

