require 'pi_piper'

puts "Press the switch to get started"

PiPiper.watch :pin => 37, :invert => true do |pin|
  puts "Pin changed from #{pin.last_value} to #{pin.value}"
end

PiPiper.wait

