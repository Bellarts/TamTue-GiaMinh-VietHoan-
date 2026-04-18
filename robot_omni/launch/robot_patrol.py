import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from rclpy.parameter import Parameter
from tf2_ros import Buffer, TransformListener
from ga_path_optimizer import optimize_route
import math

def main():
    rclpy.init()
    nav = BasicNavigator()
    nav.waitUntilNav2Active()

    # --- BƯỚC 1: ĐỊNH VỊ NHANH ---
    input("\n[!] Chấm '2D Pose Estimate' trên RViz rồi nhấn ENTER...")
    
    node = rclpy.create_node('pos_getter', parameter_overrides=[Parameter('use_sim_time', value=True)])
    buffer = Buffer()
    TransformListener(buffer, node)
    
    curr_x, curr_y = 0.0, 0.0
    for _ in range(30): # Chờ bắt tọa độ
        rclpy.spin_once(node, timeout_sec=0.1)
        try:
            t = buffer.lookup_transform('map', 'base_link', rclpy.time.Time())
            curr_x, curr_y = t.transform.translation.x, t.transform.translation.y
            break
        except: continue
    node.destroy_node()

    # --- BƯỚC 2: TỌA ĐỘ PHÒNG ---
    all_rooms = [
        {"n": "r1", "x": 4.51, "y": 6.12},   {"n": "r2", "x": -4.43, "y": 6.33},
        {"n": "r3", "x": 7.71, "y": 3.45},   {"n": "r4", "x": -7.53, "y": 3.54},
        {"n": "r5", "x": 11.14, "y": 0.11},  {"n": "r6", "x": -10.61, "y": -0.89},
        {"n": "r7", "x": 10.76, "y": -5.08}, {"n": "r8", "x": -9.98, "y": -4.64},
        {"n": "r9", "x": 1.38, "y": -13.01}, {"n": "r10", "x": -1.16, "y": -13.08},
        {"n": "r11", "x": 8.28, "y": -17.81}, {"n": "r12", "x": -7.98, "y": -18.17},
        {"n": "r13", "x": 7.14, "y": -10.43}, {"n": "r14", "x": -7.24, "y": -10.21},
        {"n": "r15", "x": 1.78, "y": -22.22}, {"n": "r16", "x": -1.68, "y": -22.29},
        {"n": "r17", "x": 2.17, "y": -28.47}, {"n": "r18", "x": -2.40, "y": -27.78},
        {"n": "r19", "x": 8.33, "y": -31.87}, {"n": "r20", "x": -8.17, "y": -32.09},
        {"n": "r21", "x": 7.09, "y": -24.40}, {"n": "r22", "x": -7.32, "y": -24.40},
        {"n": "r23", "x": 1.43, "y": -38.35}, {"n": "r24", "x": -2.21, "y": -40.59},
        {"n": "r25", "x": -7.97, "y": -39.53}, {"n": "r26", "x": -8.58, "y": -35.85}
    ]
        #r12 - phong 1, r11 - phong 6, r23 - phong 4
    # --- BƯỚC 3: CHỌN PHÒNG & GA ---
    ids = input("Nhập số phòng (vd: 1,5,10): ")
    targets = [{"n": "START", "x": curr_x, "y": curr_y}]
    for i in ids.replace(",", " ").split():
        idx = int(i.strip()) - 1
        if 0 <= idx < 26: targets.append(all_rooms[idx])

    dist_m = [[math.hypot(targets[j]["x"]-targets[i]["x"], targets[j]["y"]-targets[i]["y"]) 
               for j in range(len(targets))] for i in range(len(targets))]
    
    path = optimize_route(dist_m)

    # --- BƯỚC 4: CHẠY ---
    for i in path[1:]: # Bỏ qua điểm xuất phát
        p = targets[i]
        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x, goal.pose.position.y = p["x"], p["y"]
        goal.pose.orientation.w = 1.0
        
        print(f">> Đi tới: {p['n']}")
        nav.goToPose(goal)
        while not nav.isTaskComplete(): pass
        
        if nav.getResult() != TaskResult.SUCCEEDED:
            print("!! Lỗi di chuyển. Dừng."); break

    rclpy.shutdown()

if __name__ == '__main__': main()