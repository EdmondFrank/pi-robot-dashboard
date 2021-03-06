require 'sinatra/reloader' if development?

DISK_STATUS_NAME_MAP = {
  "Filesystem" => "文件系统",
  "Size"       => "容量",
  "Used"       => "消耗",
  "Avail"      => "剩余",
  "Use%"       => "使用百分比",
  "Mounted"    => "挂载点"
}.freeze

SERVICES = {
  "[s]mbd"      => "NAS",
  "[p]uma"      => "监控面板",
  "[c]lockwork" => "温度采集"
}

SETTINGS = {
  :debug => 0,
  :pid => nil,
  :gestures => -1
}
COMMAND_STATUS = {
  # id => "pid/nil"
}

get '/' do
  slim :index
end

get '/temperature' do
  startTime = DateTime.now.strftime("%F")
  endTime   = DateTime.now.next.strftime("%F")
  @data = Temperature.all(:created_at => (startTime..endTime), :order => [:id.asc])

  slim :temperature
end

get '/disk' do
  info = `df -h / /boot/`.split("\n")
  @headers = []
  info.shift.split(" ").each { |name| @headers << DISK_STATUS_NAME_MAP[name] }
  @items = info.each do |mount|
    mount.gsub!("/dev/root", "Raspberry")
    mount.gsub!("/dev/mmcblk0p1", "Boot")
  end

  slim :disk
end

get '/services' do
  @services_with_status = {}
  SERVICES.each do |k,v|
    pid = `ps aux | grep "#{k}" | awk '{print $2}'`
    @services_with_status[v] = (pid.empty? ? "停止" : "正常")
  end

  slim :services
end

get '/control' do
  @command_datas = Command.all
  @flag = SETTINGS[:debug]
  slim :control
end

post '/control' do
  puts params
  if SETTINGS[:pid] == nil
    SETTINGS[:pid] = Process.spawn("python drive_api.py --speed 20")
    SETTINGS[:debug] = 1
    SERVICES[SETTINGS[:pid]] = "调试模式"
    json pid: SETTINGS[:pid], msg: "debug active"
  else
    pid = SETTINGS[:pid]
    res = Process.kill('INT',pid)
    SETTINGS[:debug] = 0
    SETTINGS[:pid] = nil
    SERVICES.delete(pid)
    json pid: res, msg: "debug end"
  end
end

post '/gestures' do
  puts params
  pin = params["pin"]
  exec_id = params["id"]
  pull = params["pull"] || "down"
  bouncetime = params["bouncetime"]
  if SETTINGS[:gestures] == -1
    SETTINGS[:gestures] =
      Process.
        spawn("python gestures.py -p #{pin} -e #{exec_id} -i #{pull}
  -d #{bouncetime}")
    puts "启用手势 #{SETTINGS[:gestures]}"
    SERVICES[SETTINGS[:gestures]] = "手势启动"
    json pid: SETTINGS[:gestures], msg: "gestures active"
  else
    pid = SETTINGS[:gestures]
    puts "停用手势#{pid}"
    res = Process.kill('QUIT', pid)
    SETTINGS[:gestures] = -1
    SERVICES.delete(pid)
    json pid: res, msg: "gestures end"
  end

end


get '/gpio' do

  pin_collect = `gpio readall`.split("\n").select do |line|
    line.split("|").length == 14
  end

  @pin_datas = pin_collect.reduce([]) do |res, line|
    v = line.split("|").map{|v|v.strip}
    res << ({ id: v[6], w_id: v[2], mode: v[4], value: v[5], name: v[3] })
    res << ({ id: v[8], w_id: v[12], mode: v[10], value: v[9], name: v[11] })
  end

  slim :gpio
end

post '/gpio' do
  return 400 unless params.is_a?(Hash)
  if params["pk"] =~ /\d+/ && params["value"] =~ /^\d$/
    `gpio write #{params['pk']} #{params["value"] == "1" ? 1 : 0}`
  elsif params["pk"] =~ /\d+/ && params["value"] =~ /[IN|OUT]/
    `gpio mode #{params['pk']} #{params["value"]}`
  end
end

get '/start' do
  @command_datas = Command.all
  @command_status = {}
  @command_datas.each do |item|
    @command_status[item[:id]] = COMMAND_STATUS.has_key?(item[:id].to_s) ? 1 : 0
  end

  slim :start
end

post '/start' do
  if params.is_a?(Hash) && params[:name]!="" && params[:cmd]!=""
  res = Command.create({
    name: params[:name],
    command: params[:cmd] })
  return json id: res.id
  end
  status 400
  json message: "Invalid Params"
end


post '/start/:id' do
  if COMMAND_STATUS.has_key?(params[:id]) && COMMAND_STATUS[params[:id]]
    pid = COMMAND_STATUS[params[:id]]
    res = Process.kill('QUIT',pid)
    COMMAND_STATUS.delete(params[:id])
    json pid: res, message: "kill process"
  else
    obj = Command.get(params[:id])
    pid = Process.spawn(obj['command'])
    SERVICES[pid] = obj['name']
    COMMAND_STATUS[params[:id]] = pid if pid
    json pid: pid, message: "success"
  end
end

delete '/start/:id' do
  if COMMAND_STATUS.has_key?(params[:id]) && COMMAND_STATUS[params[:id]]
    status 400
    json message: "服务正在运行，无法删除"
  else
    obj = Command.get(params[:id])
    obj.destroy
    json message: "删除成功"
  end

end


get '/styles.css' do
  scss :styles
end

before do
  time, connections, loads = `uptime`.chomp.split(",",3)
  sys_time, run_time = time.split("up")
  @info = ["系统时间: #{sys_time.strip}", "已运行: #{run_time.strip}", "连接数: #{connections}", "负载: #{loads.strip}"]
end

error 400 do
  'Invalid Params'
end
