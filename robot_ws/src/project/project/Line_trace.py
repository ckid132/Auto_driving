import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
import cv2
import numpy as np

TB_LIN_SPD = 0.1
TB_ANG_SPD = 1

class LineDetector(Node):

    def __init__(self):
        super().__init__('img_convert')
        qos_profile = QoSProfile(depth=10)

        self.subscription = self.create_subscription(CompressedImage, 
                'camera/image/compressed', 
                self.get_compressed, 
                10)
        self.bridge = CvBridge()
        #self.cv_img = cv2.imread("empty1.png", cv2.IMREAD_UNCHANGED)
        self.cv_img = np.zeros([120,160])
        print("type(cv_img)", type(self.cv_img))

    def get_compressed(self, msg):
        self.cv_img = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")

def main(args=None):
    rclpy.init(args=args)
    node = LineDetector()
    tw = Twist()
    pub = node.create_publisher(Twist, '/cmd_vel', 10)
    
    try:   
        while rclpy.ok():
            print("type(node.cv_img) : ", type(node.cv_img))
            rclpy.spin_once(node, timeout_sec=0.1)
            img = node.cv_img
            print("type(img)", type(img))
            if img is not None and not img.size == 0: 
                frame = img
                frame = cv2.resize(img, (160,120))
                frame = cv2.flip(frame,-1)
                frame = cv2.flip(frame, 1)
                cv2.imshow( 'normal' , frame)
                cv2.moveWindow('normal', 200, 30)
                crop_img =frame[60:120, 0:160]
                gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (5,5) , 0)
                ret,thresh1 = cv2.threshold(blur, 123, 255, cv2.THRESH_BINARY_INV)
                mask = cv2.erode(thresh1, None, iterations=2)  
                mask = cv2.dilate(mask, None, iterations=2)
                
                cv2.imshow('mask',mask)
                mask_1 = mask.copy()
                contours,hierarchy = cv2.findContours(mask_1, 1, cv2.CHAIN_APPROX_NONE)
                
                
                if len(contours) > 0:
                    c = max(contours, key=cv2.contourArea)
                    M = cv2.moments(c)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    
                    cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
                    cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
                    cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
                    cv2.imshow('crop_img', crop_img)
                    
                    #cv2.line(mask_1,(cx,0),(cx,720),(255,0,0),1)
                    #cv2.line(mask_1,(0,cy),(1280,cy),(255,0,0),1)
                    cv2.rectangle(mask_1, (cx-3,cy-3), (cx+3, cy+3), (0,0,0), -1)
                    cv2.drawContours(mask_1, contours, -1, (0,255,0), 1)
                    
                    cv2.imshow('mask_1', mask_1)
                    
                    print(cx) 
                    
                    if 0<cx and cx <75:              
                        print("Turn Left!")
                        tw.angular.z = 0.2
                        tw.linear.x = 0.0
                        
                    elif 85<cx and cx<160:
                        print("Turn Right")
                        tw.angular.z = -0.2
                        tw.linear.x = 0.0
                    else:
                        print("go")
                        string = "go"
                        tw.angular.z = 0.0
                        tw.linear.x = 0.03                  
                        
                    pub.publish(tw)
                    
                if cv2.waitKey(1) == ord('q'):
                    tw.linear.x = 0.0
                    tw.angular.z = 0.0
                    pub.publish(tw)
                    break
    
        cv2.destroyAllWindows()
            
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt(SIGINT)')
        tw.linear.x = 0.0
        tw.angular.z = 0.0
        pub.publish(tw)
        
    finally:
        node.destroy_node()
        rclpy.shutdown()
            
if __name__ == '__main__':
    main()
    
    # cv2.rectangle(mask, (cx-3, cy-3), (cx+3,cv+3), (255,255,255), 1, lineType=None, shift=None)
