require 'data_mapper'

DataMapper.setup(:default, 'postgres://postgres:root@localhost/postgres/pi')

class Temperature
  include DataMapper::Resource

  property :id, Serial
  property :temp, Float
  property :created_at, DateTime
end

DataMapper.finalize.auto_upgrade!
