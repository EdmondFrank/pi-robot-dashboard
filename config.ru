require 'rubygems'
require 'bundler/setup'
require 'sinatra'
require 'slim'
require 'sass'
# require 'rpi_gpio'
# require 'pi_piper'
require './schema'
require './app'

set :environment, :development
set :server, :puma
set :run, false
set :raise_errors, true

run Sinatra::Application
