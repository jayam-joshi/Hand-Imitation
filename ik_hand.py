import pybullet as p
import pybullet_data
import time
import numpy as np

pc = p.connect(p.GUI)

p.setAdditionalSearchPath(pybullet_data.getDataPath())

plane = p.loadURDF('plane.urdf')

hand1= p.loadURDF('hand_model.urdf',[4,0,3.2],[ 0.706825181105366,0.0,0.0, 0.7073882691671998])
hand2= p.loadURDF('hand_model.urdf',[-4,0,3.2],[0.706825181105366,0.0,0.0, 0.7073882691671998])

csnt1 = p.createConstraint(plane,-1,hand1, -1, p.JOINT_FIXED, [0,1,0], [4,0,0],[0,3.2,0])
csnt2 = p.createConstraint(plane,-1,hand2, -1, p.JOINT_FIXED, [0,1,0], [-4,0,0],[0,3.2,0])

print(p.getBasePositionAndOrientation(hand1))


#p.setGravity(0,0,-10)

_link_name_to_index = {p.getBodyInfo(hand1)[0].decode('UTF-8'):-1,}
        
for _id in range(p.getNumJoints(hand1)):
	_name = p.getJointInfo(hand1, _id)[12].decode('UTF-8')
	_link_name_to_index[_name] = _id

print(_link_name_to_index)

for i in range(p.getNumJoints(hand1)):
  print(p.getJointInfo(hand1,i))
  



linkIdx=[3,7,11,15,19]  #indices of the dummy spheres

jointIdx=[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18]                #joint indices except fixed joints

angles=[0.314,1.5,1.5,0,1.5,1.5,0,1.5,1.5,0,1.5,1.5,0,1.5,1.5] #initial angles for fwd kinematics of hand1


print(p.getEulerFromQuaternion([0,0,0,1]))



while(1):
  
  p.setJointMotorControlArray(bodyIndex=hand1,               #fwd kinematics to set hand1 in an orientation
                                     jointIndices=jointIdx,
                                     controlMode=p.POSITION_CONTROL,
                                     targetPositions=angles,
                                     forces=[100, 100,100,100,100,100,100,100,100,100,100,100,100,100,100])
  
  
  w, h = 3, 5;
  targetPoses = [[0 for x in range(w)] for y in range(h)]  
                               
  x=3
  i=0
  while(x<=19):
    targetPoses[i] = np.array(p.getLinkState(hand1,x)[0]) #obtaining positions of dummy spheres in the orientation
    x+=4
    i+=1
    
  tpos=list(targetPoses)  
    
  for i in range(5):
    tpos[i][0]-=8  
    
  
    
      
       # Inv kinematics of hand 2 using targetpositions obtained
  jointPoses=p.calculateInverseKinematics2(hand2,linkIdx,tpos)
  
  p.setJointMotorControlArray(bodyIndex=hand2,            
                                    jointIndices=jointIdx,
                                    controlMode=p.POSITION_CONTROL,
                                    targetPositions=jointPoses,
                                    forces=[10 for i in jointIdx])
  
  
  
  p.stepSimulation()
  time.sleep(0.001)

