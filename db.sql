/*
 Navicat Premium Data Transfer

 Source Server         : frp 开发
 Source Server Type    : SQLite
 Source Server Version : 3021000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3021000
 File Encoding         : 65001

 Date: 11/07/2022 16:14:00
*/

PRAGMA foreign_keys = false;


-- ----------------------------
-- Table structure for frpc_clients
-- ----------------------------
DROP TABLE IF EXISTS "frpc_clients";
CREATE TABLE "frpc_clients" (
  "id" INTEGER NOT NULL,
  "name" TEXT,
  "extend" TEXT,
  "auto_run" TEXT,
  "status" TEXT,
  'uuid'    TEXT,
  "pid" INTEGER,
  "is_warning" int,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for frpc_config
-- ----------------------------
DROP TABLE IF EXISTS "frpc_config";
CREATE TABLE "frpc_config" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" TEXT,
  "value" TEXT,
  "type" TEXT,
  "group" TEXT,
  "content" TEXT,
  "default" TEXT,
  "support" TEXT,
  "extend" TEXT,
  "help_url" TEXT,
  "is_dev" integer,
  "is_require" TEXT
);

-- ----------------------------
-- Records of frpc_config
-- ----------------------------
INSERT INTO "frpc_config" VALUES (46, 'server_addr', '0.0.0.0', 'string', 'client', '连接服务端的地址', '0.0.0.0', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (47, 'server_port', 7000, 'int', 'client', '连接服务端的端口', 7000, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (48, 'connect_server_local_ip', NULL, 'string', 'client', '连接服务端时所绑定的本地 IP', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (49, 'dial_server_timeout', 10, 'int', 'client', '连接服务端的超时时间', 10, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (50, 'dial_server_keepalive', 7200, 'int', 'client', '和服务端底层 TCP 连接的 keepalive 间隔时间，单位秒', 7200, NULL, '负数不启用', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (51, 'http_proxy', NULL, 'string', 'client', '连接服务端使用的代理地址', NULL, NULL, '格式为 {protocol}://user:passwd@192.168.1.128:8080 protocol 目前支持 http、socks5、ntlm', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (52, 'log_file', './frpc.log', 'string', 'client', '日志文件地址', './frpc.log', NULL, '如果设置为 console，会将日志打印在标准输出中', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (53, 'log_level', 'info', 'string', 'client', '日志等级', 'info', 'trace, debug, info, warn, error', NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (54, 'log_max_days', 3, 'int', 'client', '日志文件保留天数', 3, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (55, 'disable_log_color', 'false', 'bool', 'client', '禁用标准输出中的日志颜色', 'false', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (56, 'pool_count', 0, 'int', 'client', '连接池大小', 0, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (57, 'user', NULL, 'string', 'client', '用户名', NULL, NULL, '设置此参数后，代理名称会被修改为 {user}.{proxyName}，避免代理名称和其他用户冲突', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (58, 'dns_server', NULL, 'string', 'client', '使用 DNS 服务器地址', NULL, NULL, '默认使用系统配置的 DNS 服务器，指定此参数可以强制替换为自定义的 DNS 服务器地址', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (59, 'login_fail_exit', 'false', 'bool', 'client', '第一次登陆失败后是否退出', 'true', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (60, 'protocol', 'tcp', 'string', 'client', '连接服务端的通信协议', 'tcp', 'tcp, kcp, websocket', NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (61, 'tls_enable', 'false', 'bool', 'client', '启用 TLS 协议加密连接', 'false', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (62, 'tls_cert_file', NULL, 'string', 'client', 'TLS 客户端证书文件路径', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (63, 'tls_key_file', NULL, 'string', 'client', 'TLS 客户端密钥文件路径', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (64, 'tls_trusted_ca_file', NULL, 'string', 'client', 'TLS CA 证书路径', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (65, 'tls_server_name', NULL, 'string', 'client', 'TLS Server 名称', NULL, NULL, '为空则使用 server_addr', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (66, 'disable_custom_tls_first_byte', 'false', 'bool', 'client', 'TLS 不发送 0x17', 'false', NULL, '当为 true 时，不能端口复用', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (67, 'tcp_mux_keepalive_interval', 60, 'int', 'client', 'tcp_mux 的心跳检查间隔时间', 60, NULL, '单位：秒', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (68, 'heartbeat_interval', 30, 'int', 'client', '向服务端发送心跳包的间隔时间', 30, NULL, '建议启用 tcp_mux_keepalive_interval，将此值设置为 -1', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (69, 'heartbeat_timeout', 90, 'int', 'client', '和服务端心跳的超时时间', 90, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (70, 'udp_packet_size', 1500, 'int', 'client', '代理 UDP 服务时支持的最大包长度', 1500, NULL, '服务端和客户端的值需要一致', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (71, 'start', NULL, 'string', 'client', '指定启用部分代理', NULL, NULL, '当配置了较多代理，但是只希望启用其中部分时可以通过此参数指定，默认为全部启用', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (72, 'meta_xxx', NULL, 'map', 'client', '附加元数据', NULL, NULL, '会传递给服务端插件，提供附加能力', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (74, 'authentication_method', 'token', 'string', 'client', '鉴权方式', 'token', 'token, oidc', '需要和服务端一致', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (75, 'authenticate_heartbeats', 'true', 'bool', 'client', '开启心跳消息鉴权', 'true', NULL, '需要和服务端一致', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (76, 'authenticate_new_work_conns', 'false', 'bool', 'client', '开启建立工作连接的鉴权', 'false', NULL, '需要和服务端一致', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (77, 'token', NULL, 'string', 'client', '鉴权使用的 token 值', NULL, NULL, '需要和服务端设置一样的值才能鉴权通过', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (78, 'oidc_client_id', NULL, 'string', 'client', 'oidc_client_id', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (79, 'oidc_client_secret', NULL, 'string', 'client', 'oidc_client_secret', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (80, 'oidc_audience', NULL, 'string', 'client', 'oidc_audience', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (81, 'oidc_token_endpoint_url', NULL, 'string', 'client', 'oidc_token_endpoint_url', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (82, 'oidc_additional_xxx', NULL, 'map', 'client', 'OIDC 附加参数', NULL, NULL, 'map 结构，key 需要以 oidc_additional_ 开头', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (84, 'admin_addr', '0.0.0.0', 'string', 'client', '启用 AdminUI 监听的本地地址', '0.0.0.0', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (85, 'admin_port', 0, 'int', 'client', '启用 AdminUI 监听的本地端口', 0, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (86, 'admin_user', NULL, 'string', 'client', 'HTTP BasicAuth 用户名', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (87, 'admin_pwd', NULL, 'string', 'client', 'HTTP BasicAuth 密码', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (88, 'asserts_dir', NULL, 'string', 'client', '静态资源目录', NULL, NULL, 'AdminUI 使用的资源默认打包在二进制文件中，通过指定此参数使用自定义的静态资源', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (89, 'pprof_enable', 'false', 'bool', 'client', '启动 Go HTTP pprof', 'false', NULL, '用于应用调试', NULL, NULL, NULL);
INSERT INTO "frpc_config" VALUES (92, 'type', NULL, 'string', 'proxy_base', '代理类型', 'tcp', 'tcp, udp, http, https, stcp, sudp, xtcp, tcpmux', NULL, NULL, NULL, '是');
INSERT INTO "frpc_config" VALUES (93, 'use_encryption', NULL, 'bool', 'proxy_base', '是否启用加密功能', 'N', NULL, '启用后该代理和服务端之间的通信内容都会被加密传输', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (94, 'use_compression', NULL, 'bool', 'proxy_base', '是否启用压缩功能', 'N', NULL, '启用后该代理和服务端之间的通信内容都会被压缩传输', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (95, 'proxy_protocol_version', NULL, 'string', 'proxy_base', '启用 proxy protocol 协议的版本', NULL, 'v1, v2', '如果启用，则 frpc 和本地服务建立连接后会发送 proxy protocol 的协议，包含了原请求的 IP 地址和端口等内容', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (96, 'bandwidth_limit', NULL, 'string', 'proxy_base', '设置单个 proxy 的带宽限流', NULL, NULL, '单位为 MB 或 KB，0 表示不限制，如果启用，会作用于对应的 frpc', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (103, 'local_ip', NULL, 'string', 'proxy_local', '本地服务 IP', '127.0.0.1', NULL, '需要被代理的本地服务的 IP 地址，可以为所在 frpc 能访问到的任意 IP 地址', NULL, NULL, '是');
INSERT INTO "frpc_config" VALUES (104, 'local_port', NULL, 'int', 'proxy_local', '本地服务端口', NULL, NULL, '配合 local_ip', NULL, NULL, '是');
INSERT INTO "frpc_config" VALUES (105, 'plugin', NULL, 'string', 'proxy_local', '客户端插件名称', NULL, '见客户端插件的功能说明', '用于扩展 frpc 的能力，能够提供一些简单的本地服务，如果配置了 plugin，则 local_ip 和 local_port 无效，两者只能配置一个', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (106, 'plugin_params', NULL, 'map', 'proxy_local', '客户端插件参数', NULL, NULL, 'map 结构，key 需要都以 “plugin_” 开头，每一个 plugin 需要的参数也不一样，具体见客户端插件参数中的内容', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (111, 'group', NULL, 'string', 'proxy_group', '负载均衡分组名称', NULL, NULL, '用户请求会以轮询的方式发送给同一个 group 中的代理', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (112, 'group_key', NULL, 'string', 'proxy_group', '负载均衡分组密钥', NULL, NULL, '用于对负载均衡分组进行鉴权，group_key 相同的代理才会被加入到同一个分组中', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (113, 'health_check_type', NULL, 'string', 'proxy_group', '健康检查类型', NULL, 'tcp,http', '配置后启用健康检查功能，tcp 是连接成功则认为服务健康，http 要求接口返回 2xx 的状态码则认为服务健康', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (114, 'health_check_timeout_s', NULL, 'int', 'proxy_group', '健康检查超时时间(秒)', 3, NULL, '执行检查任务的超时时间', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (115, 'health_check_max_failed', NULL, 'int', 'proxy_group', '健康检查连续错误次数', 1, NULL, '连续检查错误多少次认为服务不健康', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (116, 'health_check_interval_s', NULL, 'int', 'proxy_group', '健康检查周期(秒)', 10, NULL, '每隔多长时间进行一次健康检查', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (117, 'health_check_url', NULL, 'string', 'proxy_group', '健康检查的 HTTP 接口', NULL, NULL, '如果 health_check_type 类型是 http，则需要配置此参数，指定发送 http 请求的 url，例如 “/health”', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (122, 'remote_port', NULL, 'int', 'proxy_tcp', '服务端绑定的端口', NULL, NULL, '用户访问此端口的请求会被转发到 local_ip:local_port', NULL, NULL, '是');
INSERT INTO "frpc_config" VALUES (127, 'remote_port', NULL, 'int', 'proxy_udp', '服务端绑定的端口', NULL, NULL, '用户访问此端口的请求会被转发到 local_ip:local_port', NULL, NULL, '是');
INSERT INTO "frpc_config" VALUES (134, 'custom_domains', NULL, 'json', 'proxy_http', '服务器绑定自定义域名', NULL, NULL, '用户通过 vhost_http_port 访问的 HTTP 请求如果 Host 在 custom_domains 配置的域名中，则会被路由到此代理配置的本地服务', NULL, NULL, '是(和 subdomain 两者必须配置一个)');
INSERT INTO "frpc_config" VALUES (135, 'subdomain', NULL, 'string', 'proxy_http', '自定义子域名', NULL, NULL, '和 custom_domains 作用相同，但是只需要指定子域名前缀，会结合服务端的 subdomain_host 生成最终绑定的域名', NULL, NULL, '是(和 custom_domains 两者必须配置一个)');
INSERT INTO "frpc_config" VALUES (136, 'locations', NULL, 'json', 'proxy_http', 'URL 路由配置', NULL, NULL, '采用最大前缀匹配的规则，用户请求匹配响应的 location 配置，则会被路由到此代理', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (137, 'route_by_http_user', NULL, 'string', 'proxy_http', '根据 HTTP Basic Auth user 路由', NULL, NULL, NULL, NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (138, 'http_user', NULL, 'string', 'proxy_http', '用户名', NULL, NULL, '如果配置此参数，暴露出去的 HTTP 服务需要采用 Basic Auth 的鉴权才能访问', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (139, 'http_pwd', NULL, 'string', 'proxy_http', '密码', NULL, NULL, '结合 http_user 使用', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (140, 'host_header_rewrite', NULL, 'string', 'proxy_http', '替换 Host header', NULL, NULL, '替换发送到本地服务 HTTP 请求中的 Host 字段', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (141, 'headers', NULL, 'json', 'proxy_http', '替换 header', NULL, NULL, 'map 中的 key 是要替换的 header 的 key，value 是替换后的内容', NULL, NULL, '否');
INSERT INTO "frpc_config" VALUES (148, 'custom_domains', NULL, 'json', 'proxy_https', '服务器绑定自定义域名', NULL, NULL, '用户通过 vhost_http_port 访问的 HTTP 请求如果 Host 在 custom_domains 配置的域名中，则会被路由到此代理配置的本地服务', NULL, NULL, '是(和 subdomain 两者必须配置一个)');
INSERT INTO "frpc_config" VALUES (149, 'subdomain', NULL, 'string', 'proxy_https', '自定义子域名', NULL, NULL, '和 custom_domains 作用相同，但是只需要指定子域名前缀，会结合服务端的 subdomain_host 生成最终绑定的域名', NULL, NULL, '是(和 custom_domains 两者必须配置一个)');
INSERT INTO "frpc_config" VALUES (154, 'role', NULL, 'string', 'proxy_stcp', '角色', 'server', 'server,visitor', 'server 表示服务端，visitor 表示访问端', NULL, NULL, '是');
INSERT INTO "frpc_config" VALUES (155, 'sk', NULL, 'string', 'proxy_stcp', '密钥', NULL, NULL, '服务端和访问端的密钥需要一致，访问端才能访问到服务端', NULL, NULL, '是');
INSERT INTO "frpc_config" VALUES (160, 'role', NULL, 'string', 'proxy_sudp', '角色', 'server', 'server,visitor', 'server 表示服务端，visitor 表示访问端', NULL, NULL, '是');
INSERT INTO "frpc_config" VALUES (161, 'sk', NULL, 'string', 'proxy_sudp', '密钥', NULL, NULL, '服务端和访问端的密钥需要一致，访问端才能访问到服务端', NULL, NULL, '是');
INSERT INTO "frpc_config" VALUES (166, 'role', NULL, 'string', 'proxy_xtcp', '角色', 'server', 'server,visitor', 'server 表示服务端，visitor 表示访问端', NULL, NULL, '是');
INSERT INTO "frpc_config" VALUES (167, 'sk', NULL, 'string', 'proxy_xtcp', '密钥', NULL, NULL, '服务端和访问端的密钥需要一致，访问端才能访问到服务端', NULL, NULL, '是');
INSERT INTO "frpc_config" VALUES (174, 'multiplexer', NULL, 'string', 'proxy_tcpmux', '复用器类型', NULL, 'httpconnect', NULL, NULL, NULL, '是');
INSERT INTO "frpc_config" VALUES (175, 'custom_domains', NULL, 'json', 'proxy_tcpmux', '服务器绑定自定义域名', NULL, NULL, '用户通过 tcpmux_httpconnect_port 访问的 CONNECT 请求如果 Host 在 custom_domains 配置的域名中，则会被路由到此代理配置的本地服务', NULL, NULL, '是(和 subdomain 两者必须配置一个)');
INSERT INTO "frpc_config" VALUES (176, 'subdomain', NULL, 'string', 'proxy_tcpmux', '自定义子域名', NULL, NULL, '和 custom_domains 作用相同，但是只需要指定子域名前缀，会结合服务端的 subdomain_host 生成最终绑定的域名', NULL, NULL, '是(和 custom_domains 两者必须配置一个)');
INSERT INTO "frpc_config" VALUES (177, 'route_by_http_user', NULL, 'string', 'proxy_tcpmux', '根据 HTTP Basic Auth user 路由', NULL, NULL, NULL, NULL, NULL, '否');

-- ----------------------------
-- Table structure for frpc_config_detail
-- ----------------------------
DROP TABLE IF EXISTS "frpc_config_detail";
CREATE TABLE "frpc_config_detail" (
  "id" INTEGER NOT NULL,
  "client_id" INTEGER,
  "proxy_id" INTEGER,
  "detail_type" integer,
  "name" TEXT,
  "value" TEXT,
  "type" TEXT,
  "content" TEXT,
  "default" TEXT,
  "extend" TEXT,
  "support" TEXT,
  "is_require" int,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for frpc_proxys
-- ----------------------------
DROP TABLE IF EXISTS "frpc_proxys";
CREATE TABLE "frpc_proxys" (
  "id" INTEGER NOT NULL,
  "name" TEXT,
  "client_id" INTEGER,
  "proxy_type" TEXT,
  "extend" TEXT,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for frps_config
-- ----------------------------
DROP TABLE IF EXISTS "frps_config";
CREATE TABLE "frps_config" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" TEXT,
  "value" TEXT,
  "type" TEXT,
  "group" TEXT,
  "content" TEXT,
  "default" TEXT,
  "support" TEXT,
  "extend" TEXT,
  "help_url" TEXT,
  "is_dev" integer
);

-- ----------------------------
-- Records of frps_config
-- ----------------------------
INSERT INTO "frps_config" VALUES (1, 'bind_addr', '0.0.0.0', 'string', 'base', '服务端监听地址', '0.0.0.0', NULL, NULL, NULL, 0);
INSERT INTO "frps_config" VALUES (2, 'bind_port', 65000, 'int', 'base', '服务端监听端口', 65000, NULL, '接收 frpc 的连接', NULL, 0);
INSERT INTO "frps_config" VALUES (3, 'bind_udp_port', 65001, 'int', 'base', '服务端监听 UDP 端口', 65001, NULL, '用于辅助创建 P2P 连接', NULL, 0);
INSERT INTO "frps_config" VALUES (4, 'kcp_bind_port', 65002, 'int', 'base', '服务端监听 KCP 协议端口', 65002, NULL, '用于接收采用 KCP 连接的 frpc', NULL, 0);
INSERT INTO "frps_config" VALUES (5, 'proxy_bind_addr', '0.0.0.0', 'string', 'base', '代理监听地址', '0.0.0.0', NULL, '可以使代理监听在不同的网卡地址', NULL, 0);
INSERT INTO "frps_config" VALUES (6, 'log_file', './data/log/frps.log', 'string', 'base', '日志文件地址', './data/log/frps.log', NULL, '如果设置为 console，会将日志打印在标准输出中', NULL, 0);
INSERT INTO "frps_config" VALUES (7, 'log_level', 'info', 'string', 'base', '日志等级', 'info', 'trace, debug, info, warn, error', NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (8, 'log_max_days', 3, 'int', 'base', '日志文件保留天数', 3, NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (9, 'disable_log_color', 'false', 'bool', 'base', '禁用标准输出中的日志颜色', 'false', NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (10, 'detailed_errors_to_client', 'true', 'bool', 'base', '服务端返回详细错误信息给客户端', 'true', NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (11, 'tcp_mux_keepalive_interval', 60, 'int', 'base', 'tcp_mux 的心跳检查间隔时间', 60, NULL, '单位：秒', NULL, 1);
INSERT INTO "frps_config" VALUES (12, 'tcp_keepalive', 7200, 'int', 'base', '和客户端底层 TCP 连接的 keepalive 间隔时间，单位秒', 7200, NULL, '负数不启用', NULL, 1);
INSERT INTO "frps_config" VALUES (13, 'heartbeat_timeout', 90, 'int', 'base', '服务端和客户端心跳连接的超时时间', 90, NULL, '单位：秒', NULL, 1);
INSERT INTO "frps_config" VALUES (14, 'user_conn_timeout', 10, 'int', 'base', '用户建立连接后等待客户端响应的超时时间', 10, NULL, '单位：秒', NULL, 1);
INSERT INTO "frps_config" VALUES (15, 'udp_packet_size', 1500, 'int', 'base', '代理 UDP 服务时支持的最大包长度', 1500, NULL, '服务端和客户端的值需要一致', NULL, 1);
INSERT INTO "frps_config" VALUES (16, 'tls_cert_file', './data/tls/server/server.crt', 'string', 'base', 'TLS 服务端证书文件路径', './data/tls/server/server.crt', NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (17, 'tls_key_file', './data/tls/server/server.key', 'string', 'base', 'TLS 服务端密钥文件路径', './data/tls/server/server.key', NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (18, 'tls_trusted_ca_file', './data/tls/ca/ca.crt', 'string', 'base', 'TLS CA 证书路径', './data/tls/ca/ca.crt', NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (19, 'authentication_method', 'token', 'string', 'auth', '鉴权方式', 'token', 'token, oidc', NULL, NULL, 0);
INSERT INTO "frps_config" VALUES (20, 'authenticate_heartbeats', 'false', 'bool', 'auth', '开启心跳消息鉴权', 'false', NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (21, 'authenticate_new_work_conns', 'false', 'bool', 'auth', '开启建立工作连接的鉴权', 'false', NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (22, 'token', NULL, 'string', 'auth', '鉴权使用的 token 值', NULL, NULL, '客户端需要设置一样的值才能鉴权通过', NULL, 0);
INSERT INTO "frps_config" VALUES (23, 'oidc_issuer', NULL, 'string', 'auth', 'oidc_issuer', NULL, NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (24, 'oidc_audience', NULL, 'string', 'auth', 'oidc_audience', NULL, NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (25, 'oidc_skip_expiry_check', NULL, 'bool', 'auth', 'oidc_skip_expiry_check', NULL, NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (26, 'oidc_skip_issuer_check', NULL, 'bool', 'auth', 'oidc_skip_issuer_check', NULL, NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (27, 'allow_ports', NULL, 'string', 'client', '允许代理绑定的服务端端口', NULL, NULL, '格式为 1000-2000,2001,3000-4000', NULL, 0);
INSERT INTO "frps_config" VALUES (28, 'max_pool_count', 5, 'int', 'client', '最大连接池大小', 5, NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (29, 'max_ports_per_client', 0, 'int', 'client', '限制单个客户端最大同时存在的代理数', 0, NULL, '0 表示没有限制', NULL, 1);
INSERT INTO "frps_config" VALUES (30, 'tls_only', 'false', 'bool', 'client', '只接受启用了 TLS 的客户端连接', 'false', NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (31, 'dashboard_addr', '127.0.0.1', 'string', 'dashboard', '启用 Dashboard 监听的本地地址', '127.0.0.1', NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (32, 'dashboard_port', 65003, 'int', 'dashboard', '启用 Dashboard 监听的本地端口', 65003, NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (33, 'dashboard_user', NULL, 'string', 'dashboard', 'HTTP BasicAuth 用户名', NULL, NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (34, 'dashboard_pwd', NULL, 'string', 'dashboard', 'HTTP BasicAuth 密码', NULL, NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (35, 'enable_prometheus', 'false', 'bool', 'dashboard', '是否提供 Prometheus 监控接口', 'false', NULL, '需要同时启用了 Dashboard 才会生效', NULL, 1);
INSERT INTO "frps_config" VALUES (36, 'asserts_dir', NULL, 'string', 'dashboard', '静态资源目录', NULL, NULL, 'Dashboard 使用的资源默认打包在二进制文件中，通过指定此参数使用自定义的静态资源', NULL, 1);
INSERT INTO "frps_config" VALUES (37, 'pprof_enable', 'false', 'bool', 'dashboard', '启动 Go HTTP pprof', 'false', NULL, '用于应用调试', NULL, 1);
INSERT INTO "frps_config" VALUES (38, 'vhost_http_port', 80, 'int', 'http_https', '为 HTTP 类型代理监听的端口', 80, NULL, '启用后才支持 HTTP 类型的代理，默认不启用', NULL, 0);
INSERT INTO "frps_config" VALUES (39, 'vhost_https_port', 443, 'int', 'http_https', '为 HTTPS 类型代理监听的端口', 443, NULL, '启用后才支持 HTTPS 类型的代理，默认不启用', NULL, 0);
INSERT INTO "frps_config" VALUES (40, 'vhost_http_timeout', 60, 'int', 'http_https', 'HTTP 类型代理在服务端的 ResponseHeader 超时时间', 60, NULL, NULL, NULL, 1);
INSERT INTO "frps_config" VALUES (41, 'subdomain_host', NULL, 'string', 'http_https', '二级域名后缀', NULL, NULL, NULL, NULL, 0);
INSERT INTO "frps_config" VALUES (42, 'custom_404_page', './data/conf/error.html', 'string', 'http_https', '自定义 404 错误页面地址', './data/conf/error.html', NULL, NULL, NULL, 0);
INSERT INTO "frps_config" VALUES (43, 'tcpmux_httpconnect_port', 65004, 'int', 'tcpmux', '为 TCPMUX 类型代理监听的端口', 65004, NULL, '启用后才支持 TCPMUX 类型的代理，默认不启用', NULL, 1);
INSERT INTO "frps_config" VALUES (44, 'tcpmux_passthrough', 'false', 'bool', 'tcpmux', '是否透传 CONNECT 请求', 'false', NULL, '通常在本地服务是 HTTP Proxy 时使用', NULL, 1);
INSERT INTO "frps_config" VALUES (45, 'tls_enable', 'true', 'bool', 'base', '启用tls 协议对数据加密', 'true', NULL, NULL, NULL, 1);

-- ----------------------------
-- Table structure for global_config
-- ----------------------------
DROP TABLE IF EXISTS "global_config";
CREATE TABLE "global_config" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" TEXT,
  "value" TEXT,
  "group" TEXT,
  "extend" TEXT
);

-- ----------------------------
-- Records of global_config
-- ----------------------------
INSERT INTO "global_config" VALUES (1, 'base', '基础配置', 'frps_group', 'frps的配置群组');
INSERT INTO "global_config" VALUES (2, 'auth', '权限验证', 'frps_group', 'frps的配置群组');
INSERT INTO "global_config" VALUES (3, 'dashboard', 'frp 监控', 'frps_group', 'frps的配置群组');
INSERT INTO "global_config" VALUES (4, 'client', '客户端管理', 'frps_group', 'frps的配置群组');
INSERT INTO "global_config" VALUES (5, 'http_https', 'HTTP/HTTPS 代理', 'frps_group', 'frps的配置群组');
INSERT INTO "global_config" VALUES (6, 'tcpmux', 'TCPMUX 代理', 'frps_group', 'frps的配置群组');



PRAGMA foreign_keys = true;
