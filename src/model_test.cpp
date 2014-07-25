/*
 * model_fitting_demo.cpp
 *
 *  Created on: Jun 8, 2010
 *      Author: sturm
 */

#include <ros/ros.h>

//#include "articulation_models/models/factory.h"

#include "articulation_model_msgs/ModelMsg.h"
#include "articulation_model_msgs/TrackMsg.h"
#include "articulation_model_msgs/ParamMsg.h"
#include "particle_filter/articulation_model.h"
#include "particle_filter/rotational_model.h"
#include "particle_filter/rigid_model.h"


#include <boost/random.hpp>
#include <boost/random/normal_distribution.hpp>

int main(int argc, char** argv)
{
  ros::init(argc, argv, "model_fitting");
  ros::NodeHandle n;
  ros::Rate loop_rate(5);
  int count = 0;

  boost::normal_distribution<> nd(0.0, 0.02);
  boost::mt19937 rng;
  boost::variate_generator<boost::mt19937&, boost::normal_distribution<> >
                  var_nor(rng, nd);

//  MultiModelFactory factory;

  while (ros::ok())
  {
    articulation_model_msgs::ModelMsg model_msg;
//    model_msg.name = "rotational";
    articulation_model_msgs::ParamMsg sigma_param;
    sigma_param.name = "sigma_position";
    sigma_param.value = 0.02;
    sigma_param.type = articulation_model_msgs::ParamMsg::PRIOR;
    model_msg.params.push_back(sigma_param);

    model_msg.track.header.stamp = ros::Time();
    model_msg.track.header.frame_id = "/";
//    model_msg.track.track_type = articulation_model_msgs::TrackMsg::TRACK_POSITION_ONLY;

    for (int i = 0; i < 100; i++)
    {
      geometry_msgs::Pose pose;
      pose.position.x = /*cos(i / 100.0 + count / 10.0)+*/5 + var_nor();
      pose.position.y = /*sin(i / 100.0 + count / 10.0)+*/8 + var_nor();
      pose.position.z = var_nor();
      pose.orientation.x = 0;
      pose.orientation.y = 0;
      pose.orientation.z = 0;
      pose.orientation.w = 1;
      model_msg.track.pose.push_back(pose);
    }

    std::cout << "creating object" << std::endl;
    ArticulationModelPtr model_instance(new RigidModel);//factory.restoreModel(model_msg);
    model_instance->setModel(model_msg);

    std::cout << "fitting" << std::endl;
    model_instance->fitModel();

    std::cout << "evaluating" << std::endl;
    model_instance->evaluateModel();
    std::cout << "done" << std::endl;


//    std::cout << "model class = "<< model_instance->getModelName() << std::endl;
//    std::cout << "       radius = "<<model_instance->getParam("rot_radius")<< std::endl;

//    boost::shared_ptr<RotationalModel> rotational = boost::dynamic_pointer_cast< RotationalModel > (model_instance);
//    std::cout << "    rotational   radius = "<<rotational->rot_radius<< std::endl;

    std::cout << "       rigid_position.x = "<<model_instance->getParam("rigid_position.x")<< std::endl;
    boost::shared_ptr<RigidModel> rigid = boost::dynamic_pointer_cast< RigidModel > (model_instance);
    std::cout << "     pos.x = " << rigid->pos_x << std::endl;



    std::cout << "       center.x = "<<model_instance->getParam("rot_center.x")<< std::endl;
    std::cout << "       center.y = "<<model_instance->getParam("rot_center.y")<< std::endl;
    std::cout << "       center.z = "<<model_instance->getParam("rot_center.z")<< std::endl;
    std::cout << "       log LH = " << model_instance->getParam("loglikelihood") << std::endl; //TODO: change back to getLikelihood
    std::cout << " points= "<<model_msg.track.pose.size()<< std::endl;

//    ModelMsg fitted_model_msg = model_instance->getModel();

    ros::spinOnce();
    loop_rate.sleep();
    ++count;
  }
}