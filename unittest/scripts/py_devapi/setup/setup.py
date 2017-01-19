def validate_crud_functions(crud, expected):
	actual = crud.__members__

	# Ensures expected functions are on the actual list
	missing = []
	for exp_funct in expected:
		try:
			pos = actual.index(exp_funct)
			actual.remove(exp_funct)
		except:
			missing.append(exp_funct)

	if len(missing) == 0:
		print ("All expected functions are available\n")
	else:
		print "Missing Functions:", missing

	if len(actual) == 0:
		print "No additional functions are available\n"
	else:
		print "Extra Functions:", actual

def ensure_schema_does_not_exist(session, name):
	try:
		schema = session.get_schema(name)
		session.drop_schema(name)
	except:
		# Nothing happens, it means the schema did not exist
		pass

def validateMember(memberList, member):
	index = -1
	try:
		index = memberList.index(member)
	except:
		pass

	if index != -1:
		print member + ": OK\n"
	else:
		print member + ": Missing\n"

def validateNotMember(memberList, member):
	index = -1
	try:
		index = memberList.index(member)
	except:
		pass

	if index != -1:
		print member + ": Unexpected\n"
	else:
		print member + ": OK\n"

def getSchemaFromList(schemas, name):
  for schema in schemas:
    if schema.name == name:
      return schema

  return None

import time
def wait(timeout, wait_interval, condition):
  waiting = 0
  res = condition()
  while not res and waiting < timeout:
    time.sleep(wait_interval)
    waiting = waiting + 1
    res = condition()
  return res


ro_session = None;
from mysqlsh import mysql as ro_module;
def wait_super_read_only_done():
  global ro_session

  super_read_only = ro_session.run_sql('select @@super_read_only').fetch_one()[0]

  print "---> Super Read Only = %s" % super_read_only

  return super_read_only == "0"

def check_super_read_only_done(connection):
  global ro_session

  ro_session = ro_module.get_classic_session(connection)
  wait(60, 1, wait_super_read_only_done)
  ro_session.close()

recov_cluster = None
recov_master_uri = None
recov_slave_uri = None
recov_state_list = None;

def _check_slave_state():
  global recov_cluster
  global recov_slave_uri
  global recov_state_list

  full_status = recov_cluster.status()
  slave_status = full_status.defaultReplicaSet.topology[recov_slave_uri].status

  print "--->%s: %s" % (recov_slave_uri, slave_status)

  ret_val = False
  for state in recov_state_list:
    if state == slave_status:
      ret_val = True
      print "Done!"
      break

  return ret_val

def wait_slave_state(cluster, slave_uri, states):
  global recov_cluster
  global recov_slave_uri
  global recov_state_list

  recov_cluster = cluster
  recov_slave_uri = slave_uri

  if type(states) is list:
    recov_state_list = states
  else:
    recov_state_list = [states]

  print "WAITING for %s to be in one of these states: %s" % (slave_uri, states)

  wait(60, 1, _check_slave_state)

  recov_cluster = None

# Smart deployment routines
def reset_or_deploy_sandbox(port):
  deployed_here = False;

  options = {}
  if __sandbox_dir != '':
    options['sandboxDir'] = __sandbox_dir

  print 'Killing sandbox at: %s' % port

  try:
    dba.kill_sandbox_instance(port, options)
  except Exception, err:
    pass

  started = False
  print 'Starting sandbox at: %s' % port
  def try_start():
    try:
      dba.start_sandbox_instance(port, options)
      return True
    except Exception, err:
      print "failed: %s" % str(err)
      return False

  if wait(10, 1, try_start):
    started = True
    print 'succeeded'

  if started:
    connected = False
    try:
      print 'Dropping metadata...'
      shell.connect({'host':localhost, 'port':port, 'password':'root'})
      connected = True
      session.run_sql('set sql_log_bin = 0')
      session.run_sql('drop schema mysql_innodb_cluster_metadata')
      session.run_sql('flush logs')
      session.run_sql('set sql_log_bin = 1')
      print 'succeeded'
    except Exception, err:
      print 'failed: %s' % str(err)

    if connected:
      session.run_sql('set sql_log_bin = 1')
      session.close()
  else:
    print 'Deploying instance'
    options['password'] = 'root'
    options['allowRootFrom'] = '%'

    dba.deploy_sandbox_instance(port, options)
    deployed_here = True

  return deployed_here

def reset_or_deploy_sandboxes():
  deploy1 = reset_or_deploy_sandbox(__mysql_sandbox_port1)
  deploy2 = reset_or_deploy_sandbox(__mysql_sandbox_port2)
  deploy3 = reset_or_deploy_sandbox(__mysql_sandbox_port3)

  return deploy1 or deploy2 or deploy3

def cleanup_sandbox(port):
  options = {}
  if __sandbox_dir != '':
    options['sandboxDir'] = __sandbox_dir

  dba.kill_sandbox_instance(port, options)
  dba.delete_sandbox_instance(port, options)

def cleanup_sandboxes(deployed_here):
  if deployed_here:
    cleanup_sandbox(__mysql_sandbox_port1)
    cleanup_sandbox(__mysql_sandbox_port2)
    cleanup_sandbox(__mysql_sandbox_port3)

# Operation that retries adding an instance to a cluster
# 3 retries are done on each case, expectation is that the addition
# is done on the first attempt, however, we have detected some OS
# delays that cause it to fail, that's why the retry logic
def add_instance_to_cluster(cluster, port, name = None):
  global add_instance_options
  add_instance_options['port'] = port
  
  named = False
  if not name is None:
    add_instance_options['name'] = name
    named = True
  
  attempt = 0
  success = False
  while attempt < 3 and not success:
    try:
      cluster.add_instance(add_instance_options, add_instance_extra_opts)
      print "Instance added successfully..."
      success = True
    except Exception, err:
      attempt = attempt + 1
      print "Failed adding instance on attempt %s" % attempt
      print str(err)
      print "Waiting 5 seconds for next attempt"
      time.sleep(5)
  
  if named:
    del add_instance_options['name']

  if not success:
    raise Exception('Failed adding instance : %s' % add_instance_options)