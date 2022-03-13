#!/bin/sh

VERSION="ng"
ADVISORY="This script should be used for authorized penetration testing and/or educational purposes only. Any misuse of this software will not be the responsibility of the author or of any other collaborator. Use it at your own computers and/or with the computer owner's permission."

###########################################
#-------) Checks pre-everything (---------#
###########################################
if ([ -f /usr/bin/id ] && [ "$(/usr/bin/id -u)" -eq "0" ]) || [ "`whoami 2>/dev/null`" = "root" ]; then
  IAMROOT="1"
  MAXPATH_FIND_W="3"
else
  IAMROOT=""
  MAXPATH_FIND_W="7"
fi


###########################################
#---------------) Colors (----------------#
###########################################

C=$(printf '\033')
RED="${C}[1;31m"
SED_RED="${C}[1;31m&${C}[0m"
GREEN="${C}[1;32m"
SED_GREEN="${C}[1;32m&${C}[0m"
YELLOW="${C}[1;33m"
SED_YELLOW="${C}[1;33m&${C}[0m"
SED_RED_YELLOW="${C}[1;31;103m&${C}[0m"
BLUE="${C}[1;34m"
SED_BLUE="${C}[1;34m&${C}[0m"
ITALIC_BLUE="${C}[1;34m${C}[3m"
LIGHT_MAGENTA="${C}[1;95m"
SED_LIGHT_MAGENTA="${C}[1;95m&${C}[0m"
LIGHT_CYAN="${C}[1;96m"
SED_LIGHT_CYAN="${C}[1;96m&${C}[0m"
LG="${C}[1;37m" #LightGray
SED_LG="${C}[1;37m&${C}[0m"
DG="${C}[1;90m" #DarkGray
SED_DG="${C}[1;90m&${C}[0m"
NC="${C}[0m"
UNDERLINED="${C}[5m"
ITALIC="${C}[3m"


###########################################
#---------) Parsing parameters (----------#
###########################################
# --) FAST - Do not check 1min of procceses and su brute
# --) SUPERFAST - FAST & do not search for special filaes in all the folders

if uname 2>/dev/null | grep -q 'Darwin' || /usr/bin/uname 2>/dev/null | grep -q 'Darwin'; then MACPEAS="1"; else MACPEAS=""; fi
FAST="1" #By default stealth/fast mode
SUPERFAST=""
DISCOVERY=""
PORTS=""
QUIET=""
CHECKS="system_information,container,procs_crons_timers_srvcs_sockets,network_information,users_information,software_information,interesting_files"
WAIT=""
PASSWORD=""
NOCOLOR=""
DEBUG=""
AUTO_NETWORK_SCAN=""
EXTRA_CHECKS=""
THREADS="$( ( (grep -c processor /proc/cpuinfo 2>/dev/null) || ( (command -v lscpu >/dev/null 2>&1) && (lscpu | grep '^CPU(s):' | awk '{print $2}')) || echo -n 2) | tr -d "\n")"
[ -z "$THREADS" ] && THREADS="2" #If THREADS is empty, put number 2
[ -n "$THREADS" ] && THREADS="2" #If THREADS is null, put number 2
[ "$THREADS" -eq "$THREADS" ] 2>/dev/null && : || THREADS="2" #It THREADS is not a number, put number 2
HELP=$GREEN"Enumerate and search Privilege Escalation vectors.
${NC}This tool enum and search possible misconfigurations$DG (known vulns, user, processes and file permissions, special file permissions, readable/writable files, bruteforce other users(top1000pwds), passwords...)$NC inside the host and highlight possible misconfigurations with colors.
      ${YELLOW}-h${BLUE} To show this message
      ${YELLOW}-q${BLUE} Do not show banner
      ${YELLOW}-e${BLUE} Perform extra enumeration
      ${YELLOW}-s${BLUE} SuperFast (don't check some time consuming checks) - Stealth mode
      ${YELLOW}-a${BLUE} All checks (1min of processes and su brute) - Noisy mode, for CTFs mainly
      ${YELLOW}-w${BLUE} Wait execution between big blocks of checks
      ${YELLOW}-N${BLUE} Do not use colours
      ${YELLOW}-D${BLUE} Debug mode
      ${YELLOW}-P${BLUE} Indicate a password that will be used to run 'sudo -l' and to bruteforce other users accounts via 'su'
      ${YELLOW}-o${BLUE} Only execute selected checks (system_information,container,procs_crons_timers_srvcs_sockets,network_information,users_information,software_information,interesting_files). Select a comma separated list.
      ${YELLOW}-L${BLUE} Force linpeas execution.
      ${YELLOW}-M${BLUE} Force macpeas execution.
      ${YELLOW}-d <IP/NETMASK>${BLUE} Discover hosts using fping or ping.$DG Ex: -d 192.168.0.1/24
      ${YELLOW}-p <PORT(s)> -d <IP/NETMASK>${BLUE} Discover hosts looking for TCP open ports (via nc). By default ports 22,80,443,445,3389 and another one indicated by you will be scanned (select 22 if you don't want to add more). You can also add a list of p