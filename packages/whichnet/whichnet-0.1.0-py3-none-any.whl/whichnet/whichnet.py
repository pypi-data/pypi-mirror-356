#!/usr/bin/env python3
from scapy.all import *
import os
import argparse
import ipaddress
import threading
import datetime, time

class WhichNet:

	def __init__(self):
		self.seen_addresses = {
				#'mac addr': {ips:[], related_ips:[], related_operations:[]}
			}
		self.seen_vlans = {
			#vlanid : {ips:[]}
		}
		self.interface = None
		self.DEBUG = False
		self.stopping = False
		self.count_ips = 0
		self.scanned_ips = 0
		self.display_width = 30
		self.last_display = datetime.datetime.now()
		self.quiet=False
		self.sniff_thread=None

	#create a function the capture all packets with arp protocol on a given interface
	def sniff_arp(self,interface, operation):
		try:
			self.interface = interface
			self.clear()
			#sniff(iface=interface, store=False, prn=process_sniffed_packet, filter="arp" )
			if operation != "all":
				filter = "arp and arp [6:2] = "
			else:
				filter = "arp"
			sniff(iface=interface, store=False, prn=self.process_sniffed_packet, filter=filter, stop_filter=lambda x: self.stopping)
		except KeyboardInterrupt:
			STOPPING = True
			return

	def clear(self):
		if self.quiet:
			return
		os.system("clear")
		print("Sniffing on interface " + self.interface + "...")
		print("Scanned " + str(self.scanned_ips) + " of " + str(self.count_ips) + " IPs")
		print("")

	def update_display(self):
		if self.quiet:
			return
		"""show all entries in seen addresses, with columns for mac, ips, related ips, related operations, and count, sorted by count desc. With the ips and related ips one per line."""
		if self.last_display + datetime.timedelta(seconds=1) > datetime.datetime.now():
			return
		self.last_display = datetime.datetime.now()
		self.clear()
		print("MAC\t\t\tIPs\t\tRelated IPs\tRelated Operations\tCount")
		print("-" * self.display_width)
		for mac, info in sorted(self.seen_addresses.items(), key=lambda x: x[1]['count'], reverse=True):
			ips = info['ips'].copy()
			ips=sorted(ips, reverse=True)
			related_ips = info['related_ips'].copy()
			related_ips=sorted(related_ips, reverse=True)
			print(mac + "\t" + str(ips.pop() if ips else "1\t") + "\t" + str(related_ips.pop() if related_ips else "2\t") + "\t" + str(
				info['related_operations']) + "\t\t\t" + str(info['count']))
			while ips or related_ips:
				print("\t\t"+str(ips.pop() if ips else "\t\t") + "\t" + str(related_ips.pop() if related_ips else "2\t\t"))
		print("\n" +"=" * self.display_width + "\nVLAN\t\tIPs")
		print("-" * self.display_width)
		for vlan, ips in self.seen_vlans.items():
			if not ips:
				continue
			ips=ips.copy()
			print(f"{vlan}\t\t{ips.pop()}")
			while ips:
				print(f"\t\t{ips.pop()}")
		if self.DEBUG:
			print(self.seen_addresses)
			print(self.seen_vlans)


	#create a function to process the captured packets
	def process_sniffed_packet(self,packet):
		src_ip=None
		dst_ip=None
		if packet.haslayer(ARP):
			src_mac = packet[ARP].hwsrc
			src_ip = ipaddress.ip_address(packet[ARP].psrc)
			dst_ip = ipaddress.ip_address(packet[ARP].pdst)
			op = 0
			if not src_mac in self.seen_addresses:
				self.seen_addresses[src_mac] = {'ips': [], 'related_ips': [], 'related_operations': [], 'count': 0}
			if self.DEBUG:
				print(packet.show())

			if packet[ARP].op == 1:
				op = 1
			elif packet[ARP].op == 2:
				op = 2
			else:
				print("Unknown operation : " + str(packet[ARP].op))

			if not src_ip in self.seen_addresses[src_mac]['ips']:
				self.seen_addresses[src_mac]['ips'].append(src_ip)
			if not dst_ip in self.seen_addresses[src_mac]['related_ips']:
				self.seen_addresses[src_mac]['related_ips'].append(dst_ip)
			if not op in self.seen_addresses[src_mac]['related_operations']:
				self.seen_addresses[src_mac]['related_operations'].append(op)
			self.seen_addresses[src_mac]['count'] += 1

			self.update_display()

		vlan_id=None
		if Dot1Q in packet:
			vlan_layer = packet[Dot1Q]
			vlan_id=vlan_layer.vlan
	#		print(f"[+] VLAN ID: {vlan_layer.vlan}")
		if not vlan_id in self.seen_vlans:
			self.seen_vlans[vlan_id]=[]
		if src_ip and not src_ip in self.seen_vlans[vlan_id]:
			self.seen_vlans[vlan_id].append(src_ip)
		if dst_ip and not dst_ip in self.seen_vlans[vlan_id]:
			self.seen_vlans[vlan_id].append(dst_ip)
		self.update_display()

	def scan(self,ranges,interface):
		try:
			for r in ranges:
				self.count_ips += r.num_addresses
			s = conf.L2socket(iface=interface)
			for r in ranges:
				for ip in r.hosts():
					arp = ARP(pdst=str(ip))
					broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
					arp_broadcast = broadcast/arp
					s.send(arp_broadcast)
					self.scanned_ips += 1
					if self.stopping:
						return
			self.update_display()

		except KeyboardInterrupt:
			self.stopping = True
			return

	def run_async(self,interface,arp_operations="all"):
		"""Run without display"""
		if not os.getuid() == 0:
			print("This program must be run as root.")
			exit(1)
		if self.sniff_thread:
			print("Thread already running")
		self.quiet = True

		self.sniff_thread = threading.Thread(target=self.sniff_arp, args=(interface, arp_operations))
		self.sniff_thread.start()

	def stop(self):
		if not self.sniff_thread:
			print("No running thread")
			return
		self.stopping=True
		self.sniff_thread.join()
		self.sniff_thread=None

	def main(self):
		"""parse command line arguments with interface, passive or active mode and operation 1,2 or all and multiple ip addresses scan range"""
		if not os.getuid() == 0:
			print("This program must be run as root.")
			exit(1)

		argparser = argparse.ArgumentParser()
		argparser.add_argument("-i", "--interface", help="Interface to sniff on", required=True)
		argparser.add_argument("-p", "--passive", help="Passive mode", action="store_true", default=False)
		argparser.add_argument("-o", "--operation", help="Operation to sniff for (1, 2, or all)", default="2", choices=["1", "2", "all"])
		argparser.add_argument("-r", "--range", help="IP range to scan, can have multiple", action="append")
		argparser.add_argument("-w", "--wait", help="Wait when scan finished, else exit", action="store_true", default=True)
		args = argparser.parse_args()

		if args.passive and args.range:
			print("Passive mode and IP range are mutually exclusive.")
			exit(1)

		if not args.passive and not args.range:
			print("Active mode requires an IP range.")
			exit(1)

		if not args.passive:
			ranges = []
			for r in args.range:
				try:
					ranges.append(ipaddress.ip_network(r,strict=True))
				except ValueError:
					print("Invalid IP range: " + r)
					exit(1)

		#Start sniffing thread
		sniff_thread = threading.Thread(target=self.sniff_arp, args=(args.interface, args.operation))
		sniff_thread.start()

		#Start scanning thread
		scan_thread = None
		if not args.passive:
			scan_thread = threading.Thread(target=self.scan, args=(ranges,args.interface))
			#grant time for sniff thread to start
			time.sleep(1)
			scan_thread.start()

		while True:
			try:
				if not args.wait:
					break
				time.sleep(0.1)
				self.update_display()
			except KeyboardInterrupt:
				self.stopping = True
				break

		if scan_thread:
			scan_thread.join()

		#senmd a packet to trigger a sniff dislock
		arp = ARP(pdst=str("192.168.1.1"),op=int(args.operation) if args.operation != "all" else 2)
		broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
		arp_broadcast = broadcast/arp
		sendp(arp_broadcast, iface=args.interface, verbose=False)

		sniff_thread.join()

if __name__ == "__main__":
	wn=WhichNet()
	wn.main()
	#To run in another python script
	# wn.run_async("enx0050b61b1c31")
	# time.sleep(10)
	# wn.stop()
	# print(wn.seen_vlans)