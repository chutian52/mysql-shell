import subprocess
import time
import sys
import datetime
import platform
import os
import threading
import functools
import unittest
import json
import xmlrunner
import shutil

from testFunctions import read_line
from testFunctions import read_til_getShell
from testFunctions import kill_process
from testFunctions import exec_xshell_commands


############   Retrieve variables from configuration file    ##########################
class LOCALHOST:
    user =""
    password = ""
    host = ""
    xprotocol_port = ""
    port =""
class REMOTEHOST:
    user = ""
    password =""
    host = ""
    xprotocol_port = ""
    port = ""

if 'CONFIG_PATH' in os.environ and 'MYSQLX_PATH' in os.environ and os.path.isfile(os.environ['CONFIG_PATH']) and os.path.isfile(os.environ['MYSQLX_PATH']):
    # **** JENKINS EXECUTION ****
    config_path = os.environ['CONFIG_PATH']
    config=json.load(open(config_path))
    MYSQL_SHELL = os.environ['MYSQLX_PATH']
    Exec_files_location = os.environ['AUX_FILES_PATH']
    cluster_Path = os.environ['CLUSTER_PATH']
    XSHELL_QA_TEST_ROOT = os.environ['XSHELL_QA_TEST_ROOT']
    XMLReportFilePath = XSHELL_QA_TEST_ROOT+"/adminapi_qa_test.xml"
else:
    # **** LOCAL EXECUTION ****
    config=json.load(open('config_local.json'))
    MYSQL_SHELL = str(config["general"]["xshell_path"])
    Exec_files_location = str(config["general"]["aux_files_path"])
    cluster_Path = str(config["general"]["cluster_path"])
    XMLReportFilePath = "adminapi_qa_test.xml"

#########################################################################

LOCALHOST.user = str(config["local"]["user"])
LOCALHOST.password = str(config["local"]["password"])
LOCALHOST.host = str(config["local"]["host"])
LOCALHOST.xprotocol_port = str(config["local"]["xprotocol_port"])
LOCALHOST.port = str(config["local"]["port"])

REMOTEHOST.user = str(config["remote"]["user"])
REMOTEHOST.password = str(config["remote"]["password"])
REMOTEHOST.host = str(config["remote"]["host"])
REMOTEHOST.xprotocol_port = str(config["remote"]["xprotocol_port"])
REMOTEHOST.port = str(config["remote"]["port"])



class globalvar:
    last_found=""
    last_search=""

###########################################################################################

class XShell_TestCases(unittest.TestCase):


  def test_MYS_769_cluster_removeInstance(self):
      '''MYS-735 [MYAA] CreateCluster() Empty'''
      ################################ deploySandboxInstance 3312  #####################################################
      instance1 = "3312"
      kill_process(instance1,cluster_Path, MYSQL_SHELL)
      results = ''
      init_command = [MYSQL_SHELL, '--interactive=full', '--passwords-from-stdin']
      x_cmds = [("dba.deploySandboxInstance(" + instance1 + ", { sandboxDir: \"" + cluster_Path + "\"});\n",
                 'Please enter a MySQL root password for the new instance:'),
                (LOCALHOST.password + '\n',
                 "Instance localhost:" + instance1 + " successfully deployed and started."),
                ]
      results = exec_xshell_commands(init_command, x_cmds)
      if results.find(bytearray("FAIL", "ascii"), 0, len(results)) > -1:
          self.assertEqual(results, 'PASS')
      ################################ deploySandboxInstance 3313  #####################################################
      instance2 = "3313"
      kill_process(instance2,cluster_Path, MYSQL_SHELL)
      results = ''
      init_command = [MYSQL_SHELL, '--interactive=full', '--passwords-from-stdin']
      x_cmds = [("dba.deploySandboxInstance(" + instance2 + ", { sandboxDir: \"" + cluster_Path + "\"});\n",
                 'Please enter a MySQL root password for the new instance:'),
                (LOCALHOST.password + '\n',
                 "Instance localhost:" + instance2 + " successfully deployed and started."),
                ]
      results = exec_xshell_commands(init_command, x_cmds)
      if results.find(bytearray("FAIL", "ascii"), 0, len(results)) > -1:
          self.assertEqual(results, 'PASS')
      ################################# deploySandboxInstance 3314  ###################################################
      instance3 = "3314"
      kill_process(instance3,cluster_Path, MYSQL_SHELL)
      results = ''
      init_command = [MYSQL_SHELL, '--interactive=full', '--passwords-from-stdin']
      x_cmds = [("dba.deploySandboxInstance(" + instance3 + ", { sandboxDir: \"" + cluster_Path + "\"});\n",
                 'Please enter a MySQL root password for the new instance:'),
                (LOCALHOST.password + '\n',
                 "Instance localhost:" + instance3 + " successfully deployed and started."),
                ]
      results = exec_xshell_commands(init_command, x_cmds)
      if results.find(bytearray("FAIL", "ascii"), 0, len(results)) > -1:
          self.assertEqual(results, 'PASS')
      #################################### createCluster  #################################################
      results = ''
      init_command = [MYSQL_SHELL, '--interactive=full', '-u' + LOCALHOST.user, '--password=' + LOCALHOST.password,
                      '-h' + LOCALHOST.host, '-P' + instance1, '--classic']
      x_cmds = [("dba.createCluster(\"devCluster\", {\"clusterAdminType\": \"local\"});\n", "<Cluster:devCluster>"),
                ("cluster = dba.getCluster('devCluster');\n", "<Cluster:devCluster>"),
                # ("cluster.addInstance({host: '"+ LOCALHOST.host+"', port: "+instance2+", user: 'root', name: 'InstanceOne'});\n", "\"devCluster\""),
                # ("cluster.addInstance({user: '"+ LOCALHOST.user+"password: '"+ LOCALHOST.password+"', port: "+instance2+", name: 'InstanceOne'});\n", "\"devCluster\""),
                # ("cluster.addInstance( {user: \"root\", password: \"guidev!\", host: \"localhost\", port: 3313, name: \"instance3313\"});\n", "\"devCluster\"")
                ("cluster.addInstance( \"{0}:{1}@{2}:3313\");\n".format(LOCALHOST.user, LOCALHOST.password,
                                                                        LOCALHOST.host),
                 "was successfully added to the cluster"),
                ("cluster.addInstance( \"{0}:{1}@{2}:3314\");\n".format(LOCALHOST.user, LOCALHOST.password,
                                                                        LOCALHOST.host),
                 "was successfully added to the cluster"),
                ("cluster.removeInstance(\"{0}:3312\");\n".format(LOCALHOST.host),
                 "was successfully removed from the cluster.")
                ]
      results = exec_xshell_commands(init_command, x_cmds)
      ##########################
      kill_process(instance1,cluster_Path, MYSQL_SHELL)
      kill_process(instance2,cluster_Path, MYSQL_SHELL)
      kill_process(instance3,cluster_Path, MYSQL_SHELL)

      self.assertEqual(results, 'PASS')


  # ----------------------------------------------------------------------
#
# if __name__ == '__main__':
#     unittest.main()

if __name__ == '__main__':
  unittest.main( testRunner=xmlrunner.XMLTestRunner(file(XMLReportFilePath,"w")))
