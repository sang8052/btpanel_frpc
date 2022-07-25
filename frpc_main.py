#! /usr/bin/btpython
#  coding: utf-8

import os,sys,time,json,re
import requests,psutil


os.chdir("/www/server/panel")
sys.path.append("class/")
sys.path.append("class/msg")

plugin_path = '/www/server/panel/plugin/frpc/'
db_path = '../plugin/frpc/data/frpc'

import public, db,panelTask,send_mail


class frpc_main:
    def get_app_version(self,argv):
        app = json.loads(public.readFile(plugin_path + 'info.json'))
        return self.__response_json(app['versions'])

    # 查询当前frpc 的内核版本
    def get_frpc_version(self, argv):
        version = json.loads(public.readFile("%sbin/version.json" % plugin_path))
        return self.__response_json(version['version'])

    # 查询当前云端所支持的frpc 的版本
    def get_frpc_version_update(self, argv):
        version_list = self._get_frp_version_update()
        versions = []
        for version in version_list['version'].keys():
            versions.append(version)
        versions.sort(reverse=True)
        return self.__response_json(versions)

    # 清空 云端的frpc 的缓存信息
    def update_frpc_version_cache(self,argv):
        db_obj = self.__db()
        db_obj.table('global_config').where('`name` = ?', 'frp_version_cache').update(
            {'value': 0})
        self._get_frp_version_update()
        return self.__response_json(True)

    # 更新frpc 的版本
    def update_frpc_version(self, args):
        db_obj = self.__db()
        clients = db_obj.table('frpc_clients').select()
        for client in clients:
            self._stop_client(client['id'],client['pid'])
        task = panelTask.bt_task()
        result = task.create_task('更新frp 内核', 0,
                                  'btpython /www/server/panel/plugin/frpc/frpc_main.py install ' + args.version,
                                  args.version)
        return self.__response_json(result)

    # 查询指定任务的执行状态
    def get_task_status(self, args):
        task = panelTask.bt_task()
        status = task.get_task_find(args.id)
        return self.__response_json(status)

    # 查询新建一个frpc 客户端时 admin port 的端口号
    def get_create_client_admin_port(self,argv):
        db_obj = self.__db()
        clients = db_obj.table('frpc_clients').field('max(`id`)').select()[0]
        try:
            port = int(clients['max(`id`)']) + 65000
        except:
            port = 65000
        return self.__response_json(port)


    # 新建一个frpc 的客户端
    def create_frpc_client(self, argv):
        db_obj = self.__db()
        server_addr = getattr(argv,'server_addr')
        detail = db_obj.table('frpc_config_detail').where('`name` = ? and `value` =?',('server_addr',server_addr)).select()
        if len(detail) > 0:
            client_id = detail[0]['client_id']
            client = db_obj.table('frpc_clients').where('id = ?',client_id).select()[0]
            return self.__response_json(client,500,'已经存在服务器ip地址为%s的客户端' % server_addr)
        frp_client = {'name': argv.client_name, 'extend': argv.client_extend, 'status': 'start', 'pid': '',
                      'is_warning': 0, 'uuid': argv.client_uuid,'auto_run':'stop'}
        client_id = db_obj.table('frpc_clients').insert(frp_client)
        detail_ids = []
        list = db_obj.table("frpc_config").where('`group` = ?', 'client').field(
            'name,value,type,content,support,extend,is_dev').select()
        for item in list:
            detail = {'detail_type': 0, 'name': item['name'], 'type': item['type'], 'client_id': client_id,
                      'content': item['content'], '`default`': item['value'], 'extend': item['extend'],
                      'support': item['support']}
            if hasattr(argv, item['name']):
                detail['value'] = getattr(argv, item['name'])
            else:
                if item['value'] == None:
                    item['value'] = ''
                detail['value'] = item['value']
            detail['detail_id'] = db_obj.table('frpc_config_detail').insert(detail)
            detail_ids.append(detail)
        os.mkdir(plugin_path + 'data/log/' + argv.client_uuid)
        os.mkdir(plugin_path + 'data/tls/' + argv.client_uuid)
        tls = {'cert':"",'key':"",'ca':""}
        if hasattr(argv,'tls_cert'):
            public.writeFile(('%sdata/tls/%s/client.crt' % (plugin_path,argv.client_uuid)),getattr(argv,'tls_cert'))
            update = {'value':'./data/tls/' + argv.client_uuid + '/client.crt'}
            db_obj.table('frpc_config_detail').where('client_id = ? and `name` = ?',(client_id,'tls_cert_file')).update(update)
            tls['cert'] = public.FileMd5(plugin_path + update['value'])
        if hasattr(argv,'tls_key'):
            public.writeFile(('%sdata/tls/%s/client.key' % (plugin_path,argv.client_uuid)),getattr(argv,'tls_key'))
            update = {'value':'./data/tls/' + argv.client_uuid + '/client.key'}
            db_obj.table('frpc_config_detail').where('client_id = ? and `name` = ?',(client_id,'tls_key_file')).update(update)
            tls['key'] = public.FileMd5(plugin_path + update['value'])
        if hasattr(argv,'tls_trusted_ca'):
            public.writeFile(('%sdata/tls/%s/ca.crt' % (plugin_path,argv.client_uuid)),getattr(argv,'tls_trusted_ca'))
            update = {'value':'./data/tls/' + argv.client_uuid + '/ca.crt'}
            db_obj.table('frpc_config_detail').where('client_id = ? and `name` = ?',(client_id,'tls_trusted_ca_file')).update(update)
            tls['ca'] = public.FileMd5(plugin_path + update['value'])
        self._start_client(client_id)
        return self.__response_json({'client_id': client_id, 'detail_ids': detail_ids,'tls':tls})

    # 查询frpc 的客户端列表
    def get_frpc_client(self, argv):
        db_obj = self.__db()
        _clients = db_obj.table('frpc_clients').select()
        clients = []
        for client in _clients:
            client['client_id'] = client['id']
            del client['id']
            client['config'] = []
            client_config = db_obj.table('frpc_config_detail').where('client_id = ? and detail_type = 0',
                                                                     client['client_id']).field(
                'name,value,type').select()
            for c_config in client_config:
                client['config'].append(c_config)
            client['is_running'] = self._status_client(client['client_id'])['is_running']
            client['is_connect'] = self._connect_client(client['client_id'])
            clients.append(client)
        return self.__response_json(clients)

    # 查询frpc 的客户端的详细信息
    def detail_frpc_client(self,argv):
        client_id = argv.client_id
        db_obj = self.__db()
        client = db_obj.table('frpc_clients').where('id = ?',client_id).select()[0]
        client['config'] = []
        client_config = db_obj.table('frpc_config_detail').where('client_id = ? and detail_type = 0',client_id).field('name,value,type').select()
        for c_config in client_config:
            if c_config['name'] == 'tls_cert_file':
                c_config['name'] = 'tls_cert'
                c_config['value'] = public.readFile(plugin_path + c_config['value'])
            if c_config['name'] == 'tls_key_file':
                c_config['name'] = 'tls_key'
                c_config['value'] = public.readFile(plugin_path + c_config['value'])
            if c_config['name'] == 'tls_trusted_ca_file':
                c_config['name'] = 'tls_trusted_ca'
                c_config['value'] = public.readFile(plugin_path + c_config['value'])
            client['config'].append(c_config)
        client['is_running'] = self._status_client(client_id)['is_running']
        client['is_connect'] = self._connect_client(client_id)
        return self.__response_json(client)

    # 修改frpc 的客户端的配置
    def update_frpc_client(self, argv):
        db_obj = self.__db()
        if hasattr(argv,'server_addr'):
            server_addr = getattr(argv,'server_addr')
            detail = db_obj.table('frpc_config_detail').where('`name` = ? and `value` =? and `client_id` != ?',
                                                              ('server_addr', server_addr,argv.client_id)).select()
            if len(detail) > 0:
                client_id = detail[0]['client_id']
                client = db_obj.table('frpc_clients').where('id = ?', client_id).select()[0]
                return self.__response_json(client, 500, '已经存在服务器ip地址为%s的客户端' % server_addr)


        status = db_obj.table('frpc_clients').where('id = ?', argv.client_id).field('status').select()[0]['status']
        self._stop_client(argv.client_id, False)
        client = {}
        if hasattr(argv, 'client_name'):
            client['name'] = getattr(argv, 'client_name')
        if hasattr(argv, 'client_extend'):
            client['extend'] = getattr(argv, 'client_extend')
        if hasattr(argv, 'auto_run'):
            client['auto_run'] = getattr(argv, 'auto_run')
        client['is_warning'] = 0

        db_obj.table('frpc_clients').where('id = ?', argv.client_id).update(client)
        client_config = db_obj.table('frpc_config_detail').where('client_id = ? and detail_type = 0',
                                                                 argv.client_id).select()
        client['config'] = {}
        for gconfig in client_config:
            if hasattr(argv, gconfig['name']):
                value =  getattr(argv, gconfig['name'])
                db_obj.table('frpc_config_detail').where('id = ?', gconfig['id']).update({'value':value})
                client['config'][gconfig['name']] =  value
        client_uuid = self.__get_client_uuid(argv.client_id)
        tls = {'cert':'','key':'','ca':''}
        if hasattr(argv, 'tls_cert'):
            public.writeFile(('%sdata/tls/%s/client.crt' % (plugin_path, client_uuid)), getattr(argv, 'tls_cert'))
            tls['cert'] = public.FileMd5(plugin_path + 'data/tls/' + client_uuid + '/client.crt')
        if hasattr(argv, 'tls_key'):
            public.writeFile(('%sdata/tls/%s/client.key' % (plugin_path, client_uuid)), getattr(argv, 'tls_key'))
            tls['key'] = public.FileMd5(plugin_path + 'data/tls/' + client_uuid + '/client.key')
        if hasattr(argv, 'tls_trusted_ca'):
            public.writeFile(('%sdata/tls/%s/ca.crt' % (plugin_path, client_uuid)),getattr(argv, 'tls_trusted_ca'))
            tls['ca'] = public.FileMd5(plugin_path + 'data/tls/' + client_uuid + '/ca.crt')
        if status == 'start':
            self._start_client(argv.client_id)
        client['tls'] = tls
        return self.__response_json(client)

    def update_frpc_client_status(self,argv):
        status = argv.status
        client_id = argv.client_id
        if status == 'start':
            res = self._start_client(client_id)
        if status == 'stop':
            res = self._stop_client(client_id)
        if status == 'reload':
            res = self._reload_client(client_id)
        return self.__response_json(res)

    # 删除frpc 的客户端的配置
    def delete_frpc_client(self, argv):
        db_obj = self.__db()
        self._stop_client(argv.client_id, False)
        client =  db_obj.table('frpc_clients').where('id = ?', argv.client_id).select()[0]
        db_obj.table('frpc_clients').where('id = ?', argv.client_id).delete()
        db_obj.table('frpc_proxys').where('client_id = ?', argv.client_id).delete()
        db_obj.table('frpc_config_detail').where('client_id = ? ', argv.client_id).delete()
        # 删除 日志,证书,配置文件
        os.system('rm -rf %sdata/log/%s' % (plugin_path,client['uuid']))
        os.system('rm -rf %sdata/tls/%s' % (plugin_path, client['uuid']))
        os.system('rm -rf %sdata/conf/frpc_%s.ini' % (plugin_path, client['uuid']))
        return self.__response_json(True)

    # 查询指定客户端的代理列表
    def get_frpc_proxy_list(self, argv):
        db_obj = self.__db()
        proxys = []
        proxy_list = db_obj.table('frpc_proxys').where('client_id = ?', argv.client_id).select()
        for proxy in proxy_list:
            proxy['config'] = []
            details = db_obj.table('frpc_config_detail').where('proxy_id = ?', proxy['id']).select()
            for detail in details:
                detail['detail_id'] = detail['id']
                del detail['id']
                proxy['config'].append(detail)
            proxy['proxy_id'] = proxy['id']
            del proxy['id']
            proxys.append(proxy)
        return self.__response_json(proxys)

    # 新增一个客户端的代理
    def create_frpc_proxy(self, argv):
        self._stop_client(argv.client_id, False)
        db_obj = self.__db()
        frpc_proxy = {'client_id': argv.client_id, 'proxy_type': argv.proxy_type, 'name': argv.proxy_name,
                      'extend': argv.proxy_extend}
        proxy_id = db_obj.table('frpc_proxys').insert(frpc_proxy)
        config_list = json.loads(argv.config_list)
        details = []
        for item in config_list:
            xconfig = db_obj.table("frpc_config").where('`group` = ? and `name` = ?', (item['group'],item['name'])).select()
            if len(xconfig) > 0:
                xconfig = xconfig[0]
                if 'value' not in item:
                    item['value'] = ''
                if xconfig['type'] == 'json':
                    item['value'] = json.dumps(item['value'])
                detail = {
                    'detail_type': 1, 'name': xconfig['name'], 'type': xconfig['type'], 'proxy_id': proxy_id,
                    'client_id': argv.client_id, '`value`': item['value'],
                    'content': xconfig['content'], '`default`': xconfig['default'], 'extend': xconfig['extend'],
                    'support': xconfig['support']
                }
                detail['detail_id'] = db_obj.table('frpc_config_detail').insert(detail)
                details.append(detail)
        self._start_client(argv.client_id)
        return self.__response_json({'config_list':config_list,'details':details})

    # 修改指定代理的配置
    def update_frpc_proxy(self, argv):
        db_obj = self.__db()
        self._stop_client(argv.client_id, False)
        proxy = {}
        update = {}
        if hasattr(argv, 'proxy_name'):
            update['name'] = getattr(argv, 'proxy_name')
            proxy['name'] = update['name']
        if hasattr(argv, 'proxy_extend'):
            update['extend'] = getattr(argv, 'proxy_extend')
            proxy['extend'] = update['extend']
        db_obj.table('frpc_proxys').where('id = ?', argv.proxy_id).update(update)
        config_list = json.loads(argv.config_list)
        for config in config_list:
            xconfig = db_obj.table("frpc_config_detail").where('proxy_id = ?  and `name` = ?',(argv.proxy_id, config['name'])).select()
            if len(xconfig) > 0:
                if 'value' not in config:
                    config['value'] = ''
                xconfig = xconfig[0]
                if xconfig['type'] == 'json':
                    config['value'] = json.dumps(config['value'])
                db_obj.table('frpc_config_detail').where('proxy_id = ? and `name` = ?', (argv.proxy_id,config['name'])).update({'value': config['value']})
                update[config['name']] = config['value']
        self._start_client(argv.client_id)
        return self.__response_json({'client_id': argv.client_id, 'proxy_id': argv.proxy_id, 'update': update})

    # 删除指定的代理的配置
    def delete_frpc_proxy(self, argv):
        db_obj = self.__db()
        self._stop_client(argv.client_id)
        db_obj.table('frpc_proxys').where('id = ?', argv.proxy_id).delete()
        db_obj.table('frpc_config_detail').where('proxy_id = ? ', argv.proxy_id).delete()
        self._start_client(argv.client_id)
        return self.__response_json({})

    # 查询指定的代理的配置信息
    def datail_frpc_proxy(self,argv):
        db_obj = self.__db()
        proxy =   db_obj.table('frpc_proxys').where('id = ?', argv.proxy_id).select()
        if len(proxy) == 0:
            return self.__response_json({'proxy_id':argv.proxy_id},500,'请求的proxy_id 不存在或者已经删除')
        else:
            proxy = proxy[0]
            proxy['config'] = []
            details = db_obj.table('frpc_config_detail').where('proxy_id = ?', proxy['id']).select()
            for detail in details:
                detail['detail_id'] = detail['id']
                del detail['id']
                proxy['config'].append(detail)
            proxy['proxy_id'] = proxy['id']
            return self.__response_json(proxy)

    # 修改指定的客户端的状态
    def update_client_status(self, argv):
        status = ['start', 'stop', 'reload']
        if argv.status in status:
            if status == 'start':
                update = self._start_client(argv.client_id)
            if status == 'stop':
                update = self._stop_client(argv.client_id)
            if status == 'reload':
                update = self._reload_client(argv.client_id)
            return self.__response_json({'update': update})
        else:
            return self.__response_json(None, 500, '请求的参数有误,status 必须是 [start,stop,reload] 中的一种')

    # 查询指定客户端的日志信息
    def get_client_log(self, argv):
        db_obj = self.__db()
        log_file = \
            db_obj.table('frpc_config_detail').where('client_id = ? and `name` = ?',
                                                     (argv.client_id, 'log_file')).select()[0]
        log = public.readFile('%s%s' % (plugin_path, log_file['value']))
        return self.__response_json(log)

    # 通过group 查询需要的配置信息
    def get_config_by_group(self, argv):
        db_obj = self.__db()
        _list = db_obj.table("frpc_config").where('`group` = ?', 'client').field(
            'name,value,type,content,support,extend,is_dev').select()
        return self.__response_json(_list)

    # 渲染指定的客户端的配置文件
    def format_config_client(self, argv):
        self._format_config(argv.client_id)
        configContent = public.readFile('%sdata/conf/frpc_%s.ini' % (plugin_path, str(argv.client_id)))
        return self.__response_json({'config': configContent})

    # 修改巡检方式
    def update_config_watch_type(self, argv):
        status = argv.status
        if status == 'thread':
            self._delete_watch_cronta()
            self._start_watch_thread()
        else:
            self._stop_watch_thread()
            self._create_watch_crontab()
        return self.__response_json(argv.status)

    # 修改掉线报警通知消息
    def update_config_msg_warning(self,argv):
        send = send_mail.send_mail()
        db_obj = self.__db()
        if argv.status == 'true':
            tunnel = send.get_settings()
            if not tunnel['user_mail']['user_name']:
                return self.__response_json({},500,'请先配置邮件通道!')
            else:
                db_obj.table('global_config').where('`name` = ?', 'frp_msg_warning').update({'value': 'true'})
        else:
            db_obj.table('global_config').where('`name` = ?', 'frp_msg_warning').update({'value': 'false'})
        return self.__response_json(argv.status)

    # 修改开机报警通知消息
    def update_config_msg_poweron(self,argv):
        send = send_mail.send_mail()
        db_obj = self.__db()
        if argv.status == 'true':
            tunnel = send.get_settings()
            if not tunnel['user_mail']['user_name']:
                return self.__response_json({}, 500, '请先配置邮件通道!')
            else:
                db_obj.table('global_config').where('`name` = ?', 'frp_msg_poweron').update({'value': 'true'})
        else:
            db_obj.table('global_config').where('`name` = ?', 'frp_msg_poweron').update({'value': 'false'})
        return self.__response_json(argv.status)

    def get_global_config(self,argv):
        db_obj = self.__db()
        res = {}
        res["watch_type"] =  db_obj.table('global_config').where('`name` = ?', 'frp_watch_type').select()[0]['value']
        res["crontab_id"] =  db_obj.table('global_config').where('`name` = ?', 'frp_watch_crontab_id').select()[0]['value']
        res["thread_id"]  =  db_obj.table('global_config').where('`name` = ?', 'frp_watch_thread_pid').select()[0]['value']
        if res['crontab_id'] == '' and res['thread_id'] == '':
            res['crontab_id'] = str(self._create_watch_crontab())
        if res['crontab_id'] !='':
            res['crontab_id'] = int(res['crontab_id'])
        if res['thread_id'] !='':
            res['thread_id'] = int(res['thread_id'])
            res["thread_running"] = psutil.pid_exists(int(res['thread_id']))
        else:
            res['thread_running'] = False
        res["msg_warning"] = db_obj.table('global_config').where('`name` = ?', 'frp_msg_warning').select()[0]['value']
        res["msg_poweron"] = db_obj.table('global_config').where('`name` = ?', 'frp_msg_poweron').select()[0]['value']
        return self.__response_json(res)

    # 巡检客户端状态
    def _check_up_status(self):
        db_obj = self.__db()
        is_send = db_obj.table('global_config').where('`name` = ?','frp_msg_warning').select()[0]['value']
        if is_send == 'true':
            is_send = True
        else:
            is_send = False
        clients = db_obj.table('frpc_clients').select()
        for client in clients:
            self.__log('巡检 client_id:%d,name:%s 的设备中...' % (client['id'],client['name']))
            if client['status'] == 'start':
                is_running = self._status_client(client['id'])['is_running']
                is_connect = self._connect_client(client['id'])
                is_warning = int(client['is_warning'])
                # 发送报警消息
                if is_warning != 1 and not ( is_running and is_connect ==1):
                    send = send_mail.send_mail()
                    if not is_running:
                        errmsg = '进程异常退出'
                        try:
                            self._start_client(client['id'])
                        except:
                            self.__log('尝试重启client_id:' + client['id'] +'的进程失败')
                    else:
                        errmsg = '连接服务器状态异常'
                    format_time = public.format_date()
                    panel_name = public.GetConfigValue('title')
                    local_ip = requests.get('https://ip.iw3c.top').text
                    config_ip = db_obj.table('frpc_config_detail').where('client_id = ? and `name` = ? and detail_type = ?',
                                                             (client['id'], 'server_addr', '0')).select()[0]['value']
                    config_port = db_obj.table('frpc_config_detail').where('client_id = ? and `name` = ? and detail_type = ?',
                                                             (client['id'], 'server_port', '0')).select()[0]['value']
                    self.__log('巡检 client_id:%s,name:%s 发现异常:%s' % (client['id'],client['name'],errmsg))
                    if is_send:
                        content = """
尊敬的用户你好,[UTC-8]%s,您在[%s](ip:%s)上运行的FRP客户端在连接服务端[%s]时状态异常,下面时关于异常的详情信息:
服务端名称:%s
备注信息:%s
服务端ip:%s
服务端通讯端口:%s
异常原因:%s

FRPC 客户端插件 copyright © <a href="https://www.atonal.cn">atonal.cn</a>
""" % (format_time, panel_name, local_ip, client['name'], client['name'],client['extend'], config_ip, config_port,errmsg)

                        try:
                            import mail_msg
                            content = content.replace('\n', "<br/>")
                            mail = mail_msg.mail_msg()
                            mail.send_msg(content, '[FRPC]异常报警')
                        except:
                            self.__log('尝试发送异常消息邮件遇到问题')
                        db_obj.table('frpc_clients').where('id = ?',client['id']).update({'is_warning':'1'})
                # 发送消警消息
                if is_warning == 1 and ( is_running and is_connect ==1):
                    self.__log('巡检 client_id:%s,name:%s 已自动消警' % (client['id'], client['name']))
                    format_time = public.format_date()
                    panel_name = public.GetConfigValue('title')
                    local_ip = requests.get('https://ip.iw3c.top').text
                    if is_send:
                        content = """
尊敬的用户你好,[UTC-8]%s,您在[%s](ip:%s)上运行的FRP客户端在连接服务端[%s]时发生的异常情况已经自动恢复。

FRPC 客户端插件 copyright © <a href="https://www.atonal.cn">atonal.cn</a>
""" % (format_time, panel_name, local_ip, client['name'])
                        try:
                            import mail_msg
                            content = content.replace('\n', "<br/>")
                            mail = mail_msg.mail_msg()
                            mail.send_msg(content, '[FRPC]异常消警')

                        except:
                            self.__log('尝试发送消警邮件遇到问题')
                        db_obj.table('frpc_clients').where('id = ?', client['id']).update({'is_warning': '0'})

            else:
                self._stop_client(client['id'])
            self.__log('巡检 client_id:%s,name:%s 的设备结束...' % (client['id'], client['name']))

    def _create_watch_crontab(self):
        import crontab
        obj = public.dict_obj()
        obj.name = 'FRP定时巡检'
        obj.type = 'minute-n'
        obj.where1 = 1
        obj.sType = 'toShell'
        obj.sBody = 'btpython /www/server/panel/plugin/frpc/frpc_main.py checkup'
        obj.save_local = 1
        obj.sName = ''
        obj.urladdress = ''
        obj.setup_path = ''
        obj.backupTo = ''
        btCrontab = crontab.crontab()
        res = btCrontab.AddCrontab(obj)
        db_obj = self.__db()
        db_obj.table('global_config').where('`name` = ?', 'frp_watch_type').update({'value': 'crontab'})
        db_obj.table('global_config').where('`name` = ?', 'frp_watch_crontab_id').update({'value': res['id']})
        return res['id']

    def _delete_watch_cronta(self):
        import crontab
        db_obj = self.__db()
        crontab_id =  db_obj.table('global_config').where('`name` = ?', 'frp_watch_crontab_id').select()[0]['value']
        if crontab_id != '':
            crontab_id = int(crontab_id)
            btCrontab = crontab.crontab()
            obj={'id':crontab_id}
            btCrontab.DelCrontab(obj)
            db_obj.table('global_config').where('`name` = ?', 'frp_watch_type').update({'value': 'thread'})
            db_obj.table('global_config').where('`name` = ?', 'frp_watch_crontab_id').update({'value': ''})

    def _start_client(self, client_id):
        status = self._status_client(client_id)
        if status['is_running']:
            return True
        else:
            # 重新编译配置文件
            self._format_config(client_id)
            pid = public.ExecShell('nohup ./bin/frpc -c ./data/conf/frpc_' + self.__get_client_uuid(client_id) + '.ini & \n echo $! ',
                                   None, True, plugin_path)
            pid = re.findall(r"^\d+",pid[0])[0]
            db_obj = self.__db()
            db_obj.table('frpc_clients').where('id = ?', client_id).update(
                {'pid': pid, 'status': 'start', 'is_warning': 0})
            try:
                if psutil.pid_exists(int(pid)):
                    return True
                else:
                    return False
            except:
                return False

    def _stop_client(self, client_id, pid=False):
        db_obj = self.__db()
        if not pid:
            try:
                pid = db_obj.table('frpc_clients').where('id = ?', client_id).field('status,pid,is_warning').select()[0]['pid']
            except:
                pid = ''
        if pid == '':
            return True
        else:
            db_obj.table('frpc_clients').where('id = ?', client_id).update(
                {'pid': '', 'status': 'stop', 'is_warning': 0})
            try:
                if psutil.pid_exists(int(pid)):
                    os.system('kill -9 ' + str(pid))
            except:
                pass

        return True

    def _reload_client(self, client_id):
        self._stop_client(client_id)
        print('停止frpc 的客户端成功')
        return self._start_client(client_id)

    def _connect_client(self,client_id):
        status = self._status_client(client_id)
        if not status['is_running']:
            return -2
        client_uuid = self.__get_client_uuid(client_id)
        logpath = plugin_path + 'data/log/' + client_uuid + '/frpc.log'
        if not os.path.exists(logpath):
            return -2
        logcontent = public.readFile(logpath)
        logcontent = logcontent.split("\n")
        lines = len(logcontent)
        i = lines - 1
        while i>=0:
            line = logcontent[i]
            if line.find('login to server success') != -1:
                return 1
            if line.find('try to reconnect to server') != -1:
                return 0
            if line.find('login to server failed') != -1:
                return -1
            i = i - 1
        return 1


    def _status_client(self, client_id):
        db_obj = self.__db()
        client = db_obj.table('frpc_clients').where('id = ?', client_id).field('status,pid,is_warning').select()[0]
        try:
            if psutil.pid_exists(int(client['pid'])):
                client['is_running'] = True
            else:
                client['is_running'] = False
        except:
            client['is_running'] = False
        return client

    def _format_config(self, client_id):
        config = """# 本配置文件由宝塔面板 frp 客户插件自动生成
# 本配置文件会在每次启动时自动更新,请不要手动修改该配置文件
# 生成时间 ： %s

# 服务端连接配置
[common]
""" % public.format_date()
        db_obj = self.__db()
        base_list = db_obj.table('frpc_config_detail').where('client_id = ? and detail_type = 0',
                                                             client_id).select()
        for c in base_list:
            if not c['support']:
                c['support'] = ''
            if not c['default']:
                c['default'] = ''
            if not c['value']:
                c['value'] = ''
            config = config + "\n # 配置项: " + c['name'] + "\n # 参数类型: " + c['type'] + '\n # 默认值: ' + c['default']
            config = config + "\n # 可选值: " + c['support'] + "\n # 用途: " + c['content']
            if c['extend']:
                config = config + '\n # 备注: ' + c['extend']
            if c['value'] != "0" and c['value'] != "":
                config = config + ("\n %s = %s\n" % (c['name'], c['value']))
            else:
                config = config + ("\n# %s = %s\n" % (c['name'], c['value']))

        config = config + "\n\n\n#客户端代理配置"
        proxy_list = db_obj.table('frpc_proxys').where('client_id = ?', client_id).select()
        for proxy in proxy_list:
            config = config + "\n\n[" + proxy['proxy_type'] + '_' + proxy['name'] + "]\n"
            config = config + """
 # 配置项: type
 # 参数类型: string
 # 默认值: tcp
 # 可选值: tcp, udp, http, https, stcp, sudp, xtcp, tcpmux
 # 用途: 代理类型
 type = %s	
""" % proxy['proxy_type']
            detail_list = db_obj.table('frpc_config_detail').where('proxy_id = ? and detail_type = 1',
                                                                   proxy['id']).select()
            for detail in detail_list:
                if not detail['support']:
                    detail['support'] = ''
                if not detail['default']:
                    detail['default'] = ''
                if not detail['value']:
                    detail['value'] = ''
                config = config + "\n # 配置项: " + detail['name'] + "\n # 参数类型: " + detail['type'] + '\n # 默认值: ' + detail['default']
                config = config + "\n # 可选值: " + detail['support'] + "\n # 用途: " + detail['content']
                if detail['value'] != "":
                    if detail['type'] != 'json':
                        config = config + ("\n %s = %s\n" % (detail['name'], detail['value']))
                    else:
                        _value = json.loads(detail['value'])
                        if len(_value) == 0:
                            config = config + ("\n# %s = \n" % (detail['name']))
                        else:
                            if detail['name'] != 'headers':
                                value = ''
                                for v in _value:
                                    if value != '':
                                        value = value + ',' + v
                                    else:
                                        value = v
                                config = config + ("\n %s = %s\n" % (detail['name'], value))
                            else:
                                for item in _value:
                                    config = config + ("\n header_%s = %s" % (item['key'], item['val']))
                else:
                    config = config + ("\n# %s = %s\n" % (detail['name'], detail['value']))
        client_uuid = self.__get_client_uuid(client_id)
        public.writeFile('%sdata/conf/frpc_%s.ini' % (plugin_path, client_uuid), config)
        return '%sdata/conf/frpc_%s.ini' % (plugin_path, client_uuid)

    def _get_frp_version_update(self):
        db_obj = self.__db()
        frp_versions_cache = int(
            db_obj.table('global_config').where('`name` = ?', 'frp_version_cache').select()[0]['value'])
        if frp_versions_cache < int(time.time()):
            frp_versions = None
        else:
            frp_versions = json.loads(
                db_obj.table('global_config').where('`name` = ?', 'frp_version').select()[0]['value'])
        if frp_versions:
            return frp_versions
        else:
            try:
                resp = requests.get('https://cdn.iw3c.com.cn/bt-plugin/frp/data.json?t=' + str(int(time.time())))
                data = json.loads(resp.text)
                db_obj.table('global_config').where('`name` = ?', 'frp_version').update({'value': json.dumps(data)})
                db_obj.table('global_config').where('`name` = ?', 'frp_version_cache').update(
                    {'value': str(int(time.time()) + 3600 * 24)})
            except:
                frp_versions = db_obj.table('global_config').where('`name` = ?', 'frp_version').select()[0]['value']
                if frp_versions:
                    data = json.loads(frp_versions)
                else:
                    data = None
            return data

    # 从云端获取frpc的下载地址和版本信息数据
    def _get_frpc_download(self, argv):
        frp_version_list = self._get_frp_version_update()
        if hasattr(argv, 'version'):
            _version = argv.version
        else:
            _version = frp_version_list['last_version']
        if _version in frp_version_list['version']:
            version = _version
        else:
            version = frp_version_list['last_version']
        download = frp_version_list['version'][version]['linux']
        download['version'] = version
        return download

    def _install_frpc(self, download, force=False):
        if not os.path.exists(plugin_path + 'bin/') or force:
            if force:
                os.system(('rm -rf %sbin') % plugin_path)
            os.mkdir(plugin_path + 'bin/')
            print('从云端下载frp[%s]中...' % download['version'])
            os.system("wget %s -O %sbin/%s" % (download['url'], plugin_path, download['name']))
            os.system("cd %sbin && tar -zxvf %sbin/%s" % (plugin_path, plugin_path, download['name']))
            os.remove("%sbin/%s" % (plugin_path, download['name']))
            dir_name = download['name'].replace('.tar.gz', '')
            os.system("rm -rf %sbin/%s/*.ini" % (plugin_path, dir_name))
            os.remove("%sbin/%s/frps" % (plugin_path, dir_name))
            os.remove("%sbin/%s/LICENSE" % (plugin_path, dir_name))
            public.writeFile("%sbin/%s/version.json" % (plugin_path, dir_name), json.dumps(download))
            os.system("mv %sbin/%s/* %sbin/" % (plugin_path, dir_name, plugin_path))
            os.system("rm -rf %sbin/%s/" % (plugin_path, dir_name))
            print('frpc 内核安装成功,版本:' + download['version'])
            db_obj = self.__db()
            db_obj.table('global_config').where('`name` = ?', 'core_version').update({'value': download['version']})
        else:
            version = json.loads(public.readFile(plugin_path + 'bin/version.json'))['version']
            print('frpc 内核已经安装,版本:' + version)

    def _init_frpc(self):

        # 新建用于 存放数据,配置的目录
        if not os.path.exists(plugin_path + 'data'):
            os.mkdir(plugin_path + 'data')
        if not os.path.exists(plugin_path + 'data/conf'):
            os.mkdir(plugin_path + 'data/conf')
        if not os.path.exists(plugin_path + 'data/log'):
            os.mkdir(plugin_path + 'data/log')
        if not os.path.exists(plugin_path + 'data/tls'):
            os.mkdir(plugin_path + 'data/tls')

        # 初始化数据库
        db_obj = self.__db()
        db_obj.fofile(plugin_path + 'db.sql')

        db_obj.table('global_config').insert({'name': 'core_version', 'value': '', '`group`': 'all', 'extend': 'frp的内核版本'})
        db_obj.table('global_config').insert({'name': 'frp_version', 'value': '', '`group`': 'version', 'extend': 'frp 云端数据缓存'})
        db_obj.table('global_config').insert({'name': 'frp_version_cache', 'value': '0', '`group`': 'version', 'extend': 'frp 云端数据缓存过期时间'})

        db_obj.table('global_config').insert({'name': 'frp_watch_type', 'value': 'crontab', '`group`': 'base', 'extend': 'frp 巡检方式'})
        db_obj.table('global_config').insert({'name': 'frp_watch_crontab_id', 'value': '', '`group`': 'base', 'extend': 'frp 异步巡检任务的id'})
        db_obj.table('global_config').insert({'name': 'frp_watch_thread_pid', 'value': '', '`group`': 'base', 'extend': 'frp 异步巡检任务的pid'})
        db_obj.table('global_config').insert({'name': 'frp_msg_warning', 'value': 'false', '`group`': 'base', 'extend': 'frp 掉线自动报警'})
        db_obj.table('global_config').insert({'name': 'frp_msg_poweron', 'value': 'false', '`group`': 'base', 'extend': 'frp 开机自动报警'})


    # 开机启动客户端
    def _auto_run(self):
        db_obj = self.__db()
        clients = db_obj.table('frpc_clients').select()
        for client in clients:
            if client['auto_run'] == 'start':
                self._start_client(client['id'])
            else:
                self._stop_client(client['id'])
        is_send = db_obj.table('global_config').where('`name` = ?', 'frp_msg_poweron').select()[0]['value']
        if is_send == 'true':
            is_send = True
        else:
            is_send = False
        if is_send:
            send = send_mail.send_mail()
            format_time = public.format_date()
            panel_name  = public.GetConfigValue('title')
            local_ip    = requests.get('https://ip.iw3c.top').text

            content="""
尊敬的用户你好,[UTC-8]%s,您在[%s](ip:%s)上运行的FRP客户端插件在服务器开机后已经自动启动

FRPC 客户端插件 copyright © <a href="https://www.atonal.cn">atonal.cn</a>
""" % (format_time,panel_name,local_ip)
            try:
                import mail_msg
                content = content.replace('\n', "<br/>")
                mail = mail_msg.mail_msg()
                mail.send_msg(content, '[FRPC]开机通知')
            except:
                self.__log('尝试发送开机通知邮件遇到问题')
        watch_type = db_obj.table('global_config').where('`name` = ?', 'frp_watch_type').select()[0]['value']
        if watch_type == 'thread':
            self._start_watch_thread()

    def _start_watch_thread(self):
        db_obj = self.__db()
        pid = db_obj.table('global_config').where('`name` = ?', 'frp_watch_thread_pid').select()[0]['value']
        if pid != '':
            if psutil.pid_exists(int(pid)):
                os.system('kill -9 '+str(pid))

        pid = public.ExecShell('nohup btpython frpc_watch.py > frpc_watch.log & \n echo $! ',None, True, plugin_path)
        pid = re.findall(r"^\d+", pid[0])[0]
        db_obj.table('global_config').where('`name` = ?', 'frp_watch_thread_pid').update({'value':pid})
        db_obj.table('global_config').where('`name` = ?', 'frp_watch_type').update({'value': 'thread'})

    def _stop_watch_thread(self):
        db_obj = self.__db()
        pid = db_obj.table('global_config').where('`name` = ?', 'frp_watch_thread_pid').select()[0]['value']
        if pid != '':
            if psutil.pid_exists(int(pid)):
                os.system('kill -9 ' + str(pid))
        db_obj.table('global_config').where('`name` = ?', 'frp_watch_thread_pid').update({'value': ''})
        db_obj.table('global_config').where('`name` = ?', 'frp_watch_type').update({'value': 'thread'})

    def _stop_all(self):
        db_obj = self.__db()
        clients = db_obj.table('frpc_clients').select()
        for client in clients:
            self._stop_client(client['id'],client['pid'])



    # 新建定时任务
    def __response_json(self, data, code=0, msg=''):
        response = {"code": code, "msg": msg, "data": data}
        return response



    def __get_client_uuid(self,client_id):
        db_obj = self.__db()
        client = db_obj.table('frpc_clients').where('id = ?', client_id).select()[0]
        return client['uuid']

    def __log(self,content):
        print("[" + public.format_date() + "]:" + content)

    def __db(self):
        obj = db.Sql()
        obj.dbfile(db_path)
        return obj


if __name__ == '__main__':

    argv = sys.argv
    _func = ['auto_run', 'uninstall', 'install', 'init', 'checkup']
    try:
        func = argv[1]
        if not func in _func:
            print('[ERROR]: Please input corrent function name ! ')
            print('Support function: auto_run/install/unistall/checkup')
            exit(0)
    except:
        print('[ERROR]: Please input corrent function name ! ')
        print('Support function: auto_run/install/unistall/checkup')
        exit(0)

    frpc = frpc_main()

    # 初始化插件
    if func == 'init':
        frpc._init_frpc()

    # 安装插件内核
    if func == 'install':
        if len(argv) != 3:
            frpc._install_frpc(frpc._get_frpc_download(public.dict_obj()))
        else:
            get = public.dict_obj()
            get.version = argv[2]
            frpc._install_frpc(frpc._get_frpc_download(get), True)


    if func == 'uninstall':
        frpc._stop_watch_thread()
        frpc._stop_all()


    # 开机启动客户端
    if func == 'auto_run':
        frpc._auto_run()


    # 巡检客户端
    if func == 'checkup':
        print("[" + public.format_date() + "]开始巡检")
        frpc._check_up_status()
        print("[" + public.format_date() + "]巡检结束")







