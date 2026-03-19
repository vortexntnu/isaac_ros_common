#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from message_filters import Subscriber, ApproximateTimeSynchronizer


class ImageSyncNode(Node):

    def __init__(self):
        super().__init__('image_sync_node')

        # Subscribers
        self.color_sub = Subscriber(
            self,
            Image,
            '/camera/camera/color/image_raw'
        )

        self.depth_sub = Subscriber(
            self,
            Image,
            '/camera/camera/depth/image_rect_raw'
        )

        # Approximate sync
        self.sync = ApproximateTimeSynchronizer(
            [self.color_sub, self.depth_sub],
            queue_size=20,
            slop=0.02
        )

        self.sync.registerCallback(self.callback)

        self.get_logger().info("Image sync node started")

    def callback(self, color_msg, depth_msg):

        # Convert timestamps to seconds
        color_time = color_msg.header.stamp.sec + color_msg.header.stamp.nanosec * 1e-9
        depth_time = depth_msg.header.stamp.sec + depth_msg.header.stamp.nanosec * 1e-9

        # Compute difference
        diff = abs(color_time - depth_time)

        self.get_logger().info(
            f"Timestamp difference: {diff:.6f} seconds"
        )


def main(args=None):

    rclpy.init(args=args)

    node = ImageSyncNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

