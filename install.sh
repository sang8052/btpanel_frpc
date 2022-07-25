#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH


install_path=/www/server/panel/plugin/frpc


#安装
Install()
{
	
	echo '正在安装...'
	#==================================================================

	#依赖安装开始
  echo 'IW3C 已经更名为南京无调网络工作室,无调云官网即将上线,尽情期待...'
  echo 'https://cdn.iw3c.com.cn 为本插件提供CDN 支持'

  rm -rf $install_path/bin/


  #安装插件的logo
  if [ ! -f "/www/server/panel/BTPanel/static/img/soft_ico/ico-frpc.png" ];then
      cp $install_path/icon.png /www/server/panel/BTPanel/static/img/soft_ico/ico-frpc.png
  fi
  # 初始化插件
  btpython $install_path/frpc_main.py init
  btpython $install_path/frpc_main.py install last_version

  sed -i '/frpc_main.py/d' /etc/rc.d/rc.local && chmod +x /etc/rc.d/rc.local
  echo "btpython /www/server/panel/plugin/frpc/frpc_main.py autorun" >> /etc/rc.d/rc.local && chmod +x /etc/rc.d/rc.local

	echo '================================================'
	echo '安装完成'
}

#卸载
Uninstall()
{
   sed -i '/frpc_main.py/d' /etc/rc.d/rc.local && chmod +x /etc/rc.d/rc.local
   btpython $install_path/frpc_main.py uninstall
	 rm -rf $install_path
}

#操作判断
if [ "${1}" == 'install' ];then
	Install
elif [ "${1}" == 'uninstall' ];then
	Uninstall
else
	echo 'Error!';
fi
