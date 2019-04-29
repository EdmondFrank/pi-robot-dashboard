require 'data_mapper'

DataMapper.setup(:default, 'postgres://postgres:root@localhost/postgres/pi')

class Temperature
  include DataMapper::Resource

  property :id, Serial
  property :temp, Float
  property :created_at, DateTime
end

class Command
  include DataMapper::Resource

  property :id, Serial
  property :name, String
  property :command, String
end
DataMapper.finalize.auto_upgrade!

unless Command.get(1)
  Command.create({
    id: 1,
    name: "机器人脚本１",
    command: "python script/robot.py",})
end
