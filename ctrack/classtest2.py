from classtest import Person

class Employee(Person):
  def __init__(self, name, age, company):
    print '[Employee.__init__]'
    Person.__init__(self, name, age)
    self.company  = company
  def showinfo(self):
    print '[Employee.showinfo]'
    print '%s (%d) %s' %(self.name, self.age, self.company)
