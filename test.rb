require 'csv'

pin_collect = `gpio readall`.split("\n").select do |line|
  line.split("|").length == 14
end

pin_datas = pin_collect.reduce([]) do |res, line|
  v = line.split("|").map{|v|v.strip}
  res << ({ id: v[6], w_id: v[2], mode: v[4], value: v[5] })
  res << ({ id: v[8], w_id: v[12], mode: v[10], value: v[9] })
end

p pin_datas
