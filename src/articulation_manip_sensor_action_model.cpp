#include "particle_filter/articulation_manip_sensor_action_model.h"
#include "particle_filter/prismatic_model.h"
#include "particle_filter/rotational_model.h"
#include "particle_filter/random.h"


template <class StateType, class ZType, class AType> ArtManipSensorActionModel<StateType, ZType, AType>::ArtManipSensorActionModel():
  scale(1.0)
{
}

template <class StateType, class ZType, class AType> ArtManipSensorActionModel<StateType, ZType, AType>::~ArtManipSensorActionModel()
{
}


template <class StateType, class ZType, class AType> ZType ArtManipSensorActionModel<StateType, ZType, AType>::sense(const StateType &state, const Eigen::VectorXd &noise) const
{
}

template <class StateType, class ZType, class AType> double ArtManipSensorActionModel<StateType, ZType, AType>::senseLikelihood(const ZType &z, const AType& a,
                                                                                                                                const StateType &state,
                                                                                                                                const Eigen::MatrixXd &cov) const
{
}

template <class StateType, class ZType, class AType> double ArtManipSensorActionModel<StateType, ZType, AType>::senseLogLikelihood(const ZType &z, const AType& a,
                                                                                                                                const StateType &state,
                                                                                                                                const Eigen::MatrixXd &cov) const
{
}


template <> double ArtManipSensorActionModel<ArticulationModelPtr, int, ActionPtr>::senseLikelihood(const int &z,
                                                                                                   const ActionPtr& a,
                                                                                                   const ArticulationModelPtr &state,
                                                                                                   const Eigen::MatrixXd &cov) const
{
  return 0.0;
}
// z = 1 means it doesnt stop
//TODO: check angle comparisons
template <> double ArtManipSensorActionModel<ArticulationModelPtr, int, ActionPtr>::senseLogLikelihood(const int &z,
                                                                                                      const ActionPtr& a,
                                                                                                      const ArticulationModelPtr &state,
                                                                                                      const Eigen::MatrixXd &cov) const
{
  double loglikelihood = 0;

  switch (state->model)
  {
    case (RIGID):
      {
        if (z == 1)
        {
          loglikelihood = -std::numeric_limits<double>::lowest();
        }
        else
        {
          //TODO: how to increase likelihood here?
        }
      }

    case (PRISMATIC):
      {
        // calculate the relative angle between prismatic axis
        boost::shared_ptr<PrismaticModel> prismatic_model = boost::dynamic_pointer_cast< PrismaticModel > (state);

        tf::Vector3 model_dir = prismatic_model->prismatic_dir;
        tf::Vector3 action_dir = a->action_direction;
        model_dir.normalize();
        action_dir.normalize();
        double angle_rad = model_dir.angle(action_dir);
        //TODO: normalize the angle?
        angle_rad = fabs(angle_rad);
        double prob = exp(-scale*angle_rad);
        if (z == 1)
        {
          loglikelihood = log(prob);
        }
        else
        {
          loglikelihood = log(1-prob);
        }
      }
    case (ROTATIONAL):
      {
        // calculate the relative angle between tangents
        boost::shared_ptr<RotationalModel> rotational_model = boost::dynamic_pointer_cast< RotationalModel > (state);

        //get current pose_obs
        geometry_msgs::Pose pose_obs, pose_proj;
        tf::Quaternion quad_obs;
        tf::Vector3 pos_obs;
        state->getParam("current_pose_trans", pos_obs);
        state->getParam("current_pose_quat", quad_obs);
        tf::Transform tf_pose_obs(quad_obs, pos_obs);
        tf::poseTFToMsg(tf_pose_obs, pose_obs);

        //project current pose_obs
        V_Configuration q;
        state->getCurrentPoseProjected(pose_obs, pose_proj, q);
        tf::Transform tf_pose_proj;
        tf::poseMsgToTF(pose_proj,tf_pose_proj);

        //get the tangent vector
        tf::Matrix3x3 rot_axis_m(rotational_model->rot_axis);
        tf::Vector3 rot_axis_z = rot_axis_m.getColumn(2);
        tf::Vector3 radius = tf_pose_proj.getOrigin() - rotational_model->rot_center;
        tf::Vector3 rot_proj_dir = radius.cross(rot_axis_z);
        tf::Vector3 action_dir = a->action_direction;

        rot_proj_dir.normalize();
        action_dir.normalize();
        double angle_rad = rot_proj_dir.angle(action_dir);
        //TODO: normalize the angle?
        angle_rad = fabs(angle_rad);
        double prob = exp(-scale*angle_rad);
        if (z == 1)
        {
          loglikelihood = log(prob);
        }
        else
        {
          loglikelihood = log(1-prob);
        }
      }

  }



  return loglikelihood;
}



template class ArtManipSensorActionModel<ArticulationModelPtr, articulation_model_msgs::TrackMsg, ActionPtr>;
template class ArtManipSensorActionModel<ArticulationModelPtr, int, ActionPtr>;

