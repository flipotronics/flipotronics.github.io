
from enum import Enum
import mysql.connector

def connectDb():
  return mysql.connector.connect(user='flipotronics', password='flipotronics',host='10.0.0.183',database='flipotronics')

class Paramtype(Enum):
  DOUBLE = 0
  PAN = 1
  INT = 2
  HZ = 3
  MIDINOTE = 4
  MIDIVAL = 5


class Company:
  # INSERT INTO `flipotronics`.`company` (`uid`, `name`, `url`) VALUES ('0', 'Flipotronics', 'http://flipotronics.com');
  SELECT = "SELECT `company`.`id`,`company`.`uid`,`company`.`name`,`company`.`url` FROM `flipotronics`.`company`";

  id = 0
  uid = 0
  name = ""
  url = ""
    
  def __init__(self):
    print("init")
    
  def select(self, uid):
    sql = self.SELECT + "WHERE uid = " + str(uid)
    
class Param:
  SELECT = """SELECT `param`.`id`,
    `param`.`uid`,
    `param`.`patchtId`,
    `param`.`name`,
    `param`.`shortname`,
    `param`.`val`,
    `param`.`min`,
    `param`.`max`,
    `param`.`type`,
    `param`.`step`,
    `param`.`curve`,
    `param`.`undoval`,
    `param`.`defaultval`,
    `param`.`controller`,
    `param`.`automation`
	FROM `flipotronics`.`param` WHERE patchtId="""


  INSERT = """INSERT INTO `flipotronics`.`param`
	(`id`,
	`uid`,
	`patchtId`,
	`name`,
	`shortname`,
	`val`,
	`min`,
	`max`,
	`type`,
	`step`,
	`curve`,
	`param.undoval`,
	`param.defaultval`,
	`controller`,
	`automation`)
	VALUES
	({id},
	{uid},
	{patchtId},
	{name},
	{shortname},
	{val},
	{min},
	{max},
	{type},
	{step},
	{curve},
	{undo},
	{default},
	{controller},
	{automation:});"""

  UPDATE = """UPDATE `flipotronics`.`param` SET uid=%s,patchtId=%s,name=%s,shortname= %s,val=%s,min=%s,max=%s,type=%s,step=%s,curve=%s,undoval=%s,defaultval=%s,controller=%s,automation=%s WHERE id= %s;"""

  id = 0
  uid = 0
  patchId = 0
  name = ""
  shortname = ""
  val = 0.0
  min = 0.0
  max = 1.0
  type = 0
  step = 0.01
  curve = 0
  undo = 0.0
  default = 0.0
  controller = 0
  automation = 1

  def select(self, patchId):
  	sql = self.SELECT + str(patchId)
  	cnx = connectDb()
  	cursor = cnx.cursor()
  	cursor.execute(sql)
  	params = []
  	for (id,uid,patchId,name,shortname,val,min,max,type,step,curve,undo,default,controller,automation) in cursor:
  	  print("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}").format( id, uid, patchId, name, shortname, val, min, max, type, step, curve,undo, default, controller, automation)
  	  p = Param()
  	  p.id = int(id)
  	  p.uid = int(uid)
  	  p.patchId = int(patchId)
  	  p.name = name
  	  p.shortname = shortname
  	  p.val = float(val)
  	  p.min = float(min)
  	  p.max = float(max)
  	  p.type = type
  	  p.step = float(step)
  	  p.curve = int(curve)
  	  p.undo = float(undo)
  	  p.default = float(default)
  	  p.controller = controller
  	  p.automation = automation
  	  params.append(p)
  	cursor.close()
  	cnx.close()
  	return params

  def insert(self, param):
  	print(self.name)
  	print(self.vol)
  	print(self.patchId)

  def update(self, param):
  	cnx = connectDb()
  	cursor = cnx.cursor()
  	sql = self.UPDATE
  	print(param.id)
  	input = (param.uid, param.patchId, param.name, param.shortname,param.val,param.min,param.max,param.type,param.step,param.curve,param.undo,param.default,
  		param.controller,param.automation,param.id)

  	cursor.execute(sql, input)
  	cnx.commit()
  	cursor.close()
  	cnx.close()

class Patch:

  id = 0
  uid = 0
  bankId = 0
  categoryId = 0
  name = ""
  paramcount = 0


  def loadPatch(self, patchId ):

  	


if __name__ == '__main__':
  entity = Param()
  params = entity.select(0)
  for p in params:
    print(p)
  params = entity.select(1)
  for p in params:
    print(p)

  param = params[0]
  param.name = "NEW"
  entity.update(param)







  







