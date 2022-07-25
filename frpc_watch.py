#! /usr/bin/btpython
#  coding: utf-8
import os,sys,time

import frpc_main

os.chdir("/www/server/panel")
sys.path.append("class/")

import public

if __name__ == '__main__':
    frpc = frpc_main.frpc_main()
    while True:
        # try:
        #     print("[" + public.format_date() + "]开始巡检")
        #     frpc._check_up_status()
        #     print("[" + public.format_date() + "]巡检结束")
        # except:
        #     print("[" + public.format_date() + "]巡检过程中遇到错误")
        frpc._check_up_status()
        time.sleep(0.5)