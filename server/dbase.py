#!/usr/bin/python3
"""
FreeMind is a composition of software and config files. It will help you to manage your Linux fileserver.
Copyright (C) 2017  Daniel Körsten aka TechnikAmateur

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
# -*- coding: utf-8 -*-
import sqlite3
import os
import sys # remove if there are not sys args.
import time


# function create databse if not exists
def create():
    if not os.path.isfile("freemind.db"):
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS errorlog(
                          id INTEGER PRIMARY KEY,
                          error INTEGER,
                          date TEXT,
                          time TEXT);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS updatelog(
                          id INTEGER PRIMARY KEY,
                          date TEXT,
                          time TEXT,
                          update INTEGER);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS backupready(
                          id INTEGER PRIMARY KEY,
                          ready INTEGER);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS backuplog(
                          id INTEGER PRIMARY KEY,
                          date TEXT,
                          time TEXT,
                          error INTEGER);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS memory(
                          id INTEGER PRIMARY KEY,
                          total TEXT,
                          free TEXT,
                          drive INTEGER);""")
        connection.commit()
        connection.close()


# function insert error in db
def inserterror(dberror):
    x = 0
    dberror = int(dberror)
    dbdate = time.strftime("%Y-%m-%d", time.gmtime())
    dbtime = time.strftime("%H-%M", time.gmtime())
    connection = sqlite3.connect("freemind.db")
    cursor = connection.cursor()
    for i in range(1, 9999):
        try:
            # yapf: disable
            cursor.execute("""INSERT INTO errorlog(id, error, date, time)
                              VALUES(?,?,?,?)""", (i, dberror, dbdate, dbtime))
            # yapf: enable
            connection.commit()
        except:
            x = x + 1  # only that something is happening
        else:
            break
    connection.close()
    if i >= 9998:
        os.remove("freemind.db")
        create()
        x = 0
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        for i in range(1, 9999):
            try:
                # yapf: disable
                cursor.execute("""INSERT INTO errorlog(id, error, date, time)
                                  VALUES(?,?,?,?)""", (i, dberror, dbdate, dbtime))
                # yapf: enable
                connection.commit()
            except:
                x = x + 1  # only that something is happens
            else:
                break
        connection.close()
