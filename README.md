Raspberry Robot Dashboard
---

#### This project is for monitoring and controlling Raspberry Pi, and it supports the following things:
+ **monitor and show machine temperature**
+ **monitor and show disk usage**
+ **monitor and show running services**
+ **manage raspberry gpio**

#### This project is built by using the following main things:
+ **[Ruby][1]**
+ **[Sinatra][2]**
+ **[Clockwork][3]**

> more details, please see Gemfile.

[1]: https://www.ruby-lang.org/
[2]: http://www.sinatrarb.com/
[3]: https://github.com/tomykaira/clockwork

#### Usage:
+ **local development**

  ```
  1. clone the code
  2. bundle install
  3. foreman start
  ```

+ **Raspberry deployment**

  ```
  cap staging deploy
  ```
#### Reference repository
[pi_dashboard/ruby][https://github.com/shawzt/pi_dashboard]

[pi-dashboard/php][https://github.com/spoonysonny/pi-dashboard]
