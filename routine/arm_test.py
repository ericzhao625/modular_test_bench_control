import multiprocessing
import sys
from multiprocessing import Process, Value, Array
import math
from tkinter import *

from fanucpy import Robot
default_pos = [380.318, -266.229, 99.984, -180, 0.0, 45]

default_xy_pos = [0, 0, 0, 180.0, 0.0, 0.0]

min_pos = [0, 0, -160, -180, 0, 0]
max_pos = [500+90, 580+470, 500, -180, 0, 360]
root = Tk()

point_array = []


def save_points():
    global point_array
    data_arr = []
    for i in range(6):
        data_arr.append(joint_sliders[i].get())
    point_array.append(data_arr)
    print(point_array)
    
joint_sliders = []
for i in range(6):
    pos = Scale(root, from_=min_pos[i], to=max_pos[i], orient=HORIZONTAL, resolution=0.001, length=500)
    pos.pack()
    pos.set(default_xy_pos[i])
    joint_sliders.append(pos)
    
accel_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL, resolution=1, length=500)
accel_slider.pack()

event4 = multiprocessing.Event()
w = Button(root, text="Save Point.", command=lambda: event4.set())
w.pack()
event2 = multiprocessing.Event()
x = Button(root, text="Start Routine.", command=lambda: event2.set())
x.pack()

# j1 = Scale(root, from_=0, to=50, orient=HORIZONTAL)
# j1.pack()
# j2 = Scale(root, from_=0, to=10, orient=HORIZONTAL)
# j2.pack()
# j3 = Scale(root, from_=0, to=10, orient=HORIZONTAL)
# j3.pack()
# j4 = Scale(root, from_=0, to=10, orient=HORIZONTAL)
# j4.pack()
# j5 = Scale(root, from_=0, to=10, orient=HORIZONTAL)
# j5.pack()
# j6 = Scale(root, from_=0, to=10, orient=HORIZONTAL)
# j6.pack()

def gui_app(data:Array, accel, event1):
    while True:
        for j in range(6):
            data[j] = joint_sliders[j].get()
        accel.value = accel_slider.get()
        root.update_idletasks()
        root.update()
        if event2.is_set():
            event1.set()


def move_robot_routine(data, accel, event3):
    robot = Robot(
    robot_model="Fanuc",
    host="192.168.1.52",
    port=18735,
    ee_DO_type="RDO",
    ee_DO_num=7,
    )
    
    robot.__version__()
    robot.connect()

    while not event3.is_set():
        rotation_matrix = [
            [math.cos(math.pi / 4), -math.sin(math.pi / 4)],
            [math.sin(math.pi / 4), math.cos(math.pi / 4)]
                           ]
        x_1 = rotation_matrix[0][0] * (data[0]-90) + rotation_matrix[0][1] * (data[1]-470)
        y_1 = rotation_matrix[1][0] * (data[0]-90) + rotation_matrix[1][1] * (data[1]-470)
        robot.move(
            "pose",
            vals=[x_1, y_1, data[2], data[3], data[4], data[5]],
            velocity=20,
            acceleration=accel.value,
            cnt_val=0,
            linear=False
        )
        # robot.move(
        #     "pose",
        #     vals=[400, 400, 100, -180, 0, 90],
        #     velocity=100,
        #     acceleration=accel.value,
        #     cnt_val=0,
        #     linear=False
        # )
        sys.stdout.write('\r')
        sys.stdout.flush()
        # sys.stdout.write(f"Joints: {robot.get_curjpos()} | ")
        # sys.stdout.write(f'cartesian: {robot.get_curpos()}')
        # rotation_matrix = [
        #     [math.cos(math.pi / 4), -math.sin(math.pi / 4)],
        #     [math.sin(math.pi / 4), math.cos(math.pi / 4)]
        #                    ]
        # arr = robot.get_curpos()
        # new_arr = arr
        # new_arr[0] = rotation_matrix[0][0] * arr[0] + rotation_matrix[0][1] * arr[1]
        # new_arr[1] = rotation_matrix[1][0] * arr[0] + rotation_matrix[1][1] * arr[1]
        # print(new_arr)
        
        # if event3.is_set():
        #     break
    # while True:
    #     print(point_array)
    #     for points in point_array:
    #         robot.move(
    #             "joint",
    #             vals=[points[0], points[1], points[2], points[3], points[4], points[5]],
    #             velocity=100,
    #             acceleration=accel.value,
    #             cnt_val=0,
    #             linear=False
    #         )

if __name__ == '__main__':
    
    accel = Value('i', 1)
    event_1 = multiprocessing.Event()
    origin = [380.318, -266.229, 99.984, -180, 0.0, 45]
    
    joint_pos = Array('d', range(6))
    for i in range(6):
        joint_pos[i] = origin[i]
    p1 = multiprocessing.Process(target=gui_app, args=(joint_pos, accel, event_1))
    p2 = multiprocessing.Process(target=move_robot_routine, args=(joint_pos, accel, event_1))
    p1.start()
    p2.start()
