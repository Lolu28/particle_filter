#!/usr/bin/env python

"""
usage: %(progname)s [--obs] [--tracks]
This node visualizes track messages.
"""


import rospy
import sys
from articulation_model_msgs.msg import ModelMsg
from visualization_msgs.msg import Marker,MarkerArray
from geometry_msgs.msg import Vector3, Point, Quaternion, Pose
from std_msgs.msg import ColorRGBA
from sensor_msgs.msg import ChannelFloat32
import logging
import getopt
import colorsys

class trackVisualizer:

  def __init__(self, colorize_track, colorize_obs):
	  self.pub = rospy.Publisher('visualization_marker', Marker)
	  self.pub_array = rospy.Publisher('visualization_marker_array', MarkerArray)
	  self.colorize_track = colorize_track
	  self.colorize_obs = colorize_obs
	  rospy.Subscriber("model_track", ModelMsg, self.callback)
	  self.num_poses = {}
	  self.num_markers = {}
	  self.old_num_markers = {}

  def callback(self,model):
    rospy.loginfo( "received track %d, containing %d poses",model.track.id,len(model.track.pose) )
    marker_array = MarkerArray()

    if model.track.id in self.num_markers:
      self.old_num_markers[model.track.id] = self.num_markers[model.track.id]
    else:
      self.old_num_markers[model.track.id] = 0
      self.num_markers[model.track.id] = 0
      self.num_poses[model.track.id] = len(model.track.pose)

    #channel_w = None
    #channel_h = None
    #for channel in track.channels:
    #if channel.name == 'width':
    #channel_w = channel
    #elif channel.name == 'height':
    #channel_h = channel


    marker_array = MarkerArray()
    self.render_points(model.track,marker_array)
    
    self.render_model(model, marker_array)

    #self.delete_old_markers(model.track,marker_array)	

    rospy.loginfo( "publishing MarkerArray, containing %d markers",
    len(marker_array.markers) )
    self.pub_array.publish(marker_array)

  def render_model(self, model, marker_array):
    
    if model.name == "rotational":
        self.render_rotational_model(model, marker_array)
    if model.name == "prismatic":
        self.render_prismatic_model(model, marker_array)
    if model.name == "rigid"
        self.render_rigid_model(model, marker_array)


  def render_rigid_model(self, model, marker_array):
    rigid_position_x = 0
    rigid_position_y = 0
    rigid_position_z = 0
    rigid_orientation_x = 0
    rigid_orientation_y = 0
    rigid_orientation_z = 0
    rigid_orientation_w = 0
    
    for param in model.params:
      if param.name == "rigid_position.x":
        rigid_position_x = param.value
      if param.name == "rigid_position.y":
        rigid_position_y = param.value
      if param.name == "rigid_position.z":
        rigid_position_z = param.value

      if param.name == "rigid_orientation.x":
        rigid_orientation_x = param.value
      if param.name == "rigid_orientation.y":
        rigid_orientation_y = param.value
      if param.name == "rigid_orientation.z":
        rigid_orientation_z = param.value
      if param.name == "rigid_orientation.w":
        rigid_orientation_w = param.value

      rigid_pose_orientation = Quaternion(rigid_orientation_x, rigid_orientation_y, rigid_orientation_z, rigid_orientation_w)  
      identity_pose_orientation = Quaternion(0, 0, 0, 1)                  
      rigid_pose_position = Point(rigid_position_x, rigid_position_y, rigid_position_z)
      rigid_pose = Pose(rigid_pose_position, identity_pose_orientation)


  def render_prismatic_model(self, model, marker_array):
    rigid_position_x = 0
    rigid_position_y = 0
    rigid_position_z = 0
    rigid_orientation_x = 0
    rigid_orientation_y = 0
    rigid_orientation_z = 0
    rigid_orientation_w = 0
    prismatic_dir_x = 0
    prismatic_dir_y = 0
    prismatic_dir_z = 0
    for param in model.params:
      if param.name == "rigid_position.x":
        rigid_position_x = param.value
      if param.name == "rigid_position.y":
        rigid_position_y = param.value
      if param.name == "rigid_position.z":
        rigid_position_z = param.value

      if param.name == "rigid_orientation.x":
        rigid_orientation_x = param.value
      if param.name == "rigid_orientation.y":
        rigid_orientation_y = param.value
      if param.name == "rigid_orientation.z":
        rigid_orientation_z = param.value
      if param.name == "rigid_orientation.w":
        rigid_orientation_w = param.value

      if param.name == "prismatic_dir.x":
        prismatic_dir_x = param.value
      if param.name == "prismatic_dir.y":
        prismatic_dir_y = param.value
      if param.name == "prismatic_dir.z":
        prismatic_dir_z = param.value

      rigid_pose_orientation = Quaternion(rigid_orientation_x, rigid_orientation_y, rigid_orientation_z, rigid_orientation_w)  
      identity_pose_orientation = Quaternion(0, 0, 0, 1)                  
      rigid_pose_position = Point(rigid_position_x, rigid_position_y, rigid_position_z)
      rigid_pose = Pose(rigid_pose_position, identity_pose_orientation)
      prismatic_dir = Point(prismatic_dir_x, prismatic_dir_y, prismatic_dir_z)

    marker = Marker()
    marker.header.stamp = model.track.header.stamp
    marker.header.frame_id = model.track.header.frame_id
    marker.ns = "model_visualizer"
    marker.id = 0#self.num_markers[model.track.id]
    marker.action = Marker.ADD

    marker.scale = Vector3(0.01,0.01,0.01)
    marker.color.a = 1
    marker.color.b = 1

    marker.type = Marker.LINE_STRIP
    marker.pose = rigid_pose
    for axis in range(3):
      marker.points.append( Point(0,0,0) )
      marker.colors.append( ColorRGBA(0,0,0,0) )
      if axis==0:
        marker.points.append( Point(0.3,0,0) )
        marker.colors.append( ColorRGBA(1,0,0,1) )
      elif axis==1:
        marker.points.append( Point(0,0.3,0) )
        marker.colors.append( ColorRGBA(0,1,0,1) )
      elif axis==2:
        marker.points.append( Point(0,0,0.3) )
        marker.colors.append( ColorRGBA(0,0,1,1) )

    marker_array.markers.append(marker)

    #direction
    marker_dir = Marker()
    marker_dir.header.stamp = model.track.header.stamp
    marker_dir.header.frame_id = model.track.header.frame_id
    marker_dir.ns = "model_visualizer_dir"
    marker_dir.id = 0#self.num_markers[model.track.id]
    marker_dir.action = Marker.ADD

    marker_dir.scale = Vector3(0.01,0.01,0.01)
    marker_dir.color.a = 1
    marker_dir.color.r = 1

    marker_dir.type = Marker.LINE_STRIP
    marker_dir.pose = rigid_pose
    marker_dir.points.append( Point(0,0,0) )
    marker_dir.points.append( prismatic_dir )
    
    marker_array.markers.append(marker_dir)

    #marker orientation
    marker_orient = Marker()
    marker_orient.header.stamp = model.track.header.stamp
    marker_orient.header.frame_id = model.track.header.frame_id
    marker_orient.ns = "model_visualizer_orientation"
    marker_orient.id = 0#self.num_markers[model.track.id]
    marker_orient.action = Marker.ADD

    marker_orient.scale = Vector3(0.01,0.01,0.01)
    marker_orient.color.a = 1
    marker_orient.color.b = 1

    marker_orient.type = Marker.LINE_STRIP
    marker_pose = Pose( Point(rigid_pose_position.x + prismatic_dir.x, rigid_pose_position.y + prismatic_dir.y, rigid_pose_position.z + prismatic_dir.z), rigid_pose_orientation)

    marker_orient.pose = marker_pose
    for axis in range(3):
      marker_orient.points.append( Point(0,0,0) )
      marker_orient.colors.append( ColorRGBA(0,0,0,0) )
      if axis==0:
        marker_orient.points.append( Point(0.3,0,0) )
        marker_orient.colors.append( ColorRGBA(1,0,0,1) )
      elif axis==1:
        marker_orient.points.append( Point(0,0.3,0) )
        marker_orient.colors.append( ColorRGBA(0,1,0,1) )
      elif axis==2:
        marker_orient.points.append( Point(0,0,0.3) )
        marker_orient.colors.append( ColorRGBA(0,0,1,1) )
    
    marker_array.markers.append(marker_orient)


  def render_rotational_model(self, model, marker_array):
    rot_radius = 0
    rot_center_x = 0
    rot_center_y = 0
    rot_center_z = 0
    rot_orientation_x = 0
    rot_orientation_y = 0
    rot_orientation_z = 0
    rot_orientation_w = 0
    rot_axis_x = 0
    rot_axis_y = 0
    rot_axis_z = 0
    rot_axis_w = 0

    for param in model.params:
      if param.name == "rot_radius":
        rot_radius = param.value
      if param.name == "rot_center.x":
        rot_center_x = param.value
      if param.name == "rot_center.y":
        rot_center_y = param.value
      if param.name == "rot_center.z":
        rot_center_z = param.value

      if param.name == "rot_orientation.x":
        rot_orientation_x = param.value
      if param.name == "rot_orientation.y":
        rot_orientation_y = param.value
      if param.name == "rot_orientation.z":
        rot_orientation_z = param.value
      if param.name == "rot_orientation.w":
        rot_orientation_w = param.value

      if param.name == "rot_axis.x":
        rot_axis_x = param.value
      if param.name == "rot_axis.y":
        rot_axis_y = param.value
      if param.name == "rot_axis.z":
        rot_axis_z = param.value
      if param.name == "rot_axis.w":
        rot_axis_w = param.value

      rot_axis = Quaternion(rot_axis_x, rot_axis_y, rot_axis_z, rot_axis_w) 
      rot_center_position = Point(rot_center_x, rot_center_y, rot_center_z)
      rot_center_orientation = Quaternion(rot_orientation_x, rot_orientation_y, rot_orientation_z, rot_orientation_w)          
      rot_center = Pose(rot_center_position, rot_axis)#rot_center_orientation)
        
    marker = Marker()
    marker.header.stamp = model.track.header.stamp
    marker.header.frame_id = model.track.header.frame_id
    marker.ns = "model_visualizer"
    marker.id = 0#self.num_markers[model.track.id]
    marker.action = Marker.ADD

    marker.scale = Vector3(0.01,0.01,0.01)
    #marker.color = self.generate_color_axis(track.id, i,axis)
    marker.color.a = 1
    marker.color.b = 1

    marker.type = Marker.LINE_STRIP
    marker.pose = rot_center

        
    for axis in range(3):
      marker.points.append( Point(0,0,0) )
      if axis==0:
        marker.points.append( Point(0.3,0,0) )
      elif axis==1:
        marker.points.append( Point(0,0.3,0) )
      elif axis==2:
        marker.points.append( Point(0,0,0.3) )

    marker_array.markers.append(marker)

    #adding radius
    marker_radius = Marker()
    marker_radius.header.stamp = model.track.header.stamp
    marker_radius.header.frame_id = model.track.header.frame_id
    marker_radius.ns = "model_visualizer_radius"
    marker_radius.id = 0#self.num_markers[model.track.id]
    marker_radius.action = Marker.ADD

    marker_radius.scale = Vector3(0.01,0.01,0.01)
    marker_radius.color.a = 1
    marker_radius.color.r = 1

    marker_radius.type = Marker.LINE_STRIP
    marker_radius.pose = rot_center
    marker_radius.points.append( Point(0,0,0) )
    marker_radius.points.append( Point(rot_radius,0,0) )
    
    marker_array.markers.append(marker_radius)
      

  def render_points(self, track, marker_array):
    for i in range( len( track.pose ) ):
      marker = Marker()
      marker.header.stamp = track.header.stamp
      marker.header.frame_id = track.header.frame_id
      marker.ns = "track_visualizer-%d"%(track.id)
      marker.id = self.num_markers[track.id]
      marker.action = marker.ADD
      marker.lifetime = rospy.Duration.from_sec(1)

      marker.scale = Vector3(0.003,0.003,0.003)
      marker.color.g = 1
      marker.color.a = 1
      #marker.color = self.generate_color_rectangle(track.id, i)

      marker.type = Marker.SPHERE_LIST
      marker.pose = track.pose[i]
    
      marker.points.append( Point(0,0,0) )

      marker_array.markers.append(marker)
      self.num_markers[track.id] += 1

  def delete_old_markers(self,track,marker_array):
    i = self.num_markers[track.id]
    while i < self.old_num_markers[track.id]:
      marker = Marker()
      marker.header.stamp = track.header.stamp
      marker.header.frame_id = track.header.frame_id
      marker.ns = "track_visualizer-%d"%(track.id)
      marker.id = i
      marker.action = Marker.DELETE
      marker_array.markers.append(marker)
      i += 1



def main():
  colorize_track = False 
  colorize_obs = False
  try:
    rospy.init_node('track_visualizer')
    trackVisualizer(colorize_track,colorize_obs)
    rospy.spin()
  except rospy.ROSInterruptException: pass
      
if __name__ == '__main__':
  main()

