from NamingGame import *
import random
class BaselineNG(NamingGame):
  def generateContext(self):
    context = []
    #start with 1 as 0 fails the if test
    for i in range(1, 2):
      context.append(i)
    return context

  def invent(self, topic, agent):
    #perform invent of the parent
    super().invent(topic, agent)
    #generate name
    name = self.generateName()
    self.display(f"Agent {agent} has invented the name {name} for topic {topic}")
    #update agent memory
    self.adopt(name, topic, agent, agent)
    return name

  #procedure for generating names
  def generateName(self):
    name = ''
    # generate random string as name
    for _ in range(7):
      # Considering only upper and lowercase letters
      random_integer = random.randint(97, 97 + 26 - 1)
      flip_bit = random.randint(0, 1)
      # Convert to lowercase if the flip bit is on
      random_integer = random_integer - 32 if flip_bit == 1 else random_integer
      # Keep appending random characters using chr(x)
      name += (chr(random_integer))
    return name


  #just pick a random object/topic
  def pick(self, agent, context):
    #pick a random object from context
    index = random.randint(0, len(context) - 1)
    return context[index]

  #generates a name for object
  def produce(self, object, agent):
    #possible name matches for the object
    results = []
    #get memory and iterate through the vocabulary
    for name, topic in self.memory[agent]:
      if topic == object:
        results.append(name)
    #if we have found a result, pick a random name from our possible names
    if results:
      index = random.randint(0, len(results) - 1)
      return results[index]
    #else invent a new name and give this new name in return
    return self.invent(object, agent)

  #
  def interpret(self, name, agent):
    #get agent memory and iterate through vocabulary
    for vocName, topic in self.memory[agent]:
      if vocName == name:
        return topic
    #if we have not encountered this name, return None
    return None

  def adopt(self, name, topic, listener, speaker):
    #store connection in agent memory
    self.memory[listener].append((name, topic))
    #if succesfull, run super
    super().adopt(name, topic, listener, speaker)

  def remove(self, name, topic, agent):
    #remove connection from memory
    self.memory[agent].remove((name, topic))
    #if succesfull, run super
    super().remove(name, topic, agent)

  def success(self, speaker, listener, topic, name):
    #invoke super
    super().success(speaker, listener, topic, name)
    #in case of success, do not update anyone's library

  def failure(self, speaker, listener, intendedTopic, perceivedTopic, name):
    #invoke super
    super().failure(speaker, listener, intendedTopic, perceivedTopic, name)
    #in case of failure, update listener with the intendedTopic
    self.memory[listener].append((name, intendedTopic))
    #remove perceived topic
    self.memory[listener].remove((name, perceivedTopic))

  def speaker_success(self, speaker, topic, name):
      pass


