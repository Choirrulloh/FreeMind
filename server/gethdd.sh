#!/bin/bash

# FreeMind is a composition of software and config files. It will help you to manage your Linux fileserver.
# Copyright (C) 2017  Daniel Körsten aka TechnikAmateur
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# this script must run as sudo!
if [[ $EUID != 0 ]]; then
  exit 1
fi
# get S.M.A.R.T.
while read line; do
  if [[ $line == *"#"* ]] || [[ $line == *"<"* ]]; then
    :
  else
    hdd="$(echo $line | awk '$1 ~ "/dev" {print $1}')"
    status="$(smartctl -H $hdd | grep result | awk '{print $6}')"
  fi
done < disks.conf
