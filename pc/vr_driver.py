import openvr
import time

def get_hmd_pose():
    # Initialize OpenVR in Scene Application mode
    openvr.init(openvr.VRApplication_Scene)
    vr_compositor = openvr.VRCompositor()

    try:
        poses = []  # This will be populated with proper type after the first call
        while True:
            # Obtain the pose of all tracked devices
            poses, _ = vr_compositor.waitGetPoses(poses, None)
            hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]

            if hmd_pose.bPoseIsValid:
                # Extract the 3x4 transformation matrix
                matrix = hmd_pose.mDeviceToAbsoluteTracking

                # The translation components are at indices [0][3], [1][3], and [2][3]
                position = (matrix[0][3], matrix[1][3], matrix[2][3])

                print(f"HMD Position: X={position[0]:.2f}, Y={position[1]:.2f}, Z={position[2]:.2f}")
            else:
                print("HMD pose is not valid.")

            time.sleep(0.2)  # Sleep for 200 milliseconds

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        openvr.shutdown()

if __name__ == "__main__":
    get_hmd_pose()
