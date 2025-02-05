from controller import Robot

def kalkulasi_motor(signal):
    return (signal/100)*6.28

def run_robot(robot):
    timestep = int(robot.getBasicTimeStep())
    
    motor_pos_val = [0, 0]
    sensor_ir_val = [0, 0, 0, 0, 0, 0]
    sensor_jarak_val = [0, 0, 0]
    pid_parameter = [43, 0.2, 145] #Kp Ki Kd
    error = 0
    sumError = 0
    last_error = 0
    set_point = 0
    control = [0, 0, 0]
    pid_control = 0
    #ts = 1
    nilai_posisi = 0

    def read_ir():
        for i in range(6):
           if sensor_ir_val[i] > 600:
               sensor_ir_val[i] = 0
           else :
               sensor_ir_val[i] = 1
    
    def robotPos():
        if sensor_ir_val[5] == 1 :
            nilai_posisi = -7
        if sensor_ir_val[3] == 1 and sensor_ir_val[4] == 1 and sensor_ir_val[5] == 1 :
            nilai_posisi == -6
        if sensor_ir_val[4] == 1 and sensor_ir_val[5] == 1 :
            nilai_posisi = -5                     
        if sensor_ir_val[4] == 1 :
            nilai_posisi = -4
        if sensor_ir_val[2] == 1 and sensor_ir_val[3] == 1 and sensor_ir_val[4] == 1 :
            nilai_posisi = -3
        if sensor_ir_val[3] == 1 and sensor_ir_val[4] == 1 :
            nilai_posisi = -2                  
        if sensor_ir_val[3] == 1 :
            nilai_posisi = -1
        if sensor_ir_val[2] == 1 and sensor_ir_val[3] == 1 :
            nilai_posisi = 0
        if sensor_ir_val[2] == 1 :
            nilai_posisi = 1
        if sensor_ir_val[1] == 1 and sensor_ir_val[2] == 1 :
            nilai_posisi = 2
        if sensor_ir_val[1] == 1 and sensor_ir_val[2] == 1 and sensor_ir_val[3] == 1 :
            nilai_posisi = 3
        if sensor_ir_val[1] == 1 :
            nilai_posisi = 4
        if sensor_ir_val[0] == 1 and sensor_ir_val[1] == 1 :
            nilai_posisi = 5
        if sensor_ir_val[0] == 1 and sensor_ir_val[1] == 1 and sensor_ir_val[2] == 1 :
            nilai_posisi = 6
        if sensor_ir_val[0] == 1 :
            nilai_posisi = 7
        print("RobotPos: {}".format(nilai_posisi))
        
    # Deklarasi Motor
    motor = []
    motor_nama =['motor_1', 'motor_2']
    for i in range(2):
        motor.append(robot.getDevice(motor_nama[i]))
        motor[i].setPosition(float('inf'))
        motor[i].setVelocity(0.0)

    # Deklarasi Sensor Odometry
    motor_pos = []
    motor_pos_nama =['ps_1', 'ps_2']
    for i in range(2):
        motor_pos.append(robot.getDevice(motor_pos_nama[i]))
        motor_pos[i].enable(timestep)

    # Deklarasi IR Sensor
    sensor_ir = []
    sensor_ir_nama = ['IRL2', 'IRL1', 'IRCL', 'IRCR', 'IRR1', 'IRR2']
    for i in range(6):
        sensor_ir.append(robot.getDevice(sensor_ir_nama[i]))
        sensor_ir[i].enable(timestep)
    
    # Deklarasi Sensor Proximity
    sensor_jarak = []
    sensor_jarak_nama =['ds_left', 'ds_front', 'ds_right']
    for i in range(3):
        sensor_jarak.append(robot.getDevice(sensor_jarak_nama[i]))
        sensor_jarak[i].enable(timestep)

    # Deklarasi Camera
    camera = robot.getDevice('CAM')
    camera.enable(timestep)


    
    # Main Loop
    while robot.step(timestep) != -1:
        kecepatan_normal = 80
        kecepatan_lambat = 20
        kecepatan_cepat = 100

        for i in range(2):
            motor_pos_val[i] = motor_pos[i].getValue()
        
        for i in range(6):
            sensor_ir_val[i] = sensor_ir[i].getValue()
        read_ir()
        robotPos()
        
        for i in range(3):
            sensor_jarak_val[i] = sensor_jarak[i].getValue()

        #pid
        error = set_point - nilai_posisi
        DeltaError = error - last_error
        sumError += last_error

        #control P
        control[0] = pid_parameter[0] * error

        #control I
        control[1] = pid_parameter[1] * sumError 

        #control D
        control[2] = pid_parameter[2] * DeltaError

        last_error = error

        #PID Control
        pid_control = control[0] + control[1] + control[2]

        kecepatan = kalkulasi_motor(kecepatan_normal)
        pid_control = kalkulasi_motor(pid_control)
        kiri = kecepatan - pid_control
        kanan = kecepatan + pid_control

        if kiri > kecepatan_cepat :
            kiri = kecepatan_cepat
        if kiri < kecepatan_lambat :
            kiri = kecepatan_lambat
        if kanan > kecepatan_cepat :
            kanan = kecepatan_cepat
        if kanan < kecepatan_lambat :
           kanan = kecepatan_lambat
        #print("Odometry sensor values: {:.3f} {:.3f}".format(motor_pos_val[0], motor_pos_val[1]))

        #print("Proximity sensor values: {:.3f} {:.3f} {:.3f}".format(sensor_jarak_val[0], sensor_jarak_val[1], sensor_jarak_val[2]))

        #print("IR sensor values: {:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f}".format(sensor_ir_val[0], sensor_ir_val[1], sensor_ir_val[2], sensor_ir_val[3], sensor_ir_val[4], sensor_ir_val[5]))
        #print("PID: {} {} {} {}".format(error, DeltaError, sumError, last_error))
        
        motor[0].setVelocity(0)
        motor[1].setVelocity(0)

if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)