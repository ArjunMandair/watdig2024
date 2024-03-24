import rclpy
import logging
from rclpy.node import Node
from interfaces.msg import CurrentCoords
from std_msgs.msg import Float32MultiArray, Float32
from scipy.optimize import minimize
import numpy as np


class LocalizationNode(Node):
    def __init__(self):
        super().__init__('localization_node')
        
        # Publishers
        self.current_location_publisher = self.create_publisher(CurrentCoords, 'current_location_topic', 10)
        
        # UWB Anchor Points
        self.uwbs = [(0, 0), (15, 0), (0,15), (15,15)]
        
        #calibrate with inital distances

        # Placeholder for UWB distances
        self.uwbback = []
        self.uwbfront = []
        self.gyro = 0.00
        logger = logging.getLogger()
        
        logger.info("setup complete")
        #change this to starting point, make guess as close to previously known position
        self.x0 = np.array([0,0])
                
        self.subscription_frontuwb = self.create_subscription(
            Float32MultiArray,
            'front_uwb_topic',
            self.front_uwb_callback,
            10)
                
        self.subscription_gyro = self.create_subscription(
            Float32,
            'gyro_topic',
            self.gyro_callback,
            10
        )
    
    def gyro_callback(self, msg):
        self.gyro = msg.data
    
    def front_uwb_callback(self, msg):
        self.uwbfront = [distance for distance in msg.data]
        self.compute_and_publish_location()

    def compute_and_publish_location(self):
        logger = logging.getLogger()
        logger.info("computing location")
        uwb1_position = self.location_solver(self.uwbs, self.uwbback)
        logger.info("function run")
        if isinstance(uwb1_position, str):  # Check if the return value indicates an error
            self.get_logger().info(uwb1_position)
            x, y = self.x0[0], self.x0[1]
        else: 
            x, y = uwb1_position[0], uwb1_position[1]
        
        curr_angle = self.gyro

        logger.info("got gyro")
        
        # Once computed, publish the current location
        current_location = CurrentCoords()
        current_location.easting = x
        current_location.northing = y
        current_location.angle = curr_angle
        self.current_location_publisher.publish(current_location)
        logger.info(f'Published Current Location: {x}, {y}, {curr_angle}')
    
    def location_solver(self, points, distances):
        # Adjusted objective function to minimize
        def objective_func(X):
            x, y = X
            return sum([((x - point[0])**2 + (y - point[1])**2 - d**2)**2 for point, d in zip(points, distances)])
        
        # Perform the minimization with adjusted objective function
        result = minimize(objective_func, self.x0, method='L-BFGS-B')
            
        if result.success:
            # Check if the solution coordinates are reasonable, adjust as necessary
            if result.x[0] >= 0 and result.x[1] >= 0:
                self.x0 = result.x
                return result.x
            else:
                return "Solution has non-positive coordinates."
        else:
            return "Optimization failed."

        
    
def main(args=None):
    rclpy.init(args=args)
    localization_node = LocalizationNode()
    rclpy.spin(localization_node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
