<?php
/**
 * Nagios Status Query Builder
 *
 * Can be used to build urls to display active Nagios status on some kind of wall screen.
 * And browser side auto-refresh.
 *
 * Author: Elan Ruusamäe <glen@delfi.ee>
 * Copyright: GPL v2
 *
 * $Id$
 */

$defaults = array(
	'host' => 'all',
	'hostprops' => '42',
	'hoststatustypes' => '14',
	'serviceprops' => '42',
	'servicestatustypes' => '28',
	'sortoption' => '3',
	'sorttype' => '2',
);

foreach (array('servicestatustypes', 'serviceprops', 'hoststatustypes', 'hostprops') as $k) {
	if (!is_array($_GET[$k])) {
		continue;
	}
	$v = 0;
	foreach ($_GET[$k] as $bit) {
		$v |= $bit;
	}
	$_GET[$k] = $v;
}

$props = array();
foreach ($defaults as $k => $v) {
	$props[$k] = isset($_GET[$k]) ? $_GET[$k] : $defaults[$k];
}

$hoststatustypes = array(
	'HOST_PENDING' => 1,
	'HOST_UP' => 2,
	'HOST_DOWN' => 4,
	'HOST_UNREACHABLE' => 8,
);

$servicestatustypes = array(
	'SERVICE_PENDING' => 1,
	'SERVICE_OK' => 2,
	'SERVICE_WARNING' => 4,
	'SERVICE_UNKNOWN' => 8,
	'SERVICE_CRITICAL' => 16,
);

$hostprops = array(
	'HOST_SCHEDULED_DOWNTIME' => 1,
	'HOST_NO_SCHEDULED_DOWNTIME' => 2,
	'HOST_STATE_ACKNOWLEDGED' => 4,
	'HOST_STATE_UNACKNOWLEDGED' => 8,
	'HOST_CHECKS_DISABLED' => 16,
	'HOST_CHECKS_ENABLED' => 32,
	'HOST_EVENT_HANDLER_DISABLED' => 64,
	'HOST_EVENT_HANDLER_ENABLED' => 128,
	'HOST_FLAP_DETECTION_DISABLED' => 256,
	'HOST_FLAP_DETECTION_ENABLED' => 512,
	'HOST_IS_FLAPPING' => 1024,
	'HOST_IS_NOT_FLAPPING' => 2048,
	'HOST_NOTIFICATIONS_DISABLED' => 4096,
	'HOST_NOTIFICATIONS_ENABLED' => 8192,
	'HOST_PASSIVE_CHECKS_DISABLED' => 16384,
	'HOST_PASSIVE_CHECKS_ENABLED' => 32768,
	'HOST_PASSIVE_CHECK' => 65536,
	'HOST_ACTIVE_CHECK' => 131072,
	'HOST_HARD_STATE' => 262144,
	'HOST_SOFT_STATE' => 524288,
);

$serviceprops = array(
	'SERVICE_SCHEDULED_DOWNTIME' => 1,
	'SERVICE_NO_SCHEDULED_DOWNTIME' => 2,
	'SERVICE_STATE_ACKNOWLEDGED' => 4,
	'SERVICE_STATE_UNACKNOWLEDGED' => 8,
	'SERVICE_CHECKS_DISABLED' => 16,
	'SERVICE_CHECKS_ENABLED' => 32,
	'SERVICE_EVENT_HANDLER_DISABLED' => 64,
	'SERVICE_EVENT_HANDLER_ENABLED' => 128,
	'SERVICE_FLAP_DETECTION_ENABLED' => 256,
	'SERVICE_FLAP_DETECTION_DISABLED' => 512,
	'SERVICE_IS_FLAPPING' => 1024,
	'SERVICE_IS_NOT_FLAPPING' => 2048,
	'SERVICE_NOTIFICATIONS_DISABLED' => 4096,
	'SERVICE_NOTIFICATIONS_ENABLED' => 8192,
	'SERVICE_PASSIVE_CHECKS_DISABLED' => 16384,
	'SERVICE_PASSIVE_CHECKS_ENABLED' => 32768,
	'SERVICE_PASSIVE_CHECK' => 65536,
	'SERVICE_ACTIVE_CHECK' => 131072,
	'SERVICE_HARD_STATE' => 262144,
	'SERVICE_SOFT_STATE' => 524288,
);

function form_bit($field, $value, $bit) {
	echo '<option value="', $bit, '" ', ($value & $bit ? 'selected' : ''), '>', $field, '</option>';
}

function form_multiple($field, $values) {
	global $props;
	echo '<select multiple name="', $field, '[]">';
	foreach ($values as $k => $v) {
		form_bit($k, $props[$field], $v);
	}
	echo '</select>';
}

$args = http_build_query($props);
if (!empty($_GET['control'])) {
?><!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">
<html>
<head>
<meta name="robots" content="noindex, nofollow">
<title>Wall</title>
<LINK REL='stylesheet' TYPE='text/css' HREF='/nagios/stylesheets/common.css'><LINK REL='stylesheet' TYPE='text/css' HREF='/nagios/stylesheets/status.css'></head>
</head>
<form target="_top" action="?control=0">
<div style="font-family: Tahoma, Arial, Sans-Serif; font-size: 8pt; float: left;">servicestatustypes (<?= $props['servicestatustypes'] ?>):<br/><?= form_multiple('servicestatustypes', $servicestatustypes) ?><br/></div>
<div style="font-family: Tahoma, Arial, Sans-Serif; font-size: 8pt; float: left;">serviceprops(<?= $props['serviceprops'] ?>):<br/><?= form_multiple('serviceprops', $serviceprops) ?><br/></div>
<div style="font-family: Tahoma, Arial, Sans-Serif; font-size: 8pt; float: left;">hoststatustypes (<?= $props['hoststatustypes'] ?>):<br/><?= form_multiple('hoststatustypes', $hoststatustypes) ?><br/></div>
<div style="font-family: Tahoma, Arial, Sans-Serif; font-size: 8pt; float: left;">hostprops(<?= $props['hostprops'] ?>):<br/><?= form_multiple('hostprops', $hostprops) ?><br/></div>
<div class="font-family: Tahoma, Arial, Sans-Serif; font-size: 8pt; clear: both;"><input type=submit></div>
	</form>
</tr></table>
<?php
	echo "$url";
	exit;
}

?><frameset rows="90,*">
	<frame name="control" frameborder="0" src="<?= basename($_SERVER['SCRIPT_NAME']) ?>?control=1&<?= htmlspecialchars($args) ?>">
	<frame name="nagios" frameborder="0" src="/nagios/cgi-bin/status.cgi?<?= htmlspecialchars($args) ?>">
</frameset>
</html>
