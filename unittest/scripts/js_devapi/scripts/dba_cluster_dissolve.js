// Assumptions: smart deployment rountines available
//@ Initialization
testutil.deploySandbox(__mysql_sandbox_port1, "root");
testutil.deploySandbox(__mysql_sandbox_port2, "root");
testutil.deploySandbox(__mysql_sandbox_port3, "root");

//@ Create single-primary cluster
shell.connect({scheme: 'mysql', host: localhost, port: __mysql_sandbox_port1, user: 'root', password: 'root'});
var singleSession = session;

if (__have_ssl)
  var single = dba.createCluster('single', {memberSslMode: 'REQUIRED'});
else
  var single = dba.createCluster('single', {memberSslMode: 'DISABLED'});

//@ Success adding instance 2
add_instance_to_cluster(single, __mysql_sandbox_port2);

// Waiting for the added instance to become online
wait_slave_state(single, uri2, "ONLINE");

// Wait for the second added instance to fetch all the replication data
wait_sandbox_in_metadata(__mysql_sandbox_port2);

//@ Success adding instance 3
add_instance_to_cluster(single, __mysql_sandbox_port3);

// Waiting for the added instance to become online
wait_slave_state(single, uri3, "ONLINE");

// Wait for the third added instance to fetch all the replication data
wait_sandbox_in_metadata(__mysql_sandbox_port3);

//@ Cluster.dissolve no force error
single.dissolve();

//@ Success dissolving single-primary cluster
single.dissolve({force: true});

//@ Cluster.dissolve already dissolved
single.dissolve();

shell.connect({scheme: 'mysql', host: localhost, port: __mysql_sandbox_port1, user: 'root', password: 'root'});
var multiSession = session;

//@ Create multi-primary cluster
if (__have_ssl)
  var multi = dba.createCluster('multi', {multiMaster: true, memberSslMode: 'REQUIRED', clearReadOnly: true, force: true});
else
  var multi = dba.createCluster('multi', {multiMaster: true, memberSslMode: 'DISABLED', clearReadOnly: true, force: true});

//@ Success adding instance 2 mp
add_instance_to_cluster(multi, __mysql_sandbox_port2);

// Waiting for the added instance to become online
wait_slave_state(multi, uri2, "ONLINE");

// Wait for the second added instance to fetch all the replication data
wait_sandbox_in_metadata(__mysql_sandbox_port2);

//@ Success adding instance 3 mp
add_instance_to_cluster(multi, __mysql_sandbox_port3);

// Waiting for the added instance to become online
wait_slave_state(multi, uri3, "ONLINE");

// Wait for the third added instance to fetch all the replication data
wait_sandbox_in_metadata(__mysql_sandbox_port3);

//@ Success dissolving multi-primary cluster
multi.dissolve({force: true});

//@ Create single-primary cluster 2
shell.connect({scheme: 'mysql', host: localhost, port: __mysql_sandbox_port1, user: 'root', password: 'root'});
var singleSession2 = session;

if (__have_ssl)
  var single2 = dba.createCluster('single2', {memberSslMode: 'REQUIRED', clearReadOnly: true});
else
  var single2 = dba.createCluster('single2', {memberSslMode: 'DISABLED', clearReadOnly: true});

//@ Success adding instance 2 2
add_instance_to_cluster(single2, __mysql_sandbox_port2);

// Waiting for the added instance to become online
wait_slave_state(single2, uri2, "ONLINE");

// Wait for the second added instance to fetch all the replication data
wait_sandbox_in_metadata(__mysql_sandbox_port2);

//@ Success adding instance 3 2
add_instance_to_cluster(single2, __mysql_sandbox_port3);

// Waiting for the added instance to become online
wait_slave_state(single2, uri3, "ONLINE");

// Wait for the third added instance to fetch all the replication data
wait_sandbox_in_metadata(__mysql_sandbox_port3);

// stop instance 3
// Use stop sandbox instance to make sure the instance is gone before restarting it
testutil.stopSandbox(__mysql_sandbox_port3, 'root');

wait_slave_state(single2, uri3, ["(MISSING)"]);

// Regression test for BUG#26001653
//@ Success dissolving cluster 2
single2.dissolve({force: true});

// start instance 3
testutil.startSandbox(__mysql_sandbox_port3);
//the timeout for GR plugin to install a new view is 60s, so it should be at
// least that value the parameter for the timeout for the waitForDelayedGRStart
testutil.waitForDelayedGRStart(__mysql_sandbox_port3, 'root', 100);

//@ Create multi-primary cluster 2
shell.connect({scheme: 'mysql', host: localhost, port: __mysql_sandbox_port1, user: 'root', password: 'root'});
var multiSession2 = session;

if (__have_ssl)
  var multi2 = dba.createCluster('multi2', {memberSslMode: 'REQUIRED', clearReadOnly: true, multiMaster: true, force: true});
else
  var multi2 = dba.createCluster('multi2', {memberSslMode: 'DISABLED', clearReadOnly: true, multiMaster: true, force: true});

//@ Success adding instance 2 mp 2
add_instance_to_cluster(multi2, __mysql_sandbox_port2);

// Waiting for the added instance to become online
wait_slave_state(multi2, uri2, "ONLINE");

// Wait for the second added instance to fetch all the replication data
wait_sandbox_in_metadata(__mysql_sandbox_port2);

//@ Success adding instance 3 mp 2
add_instance_to_cluster(multi2, __mysql_sandbox_port3);

// Waiting for the added instance to become online
wait_slave_state(multi2, uri3, "ONLINE");

// Wait for the third added instance to fetch all the replication data
wait_sandbox_in_metadata(__mysql_sandbox_port3);

// stop instance 3
// Use stop sandbox instance to make sure the instance is gone before restarting it
testutil.stopSandbox(__mysql_sandbox_port3, 'root');

wait_slave_state(multi2, uri3, ["(MISSING)"]);

// Regression test for BUG#26001653
//@ Success dissolving multi-primary cluster 2
multi2.dissolve({force: true});

//@ Finalization
// Will close opened sessions and delete the sandboxes ONLY if this test was executed standalone
singleSession.close();
multiSession.close();
singleSession2.close();
multiSession2.close();

testutil.destroySandbox(__mysql_sandbox_port1);
testutil.destroySandbox(__mysql_sandbox_port2);
testutil.destroySandbox(__mysql_sandbox_port3);
