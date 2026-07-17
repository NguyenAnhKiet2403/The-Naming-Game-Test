from variants.BaselineNG import *
#according to the paper document (The Naming Game)
#remove procedure could be moved into its own class (if desired)
class Imitation(BaselineNG):
  #Code for removing a topic from Agent memory
  def removeTopic(self, topic, agent):
    for pairName, pairTopic in self.memory[agent]:
      #if name of pair corresponds with the adopted name
      if pairTopic == topic:
        #remove pair from memory and circulation
        self.remove(pairName, topic, agent)

  def adopt(self, name, topic, listener, speaker):
    #remove all previous bindings of the topic
    self.removeTopic(topic, listener)
    # if successful, run super
    super().adopt(name, topic, listener, speaker)

#according to Guy Nagels, only success should clear memory
class Imitationv2(BaselineNG):
  #Code for removing a topic from Agent memory, preserving the original binding
  def removeTopic(self, topic, agent, name):
    for pairName, pairTopic in self.memory[agent]:
      #if name of pair corresponds with the adopted name
      if pairTopic == topic and name != pairName:
        # remove pair from memory and circulation
        self.remove(pairName, topic, agent)
  #same code but only performs clear on success
  def success(self, speaker, listener, topic, name):
    if super().broadcast:
      #remove all previous bindings of the topic from both speaker and listener memory
      self.removeTopic(topic, listener, name)
      #invoke super
      super().success(speaker, listener, topic, name)
    else:
      #remove all previous bindings of the topic from both speaker and listener memory
      self.removeTopic(topic, speaker, name)
      self.removeTopic(topic, listener, name)
      #invoke super
      super().success(speaker, listener, topic, name)
  def speaker_success(self, speaker, topic, name):
      self.removeTopic(topic, speaker, name)
