from TaquinGame import State
from Qlearning import Qlearning


qlearning = Qlearning()

qlearning.learn_q(2000)
qlearning.run()
