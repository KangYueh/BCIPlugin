# step1：首先连接局域网，并设置IP地址为10.10.10.X，X为任意100~255
# step2：打开NetStation软件，连接好，等待连接
# step3：运行脚本


from egi_pynetstation.NetStation import NetStation

# Set an IP address for the computer running NetStation as an IPv4 string
IP_ns = '10.10.10.42'
# Set a port that NetStation will be listening to as an integer
port_ns = 55513
ns = NetStation(IP_ns, port_ns)
# Set an NTP clock server (the amplifier) address as an IPv4 string
IP_amp = '10.10.10.51'
ns.connect(ntp_ip=IP_amp)
# Do whatever setup for your experiment here...
# Begin recording
ns.begin_rec()
# You can now send events; this one just says "HIYA" and automatically
# marks the time for you
ns.send_event(event_type="HIYA")
# You can include a data dictionary; perhaps you have a dog stimulus
my_data = {"dogs": "fido"}
# Send this data with the event type of "STIM"
ns.send_event(event_type="STIM", data=my_data)
# With the experiment concluded, you can end the recording
ns.end_rec()
# You'll want to disconnect the amplifier when your program is done
ns.disconnect()


