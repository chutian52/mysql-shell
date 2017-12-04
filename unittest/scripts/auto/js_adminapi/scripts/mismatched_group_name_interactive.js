// Tests where a member with a different group_name is mixed with another cluster

//@ Deploy 2 instances, 1 for base cluster and another for intruder
testutil.deploySandbox(__mysql_sandbox_port1, "root");
testutil.deploySandbox(__mysql_sandbox_port3, "root");

shell.connect(__sandbox_uri3);
var cluster = dba.createCluster('outsider');
session.close();

shell.connect(__sandbox_uri1);
session.runSql("set sql_log_bin=0");
session.runSql("create user root@'%' identified by 'root'");
session.runSql("grant all on *.* to root@'%'");
session.runSql("set sql_log_bin=1");

cluster.disconnect();
var cluster = dba.createCluster('clus');

var outsider = mysql.getSession(__sandbox_uri3);
outsider.runSql("set sql_log_bin=0");
outsider.runSql("create user root@'%' identified by 'root'");
outsider.runSql("grant all on *.* to root@'%'");

// Regression tests for BUG #26159339: SHELL: ADMINAPI DOES NOT TAKE
// GROUP_NAME INTO ACCOUNT

// We check add and rejoin in 4 scenarios where group_name is set but different:
// 1- GR is running and metadata exists
// 2- GR is running and metadata doesn't exist
// 3- GR is stopped and metadata exists
// 4- GR is stopped and metadata doesn't exist (but group_name is still set)

//@# 1- Rejoin on a active member from different group
cluster.rejoinInstance(__sandbox_uri3);

//@# 1- Add on active member from a different group
cluster.addInstance(__sandbox_uri3);

//@ Stop GR
outsider.runSql("stop group_replication");

//@ Clear sro
outsider.runSql("set global super_read_only=0");

//@# 3- Rejoin on inactive member from different group
cluster.rejoinInstance(__sandbox_uri3);

////@# 3- Add on inactive member from a different group
// TODO(.) - test fails, possible bug
// cluster.addInstance(__sandbox_uri3);

//@ Drop MD schema
outsider.runSql("drop schema mysql_innodb_cluster_metadata");

//@# 4- Rejoin on non-cluster inactive member from different group
cluster.rejoinInstance(__sandbox_uri3);

////@# 4- Add on non-cluster inactive member from a different group
//// TODO(.) - test fails, possible bug
//cluster.addInstance(__sandbox_uri3);

//@ Start back GR
outsider.runSql("set global group_replication_bootstrap_group=1");
outsider.runSql("start group_replication");

//@# 2- Rejoin on non-cluster active member from different group
cluster.rejoinInstance(__sandbox_uri3);

//@# 2- Add on non-cluster active member from a different group
cluster.addInstance(__sandbox_uri3);

//------


//@ Preparation
// Deploy another instance, add it to the cluster, then remove it and
// create a cluster with it
testutil.deploySandbox(__mysql_sandbox_port2, "root");
testutil.snapshotSandboxConf(__mysql_sandbox_port2);

cluster.addInstance(__sandbox_uri2);
testutil.waitMemberState(__mysql_sandbox_port2, "ONLINE");

//@ Remove the persist group_replication_group_name {VER(>=8.0.4)}
var s2 = mysql.getSession(__sandbox_uri2);
s2.runSql("RESET PERSIST IF EXISTS group_replication_group_name");
s2.close();

//@ Kill instance 2, change the group_name and start it back
testutil.killSandbox(__mysql_sandbox_port2);
testutil.waitMemberState(__mysql_sandbox_port2, "UNREACHABLE");

testutil.changeSandboxConf(__mysql_sandbox_port2, "group_replication_group_name", "ffd94a44-cce1-11e7-987e-4cfc0b4022e7");
testutil.startSandbox(__mysql_sandbox_port2);

//@<OUT> status() on no-quorum
cluster.status();

session.close();
cluster.disconnect();

//@# forceQuorum
// Member 1 has group_name matching metadata
// Member 2 belongs to a different cluster
shell.connect(__sandbox_uri1);
var cluster = dba.getCluster();
cluster.status();
cluster.forceQuorumUsingPartitionOf(__sandbox_uri2);

//@ Finalize
session.close();
outsider.close();
cluster.disconnect();

testutil.destroySandbox(__mysql_sandbox_port1);
testutil.destroySandbox(__mysql_sandbox_port2);
testutil.destroySandbox(__mysql_sandbox_port3);
