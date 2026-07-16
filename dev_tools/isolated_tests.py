
class MyFirstClass:
  def __init__(self):
    self.a = 0

  def counting_function(self):
     self.a += 1

class1 = MyFirstClass()

for i in range(10000000):
  class1.counting_function()
  print(class1.a)