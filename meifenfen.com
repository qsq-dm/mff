
    server {
        server_name www.meifenfen.com;
        listen       80;

        if ($time_iso8601 ~ "^(\d{4})-(\d{2})-(\d{2})") {
            set $year $1;
            set $month $2;
            set $day $3;
        }

        access_log /data/production/$year-$month-$day.log custom;

        error_log  /data/error.log debug;

        set $mobile_request '';
         
        if ($http_user_agent ~* '(Mobile|WebOS)') {
          set $mobile_request '1';
        }
        if ($uri = /) {
        set $mobile_request "${mobile_request}1";
        }
        if ($mobile_request = '11') {
          rewrite / /mobile/ redirect;
          break;
        }

        location /static {
            root   /tmp/meifenfen/;
        }
        location /admin/static {
            root   /tmp/meifenfen/static/;
        }


        location / {
            root   /root/meifenfen;
            uwsgi_pass 127.0.0.1:10001;
            include     uwsgi_params;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

    }
