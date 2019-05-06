#!/usr/bin/python3
#ROS Libraries
import rospy
import roslib
#ROS Messages
from edo_core_msgs.msg import MovementCommand
from edo_core_msgs.msg import CartesianPose
from edo_core_msgs.msg import JointStateArray
from edo_core_msgs.msg import MovementFeedback
#Python Libraries
import sys, time, queue
#numpy
import numpy as np
#Manipulation Class
class Manipulation(object):
    #init
    def __init__(self):
        #Parameters
        self.x = 0
        self.y = 0
        self.z = 0
        self.a = 0
        self.e = 0
        self.r = 0
        self.joints = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.pickHeight = 100.0
        self.grabHeight = 34.0	
        self.pickWidth = 52.0
        self.grabWidth = 18.0
        self.moveQueue = queue.Queue()
        self.mf = MovementFeedback()
        #Node Cycle rate
        self.loop_rate = rospy.Rate(100)
        #Publishers
        self.pub = rospy.Publisher('/bridge_move', MovementCommand, queue_size = 10) 
        #Subscribers
        self.subCart = rospy.Subscriber('/cartesian_pose', CartesianPose, self.cartCallback)
        self.subJoint = rospy.Subscriber('/usb_jnt_state', JointStateArray, self.jntCallback)
        self.subAck = rospy.Subscriber('/machine_movement_ack', MovementFeedback, self.ackCallback)

        rospy.sleep(0.5)
#functions

    #Creates a Cartesian Move
    def createMove(self, type):
        msg = MovementCommand()
        msg.move_command = 77
        msg.move_type = 74
        msg.ovr = 100
        msg.delay = 0
        if type == "joint":
            msg.target.data_type = 74
        elif type == "cart":
            msg.target.data_type = 88
        else: 
            msg.target.data_type = 74
        msg.target.joints_mask = 127
        return msg

    #Picks up a piece at coordinate (x,y)
    def pickUpPiece(self, x, y):
        self.jointMove()
        self.moveToPick(x,y,self.pickHeight,self.pickWidth)
        self.moveToPick(x,y,self.grabHeight,self.pickWidth)
        self.moveToPick(x,y,self.grabHeight,self.grabWidth)
        self.moveToPick(x,y,self.pickHeight,self.grabWidth)
        self.cartMove()

    #Drops off piece at coordinate (x,y)
    def dropOffPiece(self, x, y):
        self.cartMove()
        self.moveToPick(x,y,self.pickHeight,self.grabWidth)
        self.moveToPick(x,y,self.grabHeight,self.grabWidth)
        self.moveToPick(x,y,self.grabHeight,self.pickWidth)
        self.moveToPick(x,y,self.pickHeight,self.pickWidth)
        self.jointMove()
    
    #Does a little jig
    def dance(self):
        self.jointMove()
        self.jointMove([45, -30, 60, 0.0, -30, 0.0, 0.0, 0.0, 0.0, 0.0], False)
        #self.jointMove()
        self.jointMove([-45, 30, -60, 0.0, 30, 0.0, 0.0, 0.0, 0.0, 0.0], False)
        #self.jointMove()
        self.jointMove([45, -30, 60, 0.0, -30, 0.0, 0.0, 0.0, 0.0, 0.0], False)
        #self.jointMove()
        self.jointMove([-45, 30, -60, 0.0, 30, 0.0, 0.0, 0.0, 0.0, 0.0], False)
        self.jointMove()

    #Callback function for /cartesian_pose subscriber 
    def cartCallback(self, msg):
        self.x = msg.x
        self.y = msg.y
        self.z = msg.z
        self.a = msg.a
        self.e = msg.e
        self.r = msg.r

    #Prints Cartesian Position (debug)
    def printCartPos(self):
        print("x = ", self.x)
        print("y = ", self.y)
        print("z = ", self.z)
        print("a = ", self.a)
        print("e = ", self.e)
        print("r = ", self.r)

    #Callback function for /usb_jnt_state subscriber
    def jntCallback(self, msg):
        for x in range(7):
           self.joints[x] = msg.joints[x].position

    #Prints Joint Position (debug)
    def printJntPos(self):
        print(self.joints)

    #Callback function for /machine_movement_ack subscriber
    def ackCallback(self, msg):
        self.mf = msg

    #Prints Latest MovementFeedback Message recieved
    def printMF(self, msg):
        rospy.loginfo(msg)

    #Processes moves in the MoveQueue
    def processQueue(self):
        while not(self.moveQueue.empty()):
            self.mf = MovementFeedback()
            self.pub.publish(self.moveQueue.get_nowait())
            timeout = time.time() + 30 #30 Second timeout for awaiting a MovementAck
            while self.mf.type != 2:
                time.sleep(0.01)    
                if time.time() > timeout: #If it reaches 30 seconds, it moves on to the next message
                    break

    #This function moves the robot to a joint destination (Its default is "home")
    def jointMove(self, jointData = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], debug = False ):
        msg = self.createMove("joint")
        msg.target.joints_data = jointData
        self.moveQueue.put_nowait(msg)
        self.processQueue()
        if debug:
            rospy.loginfo(msg)

    #This function moves the robot to a cartesian destination (Its default is "pick")
    def cartMove(self, x = 400.5, y = 0.05, z = 120, a = 0, e = 180, r = -1.37, gripper = 18, debug = False):
        msg = self.createMove("cart")
        msg.target.joints_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, gripper, 0.0, 0.0, 0.0]
        msg.target.cartesian_data.x = x
        msg.target.cartesian_data.y = y
        msg.target.cartesian_data.z = z
        msg.target.cartesian_data.a = a
        msg.target.cartesian_data.e = e
        msg.target.cartesian_data.r = r
        self.moveQueue.put_nowait(msg)
        self.processQueue()
        if debug:
            rospy.loginfo(msg)

    #Moves to a cartesian destination on the checkers board (z will be pick height or ground height)
    def moveToPick(self,x, y, z, gripper):
        if (x < 315 or x > 627):
            self.jointMove()
            print("Invalid Move")
            return False
        if (x >= 315 and x < 433):
            self.cartMove(x, y, z, 0, 180, -1.37, gripper, False)
        elif (x >= 433 and x < 512):
            self.cartMove(x, y, z, 0, 160, -1.37, gripper, False)
        else: 
            self.cartMove(x, y, z, 0, 130, -1.37, gripper,  False)
        return True

    #Changes gripper width (defaults to "closed")
    def setGripper(self, width = 0):
        rospy.sleep(0.2)
        self.joints[6] = width
        self.jointMove(self.joints, False)
   
    #Moves object at spot (x,y) to spot (x1,y1)
    def checkersMove(self, x, y, x1, y1):
        self.pickUpPiece(x,y)
        if ((x >= 315 and x < 433) and (x1 > 433 and x1 < 512)):
            self.changeSector(1,2)
        elif ((x >= 315 and x < 433) and (x1 >= 512 and x1 <= 627)):
            self.changeSector(1,3)
        elif ((x > 433 and x < 512) and (x1 >= 512 and x1 <= 627)):
            self.changeSector(2,3)
        elif ((x > 433 and x < 512) and (x1 >= 315 and x1 < 433)):
            self.changeSector(2,1)
        elif ((x >= 512 and x <= 627) and (x1 >= 315 and x1 < 433)):
            self.changeSector(3,1)
        elif ((x >= 512 and x <= 627) and (x1 > 433 and x1 < 512)):
            self.changeSector(3,2)
        self.dropOffPiece(x1,y1)

    #Transitions between E angle sectors
    def changeSector(self, s1, s2):
        if(s1== 1 and s2 == 2):
            self.cartMove(395.33, -209.78, self.pickHeight, 0, 180, -1.37, self.grabWidth, False)
            self.cartMove(395.33, -209.78, self.grabHeight, 0, 180, -1.37, self.grabWidth, False)
            self.cartMove(395.33, -209.78, self.grabHeight, 0, 180, -1.37, self.pickWidth, False)
            self.cartMove(395.33, -209.78, self.pickHeight, 0, 180, -1.37, self.pickWidth, False)
            self.cartMove(395.33, -209.78, self.pickHeight, 0, 160, -1.37, self.pickWidth, False)
            self.cartMove(395.33, -209.78, self.grabHeight, 0, 160, -1.37, self.pickWidth, False)
            self.cartMove(395.33, -209.78, self.grabHeight, 0, 160, -1.37, self.grabWidth, False)
            self.cartMove(395.33, -209.78, self.pickHeight, 0, 160, -1.37, self.grabWidth, False)
        if(s1 == 2 and s2 == 1):
            self.cartMove(395.33, -209.78, self.pickHeight, 0, 160, -1.37, self.grabWidth, False)
            self.cartMove(395.33, -209.78, self.grabHeight, 0, 160, -1.37, self.grabWidth, False)
            self.cartMove(395.33, -209.78, self.grabHeight, 0, 160, -1.37, self.pickWidth, False)
            self.cartMove(395.33, -209.78, self.pickHeight, 0, 160, -1.37, self.pickWidth, False)
            self.cartMove(395.33, -209.78, self.pickHeight, 0, 180, -1.37, self.pickWidth, False)
            self.cartMove(395.33, -209.78, self.grabHeight, 0, 180, -1.37, self.pickWidth, False)
            self.cartMove(395.33, -209.78, self.grabHeight, 0, 180, -1.37, self.grabWidth, False)
            self.cartMove(395.33, -209.78, self.pickHeight, 0, 180, -1.37, self.grabWidth, False)
        if(s1 == 2 and s2 == 3):
            self.cartMove(490.07, -222.78, self.pickHeight, 0, 160, -1.37, self.grabWidth, False)
            self.cartMove(490.07, -222.78, self.grabHeight, 0, 160, -1.37, self.grabWidth, False)
            self.cartMove(490.07, -222.78, self.grabHeight, 0, 160, -1.37, self.pickWidth, False)
            self.cartMove(490.07, -222.78, self.pickHeight, 0, 160, -1.37, self.pickWidth, False)
            self.cartMove(490.07, -222.78, self.pickHeight, 0, 140, -1.37, self.pickWidth, False)
            self.cartMove(490.07, -222.78, self.grabHeight, 0, 140, -1.37, self.pickWidth, False)
            self.cartMove(490.07, -222.78, self.grabHeight, 0, 140, -1.37, self.grabWidth, False)
            self.cartMove(490.07, -222.78, self.pickHeight, 0, 140, -1.37, self.grabWidth, False)
        if(s1 == 3 and s2 == 2):
            self.cartMove(490.07, -222.78, self.pickHeight, 0, 140, -1.37, self.grabWidth, False)
            self.cartMove(490.07, -222.78, self.grabHeight, 0, 140, -1.37, self.grabWidth, False)
            self.cartMove(490.07, -222.78, self.grabHeight, 0, 140, -1.37, self.pickWidth, False)
            self.cartMove(490.07, -222.78, self.pickHeight, 0, 140, -1.37, self.pickWidth, False)
            self.cartMove(490.07, -222.78, self.pickHeight, 0, 160, -1.37, self.pickWidth, False)
            self.cartMove(490.07, -222.78, self.grabHeight, 0, 160, -1.37, self.pickWidth, False)
            self.cartMove(490.07, -222.78, self.grabHeight, 0, 160, -1.37, self.grabWidth, False)
            self.cartMove(490.07, -222.78, self.pickHeight, 0, 160, -1.37, self.grabWidth, False)
        if(s1 == 1 and s2 == 3):
            self.changeSector(1,2)
            self.changeSector(2,3)
        if(s1 == 3 and s2 == 1):
            self.changeSector(3,2)
            self.changeSector(2,1)


    #Removes piece from play
    def removePiece(self, x, y):
        self.jointMove()
        self.moveToPick(x,y,self.pickHeight,self.pickWidth)
        self.moveToPick(x,y,self.grabHeight,self.pickWidth)
        self.moveToPick(x,y,self.grabHeight,self.grabWidth)
        self.moveToPick(x,y,self.pickHeight,self.grabWidth)
        self.jointMove([-178.90, 37.66, 58.04, 0.00, 84.26, -1.36,self.grabWidth,0,0,0],False)
        self.jointMove([-178.90, 37.66, 58.04, 0.00, 84.26, -1.36,self.pickWidth, 0,0,0], False) 
        self.jointMove()

#Main function    
def main(args):
    rospy.init_node("sp_demo1", anonymous = True)
    man = Manipulation()
    man.dance()

if __name__ == '__main__':
    main(sys.argv)

