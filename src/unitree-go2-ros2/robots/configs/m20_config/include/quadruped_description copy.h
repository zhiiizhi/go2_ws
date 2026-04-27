#ifndef QUADRUPED_DESCRIPTION_H
#define QUADRUPED_DESCRIPTION_H

#include <quadruped_base/quadruped_base.h>

namespace champ
{
    namespace URDF
    {
        void loadFromHeader(champ::QuadrupedBase &base)
        {
            // M20 山猫运动学参数
            // 前后腿对称设计（从侧面看是 >< 形状）
            // 
            // 前腿：knee 向后弯曲（相对于前进方向）
            //   lower_leg.setOrigin(0, 0.0984, -0.25)  // X=0，纯垂直
            //
            // 后腿：knee 向前弯曲（相对于前进方向）
            //   lower_leg.setOrigin(-0.15, 0.0984, -0.25)  // X=-0.15，向前偏移
            //
            // 左右腿 Y 偏移 0.0685（原始安装位置）
            // 腿交叉问题需要通过髋关节零位角度补偿来解决

            // 左前腿
            base.lf.hip.setOrigin(0.3141, 0.0685, 0, 0, 0, 0);
            base.lf.upper_leg.setOrigin(0, 0, 0, 0, 0, 0);
            base.lf.lower_leg.setOrigin(0, 0.0984, -0.25, 0, 0, 0);
            base.lf.foot.setOrigin(0, 0.059676, -0.25, 0, 0, 0);

            // 右前腿
            base.rf.hip.setOrigin(0.3141, -0.0685, 0, 0, 0, 0);
            base.rf.upper_leg.setOrigin(0, 0, 0, 0, 0, 0);
            base.rf.lower_leg.setOrigin(0, -0.0984, -0.25, 0, 0, 0);
            base.rf.foot.setOrigin(0, -0.059676, -0.25, 0, 0, 0);

            // 左后腿（knee 向前弯曲，X 为负）
            base.lh.hip.setOrigin(-0.3141, 0.0685, 0, 0, 0, 0);
            base.lh.upper_leg.setOrigin(0, 0, 0, 0, 0, 0);
            base.lh.lower_leg.setOrigin(-0.15, 0.0984, -0.25, 0, 0, 0);
            base.lh.foot.setOrigin(-0.15, 0.059676, -0.25, 0, 0, 0);

            // 右后腿（knee 向前弯曲，X 为负）
            base.rh.hip.setOrigin(-0.3141, -0.0685, 0, 0, 0, 0);
            base.rh.upper_leg.setOrigin(0, 0, 0, 0, 0, 0);
            base.rh.lower_leg.setOrigin(-0.15, -0.0984, -0.25, 0, 0, 0);
            base.rh.foot.setOrigin(-0.15, -0.059676, -0.25, 0, 0, 0);
        }
    }
}
#endif
